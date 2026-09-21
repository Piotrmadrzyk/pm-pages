import express from "express";
import path from "node:path";
import { promises as fs } from "node:fs";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

import {
  listProjects,
  getProject,
  saveProject,
  createProject,
  deleteProject,
  newScene,
  ensureAudioDir,
  projectAudioDir,
} from "./store.js";
import { textToSpeech, soundEffect, defaultVoiceId } from "./elevenlabs.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, "..", ".env") });

const app = express();
app.use(express.json({ limit: "10mb" }));
app.use(express.raw({ type: "video/mp4", limit: "200mb" }));

const PUBLIC_DIR = path.join(__dirname, "..", "public");
const OUTPUT_DIR = path.join(__dirname, "..", "output");

app.use(express.static(PUBLIC_DIR));
app.use("/vendor/manrope", express.static(path.join(__dirname, "..", "..", "..", "assets")));

const NODE_MODULES = path.join(__dirname, "..", "node_modules");
app.use("/vendor/ffmpeg", express.static(path.join(NODE_MODULES, "@ffmpeg", "ffmpeg", "dist", "esm")));
app.use("/vendor/ffmpeg-util", express.static(path.join(NODE_MODULES, "@ffmpeg", "util", "dist", "esm")));
app.use("/vendor/ffmpeg-core", express.static(path.join(NODE_MODULES, "@ffmpeg", "core", "dist", "esm")));

// --- Projects ---

app.get("/api/config", (req, res) => {
  res.json({ defaultVoiceId: defaultVoiceId() });
});

app.get("/api/projects", async (req, res, next) => {
  try {
    res.json(await listProjects());
  } catch (err) {
    next(err);
  }
});

app.post("/api/projects", async (req, res, next) => {
  try {
    const { title, brief, targetSeconds, voiceId } = req.body || {};
    const project = await createProject({ title, brief, targetSeconds, voiceId });
    res.status(201).json(project);
  } catch (err) {
    next(err);
  }
});

app.get("/api/projects/:id", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    res.json(project);
  } catch (err) {
    next(err);
  }
});

app.put("/api/projects/:id", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    const { title, brief, targetSeconds, voiceId } = req.body || {};
    if (title !== undefined) project.title = title;
    if (brief !== undefined) project.brief = brief;
    if (targetSeconds !== undefined) project.targetSeconds = targetSeconds;
    if (voiceId !== undefined) project.voiceId = voiceId;
    project.updatedAt = new Date().toISOString();
    await saveProject(project);
    res.json(project);
  } catch (err) {
    next(err);
  }
});

app.delete("/api/projects/:id", async (req, res, next) => {
  try {
    await deleteProject(req.params.id);
    res.status(204).end();
  } catch (err) {
    next(err);
  }
});

// --- Scenes ---

app.post("/api/projects/:id/scenes", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    const scene = newScene(req.body || {});
    project.scenes.push(scene);
    project.updatedAt = new Date().toISOString();
    await saveProject(project);
    res.status(201).json(scene);
  } catch (err) {
    next(err);
  }
});

app.put("/api/projects/:id/scenes/:sceneId", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    const scene = project.scenes.find((s) => s.id === req.params.sceneId);
    if (!scene) return res.status(404).json({ error: "Nie znaleziono sceny" });
    const { text, lektorText, type, durationSeconds } = req.body || {};
    if (text !== undefined) scene.text = text;
    if (lektorText !== undefined) {
      scene.lektorText = lektorText;
      scene.narrationFile = null; // tekst zmieniony, trzeba przegenerowac lektora
    }
    if (type !== undefined) scene.type = type;
    if (durationSeconds !== undefined) scene.durationSeconds = durationSeconds;
    project.updatedAt = new Date().toISOString();
    await saveProject(project);
    res.json(scene);
  } catch (err) {
    next(err);
  }
});

app.delete("/api/projects/:id/scenes/:sceneId", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    project.scenes = project.scenes.filter((s) => s.id !== req.params.sceneId);
    project.updatedAt = new Date().toISOString();
    await saveProject(project);
    res.status(204).end();
  } catch (err) {
    next(err);
  }
});

app.put("/api/projects/:id/scenes-order", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    const { order } = req.body || {};
    if (!Array.isArray(order)) return res.status(400).json({ error: "order musi byc tablica ID scen" });
    const byId = new Map(project.scenes.map((s) => [s.id, s]));
    const reordered = order.map((id) => byId.get(id)).filter(Boolean);
    if (reordered.length !== project.scenes.length) {
      return res.status(400).json({ error: "order nie zgadza sie ze scenami projektu" });
    }
    project.scenes = reordered;
    project.updatedAt = new Date().toISOString();
    await saveProject(project);
    res.json(project);
  } catch (err) {
    next(err);
  }
});

// --- ElevenLabs: lektor per scena ---

app.post("/api/projects/:id/scenes/:sceneId/narration", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    const scene = project.scenes.find((s) => s.id === req.params.sceneId);
    if (!scene) return res.status(404).json({ error: "Nie znaleziono sceny" });
    if (!scene.lektorText || !scene.lektorText.trim()) {
      return res.status(400).json({ error: "Scena nie ma tekstu lektora" });
    }
    const audio = await textToSpeech(scene.lektorText, project.voiceId);
    const dir = await ensureAudioDir(project.id);
    const filename = `${scene.id}.mp3`;
    await fs.writeFile(path.join(dir, filename), audio);
    scene.narrationFile = filename;
    project.updatedAt = new Date().toISOString();
    await saveProject(project);
    res.json({ scene, url: `/api/audio/${project.id}/${filename}` });
  } catch (err) {
    next(err);
  }
});

// --- ElevenLabs: efekt dzwiekowy (nie per scena - dowolny prompt) ---

app.post("/api/projects/:id/sfx", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    const { description, durationSeconds } = req.body || {};
    if (!description || !description.trim()) {
      return res.status(400).json({ error: "Podaj opis efektu dzwiekowego" });
    }
    const audio = await soundEffect(description, durationSeconds);
    const dir = await ensureAudioDir(project.id);
    const filename = `sfx-${Date.now()}.mp3`;
    await fs.writeFile(path.join(dir, filename), audio);
    res.json({ url: `/api/audio/${project.id}/${filename}`, filename });
  } catch (err) {
    next(err);
  }
});

app.get("/api/audio/:projectId/:filename", async (req, res, next) => {
  try {
    const dir = projectAudioDir(req.params.projectId);
    const file = path.join(dir, req.params.filename);
    res.sendFile(file);
  } catch (err) {
    next(err);
  }
});

// --- Render output: przegladarka wysyla gotowy MP4, zapisujemy lokalnie ---

app.post("/api/projects/:id/render", async (req, res, next) => {
  try {
    const project = await getProject(req.params.id);
    if (!project) return res.status(404).json({ error: "Nie znaleziono projektu" });
    if (!Buffer.isBuffer(req.body) || req.body.length === 0) {
      return res.status(400).json({ error: "Brak danych wideo (Content-Type: video/mp4)" });
    }
    await fs.mkdir(OUTPUT_DIR, { recursive: true });
    const safeTitle = (project.title || "rolka").replace(/[^a-z0-9-_]+/gi, "-").toLowerCase();
    const filename = `${safeTitle}-${Date.now()}.mp4`;
    const filePath = path.join(OUTPUT_DIR, filename);
    await fs.writeFile(filePath, req.body);
    res.json({ savedTo: `output/${filename}` });
  } catch (err) {
    next(err);
  }
});

app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 500).json({ error: err.message || "Blad serwera" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Maszynka do szortsow dziala: http://localhost:${PORT}`);
});
