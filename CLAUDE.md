# Dark YouTube — comece aqui

Pasta de produção de 4 canais (vídeo longo, Shorts, Reels). Dono: Maiquel. Criado em 02/11/2026.
A pasta fica em `D:\DarkYouTube`; o caminho `C:\Users\Admin\Documents\Codex\2026-09-10\Dark YouTube` é uma junção para lá. Use qualquer um dos dois.

## Ordem de leitura (toda tarefa)
1. **Este arquivo**: o que existe e onde.
2. **[`ORQUESTRADOR.md`](ORQUESTRADOR.md)**: o que fazer em cada etapa, em cada canal, quem faz (modelo) e onde parar para o Maiquel.
3. **[`REGRAS_UNIVERSAIS.md`](REGRAS_UNIVERSAIS.md)**: regras de todo vídeo de todo canal.
4. **A ficha do canal** em [`canais/`](canais/): identidade, voz, paleta, estrutura, o que deu certo e o que não deu.
5. **Skill `video-gate`** (`.claude/skills/video-gate/SKILL.md`): os gates 1 a 6 de vídeo longo.
6. Antes de kit, upload ou calendário: [`CLAUDE_YT_ANTI_DEMONETIZATION.md`](CLAUDE_YT_ANTI_DEMONETIZATION.md) §6. Em conflito de monetização, ele vence.

## Os canais
| Canal | Plataformas | Ficha | Projetos | Motor de vídeo | Voz | Chrome de automação | Prefixo da conversa |
|---|---|---|---|---|---|---|---|
| **The Cracked Ledger** (@thecrackedledger) | YouTube (longo + Shorts), TikTok (longo), Instagram | [`canais/CRACKED_LEDGER.md`](canais/CRACKED_LEDGER.md) | `projects/<id>/` + `projects/<id>.json` | `tools/produce.py`/`pipeline.py` → `tools/ec_gfx.py` → `tools/ec_montage.py`; Motion em `tools/hyperframes/` | ElevenLabs Brian 0.86 (`config/montage.json`) | `browser_profile_ledger`, porta 9336 | `Ledger · …` |
| **Show Your Work Puzzles** | YouTube Shorts (1/dia) + TikTok, Instagram, Facebook | [`canais/SHOW_YOUR_WORK.md`](canais/SHOW_YOUR_WORK.md) | `puzzles/<tema>/` | `puzzles/_engine/build.py` (puzzle) e `puzzles/ec_lib` (How It Works) | Kokoro `am_onyx` | `browser_profile_syw`, porta 9335, ou a extensão Claude in Chrome | `SYW · …` |
| **Grandpa Walt** | Facebook e Instagram (Página do Walt) | [`canais/GRANDPA_WALT.md`](canais/GRANDPA_WALT.md) | `projects/_characters/grandpa-walt/` e `projects/grandpa-walt/<ep>/` | `walt_tts.py` → `walt_montage.py` | OpenAI ash + abertura/fecho gravados | nenhum para a Meta: o Maiquel agenda à mão | `Walt · …` |
| **The Rule Changed** (@TheRuleChanged) | só YouTube (longo + Shorts) | [`canais/RULE_CHANGED.md`](canais/RULE_CHANGED.md) | `scamlaw/<epNN_tema>/` | `puzzles/ec_lib/build.py`, tema `rulechanged` | Kokoro `am_onyx` 0.95 | `browser_profile_walt` (o canal era do Walt); a porta muda quando o Chrome trava (9337 em 01/11) | `Rule Changed · …` |

Conversas fora de canal (ferramentas, skills, ec_lib, Telegram) usam o prefixo `Ferramentas · …`. Cada canal tem seu grupo na barra lateral do app.

## Onde fica cada coisa
| O quê | Onde |
|---|---|
| Regras de todos os canais | `REGRAS_UNIVERSAIS.md` |
| Regras e histórico de um canal | `canais/<CANAL>.md` (de onde veio cada regra: `canais/MAPEAMENTO.md`) |
| Detalhe operacional do Ledger | `CHECKLIST_VIDEO_YOUTUBE.md` (lista + registro de erros), `PADRAO_VIDEOS.md`, `GEMINI.md` |
| Detalhe operacional do Walt | `CLAUDE_WALT.md`, `CLAUDE_WALT_PRODUCTION.md` |
| Skills e ferramentas testadas (o que é, repo, licença, resultado) | `skills/REGISTRO.md` (fonte única); teste novo em `skills/testes/` com `skills/TESTE_MODELO.md` |
| Scripts | `tools/` (Ledger, kit, upload, QA, `produce.py`), raiz (`montage.py`, `pipeline.py`, `walt_*.py`) |
| Biblioteca de cenas EffectCraft (SYW How It Works, Rule Changed) | `puzzles/ec_lib/` — **dona: sessão ec-lib; não editar, pedir a ela** |
| Fotos e logos reaproveitáveis | `library/entities/` |
| Fontes (só OFL) | `fonts/` |
| Configuração | `config/` (`montage.json`, `chrome.json`, `publish.json`), `.env` (nunca imprimir nem commitar) |
| Fila de redes sociais | `social/queue.json` (só itens aprovados) |
| Pesquisa de temas e canais | `research/` |
| Métricas | `yt-analytics/` (`reviews/LATEST.md`), `CLAUDE_ANALYTICS_*.md` |
| Arquivo morto | `archive/`, `projects_archive/`, `projects/_archive/` |

## Modificar só onde precisa
- **Regra nova:** vale para todos → `REGRAS_UNIVERSAIS.md`; vale para um canal → `canais/<CANAL>.md`. Uma regra mora num lugar só; os outros arquivos apontam para ela.
- **Erro apontado pelo Maiquel:** vira regra no mesmo dia, e o caso entra em "Deu certo / não deu" da ficha do canal (no Ledger, também no registro de erros do CHECKLIST).
- **Ferramenta ou skill testada:** uma linha em `skills/REGISTRO.md`. Não espalhar em outros arquivos.
- **Vídeo pronto que precisa de ajuste:** refazer só a cena afetada (comandos por motor em `ORQUESTRADOR.md`, fluxo C). Nunca regerar voz, imagem ou render inteiro por causa de uma cena.
- **JSON de projeto:** cópia `.bak-<motivo>` antes; editar por Python ou Write, nunca à mão no meio de um render.
- **Código de motor:** corrigir a causa no motor, uma vez, e checar quem mais usa a função. Motor de outra sessão (ec_lib) → pedir à sessão dona.
- **Não criar arquivo novo** se um existente já cobre o assunto. Não mover pastas nem renomear arquivos de outros canais sem OK.

## Limites que não mudam
- Nada publicado, agendado, enviado ou pago (Grok, TTS pago, crédito) sem OK do Maiquel por escrito.
- Nunca pedir nem digitar senha. Tela de login = registrar e parar.
- Nunca abrir um perfil real do Chrome (`chrome_junction`, User Data, Profile N) com porta de depuração. Só as pastas `browser_profile_*` ou a extensão. Nunca matar o Chrome; fechar só por `Browser.close` e quando o Maiquel mandar.
- Meta (Facebook, Instagram, Business Suite): nada de automação por navegador.
- Nunca inventar número ou fato. Todo arquivo entregue com caminho absoluto.
- Um agente por vez em cada projeto; um render por vez na GPU (RTX 3070, 8 GB).
