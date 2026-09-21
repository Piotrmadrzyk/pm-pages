// Generator scen z briefu (AI) — jak elevenlabs.js, nie trzyma zadnego
// klucza dostawcy (Anthropic) tutaj. Woli webhook n8n, ktory sam:
// 1) probuje wyciagnac link ze strony wspomnianej w briefie i pobrac jej
//    tresc (Jina Reader, subworkflow otworz_link) — zeby nie zmyslac ofert,
// 2) generuje sceny (tekst/lektor) przez istniejacy credential Anthropic.
import { getSharedSecret } from "./dona-secret.js";

const N8N_WEBHOOK_URL =
  process.env.DONA_N8N_SCENEGEN_URL ||
  "https://pmresearch.app.n8n.cloud/webhook/maszynka-generuj-sceny";

export async function generateScenesFromBrief({ title, brief, targetSeconds }) {
  const sekret = getSharedSecret();
  const res = await fetch(N8N_WEBHOOK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sekret, title, brief, targetSeconds }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    const err = new Error(`Generator scen (przez DONA/n8n) blad ${res.status}: ${detail}`);
    err.status = res.status;
    throw err;
  }
  const data = await res.json();
  if (!Array.isArray(data.scenes)) {
    const err = new Error("Generator scen zwrocil nieprawidlowa odpowiedz (brak scenes[]).");
    err.status = 502;
    throw err;
  }
  return data.scenes;
}
