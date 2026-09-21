import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { randomUUID } from "node:crypto";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.join(__dirname, "..", "data", "projects");

async function ensureDataDir() {
  await fs.mkdir(DATA_DIR, { recursive: true });
}

function projectFile(id) {
  return path.join(DATA_DIR, `${id}.json`);
}

export async function listProjects() {
  await ensureDataDir();
  const files = await fs.readdir(DATA_DIR);
  const projects = [];
  for (const file of files) {
    if (!file.endsWith(".json")) continue;
    const raw = await fs.readFile(path.join(DATA_DIR, file), "utf8");
    projects.push(JSON.parse(raw));
  }
  projects.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
  return projects;
}

export async function getProject(id) {
  await ensureDataDir();
  try {
    const raw = await fs.readFile(projectFile(id), "utf8");
    return JSON.parse(raw);
  } catch (err) {
    if (err.code === "ENOENT") return null;
    throw err;
  }
}

export async function saveProject(project) {
  await ensureDataDir();
  await fs.writeFile(projectFile(project.id), JSON.stringify(project, null, 2), "utf8");
  return project;
}

export async function createProject({ title, brief, targetSeconds, voiceId }) {
  const now = new Date().toISOString();
  const project = {
    id: randomUUID(),
    title: title || "Nowa rolka",
    brief: brief || "",
    targetSeconds: targetSeconds || 30,
    voiceId: voiceId || null,
    createdAt: now,
    updatedAt: now,
    scenes: [],
  };
  await saveProject(project);
  return project;
}

export async function deleteProject(id) {
  await ensureDataDir();
  try {
    await fs.unlink(projectFile(id));
  } catch (err) {
    if (err.code !== "ENOENT") throw err;
  }
}

export function newScene({ text = "", lektorText = "", type = "tekst", durationSeconds = null } = {}) {
  return {
    id: randomUUID(),
    text,
    lektorText,
    type,
    durationSeconds,
    narrationFile: null,
  };
}

export function projectAudioDir(projectId) {
  return path.join(DATA_DIR, "..", "audio", projectId);
}

export async function ensureAudioDir(projectId) {
  const dir = projectAudioDir(projectId);
  await fs.mkdir(dir, { recursive: true });
  return dir;
}

export { DATA_DIR };
