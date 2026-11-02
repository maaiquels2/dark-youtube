# The Cracked Ledger: identidade do canal

Vale junto com [`REGRAS_UNIVERSAIS.md`](../REGRAS_UNIVERSAIS.md).

O conteúdo de `IDENTIDADE_CANAL_LEDGER.md` (30/10/2026) foi movido para cá sem mudanças; o arquivo antigo virou um atalho.

**Detalhe operacional do Ledger** (ficam onde estão; valem só para este canal):
- `CHECKLIST_VIDEO_YOUTUBE.md`: lista de marcar, na ordem do pipeline, com registro de erros.
- `PADRAO_VIDEOS.md`: título, capa, temas, prompts do Grok, Motion F2/F3/F4 e Shorts nativos.
- `GEMINI.md`: detalhes do EffectCraft (`tools/ec_gfx.py`).

> **OBRIGATÓRIO (analytics):** antes de roteirizar ou editar, leia [`CLAUDE_ANALYTICS_FEEDBACK.md`](../CLAUDE_ANALYTICS_FEEDBACK.md) e aplique as ações de `yt-analytics/reviews/LATEST.md` (subordinado a `CLAUDE_YT_ANTI_DEMONETIZATION.md`).

## Canal
- Documentários de Business & Finance em inglês, @thecrackedledger.
- Alvo de 10 a 12 min; o piso é 8.
- Agenda: seg, qua, sex e dom às 18:00 BRT.

## Voz
- **Hoje:** `config/montage.json` usa ElevenLabs Brian (`nPczCjzI2devNBz1zQrb`), velocidade 0.86, aprovado em 24/10.
- **Kokoro `am_onyx`:** escolhido em 30/10 como voz grátis. Perguntar antes de trocar o Ledger.

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
