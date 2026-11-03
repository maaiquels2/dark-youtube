# Registro de skills e ferramentas — fonte única

Criado em 01/11/2026. Uma linha por skill ou ferramenta. Teste novo: copiar `skills/TESTE_MODELO.md` para `skills/testes/AAAA-MM-DD_<nome>.md` e atualizar a linha aqui.
Regras da casa vencem as das skills (`video-gate`, `REGRAS_UNIVERSAIS.md`, `CLAUDE_YT_ANTI_DEMONETIZATION.md`). Instalar ou rodar código de terceiros só com OK do Maiquel.

**Status:** em uso · aprovada (instalada, sem uso real ainda) · reprovada · só lida · não instalar.
**Etapa:** video-gate 1 Pesquisa · 2 Roteiro · 3 Fala · 4 Imagens/cenas · 5 Montagem/revisão · 6 Shorts · Kit · Publicação.
"não conferido" = não achei evidência nos documentos e memórias.

## 1. Skills instaladas no projeto (`.claude/skills/`)

Todas instaladas em 01/11/2026 copiando só a pasta da skill (SOURCE.md + LICENSE); nenhum script executado.

| Skill | Para que serve | Etapa | Repositório / commit | Licença | Status | Teste (data, projeto): certo / errado | Canais |
|---|---|---|---|---|---|---|---|
| video-gate | Pipeline por etapas com revisão obrigatória; piso 8 min, alvo 10-12 | Todas | da casa (Archegos, 24/10/2026) | própria | em uso | Usada em todo vídeo longo desde 24/10 | Ledger (e regra para todos) |
| fact-check-workflow | Cada afirmação vira item com fonte, nota e decisão | 1, 2 | github.com/jamditis/claude-skills-journalism `a1e2709cea3e` | MIT | aprovada | não conferido | todos |
| technical-video-script | Revisar roteiro como folha de cenas: gancho 30 s, ritmo, orçamento de tempo, descrição com 1 CTA | 2 | github.com/samber/developer-relations-skills `a2ae344aa938` | MIT | aprovada | não conferido. Feita para screencast: PADRAO_VIDEOS.md e `cortes-verticais` têm prioridade | todos |
| flux-best-practices | Como escrever prompt para o FLUX.2 Klein local | 4 | github.com/calesthio/openmontage `195eab24478d` (autor declarado: Black Forest Labs) | AGPL-3.0 (repo) — uso interno ok, não redistribuir | aprovada | não conferido | Ledger, Walt |
| comfyui-prompt-engineer | Prompt por modelo do ComfyUI (Juggernaut XL, Wan 2.2) e negativos | 4 | github.com/mckruz/comfyui-expert `dee27dc3d69b` | MIT | aprovada | não conferido. Teve aviso em 1 auditoria do skills.sh | Walt, Ledger |
| comfyui-troubleshooter | Diagnóstico quando workflow do ComfyUI falha (erro, nó, VRAM) | 4 | github.com/mckruz/comfyui-expert `dee27dc3d69b` | MIT | aprovada | não conferido. Nó/modelo novo = perguntar antes | Walt, Ledger |
| acestep | Gerar trilha ou separar faixas com ACE-Step | 4/5 | github.com/digitalsamba/claude-code-video-toolkit `4f0d7e6cad8a` | MIT | aprovada | não conferido. Padrão da skill é a nuvem acemusic.ai: usar só o modo local | todos |
| ffmpeg | Receitas de corte, conversão, compressão, áudio, legenda queimada | 5 | github.com/digitalsamba/claude-code-video-toolkit `4f0d7e6cad8a` | MIT | aprovada | não conferido. Partes de Remotion não se aplicam | todos |
| character-animation-qa | QA de animação: amostra de quadros, prévia no navegador, ffprobe do final | 5 | github.com/calesthio/openmontage `195eab24478d` | SKILL.md diz MIT; LICENSE do repo é AGPL-3.0 | aprovada | não conferido | SYW, Ledger (Motion) |
| youtube-seo | Título, descrição, capítulos, tags, miniatura para busca | Kit | github.com/kostja94/marketing-skills `45143a7d6d8f` | MIT | aprovada | não conferido. Sempre depois do checklist anti-desmonetização §6 | todos (YouTube) |
| vercel-react-best-practices | Boas práticas de React/Next.js | — (não é de vídeo) | vercel-labs/agent-skills (skills-lock.json, sem SOURCE.md) | não conferido | só lida | Não entra no pipeline de vídeo | nenhum |

## 2. Skills globais (`C:\Users\Admin\.claude\skills\`)

| Skill | Para que serve | Etapa | Repositório / commit | Licença | Status | Teste: certo / errado | Canais |
|---|---|---|---|---|---|---|---|
| cortes-verticais | Escolher e montar cortes verticais de um vídeo longo | 6 | não conferido (sem SOURCE.md) | não conferido | em uso | `tools/shorts.py` segue esta skill. 30/10: Shorts nativos verticais viraram padrão; 01/11 Weil v1 recusado (pulsação, só frases), v2 com fundo+logos+cartões | Ledger, Walt |
| hyperframes, hyperframes-cli, hyperframes-registry, media-use | HTML → MP4 determinístico; cenas Motion, cartões, end cards | 4, 5, 6 | HeyGen hyperframes; CLI usado `hyperframes@0.8.191`; commit não conferido | não conferido | em uso | 24/10 end card do Walt ok; 28/10 Tricolor: 14 cenas Motion aprovadas (tipografia Inter nos números); padrão nas explicações do Ledger | Ledger, SYW, Walt |
| impeccable | Auditoria e design de UI web | — (web) | não conferido | não conferido | só lida para vídeo | Testada no projeto Creche, não em vídeo | nenhum |

## 3. Ferramentas locais e bibliotecas

| Ferramenta | Para que serve | Etapa | Origem / onde está | Licença | Status | Teste (data, projeto): certo / errado | Canais |
|---|---|---|---|---|---|---|---|
| FLUX.2 Klein 4B | Imagem de cena na GPU, sem crédito | 4 | `%LOCALAPPDATA%\DarkStudio\flux\.venv`; `tools/local_img.py` | Apache 2.0 (uso comercial ok) | em uso | 18/10, WeWork: 4-bit NF4 ~5 GB, ~10 s/imagem; Maiquel gostou do FLUX+parallax vs Grok. 8-bit = ruído puro (não usar). Prompt com metáfora sai simbólico | Ledger, Walt |
| Google Flow — Nano Banana Pro (imagem) | Imagem de cena na nuvem, assinatura Google AI Pro, 0 crédito | 4 | flow.google.com (navegador do app, login do Maiquel); baixar pelo endereço assinado `flow-content.google` do editor | termos do Google (uso comercial: conferir) | aprovada (teste) | 02/11, Binance, 11 cenas: melhor nitidez e composição, obedece "sem pessoas" (FLUX pôs gente em 8 de 11); ~35 s/imagem, 1376x768. Errado: puxa para o retrô (monitor de tubo, máquina de escrever) e pôs data "OCT 26 '98" na cena 18 → pedir "present day, 2026". `skills/testes/2026-11-02_img_web.md` | Ledger |
| ChatGPT Go (imagem) | Imagem de cena na nuvem, assinatura Go | 4 | chatgpt.com (navegador do app, login do Maiquel) | termos da OpenAI | só lida (teste) | 02/11, Binance, 11 cenas: época certa, 0 pessoas, 0 texto; visual de banco de imagens (laranja/teal forte). ~60 s/imagem, 1672x941. Download: funciona (navegador do app e Claude in Chrome), mas chega com atraso e só com clique real no botão; original 1672x941 PNG. `skills/testes/2026-11-02_img_web.md` | Ledger |
| Kokoro (am_onyx) | Voz local e grátis | 3 | `tools\kokoro_lib`, roda com `tools\ComfyUI\python_embeded\python.exe` | não conferido (pesos do Hugging Face) | em uso | 30/10: am_onyx escolhida entre 8 vozes, velocidade 0.95. Não trocar episódios antigos sem perguntar | SYW (oficial); outros só com OK |
| ACE-Step 1.5 | Trilha de suspense local | 4/5 | `%LOCALAPPDATA%\DarkStudio\ace-step`; `tools/ace_music.py` | MIT (código e pesos) | aprovada | 18/10: 4 faixas por ato chamadas de "perfeitas"; 90 s em ~35 s. Errado: 2ª faixa no mesmo processo trava (VRAM); via `uv run` morreu com exit 127. Ainda fora do pipeline | todos |
| faster-whisper | Conferir narração contra o roteiro, local e grátis | 3 | pacote no `.venv` (não a skill, que é só Linux/Mac); `tools/asr_local.py` | não conferido | em uso | 01/11, piloto robocalls: fidelidade 98,1% (OpenAI bruto 94,4%); CPU ~15 min, GPU 1 min 32 s após instalar cublas/cudnn (com OK) | todos |
| EffectCraft (CLI) + `tools/ec_gfx.py` / `ec_montage.py` | Gráficos animados (chart, flow, relmap, stack, list) e montagem com acabamento | 4, 5 | `%LOCALAPPDATA%\DarkStudio\effectcraft\effectcraft-cli.exe` | não conferido | em uso (0.20.0 desde 02/11; backup da 0.10.0 em `%LOCALAPPDATA%\DarkStudio\effectcraft-0.10.0-backup`) | 17-18/10 WeWork: "muito bom", 7 cenas "ficou perfeito". Errado: logo errado do AIG no Lehman (conferir logos antes); .mov antigo voltando por cima (corrigido) | Ledger, SYW |
| ec_lib (`puzzles/ec_lib`) | Biblioteca dos puzzles no EffectCraft | 4 | `puzzles/ec_lib` (não editar daqui) | não conferido | em uso | não conferido | SYW |
| FilmCraft / PhotoCraft (ArtCraft) | Montagem / melhora de capa | 5, Kit | ArtCraft | não conferido | reprovada | 17/10: FilmCraft não ganha do ffmpeg; PhotoCraft com recorte fraco nas capas | — |
| ComfyUI | Workflows de imagem/vídeo (Juggernaut XL, Wan 2.2) | 4 | `tools\ComfyUI`, porta 8188 | não conferido | em uso | Ver Wan abaixo | Walt |
| Wan 2.2 TI2V-5B | Clipe de vídeo local | 4 | via diffusers (18/10) e via ComfyUI (Walt) | não conferido | em uso só no Walt | 18/10 (diffusers, Ledger): escuro, quase sem movimento, ~93 s/passo → reprovado para o Ledger. 01/11 Walt Ep05-06: Maiquel aprovou "OpenAI + Wan local" | Walt |
| Remotion | Vídeo em React | 5 | não instalado | — | não instalar | 24/10: HyperFrames cobriu o caso | — |

## 4. Descartadas ou só lidas (com motivo)

| Nome | Origem | Status | Motivo |
|---|---|---|---|
| faceless-explainer, embedded-captions | heygen-com/hyperframes | não instalar | Aposentadas pela HeyGen em 21/10/2026; já cobertas pelas skills HyperFrames |
| motion-broll | barty-bart/motion-graphics | não instalar | Repo sem licença; aviso em 2 de 3 auditorias; depende de `setup.sh` com motor próprio |
| Voice Studio (OmniVoice) | debpalash/voicestudio | não instalar | Pesos CC-BY-NC (canal é monetizado); clonar o Brian fere a política da ElevenLabs §12; instala por script remoto |
| win4r/video-director | GitHub | só lida (29/10) | Para vídeo feito em código; brigaria com o video-gate. Ideias portadas: `tools/qa_render.py`, folhas hook/phone, `tools/critico_prompt.md` |
| Pocock/skills, Addy Osmani/agent-skills, Superpowers | GitHub | só lida (29/10) | Engenharia de software; ideias aproveitadas no plano (retro, piso escrito, revisor limpo, prova antes de "pronto") |
| Karpathy | GitHub | só lida (29/10) | Nada novo além do Ponytail |
| Ponytail | plugin | em uso | Modo de trabalho do Claude, não de vídeo |
| Caveman | GitHub | não instalar | Telemetria para Supabase, `curl \| bash`; comprimir os documentos perderia precisão |
| Graphify | GitHub | não instalar | Hooks PreToolUse e HTTP; o Ponytail já dá o mapa |
| UI UX Pro Max, Taste Skill, Anthropic/skills, 8 sites de design | GitHub / web | só lida (29/10) | Feitos para UI web, nenhum de vídeo |
| elevenlabs sound-effects / music | skills.sh | não instalar | Gastam créditos pagos |
| higgsfield-*, superpowers CLI, runcomfy, muapi-* | skills.sh | não instalar | Pagos ou prendem a fornecedor |
| youtube-clipper | skills.sh | não instalar | Baixa vídeo de terceiros (direito autoral) |
| youtube-shorts, captions-and-clipping, long-to-short, short-editing, kokoro-tts, scheduling-and-queue | skills.sh | não instalar | Repetem o que já temos |
| openmontage, josiahsiegel, skills-shell (pacotes inteiros) | skills.sh | não instalar | Só a skill específica, nunca o pacote |
| ArtCraft Crafting Apps (storytold, Apache-2.0): EffectCraft 0.20.0, VectorCraft 0.20.0, SoundCraft 0.16.0, FilmCraft 0.16.0, PhotoCraft 0.19.0, PdfCraft 0.17.0, FigCraft 0.14.0, DesignCraft 0.16.0 | github.com/storytold/<app>, baixados em `tools/craft_apps/` (02/11/2026) | testado (parcial) | EffectCraft 0.20.0: quadros das cenas 5 e 17 do Weil iguais aos da 0.10.0 (diferenca max 11/255); falta testar o mp4 animado antes de trocar `EFFECTCRAFT_CLI`. VectorCraft: `run --in logo.png --cmd select.all --cmd imageTrace.makeAndExpand --export x.svg --export x.png --scale 4` vetoriza o logo da Kirkland, nitido a 3840 px (resolve logo fino). SoundCraft: `convert --normalize` so normaliza pico (-0,1 dBFS), nao LUFS; ffmpeg segue na mixagem. FilmCraft: export aceita `loudnessLufs` (nao testado). PhotoCraft, PdfCraft, FigCraft, DesignCraft: so `--help` lido. Comparacao isolada 02/11 (copia do Weil, `scratch/craft_compare/`): FilmCraft export H.264 com `loudnessLufs=-14` chegou a -14,0 LUFS/pico -1,6 e PSNR 61 dB igual ao ffmpeg loudnorm (-14,0/-1,7), mas levou 166 s contra 20 s e gerou arquivo 4x maior: ffmpeg vence. SoundCraft normalize: -23,7 para -19,5 LUFS com pico -0,1 dBFS (estoura o limite -1,5): ffmpeg vence. PhotoCraft: levels+unsharp no avatar-aiello so realcou halos (o arquivo e monograma MA, nao foto). VectorCraft: `run --commands card.json` monta cartao estatico (retangulo, texto, SVG), mas sem animacao e sem nossas fontes: EffectCraft vence na cena; VectorCraft fica so para vetorizar logos. DesignCraft, FigCraft, PdfCraft: nao comparados. |

## Fontes deste registro
`SKILLS_PIPELINE.md`, `PLANO_MELHORIAS_SKILLS.md`, `research/skills_sh_varredura_2026-11-01.md`, `TOOLS_MOTION.md`, `.claude/skills/*/SOURCE.md` e `LICENSE`, `skills-lock.json` e as memórias do projeto (skills instaladas, revisão de skills, ACE-Step, FLUX, Kokoro, Motion, EffectCraft, voz Brian, Walt Eps 5-10).

**ArtCraft — teste de capa (02/11/2026, Weil, 1280×720).** DesignCraft 0.16 (`run --cmd file.new/frame.create/place.drop/type.char`, swatches obrigatórios, `object.fit fillProportionally`) e FigCraft 0.14 (`run fig.jsonl --out x.png`, props diretos `fill`/`fontFamily`) montaram a capa com o mesmo fundo e a fonte Anton; o resultado dos dois ficou praticamente idêntico e muito perto de `output/capa-1.jpg`. O que a capa atual tem e os dois ficaram sem: escurecimento mais forte (0,35 → ~0,6), contorno branco grosso no "$2B", "NO DEBT." maior. Veredito: **sem ganho sobre o `yt_kit`/Pillow atual**; só valem se a capa precisar de layout editável. FigCraft é o mais simples de scriptar (JSON direto, sem swatch). Arquivos: `scratch/craft_compare/cover/` (`dc_cover.png`, `fig_cover.png`, `fig.jsonl`).
