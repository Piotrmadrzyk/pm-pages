// Klucz API ElevenLabs NIE zyje tutaj — zyje wylacznie w credentialu n8n
// "PM Marketing OS — ElevenLabs" (ten sam, ktorego uzywaja juz inne workflow
// Dony/Probatum). Ta appka woli webhook n8n, ktory sam woli ElevenLabs.
// Wzorzec 1:1 z tym, jak panel Dony (dona-panel) woli n8n zamiast trzymac
// klucze w kodzie frontu/backendu — patrz DONA_2 dokumentacja architektury.
const N8N_WEBHOOK_URL =
  process.env.DONA_N8N_ELEVENLABS_URL ||
  "https://pmresearch.app.n8n.cloud/webhook/maszynka-elevenlabs";

function getSharedSecret() {
  const secret = process.env.DONA_N8N_SHARED_SECRET;
  if (!secret) {
    const err = new Error(
      "Brak DONA_N8N_SHARED_SECRET w .env. Skopiuj .env.example do .env i wklej sekret " +
        "(w n8n: tabela PM_sekrety_wspolne, wpis 'maszynka_szortow_sekret')."
    );
    err.status = 400;
    throw err;
  }
  return secret;
}

async function callN8nElevenLabs(operation, payload) {
  const sekret = getSharedSecret();
  const res = await fetch(N8N_WEBHOOK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sekret, operation, ...payload }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    const err = new Error(
      `ElevenLabs przez DONA/n8n (${operation}) blad ${res.status}: ${detail}`
    );
    err.status = res.status;
    throw err;
  }
  const buf = Buffer.from(await res.arrayBuffer());
  return buf;
}

export function defaultVoiceId() {
  return process.env.ELEVENLABS_VOICE_ID || "21m00Tcm4TlvDq8ikWAM";
}

export async function textToSpeech(text, voiceId) {
  const voice = voiceId || defaultVoiceId();
  return callN8nElevenLabs("tts", { text, voiceId: voice });
}

export async function soundEffect(description, durationSeconds) {
  return callN8nElevenLabs("sfx", {
    text: description,
    durationSeconds: durationSeconds || undefined,
  });
}
