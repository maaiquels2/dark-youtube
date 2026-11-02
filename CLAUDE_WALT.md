# Grandpa Walt - instruções para o Claude Code

> **Regras organizadas em 01/11/2026:** o que vale para todo canal está em [`REGRAS_UNIVERSAIS.md`](REGRAS_UNIVERSAIS.md); a identidade de cada canal está em [`canais/`](canais/) (mapa em [`canais/MAPEAMENTO.md`](canais/MAPEAMENTO.md)). Este arquivo continua valendo como detalhe do Grandpa Walt.

> **OBRIGATÓRIO (analytics):** antes de roteirizar/editar, leia [`CLAUDE_ANALYTICS_FEEDBACK.md`](CLAUDE_ANALYTICS_FEEDBACK.md) e aplique as ações de `yt-analytics/reviews/LATEST.md` (subordinado a `CLAUDE_YT_ANTI_DEMONETIZATION.md`).


Raiz: esta pasta (`Dark YouTube`). Roteiros em `projects/_characters/grandpa-walt/*.md`.
Runbook completo da temporada: `CLAUDE_WALT_PRODUCTION.md`.
**YPP / anti-demonetização (obrigatório antes de kit/upload):** ler `CLAUDE_YT_ANTI_DEMONETIZATION.md`.


## Produzir EpNN (checklist)
1. Roteiro `projects/_characters/grandpa-walt/<ep>.md` (tabela de cenas + Fact check) + `episode.json` com `next_title`.
2. Imagens: `tools\ComfyUI\python_embeded\python.exe tools\walt_local.py <md> --seeds 3 --episode <ep>` → picks em `scenes/picks.json`.
3. Wan (3–6 cenas, à noite): `tools\ComfyUI\python_embeded\python.exe tools\walt_video_test.py <md> --episode <ep> --scenes 03,13` → `clips/sceneNN.mp4`.
4. Narração: `python walt_tts.py <md> --episode <ep>` (só `lines.json`). Pago: `... --approve-paid` SÓ com OK do Maiquel. Free TTS NÃO instalado.
5. Montagem: `python walt_montage.py <nome_saida> <ep>` → `out/<nome>.mp4` + `_9x16` + `.srt` + `_preview` + `_frames.jpg`.
6. Status: `python tools/walt_status.py <ep> <step> <state>`.
7. QA (ver PRODUCTION) → `approval: awaiting_user`. NUNCA publicar.

## Comandos
```
# imagens (local ComfyUI / Juggernaut XL)
tools\ComfyUI\python_embeded\python.exe tools\walt_local.py projects\_characters\grandpa-walt\<ep>.md --seeds 3 --episode <ep>
tools\ComfyUI\python_embeded\python.exe tools\walt_local.py <md> --scenes 03,08 --seeds 3 --episode <ep>

# vídeo Wan (tiled decode, 1280x704, 73 frames ≈ 3s)
tools\ComfyUI\python_embeded\python.exe tools\walt_video_test.py <md> --episode <ep> --scenes 03,13

# narração (sem gastar)
python walt_tts.py <md> --episode <ep>
# narração paga (requer aprovação explícita)
python walt_tts.py <md> --episode <ep> --approve-paid

# montagem
python walt_montage.py <nome_saida> <ep>

# status
python tools/walt_status.py ep01 images done
```

`episode.json` (em `projects/grandpa-walt/<ep>/`):
- `next_title` — texto do card final (ex. `NEXT\\: EPISODE 6 - OMAHA BEACH`)
- `intro_lines`, `outro_line`, `outro_end_at`, `porch`, `crops`, `media` (opcional; Wan auto se `clips/sceneNN.mp4` existir)

## Regras
- Nunca Grok para cenas de época. Só `walt_local.py` / `walt_video_test.py`.
- Grok (varanda/clipes) só com aprovação de crédito.
- Nunca mexer em perfis do Chrome, nunca criar sessão, nunca matar Chrome (nem Profile 10).
- Nunca imprimir/commitar `.env`.
- Nada de TTS pago sem aprovação. Nada postado sem aprovação.
- Walt é ficcional; fatos checados. Sem unidade real, sem gente real nos romances.

---

## Motion tooling (2026-10-24)

For HTML end cards / packaging video, use **HyperFrames** (not Remotion). For Creche / web UI anti-slop checks, use **Impeccable**.
See `TOOLS_MOTION.md` in this folder for install paths, commands, and the smoke-test end card.


> Alcance internacional: leia tambem CLAUDE_INTERNATIONAL_REACH.md antes de roteirizar ou preparar upload.
