# Checklist único de produção de vídeos (The Cracked Ledger)

> **Regras organizadas em 01/11/2026:** o que vale para todo canal está em [`REGRAS_UNIVERSAIS.md`](REGRAS_UNIVERSAIS.md); a identidade de cada canal está em [`canais/`](canais/) (mapa em [`canais/MAPEAMENTO.md`](canais/MAPEAMENTO.md)). Este arquivo continua valendo como detalhe do The Cracked Ledger.

> **OBRIGATÓRIO (analytics):** antes de roteirizar/editar, leia [`CLAUDE_ANALYTICS_FEEDBACK.md`](CLAUDE_ANALYTICS_FEEDBACK.md) e aplique as ações de `yt-analytics/reviews/LATEST.md` (subordinado a `CLAUDE_YT_ANTI_DEMONETIZATION.md`).


Use este arquivo do começo ao fim de cada vídeo, em qualquer ferramenta (Claude Code, Antigravity, scripts). Ele junta o `PADRAO_VIDEOS.md`, o `GEMINI.md` e os erros do documentário da Argentina. Em caso de conflito, vale a seção **Decisões em aberto** no fim, até o Maiquel decidir.
**YPP / anti-demonetização (obrigatório antes das seções 10–11 de kit/upload):** `CLAUDE_YT_ANTI_DEMONETIZATION.md`. Em conflito de política YPP, esse arquivo vence o ritmo/volume.


Ordem do pipeline: **Tema → Pesquisa → Roteiro → Entidades (fotos e logos) → Narração → Gráficos → Cenas → Revisão → Montagem → Aprovação → Kit YouTube → Shorts → Depois de publicar.** Só passa para o próximo bloco quando o anterior estiver todo marcado. Corrigir no bloco certo evita refazer os de baixo.

## 0. Regras que valem o tempo todo
- [ ] **Um agente por vez em cada projeto.** Antes de editar o JSON ou os scripts, confirmar que Claude Code, Antigravity e `produce.py` não estão mexendo no mesmo projeto. Guardar cópia do JSON (`.bak-<motivo>`) antes de mudar.
- [ ] Nada é publicado, enviado nem gasto sem aprovação do Maiquel. Nunca imprimir nem commitar chaves (`.env`).
- [ ] Chrome: só o perfil Dark Studio (CDP 9333). Nunca fechar o Chrome da Livia (Profile 10).
- [ ] **Corrigir a causa, não só o sintoma:** se o erro vem do motor (`tools/ec_gfx.py`), corrigir o motor uma vez e rerrenderizar só as cenas afetadas (`--only`). Se vem do roteiro, corrigir o roteiro e voltar à etapa dele.
- [ ] Todo erro novo que o Maiquel apontar vira regra neste arquivo (seção **Registro de erros**) no mesmo dia.

## 1. Tema e título
- [ ] Tema famoso com ângulo novo, ou notícia só na mesma semana do fato. Série com nome fixo.
- [ ] 5 opções de título. O título vende uma história, não um assunto; sem o nome da empresa no título; valor exato em destaque; até ~60 caracteres. Fórmulas: personagem + valor + contradição, pergunta com "Actually", ou "Explained Simply".

- [ ] Padrões de título de 15 vídeos do nicho (24/10/2026, títulos conferidos no YouTube; fonte: `youtube_padroes.md` do Hermes): valor em dólar em destaque ("$9 Billion Fraud"), trajetória em duas pontas ("From X to Zero", "Rise and Fall"), pessoa como vilão quando há rosto, vocabulário de óbito (collapse, ruin, vanished) em vez de "decline". **Orientação, não bloqueio:** só usar valor que a fonte do roteiro confirma. Esses canais citam o nome da empresa no título; a regra "sem o nome da empresa" continua valendo até o Maiquel decidir.
- [ ] Padrões de abertura do mesmo relatório (cold open com data e cena, par de números em contradição) **não foram conferidos nos vídeos**; tratar como hipótese.

## 2. Pesquisa e roteiro (PARADA: roteiro)
- [ ] Cada fato, número e data tem fonte real (URL ou documento). Fato sem fonte não entra. O que ainda não foi checado fica marcado como "Checar".
- [ ] Lista de **todas as pessoas, empresas e órgãos citados** (incluindo juízes, ministros, executivos). Ela alimenta o bloco 3.
- [ ] Gancho nos primeiros 15 s que entrega a promessa do título. 3 atos, tensão crescente.
- [ ] **O roteiro termina com a chamada falada:** inscrever no canal, curtir e comentar qual quebra investigar a seguir.
- [ ] Nenhum texto de rascunho ou nota interna nos campos que viram tela ("Provided notes", "No source URL supplied", "Draft").
- [ ] Capítulo é uma cena própria narrada ("Chapter two. The Cracks."), com `hold`, nunca por cima de um gráfico.

## 3. Entidades: fotos e logos (PARADA: logos) — antes de renderizar qualquer coisa
- [ ] **Toda pessoa citada na narração tem foto real própria** em `entities/`, de fonte válida (Wikimedia Commons, arquivo oficial) com licença e crédito em `credits.json`. Nunca rosto gerado por IA de pessoa real. Caso Argentina: faltaram Lavagna e Cristina Kirchner.
- [ ] **Recortes de notícia/página oficial:** 6 a 10 por vídeo, pelo menos 1 por capítulo, só a manchete, capturados com `tools/web_clip.py`. Regra em `canais/CRACKED_LEDGER.md`, seção "Recortes" (02/11).
- [ ] Toda empresa, banco central, organismo multilateral (FMI, BCRA, Fed) e agência citada tem logo ou selo oficial em alta resolução. **Conferir os logos numa folha de contato** (o Commons já trouxe logo errado: AIG).
- [ ] Fato grave (protesto, repressão, renúncia, fuga de helicóptero) tem foto histórica real da época, sem corte no assunto principal.
- [ ] Foto vertical de pessoa **nunca** vira fundo 16:9 com parallax nem zoom esticado. Pessoa em tela cheia usa o card `person`.
- [ ] Imagem com resolução suficiente. Ver "Upscaler" em **Decisões em aberto**.

## 4. Narração
- [ ] Voz onyx. Rodar `montage.py <id> --step tts`; cena nova ou alterada tem o `.mp3` apagado antes, para regerar.
- [ ] Rodar `tools/words.py <id>` depois de qualquer mudança de narração (tempo das palavras, legenda e sincronia dos gráficos).
- [ ] A cena final tem a chamada falada de inscrição, curtida e comentário.

## 5. Gráficos animados (EffectCraft) — regras de cada cena
- [ ] **Foco único:** uma ideia visual por cena. Linha do tempo não recebe callout e lower-third juntos. Card `person` não recebe lower-third.
- [ ] **Texto contido** em cartões e caixas (`fit`). Nenhuma letra passa da borda.
- [ ] **Fluxo de ida e volta** entre os mesmos nós: canal de cima e canal de baixo, rótulo acima de um e abaixo do outro. Nunca duas setas na mesma linha.
- [ ] Fluxos simples: no máximo 2 a 3 nós e uma ideia. Rota bloqueada em vermelho, com o texto legível. Nenhuma linha passa por baixo de caixa nem cruza texto.
- [ ] **Quem é citado aparece:** `person` (foto na proporção original, moldura inclinada, nome, cargo em âmbar, tópicos, crédito) ou `pair` para dois personagens. No `pair`, a ligação é um `&` discreto, sem linha de laser e sem texto invadindo as fotos. Lower-third de pessoa leva foto em moldura. Nunca o nome de uma pessoa por cima da foto de outra.
- [ ] Rodapé de fonte só com fonte real (BCRA, INDEC, Ministry of Economy, IMF, tribunal). Crédito de foto presente.
- [ ] Número que explode (inflação, dívida, reservas) = gráfico de linha animado com dados oficiais. Queda de índice = gráfico de linha com valores nos pontos. Nunca gráfico de uma barra só.
- [ ] `tools/palette_check.py <id>` rodado; `accent` declarado no JSON; cor fora da paleta so em logo/foto de terceiro (IDENTIDADE_CANAL_LEDGER.md).
- [ ] Avisos `lugar_sem_mapa` do qa_gate lidos: mapa onde o lugar sustenta a historia, justificativa no gate onde nao.
- [ ] Mapa mostra a silhueta real do país, com `inset` nos pontos locais. Logo real dentro de gráficos comparativos.
- [ ] Capítulo: nada de `ec.full` junto; callout, lower-third e logo só depois de 3,6 s.
- [ ] Proibido: brilho, partículas decorativas, lens flare, degradê roxo, tudo surgindo junto, texto que se mexe enquanto é lido. Fontes só Playfair Display e Inter (nunca Arial, Impact ou Georgia do Windows).
- [ ] **Cargo/kicker e rótulos cabem na largura** (`fit` ou 2 linhas); nada corta na borda direita do card `person`, do lower-third nem do callout.
- [ ] **Lower-third ou callout só quando acrescenta algo.** Pessoa que já tem card `person` na cena ou na vizinha não ganha lower-third. Callout "ALSO INVOLVED" sem informação nova não entra. Nunca nome de pessoa sobre imagem genérica.
- [ ] **Título de capítulo não deixa fantasma:** o gráfico ou card de baixo some por completo (ou só entra depois do capítulo).
- [ ] Rodapé de fonte nunca usa linguagem de rascunho ("Supplied verified facts", "attributed in notes", "Provided notes"). Número 1 usa singular ("1 US dollar").
- [ ] Rerrenderizar só o que mudar (`python tools/ec_gfx.py <id> --only 49,71`).

## 6. Cenas de imagem e vídeo (PARADA: cenas)
- [ ] Gráfico antes de IA: número, dinheiro entre partes ou ordem viram gráfico. IA só no resto.
- [ ] Reconstrução realista do fato, na época e no lugar certos. Nada de cena simbólica ("analista olhando papéis").
- [ ] **Revisar cada clipe a 6 fps** em toda ação. Checar a lógica: mesmo número de pessoas do início ao fim, ninguém aparece do nada, veículos na pista.
- [ ] Prédio e casa com zoom simples (`camera: "zoom"`), não parallax recortado.
- [ ] Grok: gasta crédito, só com aprovação, uma cena por vez. Nunca para cena de época do Walt.

## 7. Revisão de qualidade (antes de dizer "corrigido")
- [ ] **O `qa_gate` roda sozinho no `produce.py` (etapa `qa`, antes da montagem) e para se houver BLOQUEIA; para rodar à mão: `python tools/qa_gate.py <id>`.** Zero BLOQUEIA para seguir; cada AVISO é olhado nos frames. Ele confere o plano (JSON), não os pixels, e grava `logs/qa_gate.md`. Na Argentina ele achou o texto "Provided notes... No source URL supplied" ainda na tela, em 18:00, num master dado como corrigido.
- [ ] **Revisão por folhas de contato:** depois da montagem, `python tools/qa_sheets.py <id>` gera 2 quadros por cena com gráfico (35% e 85% do tempo) e 1 nas demais, mais os 3 quadros finais, em `logs/qa_video/sheet-NN.jpg`. O Claude lê as folhas, dá nota de 0 a 10 por minuto e grava `logs/qa_video.md`; nota abaixo de 8 volta para correção. Sem custo de API.
- [ ] **Revisor independente (29/10/2026):** depois de `qa_render` e `qa_sheets`, um subagente novo, que não viu a montagem, recebe só as folhas (`hook.jpg`, `phone-NN.jpg`, `sheet-NN.jpg`), o roteiro e a saída do `qa_render`, com o rubrico de `tools/critico_prompt.md`. Aprova com todos os eixos >= 8 e nenhum P0; uma rodada de correção e uma conferência (máx. 3 ciclos). Resposta em `logs/critico.md`. Não substitui assistir o master (§9).
- [ ] **Abrir o frame de cada minuto apontado e de cada gráfico novo ou alterado, e olhar.** O validador automático e o relatório não bastam: o relatório da Argentina disse "36 pontos validados" e 6 ainda estavam errados.
- [ ] Olhar também o momento em que cada rótulo aparece (um aviso de bloqueio pode estar apagado no frame escolhido) e o último quadro do vídeo.
- [ ] O relatório diz o que **não** foi conferido, em vez de afirmar que tudo foi validado.

## 8. Montagem e áudio
- [ ] Loudness -14 LUFS, pico -1,5 dB. A música abaixa quando a voz entra (ducking). Trilha de suspense, nada cômico; crédito da música na descrição.
- [ ] Cada impacto visual (entrada de card, carimbo, gráfico preenchendo) tem seu som, 1 frame depois da imagem.
- [ ] Legenda SRT/queimada: até 2 linhas de 42 caracteres, sem terminar linha em "the/of/and", mínimo ~1,5 s na tela. Texto da legenda vem do roteiro, o tempo vem do reconhecimento de voz.
- [ ] **Encerramento:** a citação final transiciona para o card oficial animado: THE CRACKED LEDGER, slogan "DEEP-DIVE FINANCIAL INVESTIGATIONS", botão SUBSCRIBE, "LIKE · COMMENT · NOTIFICATIONS", parado por 6 a 8 s. Sem linha cortando o título, sem título repetido, sem rodapé "SOURCE" no card de marca.
- [ ] Pasta de entrega só com o que o Maiquel abre (nunca `.ass` ao lado do `.mp4`).

## 9. Aprovação do master (PARADA: final)
- [ ] O Maiquel assistiu o vídeo inteiro no player e aprovou por escrito. Sem esse OK, nada de kit nem Shorts.

## 10. Kit do YouTube
- [ ] **Gerar com `python tools/yt_kit.py <id>` e conferir com `python tools/kit_check.py <id>` (zero ERRO).** O gerador lê tudo do projeto (capítulos da linha do tempo, músicas usadas, créditos só das fotos que aparecem, fontes do dossiê); título, abertura, resumo, hashtags e tags vêm de `projects/<id>/kit_input.json`. Nunca copiar um kit de outro vídeo.
- [ ] O `kit_input.json` registra as **5 opções de título** (com a fórmula de cada uma) e qual foi escolhida. Descrição em inglês, primeira linha é a promessa, sem nota de pesquisa.
- [ ] Descrição termina com **exatamente 5 hashtags** (2 a 3 de tema, 2 a 3 de canal) e tem o pedido de inscrição com o link do canal.
- [ ] **Rodar `python tools/kit_check.py <id> --online` antes de aprovar.** Ele baixa a miniatura de cada arquivo creditado no Commons e compara com a foto usada no vídeo; confira `logs/credit-pairs.jpg` (esquerda: vídeo, direita: Commons). Sem `--online` o `kit_check` só compara nomes e pode dar 10/10 com crédito de outra foto. Na Argentina, 11 de 17 créditos apontavam para outra foto, uma assinatura, outra pessoa ou um arquivo inexistente.
- [ ] Cada crédito de foto aponta para o arquivo certo do Commons (o `kit_check` compara). Logo não entra em "photo credits". Fonte da descrição é documento oficial, não Wikipedia.
- [ ] Título escolhido pela fórmula; capa com 3 versões (foto real do protagonista, logo, valor); descrição com fontes, créditos de foto, nota de uso justo, crédito da música e capítulos; tags; SRT em inglês.
- [ ] Config do upload: não é para crianças, conteúdo alterado = Sim, inglês, categoria Educação.
- [ ] **Antes de enviar, abrir `studio.youtube.com/channel/UCvmyoFV8fg5fMtoejd82CRA`** e conferir que não caiu em `channel-appeal`. Se cair, parar e pedir ao Maiquel para trocar a conta.
- [ ] Envio e agendamento só com aprovação. Agenda: seg, qua, sex e dom às 18:00 BRT.

## 11. Shorts, Reels e TikTok
- [ ] **Só depois do vídeo final aprovado:** analisar o vídeo e dar nota de 0 a 10 a cada trecho candidato (força do gancho nos 3 primeiros segundos, clareza sozinho, entrega do que promete, emoção ou curiosidade, ritmo). **Só vira corte quem tem nota 8 ou mais.** O número de cortes não é fixo: pode ser 2 ou 7. Não completar a cota com trecho fraco. Cada corte guarda a nota e o motivo (`score`, `score_why` no `shorts.json`).
- [ ] Cortes de 20 a 45 s (o `tools/shorts.py` aceita até 58 s), cada um de cenas seguidas, sem sobreposição, com gancho de até 12 palavras sustentado por uma frase literal do roteiro. Sem clickbait. O corte precisa chamar a atenção de quem nunca viu o vídeo.
- [ ] **Legenda + chamada para o vídeo completo + exatamente 5 hashtags** (2 a 3 de tema e 2 a 3 de nicho/canal, somando 5), nas 4 plataformas. Instagram: "link in bio".
- [ ] Aviso de ficção nos vídeos do Walt ("Walt is a fictional character. The history is real.").
- [ ] Legenda de trabalho em subpasta; conferir a sequência quadro a quadro na área da legenda.
- [ ] TikTok vai pelo Telegram (`config/publish.json`); Reels e Shorts só entram na fila `social/queue.json` com aprovação. Nada sobe sozinho.

## 12. Depois de publicar
- [ ] Em 48 h, ver o CTR no YouTube Studio. Abaixo de 4%, trocar título ou capa (teste de 3 capas).

---

## Decisões em aberto (o Maiquel decide; até lá, vale a regra provisória)
| Tema | Conflito | Regra provisória |
|---|---|---|
| Upscaler de fotos | `PADRAO_VIDEOS.md` pede restauração Real-ESRGAN 4x; o `GEMINI.md` proíbe "upscalers AI plásticos" e manda usar RAW | Usar a foto RAW de maior resolução; só passar upscaler se a foto for pequena, e conferir o rosto |
| Música | `PADRAO_VIDEOS.md`: uma faixa só; preferência registrada: deixas de suspense só onde faz sentido | Deixas de suspense, sem faixa cômica |
| Duração | Padrão: 10 a 12 min; dados do nicho sugerem 13 a 16 min | 10 a 12 min até decidir |
| Abertura de capítulo | `PADRAO_VIDEOS.md`: capítulo nunca junto de gráfico em tela cheia; `GEMINI.md`: preservar o `full` quando há capítulo | O `qa_gate` só avisa; conferir nos frames que não sobrepõe |
| Fonte do vídeo | Padrão: só Playfair Display e Inter; Walt usa Georgia (Windows) | Georgia só nos vídeos do Walt |

## Decisões de exceção (registro)
- **24/10/2026, caso MFS (empresas em administração):** logos de Morgan Stanley, AlixPartners, Amber Bridging e Zircon Bridging não têm arquivo com licença verificada (busca no Commons sem resultado; CDNLogo indica copyright; Amber e Zircon sem logo público). Decisão do Maiquel: cartão de texto no lugar do logo. Isso contraria o bloco 3 ("toda empresa citada tem logo"). Aviso do qa_gate aceito e anotado.
- **Foto de Paresh Raja (MFS) — REMOVIDA em 26/10/2026:** decisão do Maiquel, só o nome, sem foto (licença não verificada, pessoa viva acusada em processos). Lower-thirds viraram callout "Paresh Raja: denies wrongdoing"; entidade com `sem_foto_aceito` (o qa_gate não bloqueia `pessoa_sem_foto` nesse caso); capas sem rosto.
- **25/10/2026, MFS: logo da própria MFS (Market Financial Solutions) no caso:** a empresa está em administração e não há logo com licença verificada. Decisão do Maiquel: cartão de texto no lugar do logo, pelo mesmo motivo das quatro empresas acima. Afeta as cenas 2, 4, 6, 13 e 24 (avisos do qa_gate de 25/10). Aviso sem_logo do qa_gate para a MFS é aceito por esta exceção.

## Registro de erros → regra
| Erro (projeto Argentina) | Regra que o evita |
|---|---|
| Texto vazando dos cartões | Bloco 5: texto contido (`fit`) |
| Texto secundário de cartão de relação saindo da caixa (MFS, cena 1, 2 linhas em caixa de 180 px) | Bloco 5: caixa do cartão cresce com o texto (tools/ec_gfx.py, relmap); e texto curto nos cartões de capa |
| Textos "Provided notes... no source URL" na tela | Blocos 2 e 5: sem rascunho, fonte real |
| Pessoa citada sem foto (Lavagna, Cristina Kirchner) | Bloco 3: foto real de toda pessoa citada |
| Lower-third do Cavallo sobre a foto do Menem | Bloco 5: nome nunca sobre a foto de outra pessoa |
| Rótulos "ASSETS" e "CASH" empilhados (8:53) | Bloco 5: ida e volta em dois canais |
| Gráfico do Pari Passu confuso (15:51) | Bloco 5: no máximo 2 a 3 nós, uma ideia |
| Cena poluída (16:40) | Bloco 5: foco único |
| Linha estranha entre Milei e Caputo (19:13) | Bloco 5: `&` discreto, sem texto sobre as fotos |
| Vídeo sem pedido de inscrição | Blocos 2, 4 e 8: chamada falada e card final |
| Relatório dizendo "tudo validado" com erros ainda no vídeo | Bloco 7: abrir os frames antes de dizer "corrigido" |
| Linha dourada cortando o título do card final | Bloco 8: encerramento sem linha no título |
| Cargo do card `person` cortado na borda (Perón, Cavallo, Singer, Lagarde, Néstor) | Bloco 5: cargo e rótulos cabem na largura |
| Lower-third de Perón e Alfonsín sem foto, sobre imagem genérica | Bloco 5: lower-third só quando acrescenta; nunca sobre imagem genérica |
| Lower-third e callout por cima do card `person` (Néstor, Singer) | Bloco 5: foco único |
| Título de capítulo "fantasma" sobre card e gráfico (Duhalde, Macri, inflação) | Bloco 5: capítulo sem fantasma |
| Rodapés "Supplied verified facts... attributed in notes" e cena "9 defaults" ainda com "Provided notes" no master | Bloco 5: rodapé sem linguagem de rascunho; bloco 7: qa_gate |
| "1 US dollars per Argentine peso" | Bloco 5: singular quando o valor é 1 |

## Registro de erros → regra (projeto Archegos, 24/10/2026)
Skill obrigatória antes de qualquer vídeo novo: `.claude/skills/video-gate/SKILL.md`.
| Erro (projeto Archegos) | Regra que o evita |
|---|---|
| Vídeo de 5 min 29 s (alvo 10 a 12; piso 8) e estimativa errada de "8 a 9 min" com 715 palavras | Bloco 2 e skill: contar palavras por script (~136 palavras/min) e escrever o número real no pedido de aprovação do roteiro |
| Bancos nomeados com 4 a 5 logos minúsculos num chip sobre imagem grande (1:54, 2:32, 2:52) | Bloco 5: nome de empresa na fala = logo grande (`lineup`, `relmap`, `logo_row`); chip só para 1 logo |
| ViacomCBS citada sem logo (2:45) | Bloco 3 e 5: toda empresa nomeada aparece com logo na própria cena |
| Crédito de foto em português na tela ("fotografo nao identificado na fonte") | Bloco 5: crédito em inglês, "Photo: Agência (via Veículo)" |
| Queda de ação de 27% só como número, sem gráfico (3:02) | Bloco 5: queda = `chart_line` com valores nos pontos e fechamentos reais |
| Linha do tempo dos bancos sem logo (3:14) | Bloco 5: `timeline` aceita `events[].file` |
| Cartão no estilo antigo (`gfx.py`, tipo `scale`) com título cortado e URL no rodapé (3:54) | Bloco 5: nada de `gfx.py` no vídeo novo; tudo EffectCraft |
| Nome do Halligan some rápido e lower-third sobre imagem genérica (4:15) | Bloco 5: pessoa citada = `pair` ou `person`; lower-third ≥ 3,5 s e só com foto |
| Encerramento "sem vida", sem o nome do canal (5:25) | Bloco 8 e regra 8 da Argentina: narração diz o nome do canal; card oficial animado 6 a 8 s |
| Validação passou com 5 de 8 folhas vistas | Bloco 7: abrir as 8 folhas e, em cada gráfico alterado, o último quadro (a folha congela contadores no meio) |
| Capítulo sobre gráfico em tela cheia (CHECKLIST dizia uma coisa, GEMINI.md outra) | Alinhado em 24/10/2026: capítulo é cena própria sem `ec.full`. `qa_gate` **bloqueia** em projeto com data de id ≥ 20261024; antes disso só avisa (Argentina e anteriores) |
| Texto de cartão de relação saindo da caixa, com "..." na tela (MFS, cenas 1, 16, 27, 28, 30) | Bloco 5: nenhum texto de overlay termina em "..."; frase longa é encurtada antes de renderizar; o frame de conferência é tirado com o overlay totalmente visível, não no início da animação |
- **26/10/2026, eleição (projeto brazil-s-stock-market…):** (1) `pipeline.collect_images` trouxe para a B3 o logo de 'Kollektiv Turmstrasse B3' e salvou na biblioteca compartilhada; sempre olhar a folha `logs/entidades-sheet.jpg` antes de seguir e apagar `library/entities/<nome>` se vier errado. (2) Reconstruir o projeto com `scratch/build_*.py` apagava `entities`; o builder agora preserva `entities`, `images_done`, `music_*`. (3) Fatos do ano mudam em horas: o roteiro dizia que o 6x1 e o MEI dependiam do Congresso, mas o Senado aprovou em 14/10 e o MEI foi sancionado em 21/10; re-pesquisar cada medida pela data mais recente antes de escrever.
- **26/10/2026, eleição (inserção de capítulo no meio):** `app.save_project` mantém `ec`, `file`, `photo_file` etc. POR POSIÇÃO da cena (`projfile.SERVER_FIELDS`). Inserir cenas pelo `save_project` desalinhou gráficos e imagens (pessoas do STF em cena errada, arquivos ausentes). Para inserir: montar a lista final de cenas (ec/file dentro de cada cena, nomes de arquivo deslocados), gravar o JSON direto no disco e só então chamar `save_project` (que regera os prompts). Conferir depois: toda `file` existe, `qa_gate` sem bloqueio, e listar o tipo de gráfico de cada cena.
- **28/10/2026, Tricolor ("Your Car Loan Is Someone Else's Bond"):** relatório completo em `projects/tricolor-car-loan-20261027-210000/logs/relatorio-erros-tricolor.md`. Regras novas: (1) rodar `tools/final_sweep.py <id>` depois de todo `final.mp4`; limites: imagem parada ≤ 45% do total e nenhum trecho parado > 8 s (Tricolor ficou em 61%, eleição em 44%); (2) prévia de abertura em 3 cenas curtas, nunca um gráfico único de 28 s; (3) não gerar imagem de fundo para cena de capítulo: o overlay `chapter` do EffectCraft é opaco e cobre; (4) Motion renderizado com duração = `timeline.plan()["L"]` + 0,5 s, nunca a duração do áudio; (5) depois de renderizar em lote, abrir o último quadro de cada clipe e testar quadro em branco; (6) legenda não quebra entre número e unidade (`tools/fix_srt_numbers.py`); (7) trilha sem silêncio > 1,2 s e limitador final a −1,5 dBTP; (8) números nas cenas Motion sempre em Inter 700 (nunca Playfair).
- **30/10/2026, Tricolor (apontado pelo Maiquel):** (1) cartão de capítulo saía só "CHAPTER" sem número: o `num` vinha vazio dos geradores; agora todo `chapter` leva `num` sequencial (conferir no quadro). (2) cartão final (`statement` com `outro`) mostrava a frase digitando por cima do "THE CRACKED LEDGER": corrigido no template (`tools/ec_gfx.py`: com `outro` o cartão é só o encerramento).

> Alcance internacional: leia tambem CLAUDE_INTERNATIONAL_REACH.md antes de roteirizar ou preparar upload.


> Lições dos dados reais (ler antes de roteirizar/publicar): [CLAUDE_ANALYTICS_LESSONS.md](CLAUDE_ANALYTICS_LESSONS.md)

