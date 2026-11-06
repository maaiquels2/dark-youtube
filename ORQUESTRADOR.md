# Orquestrador: quem faz o quê, em cada etapa, em cada canal

Criado em 02/11/2026. Porta de entrada: [`CLAUDE.md`](CLAUDE.md). As regras ficam em `REGRAS_UNIVERSAIS.md` e em `canais/`; aqui fica só o **fluxo**. Os gates de vídeo longo são os da skill `video-gate`.

## 1. Papéis (todo vídeo, todo canal; regra do Maiquel de 30/10)
| Papel | Modelo e esforço | Faz | Não faz |
|---|---|---|---|
| **Coordenador** | Opus, alto | lê a ficha do canal, decide estrutura e tipo de cena, revisa os quadros, confere o final, fala com o Maiquel | trabalho braçal que um agente faz |
| **Executor** | Sonnet, médio | pesquisa, rascunho de roteiro, `scenes.json`, correções, build com quadros de teste | julgar se o vídeo está bom; decidir estrutura |
| **Operador** | Haiku, baixo | render final, mixagem, versão de celular, upload privado, fila | julgar imagem; mexer em roteiro |
| **Fiscal** | Sonnet, médio (subagente) | lê tudo o que o Maiquel pediu para este vídeo (conversa, ficha do canal, `REGRAS_UNIVERSAIS.md`) e mantém `logs/pedidos.md`; em cada gate confere item por item se algo foi esquecido, inclusive pelo Coordenador | produzir, corrigir, aprovar |

- Agente começa sem memória. Use o modelo de brief da seção 7.
- Um render por vez na GPU. Agentes em paralelo só para leitura e pesquisa.
- Motor de outra sessão (`puzzles/ec_lib`): pedir mudança à sessão ec-lib, não editar.

## 2. Onde parar para o Maiquel
Só nestes pontos (video-gate):
1. **Vídeo final**: ele assiste o master inteiro e aprova por escrito. Sem isso, nada de kit nem Shorts.
2. **Publicar, agendar ou tornar público**: upload privado só com OK; público só com outro OK.
3. **Gasto**: Grok, ElevenLabs, OpenAI TTS ou qualquer crédito.
4. **Ação irreversível**: apagar, trocar nome de canal, rebranding.
5. **Falta algo que só ele tem**: login, chave, foto sem fonte livre, decisão de "Em aberto".

Fora disso, cada etapa roda, passa pelo gate e segue.

## 3. Fluxo A — vídeo longo novo
| # | Etapa e gate | Quem | Ledger | The Rule Changed | SYW (longo de domingo) | Walt |
|---|---|---|---|---|---|---|
| 0 | Pré-voo | Coordenador | `CHECKLIST_VIDEO_YOUTUBE.md` + `CLAUDE_ANALYTICS_FEEDBACK.md` | ficha + `research/canal_golpes_lei/PESQUISA.md` | ficha | `CLAUDE_WALT.md` + `CLAUDE_WALT_PRODUCTION.md` |
| 1 | Pesquisa (Gate 1) | Executor pesquisa, Coordenador revisa | entidades com foto/logo, preços diários para gráfico | fontes primárias (FCC, FTC, govinfo) + recortes `tools/web_clip.py` | fonte de todo fato na tela | fact check na tabela do roteiro |
| 2 | Roteiro (Gate 2) | Executor escreve, Coordenador revisa | 12 padrões de retenção, ≥ 1.100 palavras, capítulo narrado | arco SCAM → CASE → RULE → como se proteger; título e capa sem número | estrutura do puzzle/How It Works | `projects/_characters/grandpa-walt/<ep>.md` + `episode.json` |
| 3 | Voz (Gate 3) | Operador gera, Coordenador confere ASR ≥ 95% | `montage.py <id> --step tts` (Brian, pago: conferir saldo) | Kokoro → `assets/timing_raw.json` | Kokoro | `walt_tts.py <md> --episode <ep>` (pago só com OK) |
| 4 | Cenas (Gate 4) | Executor monta, Coordenador olha os quadros | `tools/ec_gfx.py`, Motion `tools/hyperframes/`, Grok só com OK; imagem de cena: `tools/scene_img.py` (Flow pela extensão Claude in Chrome, um motor por vídeo, `--era`; ChatGPT reserva; FLUX `tools/local_img.py` último recurso) | `scenes.json` + `build.py <proj> --frames`; imagem `tools/local_img.py` (FLUX) | `puzzles/_engine/build.py` ou `puzzles/ec_lib` | `tools/walt_local.py` + Wan `tools/walt_video_test.py` |
| 5 | Montagem e QA (Gate 5) | Operador renderiza, Coordenador abre todas as folhas | `tools/ec_montage.py`, `qa_gate`, `qa_sheets`, `final_sweep`, `palette_check` | `build.py <proj> --render`, depois `--sheet renders/<out>.mp4` | `--render` + folha | `walt_montage.py <saida> <ep>` |
| — | **PARADA: Maiquel aprova o final** | | | | | |
| 6 | Kit | Executor escreve, Coordenador confere checklist anti-desmonetização §6 | `tools/yt_kit.py` + `tools/kit_check.py --online`; **3 capas** (ver "Capas com teste A/B" abaixo) | `kit/youtube_kit.md` + `kit/thumb_epNN.jpg`; **3 capas** | kit do episódio | texto do post (o Maiquel publica) |
| 7 | Upload privado | Operador | `tools/yt_upload.py` (conferir canal no Studio antes) | Studio pelo Chrome `browser_profile_walt` via CDP | `puzzles/yt_long.py` / `puzzles/yt_schedule.py` (porta 9335) | manual no Facebook |
| — | **PARADA: público ou agendamento** | | | | | |
| 8 | Shorts (Gate 6) | ver fluxo B | | | | |

Cada gate grava `logs/gate-N.md` no projeto: o que foi conferido, o que **não** foi e o resultado.

### Revisão cega e controle de pedidos (desde 05/11/2026, aprovado pelo Maiquel)
Ideia do artigo de Eian (@EianLu, X, 05/11/2026), adaptada ao nosso fluxo.
- **Fiscal desde o Gate 1:** o Coordenador abre o Fiscal (tabela de papéis acima) no início do vídeo. Ao fim de cada gate, o Fiscal marca em `logs/pedidos.md` cada pedido como "feito", "não feito" ou "não se aplica", com a prova (arquivo, quadro, tempo). Gate com pedido "não feito" não fecha. Ajuste pedido pelo Maiquel no meio do caminho entra na lista no mesmo dia.
- **Revisor só do roteiro (fim do Gate 2, antes da voz):** um agente novo recebe **só o roteiro final**, sem conversa, pesquisa nem conclusões. Ele:
  1. escreve a história que entendeu;
  2. lista o que não entendeu;
  3. pergunta em cada virada "por que isso aconteceu? de onde veio?";
  4. diz se o vídeo cabe numa frase e se o gancho prende.
  Só aponta erros, não edita. Voz só depois de "aprovado".
- **Revisão cega do master (Gate 5):** o revisor independente recebe só o vídeo, sem o roteiro nem o que o Coordenador acha. Escreve o que entendeu, os problemas com tempo e diz o que **não** consegue checar (som, ritmo real).
- **Antes de gastar:** em toda geração paga (Grok, Flow com crédito, TTS pago), um agente revisor confere o prompt e as imagens de referência, item por item, e escreve "aprovado" antes do pedido de OK ao Maiquel.
- **Primeiro e último quadro em vídeo de IA:** cena de Grok/Flow/Wan sai de imagem de referência, nunca só de texto. Quando o motor aceita, mandar o 1º e o último quadro: fazer primeiro o quadro mais cheio e editar esse quadro para fazer o outro (mesma câmera e enquadramento). Antes de gerar, conferir:
  - todo objeto da ação já está no 1º quadro;
  - pessoas em poses diferentes (senão o modelo move todas juntas);
  - espaço livre para onde algo vai cair ou andar;
  - os dois quadros sobrepostos não desalinham no que não deve mudar (parede, tamanho de objeto);
  - no tamanho do celular, nada importante fica pequeno demais.
  O prompt descreve segundo a segundo, com um ou dois movimentos por tomada, direção pela tela ("para a esquerda da tela") e quantidades escritas ("só um envelope").

### Capas com teste A/B (etapa 6 e depois do upload; Ledger e The Rule Changed)
As regras estão em `REGRAS_UNIVERSAIS.md` §12, "Capas com teste A/B". Abaixo está o como fazer. O primeiro caso foi Binance/Weil, em 03/11. Os scripts ainda estão em `research/capas_ab_2026-11-03/` e passam para `tools/` quando o padrão se firmar.

1. **Conceitos (Coordenador):** escolher 3 conceitos diferentes a partir do roteiro, cada um com até 5 palavras e com fatos que estão no vídeo. Referência do nicho: `research/youtube_ab_2026-11-03/canais_vencedores.md`.
2. **Objeto (Operador):**
   - gerar no ComfyUI local (JuggernautXL, fila em `127.0.0.1:8188`, um job por vez) sobre "plain seamless light gray background", com o estado pedido no texto e o estado contrário no negativo (cofre vazio: negativo "coins, money");
   - gerar de 3 a 6 sementes e escolher olhando a folha;
   - modelo de script: `teste_photocraft/comfy_jobs*.py`;
   - se a placa estiver ocupada por outra sessão, não derrubar nada: esperar ou usar a fila do ComfyUI quando ela estiver vazia.
3. **Recorte e brilho (Operador):**
   - `tools/craft_apps/photocraft/photocraft-cli.exe run <img> --cmd select.subject --cmd layer.layerMask.revealSelection --out cut_<n>.png`;
   - brilho suave com `layer.layerStyle.outerGlow` (opacidade ~32, tamanho ~140, na cor da marca);
   - olhar o recorte sobre fundo vermelho. Se falhar e o fundo for liso, recortar pela cor (exemplo do martelo, em `skills/REGISTRO.md`).
4. **Montagem (Executor):**
   - texto, logos e fundo com as funções de `research/capas_ab_2026-11-03/make_capas.py` e `teste_photocraft/montar3.py` / `montar4.py`: papel claro, seta de subida e queda, sombra, marca do canal;
   - foto e logo reais vêm de `entities/` do projeto.
5. **Revisão (Coordenador):** folha das 3 no tamanho do feed e em tamanho cheio, com a checagem da §12. Corrigir e repetir até passar.
6. **Teste no Studio (Operador, junto com o OK de upload ou agendamento):**
   - Chrome do canal, Playwright num script só: "Teste A/B" → "Somente miniatura" → enviar as posições 2 e 3 → "Começar teste" → **"Salvar"** → conferir;
   - passo a passo e armadilhas na memória "Teste A/B de capa no Studio".
7. **Resultado (Coordenador, em até 2 semanas):** anotar na ficha do canal o vencedor e o conceito de cada opção.

## 4. Fluxo B — Shorts, Reels e TikTok
| Canal | Como nasce o vertical | Onde vai |
|---|---|---|
| Ledger | 3 roteiros próprios de 45 a 60 s, com voz nova, depois do longo aprovado (não cortar a fala do longo). Gerador: `scratch/short_native.py` | YouTube Shorts (1 caprichado/dia), Instagram; TikTok pelo Telegram |
| The Rule Changed | igual ao Ledger: 3 roteiros próprios, com a paleta do canal | só YouTube Shorts |
| SYW | o Short é o produto (puzzle ≤ 90 s, How It Works ≤ 90 s) | YouTube 1/dia; volume no TikTok, Instagram e Facebook |
| Walt | cortes do episódio longo (`_9x16` do `walt_montage.py`), conflito no 1º segundo, até ~47 s, aviso "Walt is a fictional character. The history is real." | Facebook e Instagram (manual) |

Para todos:
- nota ≥ 8 antes de mostrar;
- sem pulsação nem tremida; todo bloco com imagem, logo ou cartão;
- Reels com enquete e até 90 s, enviados pelo Telegram;
- exatamente 5 hashtags;
- fila `social/queue.json` só com item aprovado.

## 5. Fluxo C — ajustar um vídeo pronto (mexer só onde precisa)
1. **Achar a cena:** do tempo no vídeo para a cena ou bloco (`projects/<id>.json` no Ledger; blocos do `scenes.json` na ec_lib; tabela de cenas do Walt).
2. **Guardar a cópia:** `.bak-<motivo>` do JSON.
3. **Mudar só o campo daquela cena.**
4. **Refazer só o que mudou:**

| Motor | Só a cena | Só o áudio |
|---|---|---|
| Ledger (EffectCraft antigo) | `python tools/ec_gfx.py <id> --only N` e depois `python tools/ec_montage.py <id> --redo N` | `python tools/ec_montage.py <id> --audio-only` |
| Ledger, voz de 1 cena | apagar `audio/scene-NN.mp3` e rodar `montage.py <id> --step tts` (só ela é gerada); `tools/words.py` pela `.venv` | — |
| ec_lib (Rule Changed, SYW How It Works) | conferir com `build.py <proj> --frames <segundos>`, depois `build.py <proj> --render`: só as partes cujo conteúdo mudou são refeitas (hash por parte em `ec_build/parts/hashes.json`, desde 02/11). Mudar `ec_lib.jsx`, tema ou duração de bloco refaz as partes seguintes ou todas. Cena com `until` que passa mais de 1 s do próprio bloco: rodar também `--render --part N` da parte seguinte | `build.py <proj> --mix` |
| Walt | `walt_local.py <md> --scenes NN --episode <ep>` e depois `walt_montage.py` | — |

5. **Conferir:** o quadro da cena, as cenas vizinhas e o último quadro do vídeo. Dizer o que não foi visto.
6. **Vídeo já agendado ou publicado:** o YouTube não troca o arquivo; avisar o Maiquel antes de refazer.

## 6. Fluxo D — canal novo ou mudança de identidade
1. Ficha nova em `canais/<CANAL>.md`, no mesmo formato das outras, incluindo "Deu certo / não deu".
2. Uma linha na tabela de canais do `CLAUDE.md` e uma coluna no fluxo A daqui.
3. Grupo na barra lateral do app e prefixo de conversa.
4. Pasta própria de Chrome de automação (`browser_profile_<canal>`), com login feito pelo Maiquel.
5. Paleta e fontes aprovadas por escrito, com prova visual, antes do primeiro render.

## 7. Modelo de brief para agente
```
Canal: <nome> · Projeto: <caminho absoluto>
Leia antes: CLAUDE.md, REGRAS_UNIVERSAIS.md, canais/<CANAL>.md, <README do motor>
Tarefa: <uma etapa só, com o que entra e o que sai>
Mexa só em: <arquivos>. Cópia .bak-<motivo> antes de editar JSON.
Não faça: publicar, gastar crédito, editar puzzles/ec_lib, abrir Chrome real.
Entregue: <arquivo> + o que conferiu + o que NÃO conferiu.
```

## 8. Pendências do sistema (pedir ou decidir)
| Pendência | Com quem |
|---|---|
| `tools/palette_check.py` ainda não lê projetos `scamlaw/` | qualquer sessão de ferramentas |
| `CHECKLIST_VIDEO_YOUTUBE.md` tem 4 paradas (roteiro, logos, cenas, final); a `video-gate` só para no final. Vale a `video-gate` até o Maiquel decidir | Maiquel |
| Itens "Em aberto" de `REGRAS_UNIVERSAIS.md` | Maiquel |
