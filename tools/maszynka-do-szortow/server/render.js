import { spawn } from "node:child_process";
import { promises as fs } from "node:fs";
import path from "node:path";
import os from "node:os";

// Renderowanie w przegladarce (ffmpeg.wasm, patrz public/app.js) dziala wszedzie
// bez instalacji, ale jest jednowatkowe i programowe - dla 30-sekundowej rolki
// potrafi trwac wiele minut. Jesli na TYM komputerze jest zainstalowany
// prawdziwy ffmpeg (np. przez Homebrew), wolimy go: dziesiatki razy szybszy,
// czesto ze sprzetowym przyspieszeniem. Appka i tak dziala bez niego -
// przegladarka wtedy po prostu robi to sama, jak dotychczas.

let cachedAvailability = null;

export async function hasNativeFfmpeg() {
  if (cachedAvailability !== null) return cachedAvailability;
  cachedAvailability = await new Promise((resolve) => {
    const proc = spawn("ffmpeg", ["-version"]);
    proc.on("error", () => resolve(false));
    proc.on("exit", (code) => resolve(code === 0));
  });
  return cachedAvailability;
}

export async function transcodeWebmToMp4(webmBuffer) {
  const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), "maszynka-render-"));
  const inputPath = path.join(tmpDir, "input.webm");
  const outputPath = path.join(tmpDir, "output.mp4");
  try {
    await fs.writeFile(inputPath, webmBuffer);
    await new Promise((resolve, reject) => {
      const proc = spawn("ffmpeg", [
        "-y",
        "-i", inputPath,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        outputPath,
      ]);
      let stderr = "";
      proc.stderr.on("data", (d) => { stderr += d.toString(); });
      proc.on("error", reject);
      proc.on("exit", (code) => {
        if (code === 0) resolve();
        else reject(new Error(`ffmpeg (natywny) zakonczyl sie kodem ${code}: ${stderr.slice(-1500)}`));
      });
    });
    return await fs.readFile(outputPath);
  } finally {
    await fs.rm(tmpDir, { recursive: true, force: true }).catch(() => {});
  }
}
