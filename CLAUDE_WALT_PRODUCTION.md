# Grandpa Walt — Runbook de produção da Temporada 1 (Claude Code)

> **OBRIGATÓRIO (analytics):** antes de roteirizar/editar, leia [`CLAUDE_ANALYTICS_FEEDBACK.md`](CLAUDE_ANALYTICS_FEEDBACK.md) e aplique as ações de `yt-analytics/reviews/LATEST.md` (subordinado a `CLAUDE_YT_ANTI_DEMONETIZATION.md`).


Raiz: `Documents\Codex\2026-09-10\Dark YouTube` (todos os comandos rodam daqui).
Base: Page "Grandpa Walt — Plano da Temporada 1" + `CLAUDE_WALT.md`. Em caso de conflito, as REGRAS DURAS no fim vencem.
**YPP / anti-demonetização:** antes de pproval / kit / upload, seguir `CLAUDE_YT_ANTI_DEMONETIZATION.md` (Walt = risco alto Generic & Repetitive).


## 0. Regras duras
1. Grok SÓ para o banco de clipes da varanda, e SÓ com aprovação explícita do Maiquel. Nunca para cenas de época.
2. Chrome: só o perfil fixo Dark Studio (`browser_profile`, CDP 9333). Nunca criar perfil/sessão, nunca matar Chrome (nunca tocar no Profile 10 da Livia).
3. Nunca imprimir, logar ou commitar `.env` / chaves.
4. Gasto zero: `walt_tts.py` só chama OpenAI com `--approve-paid`. Sem essa flag, só grava `lines.json`. Free TTS (edge-tts/Piper) NÃO instalado — instalar precisa de OK.
5. Nada é publicado. Todo episódio termina em `approval: awaiting_user`.
6. Walt e os romances são ficção; a história é real e checada.

## 1. Pré-requisitos
- RTX 3070 8 GB, ffmpeg no PATH, Python do sistema para `walt_montage.py` / `walt_tts.py`.
- ComfyUI: `tools\ComfyUI` na porta 8188. Modelos: Juggernaut XL + Wan 2.2 TI2V-5B (fp16) + umt5 fp8 + wan2.2_vae.
- Clipes fixos: `projects\_characters\grandpa-walt\clips\intro_15s.mp4` e `outro_15s.mp4`.

### Subir / checar ComfyUI
```powershell
Invoke-RestMethod http://127.0.0.1:8188/system_stats | % devices | select name,vram_total
# sobe sozinho via walt_local.py / walt_video_test.py; ou:
cd tools\ComfyUI
Start-Process .\python_embeded\python.exe -ArgumentList "-s","ComfyUI\main.py","--windows-standalone-build","--listen","127.0.0.1","--port","8188" -WindowStyle Hidden -RedirectStandardOutput comfy_out.log -RedirectStandardError comfy_err.log
```
Wan: SEMPRE decode tiled (já em `tools\walt_video_test.py`). Travou? `POST /interrupt`; se não, matar só o processo `ComfyUI\main.py`.

## 2. Status: `projects\grandpa-walt\production_status.json`
```
python tools/walt_status.py <ep> <step> <state> [nota]
# step: script|factcheck|images|picks|wan|narration|montage|qa|approval
# state: todo|running|done|blocked:<motivo>|awaiting_user
```
Não refazer passo `done`. Scripts pulam arquivos existentes.

## 3. Checklist único — produzir EpNN
```
# A) Roteiro
#    projects/_characters/grandpa-walt/<ep>.md  (tabela + Fact check)
#    projects/grandpa-walt/<ep>/episode.json     (next_title obrigatório)
python tools/walt_status.py <ep> script done
python tools/walt_status.py <ep> factcheck done

# B) Imagens locais (3 seeds)
tools\ComfyUI\python_embeded\python.exe tools\walt_local.py projects\_characters\grandpa-walt\<ep>.md --seeds 3 --episode <ep>
# escolher seeds → scenes/picks.json  ex: {"03":3,"09":2}
python tools/walt_status.py <ep> images done
python tools/walt_status.py <ep> picks done

# C) Wan destaque (3–6 cenas, ~8 min/clipe, preferir noite)
tools\ComfyUI\python_embeded\python.exe tools\walt_video_test.py projects\_characters\grandpa-walt\<ep>.md --episode <ep> --scenes 03,13
# saída: projects/grandpa-walt/<ep>/clips/sceneNN.mp4
python tools/walt_status.py <ep> wan done

# D) Narração — PORTÃO
python walt_tts.py projects\_characters\grandpa-walt\<ep>.md --episode <ep>
# ↑ só lines.json. Pago (OpenAI): acrescentar --approve-paid SOMENTE com OK do Maiquel.
# Free TTS ainda NÃO instalado.
python tools/walt_status.py <ep> narration awaiting_user

# E) Montagem (precisa dos NN.mp3 em <ep>/audio/)
python walt_montage.py <nome_saida> <ep>
# saída: projects/grandpa-walt/out/<nome>.mp4 + _9x16 + .srt + _preview + _frames.jpg
python tools/walt_status.py <ep> montage done

# F) QA (abaixo) → approval awaiting_user. NUNCA publicar.
```

### episode.json (exemplo em `tools/episode.json.example` / raiz do episódio)
```json
{
  "next_title": "NEXT\\: EPISODE 6 - OMAHA BEACH",
  "intro_lines": [["01", 1.8], ["02", 7.4]],
  "outro_line": ["17", 1.0],
  "outro_end_at": 9.0,
  "porch": ["06", "10", "15"],
  "crops": {"12": [0.40, 0.30, 0.60]},
  "media": {
    "03": {"type": "wan", "file": "clips/scene03.mp4"}
  }
}
```
- Sem `media`, a montagem usa `clips/sceneNN.mp4` se existir, senão still de `picks.json`.
- `type`: `still` | `wan` | `porch_bank` (arquivo relativo ao episódio ou caminho sob `projects/_characters/grandpa-walt/clips/`).
- Áudio: `projects/grandpa-walt/<ep>/audio/` (fallback legado: `projects/grandpa-walt/audio/` se o do episódio não tiver `lines.json`).

## 4. QA
- [ ] Sem rosto em close / objeto moderno / texto legível nas cenas de época.
- [ ] Walt: cabeça no quadro; boca parada.
- [ ] Áudio OUVIDO do começo ao fim.
- [ ] `.srt` sincronizado.
- [ ] Card final = `next_title` do `episode.json` (número certo do PRÓXIMO episódio).
- [ ] Aviso de ficção aparece; intro e outro presentes; 8–10 min; 9:16 legível.
- [ ] Fatos batem com a lista de checagem.

## 5. Agenda semanal
| Dia | Dia | Noite (GPU) |
|---|---|---|
| Seg | Roteiro + checagem Ep A + episode.json | Imagens Ep A |
| Ter | Picks A; roteiro Ep B | Wan A + imagens B |
| Qua | Picks B; refazer ruins | Wan B |
| Qui | Narração A/B (só se aprovada) | Montagem A |
| Sex | QA A; montagem B | Re-render |
| Sáb | QA B; pacote pra aprovação | — |
| Dom | Buffer | — |

Ordem: Ep01→Ep14 (Page). Ficar 3 episódios à frente.

## 6. Episódios (resumo)
01 Pearl Harbor · 02 Queen Mary · 03♥ Rainbow Corner · 04 Exercício Tiger · 05 Véspera do Dia D (piloto) · 06 Omaha · 07 Bocages · 08 Cobra · 09♥ Paris · 10 Red Ball · 11♥ V-Mail · 12 Hürtgen · 13 Bastogne · 14♥ Remagen/VE Day. ♥ = romance fictício.

## 7. Itens em aberto
- NUMERAÇÃO DO PILOTO: Page diz Ep05 / Omaha Ep06; arquivo e fala antiga diziam Ep4 / "Episode five". Definir `next_title` no `episode.json` do piloto antes de montar.
- TTS grátis não instalado; narração depende de aprovação (pago ou instalar free).
- Banco de 8 clipes da varanda (Grok) ainda não gerado — precisa aprovação de crédito.

## 8. Flags reais dos scripts
| Script | Flags |
|---|---|
| `tools/walt_local.py` | `md` `--seeds` `--scenes` `--episode` |
| `tools/walt_video_test.py` | `md` `--episode` `--scenes` `--frames` `--w` `--h` |
| `walt_tts.py` | `md` `--episode` `--approve-paid` |
| `walt_montage.py` | `<out_name> <episode>` |
| `tools/walt_status.py` | `<ep> <step> <state> [nota]` |

> Alcance internacional: leia tambem CLAUDE_INTERNATIONAL_REACH.md antes de roteirizar ou preparar upload.
