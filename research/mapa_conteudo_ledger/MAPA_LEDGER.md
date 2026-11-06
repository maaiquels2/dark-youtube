# Mapa de conteúdo — The Cracked Ledger (05/11/2026)

Pedido do Maiquel em 05/11, a partir do artigo de Dan Koe ("research-backed content map"), na versão leve. Este documento é **pauta, não roteiro**.
- Os títulos são provisórios.
- Todo número marcado [checar] passa pelo Gate 1 antes de ir para título ou capa (REGRAS_UNIVERSAIS §2).
- Fatos recentes tirados de títulos de vídeo ou de notícia também levam [checar].

**Dados:**
- `demanda_temas.csv`: 45 temas medidos pela YouTube Data API em 05/11, vídeos dos últimos 24 meses, cerca de 4.600 unidades de cota.
- `referencias.json`: as referências citadas abaixo.
- Pesquisa de 03/11: `research/youtube_ab_2026-11-03/canais_vencedores.md`.

**Limites:**
- A busca da API traz ruído (por exemplo, "Nokia" trouxe um vídeo da Micromax), então as referências citadas foram conferidas pelo título.
- Views são as do dia 05/11.
- "Inscritos" é o tamanho do canal; um vídeo muito maior que o canal indica que o tema puxa sozinho.

## O que os dados dizem
1. **Marcas médias e nostálgicas rendem mais por canal pequeno do que as gigantes.**
   - Exemplos de vídeo muito maior que o canal:
     - Harvestore: 431 mil views com 2,6 mil inscritos (166x);
     - Eastbay: 424 mil views com 3,4 mil (126x);
     - Adams Golf: 324 mil views com 4,1 mil (79x);
     - Long John Silver's: 252 mil views com 6,5 mil (39x).
   - As gigantes (Kodak, Circuit City, Yahoo) já têm o "rise and fall" de canais de 388 mil inscritos (Michael Girdley), com 170 a 270 mil views.
2. **"Quem matou" e "para onde foi o dinheiro" vencem.** Private equity por trás de falências tem procura alta: Elizabeth Warren com 1,03 milhão de views, CNBC com 283 mil, WSJ sobre a Red Lobster com 867 mil. Esse é o ângulo natural do Ledger ("follow the money").
3. **Crashes com gráfico rendem com canal minúsculo.** Market Ghosts fez 418 mil views em Black Monday com 1,8 mil inscritos (236x), e Adam's Axiom fez 318 mil sobre bolhas.
4. **Notícia quente rende enquanto está quente:**
   - Spirit: CNN com 1,02 milhão; Motorverse com 816 mil, com 1,8 mil inscritos;
   - Evergrande: 1,5 milhão;
   - Intel.
   - Regra do canal (`PADRAO_VIDEOS.md`): só vale se sair na mesma semana do fato.

## Como usar
- **Série fixa "What Actually Happened to…"** no pilar 1, sempre com o mesmo formato de título. O público e o YouTube passam a reconhecer o tipo de vídeo (`PADRAO_VIDEOS.md`).
- **Ritmo sugerido:** a cada 4 vídeos, 2 do pilar 1, 1 do pilar 2 ou 3, e 1 vaga para o assunto quente da semana (pilar 4). Sem assunto quente, a vaga volta para o pilar 1.
- **Capa:** 3 por vídeo, conforme REGRAS_UNIVERSAIS §12, "Capas com teste A/B". O conceito abaixo é a capa principal.
- **Potencial:** A = procura alta e pouca concorrência boa; B = procura boa e concorrência forte, ou procura média; C = só com ângulo muito forte.
- **Revisão:** rever o mapa quando saírem os resultados dos testes A/B de Binance e Weil e a cada 10 vídeos publicados.

## Os 10 próximos (ordem sugerida)
| # | Tema | Pilar | Por quê |
|---|---|---|---|
| 1 | Toys "R" Us | 1 | marca enorme, dívida de private equity, concorrência fraca (o melhor vídeo recente sobre o negócio é de um canal de 492 inscritos; o mais visto do tema é um vídeo de entretenimento) |
| 2 | Black Monday 1987 | 3 | gráfico é a nossa força; 236x num canal pequeno |
| 3 | Enron | 2 | busca eterna; nosso ângulo é o do dinheiro, não o do escândalo |
| 4 | Red Lobster | 1 | private equity em alta; vários vídeos grandes, nenhum no nosso tom |
| 5 | Luckin Coffee | 2 | fraude + volta aos EUA (CNBC com 2,5 milhões) |
| 6 | 23andMe | 1 | falência + "quem ficou com o seu DNA" (algo em jogo para o espectador) |
| 7 | Evergrande | 2/4 | tema gigante; fundador condenado à prisão perpétua [checar] |
| 8 | Madoff | 2 | busca eterna; "para onde foi o dinheiro" é ângulo pouco explorado |
| 9 | Pan Am | 1 | 380 mil views num canal de 5,5 mil inscritos (70x) |
| 10 | Nokia | 1 | a maior procura medida (5,1 milhões, mas em vídeo indiano); quase sem versão em inglês com o nosso tom |

## Pilar 1 — "What Actually Happened to…" (marcas que caíram, seguindo o dinheiro)
| # | Tema | Título provisório | Capa principal (conceito) | Referência que prova o formato | Pot. | Checar |
|---|---|---|---|---|---|---|
| 1 | Toys "R" Us **[FEITO 05/11: Kti-Hj9yU9o, 06/11 18:00]** | What Actually Happened to Toys "R" Us? | foto real da fachada + corrente com cadeado; "THE DEBT DID IT." | The Business Scope, 166 mil views, 492 inscritos — https://youtu.be/jyM-mGI86b0 | A | compra alavancada de 2005 e valor da dívida [checar] |
| 2 | Red Lobster | Who Really Killed Red Lobster? | lagosta (objeto) sobre a seta caindo; logo real | Michael Girdley, 218 mil — https://youtu.be/IAJNwOXL4aM ; Elizabeth Warren (PE), 1,03 milhão — https://youtu.be/B_7SQDuUKQs | A | venda de imóveis e "endless shrimp" [checar] |
| 3 | 23andMe | 23andMe Went Bankrupt. Who Owns Your DNA? | tubo de amostra rachado + logo; "WHO OWNS IT?" | JunkBondInvestor, 238 mil, 78,8 mil inscritos — https://youtu.be/0dEhU-EZLfc | A | comprador final e data [checar] |
| 4 | Pan Am | What Actually Happened to Pan Am? | avião real (foto livre) + seta; "AMERICA'S AIRLINE." | Collapse Archive, 380 mil, 5,5 mil inscritos — https://youtu.be/XWSK-LSUjes | A | ano do fim (1991) [checar] |
| 5 | Nokia | What Actually Happened to Nokia? | celular clássico rachado; barras da fatia de mercado caindo | NewsBook, 5,1 milhões (Índia) — https://youtu.be/xdI-M1mZkek | A | venda para a Microsoft e valor [checar] |
| 6 | Sears | What Actually Happened to Sears? | catálogo de papel rasgado; "THE AMAZON BEFORE AMAZON." | Vintage America, 232 mil, 37,9 mil inscritos — https://youtu.be/oOUfAUMfiGA | A | papel de Eddie Lampert [checar] |
| 7 | Spirit Airlines | Why Spirit Airlines Really Went Under | avião amarelo parado; "GROUNDED." | CNN, 1,02 milhão — https://youtu.be/v7U7TAL3gdw ; Motorverse, 816 mil, 1,8 mil inscritos | A* | encerramento em 05/2026 visto em título da CNN [checar]; *se ainda houver notícia nova |
| 8 | Kodak | Kodak Invented the Digital Camera. Then It Died. | câmera digital de protótipo + filme queimado | Michael Girdley, 184 mil — https://youtu.be/FV36Z9WFZ7g | B | 1975, Steve Sasson [checar] |
| 9 | Blockbuster | Blockbuster Could Have Bought Netflix | capinha de VHS + seta | (busca ruidosa; tema clássico) | B | oferta de 2000 e valor [checar] |
| 10 | Peloton | What Actually Happened to Peloton? | bicicleta parada coberta de pó; "$50B → ?" | Girdley, 436 mil — https://youtu.be/k8lLYt9DNDY ; JunkBondInvestor, 343 mil | B | valor de mercado no pico [checar] |
| 11 | Circuit City | What Actually Happened to Circuit City? | fachada + etiqueta "CLOSED" | Girdley, 266 mil — https://youtu.be/Atv5HZCdwkA | B | corte dos vendedores mais bem pagos [checar] |
| 12 | RadioShack | What Actually Happened to RadioShack? | peça eletrônica velha; logo real | JunkBondInvestor, 150 mil — https://youtu.be/4SX97lCDPP8 | B | — |
| 13 | BlackBerry | What Actually Happened to BlackBerry? | teclado físico rachado | (vários pequenos, 168 mil de mediana) | B | — |
| 14 | Joann | Who Killed Joann Fabrics? | carretel de linha cortado; logo real | Warren (PE), 1,03 milhão (cita Joann) | B | liquidação em 2025 [checar] |
| 15 | TGI Fridays | What Actually Happened to TGI Fridays? | toldo listrado apagado | CNBC (PE, Red Lobster e TGI Fridays), 283 mil | B | falência em 11/2024 [checar] |
| 16 | Party City | What Actually Happened to Party City? | balão murcho; logo real | — | B | fechamento das lojas [checar] |
| 17 | Rite Aid | What Actually Happened to Rite Aid? | frasco de farmácia vazio | — | C | segunda falência [checar] |
| 18 | Yahoo / Myspace | What Actually Happened to Yahoo? | logo real + cursor sobre "Ignore" | Girdley, 167 mil — https://youtu.be/eMctBbsRISE ; Company Man (Myspace), 237 mil | C | oferta da Microsoft em 2008 [checar] |

**Ideia de fila longa (alto potencial, pouca concorrência):** marcas americanas médias e nostálgicas no estilo Harvestore e Eastbay (catálogos, redes regionais, marcas de esporte). Sugestão: pesquisar 20 nomes na API antes de cada lote e escolher os que têm procura e nenhum vídeo bom.

## Pilar 2 — Fraudes famosas, contadas pelo dinheiro
| # | Tema | Título provisório | Capa principal | Referência | Pot. | Checar |
|---|---|---|---|---|---|---|
| 19 | Enron | How Enron Made Money That Didn't Exist | prédio real (foto livre) + balanço com carimbo | Crayon Capital, 1,08 milhão, 297 mil inscritos — https://youtu.be/VSbO8vmZNm0 | A | — |
| 20 | Luckin Coffee | The Coffee Chain That Faked Its Sales | copo (objeto) + recibo desenhado com vendas riscadas | CNBC (volta aos EUA), 2,48 milhões — https://youtu.be/cqDvnmMswXA | A | valor das vendas falsas de 2019 [checar] |
| 21 | Madoff | Where Did Madoff's Money Actually Go? | envelope de extrato vazio; seta para "?" | Crayon Capital, 237 mil; Detrás del Enigma, 321 mil (espanhol) | A | quanto o administrador recuperou [checar] |
| 22 | Evergrande | Evergrande: How China's Biggest Builder Fell | prédio inacabado (foto livre) + seta | DW (fundador condenado), 238 mil — https://youtu.be/0gxquATJLCE ; Statrys, 379 mil — https://youtu.be/pPOcHWWDd2w | A | sentença de 08/2026 [checar] |
| 23 | Theranos | Theranos: The Blood Test That Didn't Work | gota de sangue sobre aparelho; carimbo | CBS (interesse renovado em 10/2026), 3,5 milhões — https://youtu.be/nj963-FoACI | A | o que está renovando o interesse (documentário novo?) [checar] |
| 24 | Archegos / Credit Suisse | How One Fund Lost Billions in Two Days | tela de cotações vermelha | Glass, 99 mil, 1,4 mil inscritos (69x) — https://youtu.be/ejjCMDTqDx8 | B | já há notas em `research/archegos_*` |
| 25 | Wirecard | The German Fintech With Missing Billions | cofre vazio + bandeira (foto) | baixa procura em inglês | B | notas prontas em `research/wirecard_notes.md` |
| 26 | Nikola | Nikola: The Truck That Rolled Downhill | caminhão real (foto de imprensa com licença) + seta | Bogetti Media, 327 mil, 43 mil inscritos | B | vídeo do caminhão em 2016–2018 [checar] |
| 27 | WorldCom | The Accounting Trick That Sank WorldCom | livro-caixa com uma linha riscada | procura baixa | C | — |
| 28 | Fyre Festival | — | — | Ray William Johnson, 944 mil (muito disputado; pouco de finanças) | C | — |

## Pilar 3 — Bolhas e crashes (gráfico é o nosso forte)
| # | Tema | Título provisório | Capa principal | Referência | Pot. | Checar |
|---|---|---|---|---|---|---|
| 29 | Black Monday 1987 | The Day the Market Fell 22% | linha do Dow despencando; "ONE DAY." | Market Ghosts, 418 mil, 1,8 mil inscritos (236x) — https://youtu.be/qeVAcEZMo4s | A | -22,6% em 19/10/1987 [checar o número exato] |
| 30 | Dot-com | The Dot-Com Crash, Explained by the Money | gráfico da Nasdaq subindo e caindo | Vanessa Wingårdh ("bolha maior que a dot-com"), 906 mil | A | ligar ao debate sobre a bolha da IA (Damon Cassidy, 2,2 milhões) sem prever nada |
| 31 | LTCM | The Nobel Winners Who Almost Broke Wall Street | duas medalhas + seta caindo | procura média; poucos vídeos bons | B | Nobel de 1997 de Merton e Scholes [checar] |
| 32 | Barings | One Trader Sank a 233-Year-Old Bank | ficha de operador (foto livre) + prédio | Samuel Leach, 14 mil (pouca concorrência) | B | 1762 a 1995 [checar] |
| 33 | Tulip mania | Was Tulip Mania Even Real? | tulipa com etiqueta de preço | Adam's Axiom, 318 mil — https://youtu.be/LQ0S_IPUOrM | B | historiadores contestam o exagero: é esse o ângulo |
| 34 | Bear Stearns | The Weekend Bear Stearns Was Sold | contrato com preço riscado | entrevista do Dimon, 235 mil | B | preço por ação da venda [checar] |

## Pilar 4 — Vaga do assunto quente (escolher na semana; ideias de hoje)
| # | Tema | Título provisório | Referência | Checar |
|---|---|---|---|---|
| 35 | Intel | What Actually Happened to Intel? | Logically Answered, 754 mil — https://youtu.be/DODTTHzUp1U ; Bloomberg (queda das ações em 30/10/2026) | queda de 30/10 [checar] |
| 36 | Dívida dos EUA | Who Actually Owns America's Debt? | OBF ("qual país rico quebra primeiro"), 8,6 milhões | números do Tesouro [checar] |
| 37 | Boeing | — | Flying for Money, 2,8 milhões | tema de acidente aéreo: cuidado com a monetização; só o ângulo financeiro |

## Fora do mapa (decidido)
- **Já feitos pelo canal:** WeWork, FTX, Lehman, SVB, First Brands, Tricolor, Weil, Binance, crise de 2008, Brasil e Argentina.
- **Procura quase zero:** Greensill, Silvergate, Mt. Gox, Celsius, Quibi.
- **Purdue/Sackler:** risco de monetização (tema de saúde e drogas). Só com OK e checagem do `CLAUDE_YT_ANTI_DEMONETIZATION.md`.
