# Gate 3 — Fala (ep02_zelle) — 02/11/2026

Resultado: PASSA.

- Voz: Kokoro am_onyx, velocidade 0,95 (local, sem custo).
- assets/voice.wav: 543,2 s (9 min 03 s), acima do piso de 8 min. assets/timing_raw.json com o tempo de cada palavra.
- ASR local (tools/asr_local.py, faster-whisper): fidelidade 96,97% contra o roteiro (sem contar formato de número).
- Corrigido na 1ª geração (cópia em narration.json.bak-pronuncia e assets/voice_v1.wav):
  - "Coned Billing" era lido "Cone Billing": o roteiro agora diz "Con Ed Billing" (blocos 1 e 7). Na tela o nome aparece escrito como no processo, "Coned Billing".
  - "ic3 dot gov" era lido "ik3": agora "I C three dot gov" (bloco 60); o ASR ouviu "ic3".
- Divergências restantes são de formato ("Zell" para Zelle, "20th", "%"); Zelle se pronuncia "zell".

## Não conferido
- Não ouvi o áudio inteiro; conferência por transcrição.
- Loudness: normalizada na mixagem do build.
