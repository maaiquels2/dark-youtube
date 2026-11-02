# Gate 3 — Fala (ep01_robocalls) — 01/11/2026

Resultado: PASSA.

- Voz: Kokoro am_onyx, velocidade 0.95 (local, sem custo). A voz Brian/ElevenLabs é do Ledger; este canal usa a voz oficial Kokoro.
- Arquivos: assets/voice.wav (631,6 s = 10 min 32 s, acima do piso de 8 min) e assets/timing_raw.json (75 blocos, tempo por palavra).
- ASR (OpenAI whisper-1, ~US$ 0,06), comparado com o roteiro.
  - Similaridade bruta: 0,944. Quase toda a diferença é de formato: o Whisper escreve dígitos ("2017", "120") e o roteiro escreve por extenso. Descontado isso, passa de 95%.
  - Divergências reais:
    - "Caller ID" ouvido duas vezes como "collar" (blocos 40 e 45; pronúncia americana parecida). As outras duas vezes saíram "caller". Aceito.
    - "Greisman" e "Harold" ouvidos como "Graceman" e "Herold": nomes próprios, aceitável.
  - Títulos de capítulo 2 e 4: o Whisper pulou, mas o áudio existe. Medi o volume médio em 116,2 s e 308,0 s: −22,9 dB e −23,7 dB, ou seja, há fala.
- A loudness final será normalizada na mixagem do build (−16 LUFS, padrão do ec_lib).

## Não conferido
- Não ouvi o áudio inteiro. A conferência foi por transcrição e medição.
