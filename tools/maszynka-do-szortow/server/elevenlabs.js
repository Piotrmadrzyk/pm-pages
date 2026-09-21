const API_BASE = "https://api.elevenlabs.io/v1";

function getApiKey() {
  const key = process.env.ELEVENLABS_API_KEY;
  if (!key) {
    const err = new Error(
      "Brak ELEVENLABS_API_KEY w .env. Skopiuj .env.example do .env i wklej swoj klucz API z ElevenLabs."
    );
    err.status = 400;
    throw err;
  }
  return key;
}

export function defaultVoiceId() {
  return process.env.ELEVENLABS_VOICE_ID || "21m00Tcm4TlvDq8ikWAM";
}

export async function textToSpeech(text, voiceId) {
  const apiKey = getApiKey();
  const voice = voiceId || defaultVoiceId();
  const res = await fetch(`${API_BASE}/text-to-speech/${voice}`, {
    method: "POST",
    headers: {
      "xi-api-key": apiKey,
      "Content-Type": "application/json",
      Accept: "audio/mpeg",
    },
    body: JSON.stringify({
      text,
      model_id: "eleven_multilingual_v2",
      voice_settings: { stability: 0.4, similarity_boost: 0.8 },
    }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    const err = new Error(`ElevenLabs TTS blad ${res.status}: ${detail}`);
    err.status = res.status;
    throw err;
  }
  const buf = Buffer.from(await res.arrayBuffer());
  return buf;
}

export async function soundEffect(description, durationSeconds) {
  const apiKey = getApiKey();
  const res = await fetch(`${API_BASE}/sound-generation`, {
    method: "POST",
    headers: {
      "xi-api-key": apiKey,
      "Content-Type": "application/json",
      Accept: "audio/mpeg",
    },
    body: JSON.stringify({
      text: description,
      duration_seconds: durationSeconds || undefined,
      prompt_influence: 0.3,
    }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    const err = new Error(`ElevenLabs SFX blad ${res.status}: ${detail}`);
    err.status = res.status;
    throw err;
  }
  const buf = Buffer.from(await res.arrayBuffer());
  return buf;
}
