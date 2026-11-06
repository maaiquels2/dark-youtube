# The Cracked Ledger: identidade do canal

Vale junto com [`REGRAS_UNIVERSAIS.md`](../REGRAS_UNIVERSAIS.md).

O conteúdo de `IDENTIDADE_CANAL_LEDGER.md` (30/10/2026) foi movido para cá sem mudanças; o arquivo antigo virou um atalho.

**Detalhe operacional do Ledger** (ficam onde estão; valem só para este canal):
- `CHECKLIST_VIDEO_YOUTUBE.md`: lista de marcar, na ordem do pipeline, com registro de erros.
- `PADRAO_VIDEOS.md`: título, capa, temas, prompts do Grok, Motion F2/F3/F4 e Shorts nativos.
- `GEMINI.md`: detalhes do EffectCraft (`tools/ec_gfx.py`).
- `research/mapa_conteudo_ledger/MAPA_LEDGER.md`: mapa de pauta (05/11/2026) com 4 pilares, 37 temas e os 10 próximos. Escolher o tema por ele e atualizar quando um tema for feito.

> **OBRIGATÓRIO (analytics):** antes de roteirizar ou editar, leia [`CLAUDE_ANALYTICS_FEEDBACK.md`](../CLAUDE_ANALYTICS_FEEDBACK.md) e aplique as ações de `yt-analytics/reviews/LATEST.md` (subordinado a `CLAUDE_YT_ANTI_DEMONETIZATION.md`).

## Canal
- Documentários de Business & Finance em inglês, @thecrackedledger.
- Alvo de 10 a 12 min; o piso é 8.
- Agenda: seg, qua, sex e dom às 18:00 BRT.

## Voz
- **Desde 03/11/2026: Kokoro `am_onyx` 0.95, local e grátis** (a mesma voz do The Rule Changed). Decisão do Maiquel: o ElevenLabs saiu por custo. `config/montage.json` → `"tts_provider": "kokoro"`; motor `tools/kokoro_tts.py`, chamado pelo `montage.py` e pelos Shorts (`scratch/short_native.py`).
- **Pronúncia:** nome que o Kokoro lê errado entra em `tts_respell` no `config/montage.json` (só muda a fala; a legenda mantém a grafia). Conferir nomes próprios no ASR de cada vídeo. Já corrigidos: Weil → "Wile", Aave → "Ah-vay", Chainalysis → "Chain-alysis".
- **Antes:** ElevenLabs Brian (`nPczCjzI2devNBz1zQrb`), velocidade 0.86, de 24/10 a 02/11. Voltar só com OK: `config/montage.json.bak-voz-elevenlabs`. Vídeos antigos ficam com a voz antiga.

## Paleta (fixa em todo vídeo)
| Item | Valor |
|---|---|
| Fundo | `#0b0e14` (gradiente escuro sutil) |
| Texto principal | creme `#f6f2ea` |
| Rótulos e destaque | âmbar `#f4b042` |
| Alegação, perda, queda | vermelho `#d63a34` (só para isso) |
| Cartões de papel ou logo | `#ece4d0` |
| Texto apagado | `#b0aaa0` |
| Fonte da informação | linha "SOURCE · …" embaixo à esquerda em toda cena |
| Fecho | card "THE CRACKED LEDGER · DEEP-DIVE FINANCIAL INVESTIGATIONS" + SUBSCRIBE âmbar, parado 6 a 8 s |
| Marca nas capas | nome do canal no mesmo canto e tamanho, fundo `#0b0e14` |

**Varia por vídeo (de propósito, regra anti-fábrica):**
- **Uma cor de acento do tema:** declarada em `"accent"` no JSON e usada só em barras, curvas e ícones de dados.
  - Opções: teal `#40c4c8`, azul-aço `#5b8fd6`, verde-musgo `#6fae7a`.
  - Nunca duas ao mesmo tempo, nunca no lugar do âmbar ou do vermelho.
- Imagem de fundo dos capítulos, fotos e composição da capa.
- Formato dos Motion (F2/F3/F4) e ordem das cenas.

**Cor de terceiros:** logo e foto entram com a cor original, em cartão `#ece4d0` ou moldura. Nunca recolorir.

**Proibido:**
- neon, gradiente colorido de fundo, fundo claro em cena inteira;
- mais de uma cor de acento;
- vermelho para algo que não seja alegação ou perda;
- bandeira ou logo desenhado pelo gerador.

**Conferência:** `python tools/palette_check.py <id>`. Avisos entram no gate com justificativa.

## Tipografia
| Elemento | Fonte |
|---|---|
| Títulos (capítulo, nome de pessoa, manchete) | Playfair Display |
| Números | Inter 700, algarismos tabulares, com brilho (s21_inter); nunca Playfair |
| Rótulos | Inter 500, caixa-alta espaçada, âmbar |
| Frases | Playfair Display itálico |
| Capa | Anton |
| Objetos de cena | Courier Prime (documento), Caveat (anotação), Bebas Neue (carimbo) |

Tamanhos em 1080p: título 132/96/76, subtítulo 48–60, texto 30–38, rótulo 24–30, crédito 16+.

## Animação
- **HyperFrames Motion** nas cenas de explicação. Cada cena escolhe o formato que serve ao conteúdo:
  - F2: SVG e curvas;
  - F3: tipografia cinética;
  - F4: câmera virtual.
  - Modelo: `tools/hyperframes/tricolor-s21`.
- **EffectCraft (`tools/ec_gfx.py`)** nos gráficos e cards: `person`, `pair`, `lineup`, `chart_line`, `map` etc. Regras de cada cena em CHECKLIST §5 e GEMINI.
- **Ritmo do Motion (05/11, Red Lobster):** cada passo de uma animação a ≥ 0,9 s do anterior e o estado final parado ≥ 1,5 s antes do corte. Volta de câmera (F4) termina ≥ 1,5 s antes do fim. Se a frase acaba antes, a cena ganha `pause_after` (segundos de pausa depois da fala, em `timeline.plan`) em vez de acelerar. Um cartão só acende quando a fala chega nele. Medir com `scratch/motion_pace.py <id>`.
- **Pessoa:** card `person` com foto P&B em moldura inclinada. Sem foto livre, vale a regra universal §3; o monograma saiu em 01/11.

## Recortes de notícia e de página oficial (obrigatório)
Pedido do Maiquel em 02/11/2026, depois do ep01 do The Rule Changed: recortes reais dão realismo e dinamismo. A regra base (só a manchete, captura, conferência no quadro) está em [`RULE_CHANGED.md`](RULE_CHANGED.md), seção "Recortes"; aqui ficam só as diferenças do Ledger.
- **Quantidade:** pelo menos 1 por capítulo, 6 a 10 por vídeo. Entra quando a fala cita um ato com data: processo, acusação, acordo, multa, falência, comunicado da empresa, decisão do banco central. Vale também quando a imprensa noticiou o fato.
- **Ordem de preferência:**
  1. página oficial: sec.gov (inclusive EDGAR), justice.gov, ftc.gov, federalreserve.gov, govinfo.gov, tribunal (courtlistener.com com o número do processo);
  2. comunicado da própria empresa (site oficial ou EDGAR 8-K);
  3. manchete de imprensa (Reuters, AP, Bloomberg, FT, WSJ, NYT), no máximo 3 por vídeo.
- **Governo fora dos EUA** (BCRA, Banco Central do Brasil, CVM, B3): tratar como imprensa, só a manchete ou o título do comunicado, com crédito. Não é domínio público.
- **Só a manchete** (Maiquel, 02/11): nunca anúncio, menu, barra lateral, foto da matéria ou paywall. Matéria paga serve: só o título aparece.
- **Captura:** `python tools/web_clip.py <url> projects/<id>/clips/<nome>.png "texto a marcar"` (print 2x + .json com caixa, URL e data).
- **Na tela:** cena `web_clip` do `tools/ec_gfx.py` (criada em 02/11). No `projects/<id>.json`: `"ec": {"full": {"type": "web_clip", "file": "clips/<nome>.png", "site": "SEC.GOV", "date": "May 10, 2018", "highlight_say": "palavra falada", "source": "SEC Litigation Release ..."}}`.
  - Recorta sozinho a caixa da manchete do .json e põe margem branca desenhada: nada da página vizinha entra. Outro trecho do documento: `"crop": [x, y, w, h]` (px do print 2x) e, se quiser marcar só uma parte, `"mark_box"`.
  - Cartão `#ece4d0` sobre `#0b0e14`, rótulo âmbar "SITE · DATA" em cima, marca-texto na manchete quando `highlight_say` é falado, zoom centrado lento, linha SOURCE e som de papel + traço.
  - Não usar `evidence_doc` no lugar do recorte: ele redigita o texto.
- **Não substitui:** foto de pessoa, logo, gráfico. É mais uma camada.

## Música
Suspense em deixas (memória "Trilha: suspense") ou faixa única com ducking (`config/montage.json`, `single_music`).
- **Nível (05/11, Red Lobster):** o `ec_montage` nivela cada faixa a −21 LUFS antes do volume da deixa (`track_gain`). Música ≥ 10 dB abaixo da voz em todo segundo, medida com `scratch/mix_audit.py <id>` (`logs/mix_audit.md`) antes de chamar o Maiquel. Efeitos (impacto, whoosh) nunca acima da voz (`sfx_volume` no projeto; padrão 0.55).
- **Duração:** deixa longa só onde a cena pede; vinheta de alegação/virada é curta (`max_dur` ≈ 2,5 s).

## Estrutura
Doze padrões de retenção (PADRAO, 24/10):
- número concreto na abertura;
- contradição como motor;
- "quem paga a conta" perto do fim;
- pausa útil no meio;
- fecho que espelha o gancho;
- capítulo como cena narrada própria.
O resto está no PADRAO.

## Pipeline
- Rotas: `tools/produce.py` ou `pipeline.py`, depois `tools/ec_gfx.py` e `montage.py`.
- Conferências: `tools/qa_gate.py`, `tools/qa_sheets.py`, revisor independente, `tools/final_sweep.py`.
- Kit: `tools/yt_kit.py` e `tools/kit_check.py --online`.
- Projetos em `projects/<id>/`; biblioteca de entidades em `library/entities/`.

## Plataformas, conta e Chrome
- YouTube (longo + 1 Short caprichado por dia), TikTok (formato longo), Instagram (Reels manuais).
- Chrome de automação: `browser_profile_ledger`, porta 9336. Nunca o perfil real "Cracked Ledger" com porta de depuração (deslogou 2 vezes em 26/10).

## Deu certo / não deu
Registro completo de erros: `CHECKLIST_VIDEO_YOUTUBE.md`, "Registro de erros → regra".

| Data | Projeto | Resultado | Lição |
|---|---|---|---|
| 19/10 | crise de 2008 (3 min) | deu certo | v2 e gráfico do Dow aprovados |
| ~23/10 | Argentina | não deu | texto vazando de cartão, pessoa sem foto, nome sobre foto de outra pessoa, rascunho na tela, sem pedido de inscrição: viraram as regras do bloco 5 |
| 24/10 | Archegos | não deu | 5 min 29 s (piso 8), logos minúsculos, queda sem gráfico, validação com 5 de 8 folhas vistas; daí nasceu a skill `video-gate` |
| 26/10 | eleição BR | não deu | logo errado da B3 entrou na biblioteca; inserir capítulo no meio desalinhou os arquivos das cenas |
| 28–30/10 | Tricolor | misto | Motion HyperFrames (`tricolor-s21`) virou o padrão das explicações; erros novos geraram `tools/final_sweep.py` e capítulo sempre com número |
| out/2026 | Bolsa do Brasil | não deu | "more than 15%" narrado contra −13,88% de fechamento oficial: o número falado é o do fechamento |
| 01/11 | Weil (weil-1, weil-3) | deu certo | aprovados; Shorts futuros com roteiro e voz próprios, não cortes |
| 01/11 | analytics | atenção | tráfego vem da busca; longos de 13 a 20 min seguram só 13–26%; sem política brasileira |
| 02/11 | regra de recortes | nova | recortes de página oficial e manchete (aprovados no ep01 do The Rule Changed) passam a valer no Ledger |
| 02/11 | Shorts Binance (binance-1, -2, -3) | não deu → deu certo | 1ª versão: empresas citadas sem logo; binance-3 com ~9 s de tela parada só com "Rebuilding". Corrigido (logo por trecho, TRM Labs em cartão de texto; trecho longo dividido em dois blocos) e os 3 aprovados. Regra em PADRAO_VIDEOS.md, "Shorts nativos" |
| 02/11 | Instagram dos Shorts | decisão | Reels do Ledger saem pela API da Meta (`tools/meta_publish.py run`), sem enquete; vale no lugar de "Reels com enquete pelo Telegram" de REGRAS_UNIVERSAIS para este canal |
| 02/11 | publicação Meta | corrigido | token da Meta invalidado em 25/10 (tarefa "Dark Studio - Reels Instagram" desativada). Renovado com `tools/meta_token.py` (token de Página que não expira); tarefa reativada (de hora em hora). 72 itens antigos da fila (recortes horizontais, Brasil 2022) ficaram `pausado_backlog` para não sair tudo de uma vez: refazer em formato nativo antes de voltar para `pendente` |
| 04/11 | Wirecard v1 (feedback do Maiquel) | não deu | (1) preço da ação citado sem gráfico montando a queda naquele momento (o gráfico só veio ~1 min depois); (2) comunicado em alemão na tela, sem tradução, num canal em inglês; (3) Jan Marsalek citado várias vezes e nunca com foto; (4) visual de "apresentação de PowerPoint" (36% cartão só de texto). Regras: toda fala com queda ou salto de preço tem o gráfico na tela naquele instante; texto em outro idioma na tela sempre com tradução em inglês ("Translated from German"); pessoa citada mais de uma vez precisa de foto de fonte legítima (Interpol, agência, Commons) ou, sem fonte, o motivo registrado; cartão só de texto ≤15% do tempo, com imagem de contexto (ChatGPT/Flow, sem rosto de pessoa real) por trás. Vale para todos os vídeos do canal; Enron, Madoff e Alta Banka ainda não passaram por essa checagem |
| 03/11 | 1º teste A/B de capa (Binance `hsIB1F5WeAc`, Weil `OsfXgi9zkmM`) | em teste | "Testar e comparar" do Studio, só miniatura, iniciado e salvo nos 2 vídeos ainda programados (Maiquel: "Suas favoritas"). Ordem: 1 = capa atual (o Studio já preenche; fica se der Inconclusive), 2 e 3 = novas. Binance: v3 antes/depois dos cofres + v9 recibo. Weil: v1 GM Building "95 YEARS." + v8 "PAID HALF.". Arquivos em `research/capas_ab_2026-11-03/ab_upload/`; como foram feitas: `research/capas_ab_2026-11-03/teste_photocraft/` e `skills/REGISTRO.md` (PhotoCraft). Ler o resultado em até 2 semanas e anotar aqui |
| 04/11 | Wirecard (revisão v2) | críticas do Maiquel | preço citado na fala sem gráfico na tela, notícia em alemão sem tradução, pessoa citada sem foto, 36% de cartão só de texto: **regras:** (1) sempre que a fala disser preço ou queda, o gráfico de linha da série está na tela naquele instante; (2) texto estrangeiro vira tradução em inglês em destaque, etiqueta "Translated from German" e original pequeno; (3) frase de cartão leva imagem de contexto (Flow, sem pessoa real, sem logo, rótulo "Illustration"), no máximo 15% de cartão só de texto; (4) palavra sozinha na última linha ("it.") é defeito |
| 04/11 | Wirecard (pos-aprovacao) | agendado | Longo `91MHL39IkK8` privado/programado 05/11 18:00 com teste A/B de 3 capas (extrato, grafico, tribunal escuro); 3 Shorts proprios agendados no Studio (06, 08 e 10/11); IG/TikTok na fila `aguardando_ok_maiquel` e enviados ao Telegram. Resultado do A/B: ler em ate 2 semanas e anotar aqui |
| 04/11 | QA independente: Alta Banka, Madoff, Enron (revisão v2) | corrigido / pendências | Vídeos aprovados em conteúdo pelo Maiquel; o revisor independente achou: (1) legenda com número por extenso separado da unidade ("forty-seven / thousand"): 6, 12 e 11 blocos, que o `final_sweep` não pegava (só olhava algarismos) → `scratch/qa2_srtfix.py`; (2) linha SOURCE com mais de ~78 caracteres colide com o selo "Illustration" (Madoff 12); (3) imagem gerada com placar e tabela de números quase legíveis (Alta 10) → borrar ou regerar; (4) título de capítulo sobre o letreiro da foto (Enron 87) → recortar a foto; (5) "cartão só de texto" medido só em statement/list/stamp dá 9 a 14%, mas contador, fluxo, linha do tempo e lista sem imagem somam 37 a 62% (Wirecard, 42%): registrar as duas medidas; (6) fala com item "Checar" do gate-1 foi para a voz (Alta 81) e cifra atribuída ao "trustee" que o gate-1 liga à AP (Madoff 17,5 bi): conferir os "Checar" contra a narração antes do Gate 3. Pendências que exigem regravar voz ficaram com o Maiquel. Detalhe em `CHECKLIST_VIDEO_YOUTUBE.md` (QA independente, 04/11) |
| 05/11 | Toys "R" Us (1º da série "What Actually Happened to…") | agendado | Pesquisa só em 10-K/8-K da SEC; nenhuma imagem de IA (fotos do Commons + 12 recortes); revisor independente aprovou no 3º ciclo (P0 do ciclo 1: frase de cena curta não terminava de digitar → `reveal` no `statement`). Master aprovado pelo Maiquel em 05/11. Longo `Kti-Hj9yU9o` programado 06/11 18:00 com teste A/B de 3 capas (A fachada + cadeado "THE DEBT DID IT.", B barras de juros "$5.6B IN INTEREST", C antes/depois "THE $6.6B BUYOUT"), salvo e conferido. Ler o resultado em até 2 semanas e anotar aqui. Shorts próprios ainda não feitos |
| 05/11 | Alta Banka, Madoff, Enron (pos-aprovacao) | agendado | Longos privados/programados 06, 07 e 08/11 18:00 (`XbwdLcP7Wdg`, `LUgWHLCkKvQ`, `Lz1cpKb6dqc`), legenda .srt anexada e teste A/B de 3 capas ativo nos tres. Capas: **Alta** A sede + "LICENSE REVOKED. ALLEGED: 45 BILLION DINARS" (principal), B papel "45.6 BILLION DINARS / ALLEGED / WHERE?", C "WHO PAYS?" + EUR 50,000 "ABOVE IT?"; **Madoff** A extrato "$65B x $17B+ / JUST PAPER." (principal), B foto do DOJ "6 COMPLAINTS. NO PONZI EXAM.", C barras $17.1B formulario / $65B extratos / $17B+ perda real (est.); **Enron** A grafico de linha real out-nov/2001 ($33.84 a 26 centavos, "6 WEEKS. ENRON.", principal), B carta "ONE PAGE. WARNED.", C logo + "LOOKING GREAT." "THEN: $1B+ CHARGE". Scripts: `scratch/make_capas_3longos.py`, `scratch/ab_longos.py`, `scratch/verify_long.py`. Conflito: o Toys "R" Us ja estava programado para 06/11 18:00 (Alta fica no mesmo horario, a pedido). Ler o resultado em ate 2 semanas e anotar aqui |
| 05/11 | Shorts de Alta Banka, Madoff e Enron | agendado em parte | 9 Shorts com roteiro proprio (Kokoro am_onyx 0.95, 32 a 39 s, `scratch/short_ledger3.py`). Agendados: YouTube 6 (`shMWUz_eulA`, `6qIIqzzk20s`, `TptmcfuY7qU`, `uIkxuy3SIe4`, `BhUpoqsEnnc`, `4TIADNQbw64`), TikTok 6 e Facebook 6 (so Facebook marcado no Business Suite), Instagram 9 na fila `pendente` (API). Faltam 3 por rede no YouTube/TikTok/Facebook (limite de ~6 por sessao), registrados em `social/queue.json` como `aguardando_agenda_manual`. Falhas do Chrome do Ledger durante render: CDP trava enquanto o HyperFrames renderiza; fazer upload so depois dos renders |
| 05/11 | Alta Banka (data do longo) | alterado | Longo `XbwdLcP7Wdg` movido de 06/11 18:00 para 09/11 18:00 (Toys "R" Us fica sozinho em 06/11 18:00; 09/11 estava livre depois do Enron, 08/11). Título, capas, teste A/B (ativo) e legenda mantidos. Shorts da Alta (todos linkam o longo) saem antes dele: conferir/mover. Enron-3 no TikTok reagendado 11/11 15:00 com legenda (o sem legenda foi excluído por ordem do Maiquel) |
| 05/11 | Red Lobster master v2 (feedback do Maiquel) | não deu → corrigido | (1) 5:35–6:10: deixa `darkest-child` de 36 s, faixa masterizada a −12,6 LUFS (as outras ~−21) com o mesmo volume, 8 dB acima das outras; (2) impactos de capítulo acima da voz; (3) Motion rápido em 8:30 (4 passos em 1,8 s, último no corte) e 10:04 (cartões acendendo no corte). Regras em "Música" e "Animação" acima; motor: `track_gain`, `max_dur`, `sfx_volume` (ec_montage) e `pause_after` (timeline) |
