// ffmpeg.wasm jest ladowany leniwie (dopiero przy renderowaniu), z wlasnego
// serwera (/vendor/ffmpeg*), zeby brak internetu nie blokowal reszty panelu.
let fetchFileFn = null;

const BRAND = {
  paper: "#f4f5f1",
  white: "#ffffff",
  ink: "#1b201e",
  gray: "#686e68",
  line: "#d8dcd4",
  blue: "#254bfa",
  lime: "#d9f975",
  pale: "#e9eddf",
};

const CANVAS_W = 1080;
const CANVAS_H = 1920;
const FPS = 30;

let state = {
  projects: [],
  currentProjectId: null,
  currentProject: null,
};

// ---------- API helpers ----------

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `Blad ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

// ---------- Project list / sidebar ----------

async function loadProjects() {
  state.projects = await api("/api/projects");
  renderProjectList();
}

function renderProjectList() {
  const el = document.getElementById("project-list");
  if (state.projects.length === 0) {
    el.innerHTML = '<p class="hint">Brak projektów. Utwórz pierwszy powyżej.</p>';
    return;
  }
  el.innerHTML = "";
  for (const p of state.projects) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "project-item" + (p.id === state.currentProjectId ? " active" : "");
    btn.innerHTML = `${escapeHtml(p.title)}<span class="meta">${p.scenes.length} scen · ${p.targetSeconds}s</span>`;
    btn.addEventListener("click", () => selectProject(p.id));
    el.appendChild(btn);
  }
}

document.getElementById("new-project-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const title = form.title.value.trim();
  const brief = form.brief.value.trim();
  const targetSeconds = Number(form.targetSeconds.value) || 30;
  const project = await api("/api/projects", {
    method: "POST",
    body: JSON.stringify({ title, brief, targetSeconds }),
  });
  form.reset();
  form.targetSeconds.value = 30;
  await loadProjects();
  await selectProject(project.id);
});

async function selectProject(id) {
  state.currentProjectId = id;
  state.currentProject = await api(`/api/projects/${id}`);
  renderProjectList();
  renderWorkspace();
}

// ---------- Workspace ----------

const sceneTemplate = document.getElementById("scene-template");

function renderWorkspace() {
  const workspace = document.getElementById("workspace");
  const p = state.currentProject;
  if (!p) {
    workspace.innerHTML = '<div class="empty-state"><p>Wybierz projekt z listy po lewej albo utwórz nowy, żeby zacząć.</p></div>';
    return;
  }

  workspace.innerHTML = `
    <div class="project-header">
      <div style="flex:1">
        <input type="text" id="project-title" value="${escapeAttr(p.title)}" />
        <textarea id="project-brief" rows="2" placeholder="Brief rolki...">${escapeHtml(p.brief)}</textarea>
      </div>
      <button type="button" class="button ghost small" id="delete-project">Usuń projekt</button>
    </div>
    <div class="project-meta-row">
      <label>Długość docelowa (s)
        <input type="number" id="project-target" value="${p.targetSeconds}" min="5" max="120" />
      </label>
      <label>ID głosu ElevenLabs (puste = domyślny)
        <input type="text" id="project-voice" value="${escapeAttr(p.voiceId || "")}" placeholder="np. sklonowany głos" />
      </label>
    </div>
    <div class="layout-columns">
      <section class="scenes-panel">
        <h2>Sceny (${p.scenes.length})</h2>
        <ul class="scene-list" id="scene-list"></ul>
        <div class="scene-list-actions">
          <button type="button" class="button" id="add-scene">+ Dodaj scenę</button>
          <button type="button" class="button accent" id="generate-scenes">✨ Wygeneruj sceny z briefu (AI)</button>
        </div>
        <div class="render-status" id="generate-scenes-status"></div>
      </section>
      <section class="preview-panel">
        <h2>Podgląd</h2>
        <div class="preview-canvas-wrap">
          <canvas id="preview-canvas" width="${CANVAS_W}" height="${CANVAS_H}"></canvas>
        </div>
        <div class="render-controls">
          <button type="button" class="button" id="preview-play">▶ Podgląd</button>
          <button type="button" class="button accent" id="render-mp4">🎬 Renderuj MP4</button>
          <div class="render-status" id="render-status"></div>
          <a href="#" class="button ghost download-link" id="download-link" hidden download>Pobierz MP4</a>
        </div>
      </section>
    </div>
  `;

  document.getElementById("project-title").addEventListener("change", (e) => updateProjectField("title", e.target.value));
  document.getElementById("project-brief").addEventListener("change", (e) => updateProjectField("brief", e.target.value));
  document.getElementById("project-target").addEventListener("change", (e) => updateProjectField("targetSeconds", Number(e.target.value)));
  document.getElementById("project-voice").addEventListener("change", (e) => updateProjectField("voiceId", e.target.value || null));
  document.getElementById("delete-project").addEventListener("click", onDeleteProject);
  document.getElementById("add-scene").addEventListener("click", onAddScene);
  document.getElementById("generate-scenes").addEventListener("click", onGenerateScenes);
  document.getElementById("preview-play").addEventListener("click", () => playPreview(false));
  document.getElementById("render-mp4").addEventListener("click", () => renderMp4());

  renderScenes();
  drawIdleFrame();
}

async function updateProjectField(field, value) {
  const p = state.currentProject;
  p[field] = value;
  await api(`/api/projects/${p.id}`, { method: "PUT", body: JSON.stringify({ [field]: value }) });
  await loadProjects();
}

async function onDeleteProject() {
  if (!confirm("Usunąć ten projekt na stałe?")) return;
  await api(`/api/projects/${state.currentProjectId}`, { method: "DELETE" });
  state.currentProjectId = null;
  state.currentProject = null;
  await loadProjects();
  renderWorkspace();
}

async function onAddScene() {
  const p = state.currentProject;
  await api(`/api/projects/${p.id}/scenes`, {
    method: "POST",
    body: JSON.stringify({ text: "", lektorText: "", type: "tekst" }),
  });
  state.currentProject = await api(`/api/projects/${p.id}`);
  renderScenes();
  document.querySelector('.scenes-panel h2').textContent = `Sceny (${state.currentProject.scenes.length})`;
}

async function onGenerateScenes() {
  const p = state.currentProject;
  const btn = document.getElementById("generate-scenes");
  const statusEl = document.getElementById("generate-scenes-status");
  if (!p.brief || !p.brief.trim()) {
    statusEl.textContent = "Wpisz najpierw brief (pole powyżej) — na jego podstawie AI napisze sceny.";
    statusEl.className = "render-status error";
    return;
  }
  btn.disabled = true;
  statusEl.className = "render-status is-working";
  statusEl.textContent = "Generuję sceny z briefu (Claude, przez DONĘ)…";
  try {
    state.currentProject = await api(`/api/projects/${p.id}/scenes/generate`, { method: "POST" });
    renderScenes();
    document.querySelector('.scenes-panel h2').textContent = `Sceny (${state.currentProject.scenes.length})`;
    statusEl.textContent = "Gotowe! Dopisano nowe sceny na końcu listy — sprawdź i popraw, jeśli trzeba.";
    statusEl.className = "render-status ok";
  } catch (err) {
    statusEl.textContent = `Błąd: ${err.message}`;
    statusEl.className = "render-status error";
  } finally {
    btn.disabled = false;
  }
}

// ---------- Scenes list (drag to reorder) ----------

let dragSceneId = null;

function renderScenes() {
  const list = document.getElementById("scene-list");
  list.innerHTML = "";
  const p = state.currentProject;
  for (const scene of p.scenes) {
    const node = sceneTemplate.content.firstElementChild.cloneNode(true);
    node.dataset.sceneId = scene.id;
    node.querySelector(".scene-type").value = scene.type || "tekst";
    node.querySelector(".scene-duration").value = scene.durationSeconds || "";
    node.querySelector(".scene-text").value = scene.text || "";
    node.querySelector(".scene-lektor").value = scene.lektorText || "";

    const audioPlayer = node.querySelector(".scene-audio-player");
    const statusEl = node.querySelector(".scene-narration-status");
    if (scene.narrationFile) {
      audioPlayer.src = `/api/audio/${p.id}/${scene.narrationFile}`;
      audioPlayer.hidden = false;
      statusEl.textContent = "Lektor gotowy";
    }

    node.querySelector(".scene-type").addEventListener("change", (e) => updateScene(scene.id, { type: e.target.value }));
    node.querySelector(".scene-duration").addEventListener("change", (e) => {
      const v = e.target.value === "" ? null : Number(e.target.value);
      updateScene(scene.id, { durationSeconds: v });
    });
    node.querySelector(".scene-text").addEventListener("change", (e) => updateScene(scene.id, { text: e.target.value }));
    node.querySelector(".scene-lektor").addEventListener("change", (e) => updateScene(scene.id, { lektorText: e.target.value }));
    node.querySelector(".scene-delete").addEventListener("click", () => deleteScene(scene.id));
    node.querySelector(".scene-generate-narration").addEventListener("click", (e) => generateNarration(scene.id, e.target, statusEl, audioPlayer));

    node.addEventListener("dragstart", () => {
      dragSceneId = scene.id;
      node.classList.add("dragging");
    });
    node.addEventListener("dragend", () => node.classList.remove("dragging"));
    node.addEventListener("dragover", (e) => e.preventDefault());
    node.addEventListener("drop", (e) => {
      e.preventDefault();
      if (!dragSceneId || dragSceneId === scene.id) return;
      reorderScenes(dragSceneId, scene.id);
    });

    list.appendChild(node);
  }
}

async function updateScene(sceneId, patch) {
  const p = state.currentProject;
  await api(`/api/projects/${p.id}/scenes/${sceneId}`, { method: "PUT", body: JSON.stringify(patch) });
  const scene = p.scenes.find((s) => s.id === sceneId);
  Object.assign(scene, patch);
  if (patch.lektorText !== undefined) scene.narrationFile = null;
}

async function deleteScene(sceneId) {
  const p = state.currentProject;
  await api(`/api/projects/${p.id}/scenes/${sceneId}`, { method: "DELETE" });
  p.scenes = p.scenes.filter((s) => s.id !== sceneId);
  renderScenes();
  document.querySelector('.scenes-panel h2').textContent = `Sceny (${p.scenes.length})`;
}

async function reorderScenes(draggedId, targetId) {
  const p = state.currentProject;
  const ids = p.scenes.map((s) => s.id);
  const from = ids.indexOf(draggedId);
  const to = ids.indexOf(targetId);
  ids.splice(to, 0, ids.splice(from, 1)[0]);
  const updated = await api(`/api/projects/${p.id}/scenes-order`, { method: "PUT", body: JSON.stringify({ order: ids }) });
  state.currentProject = updated;
  renderScenes();
}

async function generateNarration(sceneId, button, statusEl, audioPlayer) {
  const p = state.currentProject;
  button.disabled = true;
  statusEl.textContent = "Generuję…";
  try {
    const { scene, url } = await api(`/api/projects/${p.id}/scenes/${sceneId}/narration`, { method: "POST" });
    Object.assign(p.scenes.find((s) => s.id === sceneId), scene);
    audioPlayer.src = url;
    audioPlayer.hidden = false;
    statusEl.textContent = "Lektor gotowy";
  } catch (err) {
    statusEl.textContent = `Błąd: ${err.message}`;
  } finally {
    button.disabled = false;
  }
}

// ---------- Canvas scene rendering ----------

function sceneDuration(scene, project) {
  if (scene.durationSeconds) return scene.durationSeconds;
  const count = project.scenes.length || 1;
  return project.targetSeconds / count;
}

function drawScene(ctx, scene, tSeconds) {
  ctx.clearRect(0, 0, CANVAS_W, CANVAS_H);

  const isCta = scene.type === "cta";
  ctx.fillStyle = isCta ? BRAND.lime : BRAND.paper;
  ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);

  // delikatna animacja tla - dryfujace kolo, brand jako glowny nosnik
  const driftX = CANVAS_W / 2 + Math.sin(tSeconds * 0.6) * 220;
  const driftY = CANVAS_H * 0.32 + Math.cos(tSeconds * 0.4) * 160;
  ctx.globalAlpha = 0.16;
  ctx.fillStyle = isCta ? BRAND.ink : BRAND.blue;
  ctx.beginPath();
  ctx.arc(driftX, driftY, 340, 0, Math.PI * 2);
  ctx.fill();
  ctx.globalAlpha = 1;

  const text = (scene.text || "").trim();
  ctx.fillStyle = BRAND.ink;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  if (scene.type === "lista") {
    const lines = text.split("\n").filter(Boolean);
    ctx.font = "700 58px Manrope, Arial, sans-serif";
    const startY = CANVAS_H / 2 - ((lines.length - 1) * 90) / 2;
    lines.forEach((line, i) => {
      ctx.fillText(`• ${line}`, CANVAS_W / 2, startY + i * 90, CANVAS_W - 140);
    });
  } else if (scene.type === "cytat") {
    ctx.font = "italic 600 52px Manrope, Arial, sans-serif";
    wrapText(ctx, `„${text}”`, CANVAS_W / 2, CANVAS_H / 2, CANVAS_W - 180, 66);
  } else if (scene.type === "cta") {
    ctx.font = "800 66px Manrope, Arial, sans-serif";
    wrapText(ctx, text, CANVAS_W / 2, CANVAS_H / 2, CANVAS_W - 140, 78);
  } else {
    ctx.font = "800 70px Manrope, Arial, sans-serif";
    wrapText(ctx, text, CANVAS_W / 2, CANVAS_H / 2, CANVAS_W - 140, 82);
  }

  ctx.fillStyle = BRAND.gray;
  ctx.font = "600 30px Manrope, Arial, sans-serif";
  ctx.textAlign = "left";
  ctx.textBaseline = "alphabetic";
  ctx.fillText("probatum.", 50, CANVAS_H - 60);
}

function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
  const words = text.split(" ");
  const lines = [];
  let current = "";
  for (const word of words) {
    const test = current ? `${current} ${word}` : word;
    if (ctx.measureText(test).width > maxWidth && current) {
      lines.push(current);
      current = word;
    } else {
      current = test;
    }
  }
  if (current) lines.push(current);
  const startY = y - ((lines.length - 1) * lineHeight) / 2;
  lines.forEach((line, i) => ctx.fillText(line, x, startY + i * lineHeight));
}

function drawIdleFrame() {
  const canvas = document.getElementById("preview-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const p = state.currentProject;
  if (p.scenes.length > 0) {
    drawScene(ctx, p.scenes[0], 0);
  } else {
    ctx.fillStyle = BRAND.paper;
    ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);
    ctx.fillStyle = BRAND.gray;
    ctx.font = "40px Manrope, Arial, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Dodaj scenę, żeby zobaczyć podgląd", CANVAS_W / 2, CANVAS_H / 2);
  }
}

async function playPreview() {
  const p = state.currentProject;
  const canvas = document.getElementById("preview-canvas");
  const ctx = canvas.getContext("2d");
  if (p.scenes.length === 0) return;

  let start = performance.now();
  const timeline = buildTimeline(p);
  const total = timeline[timeline.length - 1].end;

  return new Promise((resolve) => {
    function frame(now) {
      const t = (now - start) / 1000;
      if (t >= total) {
        drawScene(ctx, p.scenes[p.scenes.length - 1], sceneDuration(p.scenes[p.scenes.length - 1], p));
        resolve();
        return;
      }
      const entry = timeline.find((e) => t >= e.start && t < e.end);
      if (entry) drawScene(ctx, entry.scene, t - entry.start);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  });
}

function buildTimeline(project) {
  let t = 0;
  return project.scenes.map((scene) => {
    const d = sceneDuration(scene, project);
    const entry = { scene, start: t, end: t + d, duration: d };
    t += d;
    return entry;
  });
}

// ---------- Render to MP4 ----------

let ffmpegInstance = null;

async function getFfmpeg(onLog) {
  if (ffmpegInstance) return ffmpegInstance;
  const [{ FFmpeg }, { fetchFile }] = await Promise.all([
    import("/vendor/ffmpeg/index.js"),
    import("/vendor/ffmpeg-util/index.js"),
  ]);
  fetchFileFn = fetchFile;
  const ffmpeg = new FFmpeg();
  if (onLog) ffmpeg.on("log", ({ message }) => onLog(message));
  await ffmpeg.load({
    coreURL: "/vendor/ffmpeg-core/ffmpeg-core.js",
    wasmURL: "/vendor/ffmpeg-core/ffmpeg-core.wasm",
  });
  ffmpegInstance = ffmpeg;
  return ffmpeg;
}

async function renderMp4() {
  const p = state.currentProject;
  const statusEl = document.getElementById("render-status");
  const downloadLink = document.getElementById("download-link");
  const renderBtn = document.getElementById("render-mp4");

  if (p.scenes.length === 0) {
    statusEl.textContent = "Dodaj przynajmniej jedną scenę.";
    statusEl.className = "render-status error";
    return;
  }

  renderBtn.disabled = true;
  downloadLink.hidden = true;
  statusEl.className = "render-status";

  try {
    statusEl.textContent = "Przygotowuję audio scen…";
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const dest = audioCtx.createMediaStreamDestination();
    const timeline = buildTimeline(p);

    const buffers = await Promise.all(
      timeline.map(async (entry) => {
        if (!entry.scene.narrationFile) return null;
        const res = await fetch(`/api/audio/${p.id}/${entry.scene.narrationFile}`);
        const arr = await res.arrayBuffer();
        try {
          return await audioCtx.decodeAudioData(arr);
        } catch {
          return null;
        }
      })
    );

    const canvas = document.getElementById("preview-canvas");
    // captureStream(0) = tryb reczny: sami wymuszamy kazda klatke przez
    // requestFrame() po narysowaniu. Automatyczny tryb (captureStream(FPS))
    // potrafi nie zlapac zadnej klatki w headless/bezekranowym Chromium.
    const videoStream = canvas.captureStream(0);
    const videoTrack = videoStream.getVideoTracks()[0];
    const combined = new MediaStream([videoTrack, ...dest.stream.getAudioTracks()]);

    const recorder = new MediaRecorder(combined, { mimeType: pickMimeType() });
    const chunks = [];
    recorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data); };

    const recordingDone = new Promise((resolve) => { recorder.onstop = resolve; });
    recorder.start();

    const audioStartTime = audioCtx.currentTime + 0.15;
    const totalDuration = timeline[timeline.length - 1].end;

    // MediaRecorder w niektorych przegladarkach (m.in. headless Chromium)
    // przestaje pisac dane, jesli audio destination nigdy nie dostaje
    // zadnego realnego sygnalu - wiec zawsze podlaczamy cichy bufor na
    // cala dlugosc rolki, nawet jesli zadna scena nie ma lektora.
    const silentBuffer = audioCtx.createBuffer(
      1,
      Math.ceil(audioCtx.sampleRate * (totalDuration + 1)),
      audioCtx.sampleRate
    );
    const silentSrc = audioCtx.createBufferSource();
    silentSrc.buffer = silentBuffer;
    silentSrc.connect(dest);
    silentSrc.start(audioStartTime);

    timeline.forEach((entry, i) => {
      const buf = buffers[i];
      if (!buf) return;
      const src = audioCtx.createBufferSource();
      src.buffer = buf;
      src.connect(dest);
      src.start(audioStartTime + entry.start);
    });

    const ctx = canvas.getContext("2d");
    const total = totalDuration;
    const renderStart = performance.now() + 150;
    await new Promise((resolve) => {
      function frame(now) {
        const t = (now - renderStart) / 1000;
        if (t >= total) {
          resolve();
          return;
        }
        statusEl.textContent = `Nagrywam podgląd: ${Math.min(t, total).toFixed(0)} / ${total.toFixed(0)} s…`;
        const entry = timeline.find((e) => t >= e.start && t < e.end) || timeline[0];
        drawScene(ctx, entry.scene, Math.max(0, t - entry.start));
        videoTrack.requestFrame();
        requestAnimationFrame(frame);
      }
      videoTrack.requestFrame();
      requestAnimationFrame(frame);
    });
    videoTrack.requestFrame();

    recorder.stop();
    await recordingDone;
    await audioCtx.close();

    const webmBlob = new Blob(chunks, { type: chunks[0]?.type || "video/webm" });
    console.log("[render] chunks:", chunks.length, "size:", webmBlob.size, "type:", webmBlob.type, "recorderMime:", recorder.mimeType);

    // Wolimy render na serwerze przez natywny ffmpeg (dziesiatki razy szybszy,
    // czesto ze sprzetowym przyspieszeniem) - patrz server/render.js. Jesli tego
    // komputera/serwera nie ma czym uruchomic (kod 501), appka nie utyka: cicho
    // wraca do sprawdzonej sciezki ffmpeg.wasm w przegladarce (dziala wszedzie,
    // ale jednowatkowo i wolniej - dla dluzszej rolki moze to potrwac minuty).
    let mp4Blob = null;
    let savedServerSide = false;
    statusEl.textContent = "Konwertuję do MP4 (próbuję szybkiego renderu na serwerze)…";
    try {
      const nativeRes = await fetch(`/api/projects/${p.id}/render-native`, {
        method: "POST",
        headers: { "Content-Type": "video/webm" },
        body: webmBlob,
      });
      if (nativeRes.ok) {
        mp4Blob = await nativeRes.blob();
        savedServerSide = true;
      } else if (nativeRes.status !== 501) {
        const body = await nativeRes.json().catch(() => ({}));
        throw new Error(body.error || `Render serwerowy: błąd ${nativeRes.status}`);
      }
      // 501 = brak natywnego ffmpeg na serwerze -> celowo lecimy dalej do WASM.
    } catch (err) {
      console.warn("[render] serwerowy render nieudany, wracam do ffmpeg.wasm:", err);
    }

    if (!mp4Blob) {
      statusEl.textContent = "Konwertuję do MP4 (ffmpeg.wasm w przeglądarce, pierwszy raz może pobrać ~30MB)…";
      const ffmpeg = await getFfmpeg((msg) => console.log("[ffmpeg]", msg));
      ffmpeg.on("progress", ({ progress }) => {
        if (Number.isFinite(progress)) {
          statusEl.textContent = `Konwertuję do MP4 (ffmpeg.wasm): ${Math.round(Math.min(1, Math.max(0, progress)) * 100)}%`;
        }
      });

      await ffmpeg.writeFile("input.webm", await fetchFileFn(webmBlob));
      const exitCode = await ffmpeg.exec([
        "-i", "input.webm",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "output.mp4",
      ]);
      if (exitCode !== 0) {
        throw new Error(`ffmpeg zakonczyl sie kodem ${exitCode} (zobacz konsole przegladarki)`);
      }
      const data = await ffmpeg.readFile("output.mp4");
      mp4Blob = new Blob([data.buffer], { type: "video/mp4" });
    }

    const url = URL.createObjectURL(mp4Blob);
    downloadLink.href = url;
    downloadLink.download = `${slugify(p.title)}.mp4`;
    downloadLink.hidden = false;

    if (savedServerSide) {
      statusEl.textContent = "Gotowe! Plik zapisany w output/ i dostępny do pobrania (render serwerowy).";
      statusEl.className = "render-status ok";
    } else {
      statusEl.textContent = "Zapisuję kopię w output/…";
      try {
        await fetch(`/api/projects/${p.id}/render`, {
          method: "POST",
          headers: { "Content-Type": "video/mp4" },
          body: mp4Blob,
        });
        statusEl.textContent = "Gotowe! Plik zapisany w output/ i dostępny do pobrania.";
      } catch {
        statusEl.textContent = "Gotowe! Pobierz plik (zapis lokalny w output/ się nie udał).";
      }
      statusEl.className = "render-status ok";
    }
  } catch (err) {
    console.error("RENDER ERROR", err);
    const msg = err?.message || err?.toString?.() || JSON.stringify(err);
    statusEl.textContent = `Błąd renderowania: ${msg}`;
    statusEl.className = "render-status error";
  } finally {
    renderBtn.disabled = false;
  }
}

function pickMimeType() {
  const candidates = ["video/webm;codecs=vp9,opus", "video/webm;codecs=vp8,opus", "video/webm"];
  return candidates.find((c) => MediaRecorder.isTypeSupported(c)) || "video/webm";
}

function slugify(text) {
  return (text || "rolka")
    .toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "") || "rolka";
}

function escapeHtml(str) {
  return (str || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function escapeAttr(str) { return escapeHtml(str); }

// ---------- init ----------

loadProjects();
