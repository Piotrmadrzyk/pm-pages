// Wspolny sekret miedzy tym narzedziem a integracjami n8n (TTS/SFX w
// server/elevenlabs.js, generator scen w server/scenegen.js). Trzymany w
// n8n Data Table PM_sekrety_wspolne, wiersz "maszynka_szortow_sekret" -
// NIE jest kluczem zadnego dostawcy (ElevenLabs/Anthropic), tylko haslem
// miedzy tym narzedziem a webhookami n8n, ktore te klucze faktycznie trzymaja.

export function getSharedSecret() {
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
