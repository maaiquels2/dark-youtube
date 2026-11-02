# Ep01 - Robocalls, caller-ID spoofing e o TRACED Act (GATE 1 - pesquisa)

Canal: "o golpe, o caso, a regra nova". Data da pesquisa: 2026-11-01. Texto em PT-BR; titulos e citacoes ficam em ingles.
Legenda de status: **Verificado** = fonte primaria (FCC/govinfo/FTC) ou 2+ fontes concordando. **Checar** = so fonte secundaria, fontes em conflito ou nao confirmado.

Fontes primarias principais:
- FCC 18-58 (Forfeiture Order, 10/mai/2018): https://transition.fcc.gov/eb/Orders/2018/FCC-18-58A1.html
- Pallone-Thune TRACED Act, Public Law 116-105: https://www.govinfo.gov/content/pkg/PLAW-116publ105/html/PLAW-116publ105.htm
- Audiencia do Senado (Senate Hearing 115-806): https://www.govinfo.gov/content/pkg/CHRG-115shrg56117/html/CHRG-115shrg56117.htm
- Truth in Caller ID Act, P.L. 111-331: https://www.govinfo.gov/content/pkg/PLAW-111publ331/html/PLAW-111publ331.htm
- YouMail Robocall Index (historico): https://robocallindex.com/history/time

Nota: fcc.gov (paginas de press release / statements) devolve 403 para fetch automatico; usei o PDF/HTML do order em transition.fcc.gov e docs.fcc.gov.

---

## 1. Entidades (23)

| # | Entidade | Papel | Trajetoria em 1 linha | Foto/logo |
|---|---|---|---|---|
| 1 | **Adrian Abramovich** | Empresario de Miami; ex-presidente da Marketing Strategy Leaders (dissolvida 29/01/2016, segundo a pagina do Senado) | Segundo o FCC, fez 96.758.223 chamadas spoofed em 3 meses de 2016; multa de US$120 mi (mai/2018); depoimento sob intimacao no Senado (18/abr/2018); desfecho de cobranca nao confirmado | NAO (sem foto livre) |
| 2 | **Marketing Strategy Leaders, Inc.** e **Marketing Leaders, Inc.** | Empresas de Abramovich (FL) | Co-responsaveis solidarios pela multa (FCC 18-58, par. 1, 50) | NAO (cartao) |
| 3 | **Frank Pallone (D-NJ)** | Deputado, presidente do Energy & Commerce na epoca da aprovacao | Co-autor da lei (Pallone-Thune) | SIM pallone.jpg |
| 4 | **John Thune (R-SD)** | Senador; conduziu a audiencia de 18/abr/2018 como presidente do Commerce | Co-autor da lei; "a lei vai ajudar a tornar seguro atender o telefone de novo" (TransNexus cita Thune) | SIM thune.jpg |
| 5 | **Ajit Pai** | Presidente do FCC em 2017-2019 | Defendeu a multa: "largest forfeiture in the history of the FCC" (statement) | SIM pai.jpg |
| 6 | **Jessica Rosenworcel** | Comissaria do FCC em 2018 (depois presidente do FCC; ruling de IA em 2024) | Pediu regras mais amplas contra robocalls (Kelley Drye); presidia o FCC no ruling de IA fev/2024 (**Checar** o cargo exato na data) | SIM rosenworcel.jpg |
| 7 | **Michael O'Rielly** | Comissario do FCC | Concordou em parte e discordou em parte da multa: duvidou que haja dano se o consumidor nao ouve a mensagem | SIM orielly.jpg |
| 8 | **Mignon Clyburn** | Comissaria do FCC em 2018 | Papel nesta decisao **nao verificado**; usar a foto so se confirmar | SIM clyburn.jpg |
| 9 | **Rosemary Harold** | Chefe do Enforcement Bureau do FCC (testemunha, 2018) | Disse ao Senado que robocalls sao a maior fonte de reclamacoes do FCC | NAO (so mencionar) |
| 10 | **Lois Greisman** | FTC, testemunha no Senado 2018 | Reportou >7 mi de reclamacoes de chamadas indesejadas no ano fiscal 2017 | NAO |
| 11 | **Richard Blumenthal (D-CT)** | Senador na audiencia | Pediu ao presidente que considerasse desacato (contempt) apos Abramovich invocar a 5a Emenda | SIM blumenthal.jpg (791x1002) |
| 12 | **Rand Paul (R-KY)** | Senador | Unico voto contra no Senado em 23/mai/2019 (97-1) | SIM randpaul.jpg |
| 13 | **FCC** (Federal Communications Commission) | Agencia reguladora de telecom | Aplicou a multa, regulou STIR/SHAKEN, mantem o Robocall Mitigation Database | SIM fcc_seal.png/svg |
| 14 | **FTC** (Federal Trade Commission) | Agencia de defesa do consumidor; dona do Do Not Call Registry | Coleta reclamacoes; publica Do Not Call Data Book | SIM ftc_seal, ftc_building.jpg |
| 15 | **Senate Commerce Committee** | Comissao do Senado | Intimou Abramovich; audiencia "Abusive Robocalls and How We Can Stop Them" | NAO (usar cartao) |
| 16 | **U.S. Congress** | Legislativo | Aprovou Truth in Caller ID Act (2010) e TRACED Act (2019) | NAO |
| 17 | **TripAdvisor** | Marca falsamente usada nas chamadas | Em abr/2016 reportou "several consumer complaints" ao FCC sobre robocalls usando seu nome (FCC 18-58 par. 6) | SIM tripadvisor_logo |
| 18 | **Expedia** | Marca falsamente usada | Citada no order como uma das marcas simuladas | SIM expedia_logo |
| 19 | **Marriott** | Marca falsamente usada | Consumidores citados no order dizem ter recebido chamadas "da Marriott" | SIM marriott_logo |
| 20 | **Hilton** | Marca falsamente usada | Citada no order; nenhum logo livre adequado | NAO |
| 21 | **John C. Spiller / Jakob A. Mears (Rising Eagle, JSquared Telecom)** | Telemarketers do Texas | FCC multou US$225 mi (proposta jun/2020; ordem final mar/2021; reconsideracao negada em 2023) - comparacao de "quem veio depois" | NAO |
| 22 | **U.S. Department of Justice** | Cobra multas do FCC no tribunal | Cobranca da multa de Abramovich: **nao confirmada** | NAO |
| 23 | **YouMail** | Empresa de bloqueio de chamadas; publica o Robocall Index | Fonte dos totais anuais de robocalls | NAO |

Com foto/logo livre baixado: 13 (pallone, thune, pai, rosenworcel, orielly, clyburn, blumenthal, randpaul, fcc, ftc, tripadvisor, expedia, marriott) + ftc_building como extra. Ver `entities/credits.json`.

---

## 2. Linha do tempo (cada fato com URL)

| Data | Fato | Fonte |
|---|---|---|
| 20/dez/1991 | TCPA (Telephone Consumer Protection Act), Pub. L. 102-243, assinado por George H.W. Bush; limita autodiscadores e voz pre-gravada sem consentimento | https://en.wikipedia.org/wiki/Telephone_Consumer_Protection_Act_of_1991 (lei: https://www.congress.gov/102/statute/STATUTE-105/STATUTE-105-Pg2394.pdf) |
| 22/dez/2010 | Truth in Caller ID Act (Pub. L. 111-331): proibe spoofing com intencao de fraudar, causar dano ou obter algo de valor; codificado em 47 U.S.C. 227(e) | https://www.govinfo.gov/content/pkg/PLAW-111publ331/html/PLAW-111publ331.htm |
| abr/2016 | TripAdvisor reporta ao FCC varias reclamacoes de consumidores sobre robocalls usando seu nome | FCC 18-58 par. 6: https://transition.fcc.gov/eb/Orders/2018/FCC-18-58A1.html |
| 29/jan/2016 | Marketing Strategy Leaders dissolvida (segundo o Senado); o FCC diz que Abramovich seguiu usando o nome em 2016 | https://www.commerce.senate.gov/meetings/abusive-robocalls-and-how-we-can-stop-them/ ; FCC 18-58 par. 33 |
| 1/out - 31/dez/2016 | Periodo das 96.758.223 chamadas (36.539.979 em out; 30.724.165 em nov; 29.502.000 em dez); amostra de 80.000 chamadas, todas spoofed | FCC 18-58 par. 1 e 7 |
| 22/jun/2017 | FCC emite Citation (DA 17-593) e Notice of Apparent Liability propondo US$120 mi (FCC 17-80) | Citation: FCC 18-58 n.3 e par. 8. NAL: https://docs.fcc.gov/public/attachments/FCC-17-80A1.pdf (dia exato do NAL: **Checar** no PDF; imprensa de 23/jun/2017 sustenta) |
| 10/out/2017 | Senate Commerce escreve a Abramovich; em 3/nov/2017 o advogado recusa; depois vem a intimacao (subpoena) | Hearing 115-806 (Thune): https://www.govinfo.gov/content/pkg/CHRG-115shrg56117/html/CHRG-115shrg56117.htm |
| 18/abr/2018 | Audiencia "Abusive Robocalls and How We Can Stop Them"; Abramovich depoe sob intimacao, invoca a 5a Emenda em varias perguntas, diz "I am not the king pin of robocalling that is alleged" | idem; pagina da comissao https://www.commerce.senate.gov/meetings/abusive-robocalls-and-how-we-can-stop-them/ |
| 10/mai/2018 | FCC adota e libera a Forfeiture Order FCC 18-58: US$120.000.000, solidariamente contra Abramovich, Marketing Strategy Leaders e Marketing Leaders; maior multa da historia do FCC; primeira multa baseada no Truth in Caller ID Act | https://transition.fcc.gov/eb/Orders/2018/FCC-18-58A1.html |
| 23/mai/2019 | Senado aprova o S.151 (TRACED) por 97-1 | https://tcpaworld.com/2019/05/23/traced-act-barrels-across-the-senate-goal-line/ ; https://appleinsider.com/articles/19/05/23/us-senate-greenlights-anti-robocalling-bill-to-combat-daily-deluge |
| 4/dez/2019 | Camara aprova a versao Pallone-Thune por 417-3 | https://transnexus.com/blog/2019/pallone-thune-traced-act-passes-senate (datas); votos 417-3: busca consolidada, **Checar** no roll call da Camara |
| 19/dez/2019 | Senado aprova a versao da Camara (unanime) | https://transnexus.com/blog/2019/pallone-thune-traced-act-passes-senate ; https://techcrunch.com/2019/12/19/robocall-crushing-traced-act-passes-senate-and-heads-to-oval-office |
| 30/dez/2019 | TRACED Act assinado: Public Law 116-105 | https://www.govinfo.gov/content/pkg/PLAW-116publ105/html/PLAW-116publ105.htm |
| 9/jun/2020 | FCC propoe US$225 mi contra Spiller/Mears (Rising Eagle), ~1 bilhao de chamadas; ordem final em mar/2021 | https://www.nextgov.com/modernization/2020/06/fcc-proposes-225-million-fine-telemarketers-behind-massive-robocall-operation/166057 ; https://www.fcc.gov/document/fcc-fines-telemarketer-225-million-spoofed-robocalls |
| 30/jun/2021 | Prazo geral do STIR/SHAKEN (18 meses apos a lei) para grandes operadoras | Sec. 4 da lei + https://www.tlp.law/2021/12/15/fcc-releases-ro-imposing-shortened-stir-shaken-implementation-deadline-for-certain-small-voice-service-providers/ (a data exata 30/jun/2021 vem do prazo regulatorio do FCC; **Checar** na ordem FCC 20-136) |
| dez/2021 | FCC encurta a extensao de pequenas operadoras (de 30/jun/2023 para 30/jun/2022 para as nao-facilities-based em 6 meses) | https://www.tlp.law/2021/12/15/fcc-releases-ro-imposing-shortened-stir-shaken-implementation-deadline-for-certain-small-voice-service-providers/ |
| 2023 | Enforcement Bureau comeca a remover operadoras do Robocall Mitigation Database (7 ordens iniciais de show-cause; depois 14 removidas) | https://mondaq.com/unitedstates/telecoms-mobile-cable-communications/1245260/fcc-enforcement-bureau-orders-7-providers-to-show-cause-why-they-should-not-have-traffic-blocked-for-alleged-non-compliance-with-robocall-mitigation-rules ; https://san.com/?p=470471 |
| 8/fev/2024 | FCC (5-0) declara que vozes geradas por IA sao "artificial voice" sob o TCPA (FCC 24-17, CG Docket 23-362) - nao e regra nova, e declaratory ruling | https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal ; https://www.cooley.com/news/insight/2024/2024-02-15-fcc-ai-generated-robocalls-illegal-under-the-tcpa |
| 15/set/2025 | Enforcement Bureau remove Chase Tech LLC do RMD por certificacao falsa | https://www.mintz.com/insights-center/viewpoints/2776/2025-09-29-telephone-and-texting-compliance-news-regulatory-update |

---

## 3. Tabela de numeros-chave

| Numero | O que significa | Fonte | Status |
|---|---|---|---|
| 96.758.223 | Chamadas spoofed de Abramovich, 1/out-31/dez/2016; "doesn't dispute" segundo Pai | FCC 18-58 par. 1, 7: https://transition.fcc.gov/eb/Orders/2018/FCC-18-58A1.html | Verificado ("segundo o FCC") |
| >1 milhao/dia | Media diaria (par. 7) | idem | Verificado |
| US$120.000.000 | Multa total, solidaria; maior da historia do FCC (ate entao) | idem | Verificado |
| 80.000 | Chamadas amostradas (1.000/dia em 80 dias) - so elas entram no calculo | idem par. 7, 25, 28 | Verificado |
| US$1.000 + US$40 mi | Base por chamada amostrada (US$80 mi) + ajuste para cima (US$40 mi) = ~US$1.500/chamada amostrada | idem par. 25, 33 | Verificado |
| US$11.052 | Maximo legal por violacao na epoca (par. 22, 25) | idem | Verificado |
| TripAdvisor, Expedia, Marriott, Hilton | Marcas simuladas na mensagem "Press 1" | idem par. 4, 15 | Verificado |
| ~2% | Alegacao de Abramovich: menos de 2% dos consumidores interagiram. Thune: 2% de ~100 mi = ~2 mi de pessoas | Hearing 115-806 | Verificado (como alegacao dele) |
| 97-1 | Votos no Senado, 23/mai/2019 (Rand Paul contra) | tcpaworld / appleinsider (acima); um escritorio cita 99-1, parece erro | Verificado (2 fontes) - roll call em senate.gov: **Checar** |
| 417-3 | Votos na Camara, 4/dez/2019 | pesquisa consolidada | **Checar** |
| 18 meses | Prazo para o FCC exigir STIR/SHAKEN (Sec. 4) -> ~30/jun/2021 | govinfo PLAW-116publ105 | Verificado (lei); data final: Checar |
| Ate US$10.000 | Penalidade adicional por violacao intencional (Sec. 3), alem da base. **Nao e "US$10.000 por chamada" fixo** | govinfo PLAW-116publ105 | Verificado |
| 1 ano / 4 anos | Prazo prescricional: 1 ano para multa base; 4 anos para violacao intencional (Sec. 3) | idem | Verificado |
| 270 dias | Prazo do grupo interagencia (AG) para relatorio (Sec. 5) | idem | Verificado |
| 5.422.298 | Reclamacoes Do Not Call no ano fiscal 2019 (FTC); 71% sobre robocalls | https://www.ftc.gov/reports/national-do-not-call-registry-data-book-fiscal-year-2019 | Verificado (via busca; Checar o PDF) |
| ~3,78 mi | Reclamacoes de robocalls FY2019 (release do FTC; imprensa inverteu 3,78/3,79) | https://www.ftc.gov/news-events/news/press-releases/2019/10/ftc-releases-fy-2019-national-do-not-call-registry-data-book | Verificado/Checar |
| 239,5 mi | Numeros no Do Not Call Registry no fim do FY2019 | idem | Verificado |
| >7 mi | Reclamacoes de chamadas indesejadas no FY2017 (Greisman, FTC); >60% robocalls | Hearing 115-806 | Verificado |
| 1,4 mi | Reclamacoes no 1o trimestre de 2018 (~900 mil sobre robocalls) | idem | Verificado |
| US$225 mi | Multa Rising Eagle; ~1 bilhao de chamadas | nextgov / fcc.gov (acima) | Verificado |
| 52,8 bi | Robocalls em 2024 (YouMail) | https://robocallindex.com/history/time | Verificado |

Pontos para a fala: dizer "segundo o FCC" para as 96 milhoes; dizer "a multa foi calculada sobre uma amostra de 80 mil chamadas".

---

## 4. Dados prontos para grafico

### 4.1 Robocalls por ano nos EUA (YouMail Robocall Index, estimativa nacional) - fonte: https://robocallindex.com/history/time (Verificado; pagina com totais mensais tambem)

```
year,calls
2016,29082325500
2017,30507422900
2018,47839232200
2019,58536224700
2020,45866949500
2021,50507702500
2022,50373858400
2023,55047970000
2024,52766896900
2025,52477649500
```
Em bilhoes (arredondado): 2016 29,1 | 2017 30,5 | 2018 47,8 | 2019 58,5 | 2020 45,9 | 2021 50,5 | 2022 50,4 | 2023 55,0 | 2024 52,8 | 2025 52,5. (2015 parcial, jun-dez: 7,07 bi - nao usar. 2026 incompleto - nao usar.)
Releases: 2018 = 47,8 bi (+56,8% sobre 30,5 bi) https://prnewswire.com/news-releases/nearly-48-billion-robocalls-made-in-2018-according-to-youmail-robocall-index-300782638.html ; 2020 = ~46 bi https://prnewswire.com/news-releases/americans-hit-by-just-under-46-billion-robocalls-in-2020-says-youmail-robocall-index-301215139.html ; 2021 = 50,5 bi https://prnewswire.com/news-releases/us-phones-were-hit-by-more-than-50-billion-robocalls-in-2021-says-youmail-robocall-index-301455319.html ; 2024 = 52,8 bi https://prnewswire.com/news-releases/us-consumers-received-nearly-4-4-billion-robocalls-in-december-52-8-billion-in-all-of-2024--according-to-youmail-robocall-index-302348867.html .
Leitura honesta para o roteiro: o volume cai em 2020 (pandemia, -22%) e fica num platô de ~50-55 bi depois da lei; a lei NAO zerou o problema. Atribuir: "segundo o YouMail".

### 4.2 Chamadas do caso Abramovich por mes (FCC 18-58) - Verificado
```
month,calls
2016-10,36539979
2016-11,30724165
2016-12,29502000
```

### 4.3 Multas (comparativo) - Verificado
```
case,fine_usd
Abramovich (2018),120000000
Rising Eagle / Spiller-Mears (2021),225000000
```
(Rising Eagle: valor de ordem final per fcc.gov; reconsideracao negada em 2023.)

### 4.4 Reclamacoes FTC Do Not Call (so pontos verificados)
```
fiscal_year,total_complaints,robocall_complaints
2019,5422298,~3780000
```
Outros anos: **Checar** nos Data Books (FY2018 ~5,8 mi total; ~3,79 mi robocalls - citados na pesquisa, nao abertos no PDF).

---

## 5. Como o golpe funcionava (do order FCC 18-58, par. 4, 6, 16, 37, 41-42)
1. Caller ID falsificado para parecer local: o numero chamador copia os 6 primeiros digitos do numero chamado ("neighbor spoofing", n.108).
2. Gravacao: "Press 1" para oferta "exclusiva" de viagem de uma marca conhecida (TripAdvisor, Expedia, Marriott, Hilton).
3. Quem apertava 1 era transferido para um call center onde operadores vendiam pacotes, normalmente via apresentacao de timeshare; operadores sem ligacao com as marcas.
4. Pacotes para Mexico e Caribe; fornecedores "unknown timeshare providers in Mexico and elsewhere" (par. 16). **O order nao diz que o call center era no Mexico** - nao afirmar.
5. Segundo o order, Abramovich agia como gerador de leads para clientes terceiros; o order NAO encontra evidencia de que a operadora ou os clientes sabiam do spoofing (par. 42). Nao diz como ele era pago.
6. Vitimas indiretas: donos dos numeros spoofed recebiam ligacoes furiosas de volta; marcas sofriam com consumidores irritados (par. 16, 18, 37). Comentarios de consumidores: chamadas repetidas "da Marriott", "keep spoofing different numbers".
7. Defesa dele: dano so se o consumidor atendesse e ficasse 5 min; o FCC rejeitou: a lei exige intencao de causar dano, nao dano efetivo (par. 27, 35-38). O comissario O'Rielly discordou parcialmente.

Nao ha contagem total de reclamacoes de consumidores no order (so as reportadas ao TripAdvisor e comentarios). Nao inventar numero de vitimas.

---

## 6. O que a TRACED Act faz (govinfo PLAW-116publ105)
- Sec. 3: multas novas; ate US$10.000 adicionais por violacao intencional; prescricao 1 ano / 4 anos; relatorios anuais do FCC ao Congresso.
- Sec. 4: FCC deve exigir STIR/SHAKEN em 18 meses (adiamentos para redes nao-IP com programa de mitigacao); proibido cobrar taxa do consumidor pela autenticacao; safe harbor para bloqueio.
- Sec. 5: grupo interagencia (AG) para estudar a persecucao penal; relatorio em 270 dias.
- Sec. 6: acesso a numeros; Sec. 7: regras contra chamadas de numeros nao autenticados; Sec. 8: limites nas isencoes; Sec. 11: Enforcement Bureau encaminha ao AG evidencia de violacoes dolosas com intencao de fraude; Sec. 12: "one-ring scams"; Sec. 13: consorcio unico de traceback; Sec. 14: Hospital Robocall Protection Group.
- "Robocall task force": o termo da lei e interagency working group (Sec. 5); a task force da Casa Branca/FCC e outra coisa - **nao chamar de task force sem checar**.

STIR/SHAKEN (explicacao simples): a operadora de origem assina digitalmente o numero; a de destino confere a assinatura; sem assinatura valida, a chamada pode ser marcada ou bloqueada. Fonte tecnica para checar: https://www.fcc.gov/call-authentication (403 no fetch) - **Checar** texto.

## 7. O que ainda falha (so com fonte)
- Pequenas operadoras e chamadas internacionais/gateways: o FCC encurtou prazos de pequenas operadoras (dez/2021) e criou o Robocall Mitigation Database; removeu operadoras que nao corrigiram (2023: 14 removidas; 15/set/2025 Chase Tech por certificacao falsa) - fontes na linha do tempo.
- "Gateway provider rules" 2022: **nao verificado** - Checar antes de citar.
- Volume continua ~50-55 bi/ano (secao 4.1).
- IA: fev/2024 o FCC (5-0) disse que voz gerada por IA e "artificial voice" sob o TCPA; foi declaratory ruling, nao regra nova; 26 procuradores-gerais estaduais apoiaram. Usar so como "o que vem agora", em uma frase.

---

## 8. Lado do consumidor: como se proteger / denunciar (links oficiais; conferir antes de publicar)
- FTC - denunciar fraude: https://reportfraud.ftc.gov
- FTC - Do Not Call Registry (registrar numero / denunciar chamada): https://www.donotcall.gov
- FCC - guia de robocalls e spoofing: https://www.fcc.gov/consumers/guides/stop-unwanted-robocalls-and-texts e https://www.fcc.gov/spoofing
- FCC - registrar reclamacao: https://consumercomplaints.fcc.gov
- Dicas gerais (**Checar** o texto exato nos sites oficiais antes de falar): nao apertar 1; nao devolver a ligacao; desligar; bloquear no app da operadora; marcas legitimas nao ligam oferecendo viagem "exclusiva" sem pedido.
- Fala segura: "numero local na tela nao prova que a ligacao e local" (apoiado pelo order: 100% das 80.000 amostradas eram spoofed).

---

## 9. Riscos (juridico / difamacao)
1. **Abramovich nao foi condenado criminalmente** em nada que eu tenha encontrado. A penalidade e **administrativa do FCC** (forfeiture order). Nunca dizer "condenado", "preso", "criminoso", "golpista condenado". Usar: "o FCC multou", "segundo o FCC", "acusado pelo FCC de".
2. "Robocall kingpin": e rotulo do FCC/imprensa; ele nega ("I am not the king pin of robocalling that is alleged"). Atribuir sempre ("apelidado de 'kingpin' pela imprensa").
3. O order encontra que ele agia como gerador de leads para terceiros e nao acha evidencia de que operadora/clientes sabiam do spoofing - nao acusar os resorts/clientes nem as operadoras.
4. Nao dizer que as vendas eram "fraude" no sentido penal: a Citation falou em wire fraud (18 U.S.C. 1343), mas a multa se baseia apenas no spoofing (par. 8, 20). Ele diz que os resorts eram reais ("real resorts, offering real vacation packages").
5. Ele invocou a 5a Emenda em varias perguntas; nao interpretar como confissao. Relatos divergem (Mintz: recusou responder; Kelley Drye: respondeu perguntas gerais). A transcricao no govinfo confirma: respondeu algumas, invocou a 5a em outras.
6. **Desfecho da multa: NAO CONFIRMADO.** O FCC nao cobra: o DOJ cobra. Um podcast da AARP (2021, segunda mao, nao verificado) diz que ele negociava com o U.S. Attorney acordo "bem abaixo" de US$120 mi. Roteiro: "ate onde consegui verificar, nao ha registro publico de que a multa tenha sido paga integralmente" so se a checagem confirmar; senao, omitir.
7. Marcas (TripAdvisor, Expedia, Marriott, Hilton): foram imitadas, nao envolvidas. Dizer sempre "usaram o nome sem autorizacao". Nao sugerir parceria.
8. Pessoas citadas por nome (senadores, comissarios): so atos publicos e falas oficiais.
9. Logos: marca registrada; usar apenas para identificar. Fotos de .gov sao dominio publico; Commons marca todas as usadas aqui como Public domain (exceto logos, ver credits.json).
10. Fotos de imprensa de Abramovich: nao usar.

---

## 10. Lista "Checar"
1. Desfecho da multa de US$120 mi (paga? acordo? DOJ? tribunal?). Nao encontrei fonte confiavel. Buscar no PACER/DOJ ou FCC debt-collection.
2. Votos 417-3 da Camara e 97-1 do Senado em roll call oficial (clerk.house.gov / senate.gov). "Unanime" no voto final do Senado em 19/dez/2019 - sem numero.
3. Dia exato do NAL (FCC 17-80) - 22/jun/2017 provavel.
4. Data final do prazo do STIR/SHAKEN para grandes operadoras (30/jun/2021) na ordem FCC 20-136 / pagina do FCC.
5. Gateway provider rules 2022 e outras acoes do FCC 2023-2025 (so citei os verificados).
6. Reclamacoes FTC por ano (apenas FY2019 e FY2017 verificados).
7. Papel de Clyburn e cargo exato de Rosenworcel nas datas citadas.
8. Como Abramovich era pago e quem eram os clientes (nao esta no order).
9. Texto das paginas oficiais de dicas do FCC/FTC (403 no fetch).
10. Chamada "robocall task force" (usar "interagency working group").
11. Os 50-55 bi/ano do YouMail sao estimativa de empresa privada; mencionar a fonte.
12. Se existir trecho de video publico (C-SPAN) do depoimento - licenca nao verificada; usar so a transcricao do govinfo.

Fatos que eu NAO consegui verificar: tudo da lista acima. O resto foi lido em fonte primaria ou em 2+ fontes.
