# Ep02 - Zelle: o golpe em que a vitima manda o dinheiro e o banco diz "voce autorizou" (GATE 1 - pesquisa)

Canal: The Rule Changed. Arco: SCAM -> CASE -> RULE -> como se proteger ("a regra que ainda nao existe nos EUA", contraste com o Reino Unido).
Data da pesquisa: 2026-11-02. Texto em PT-BR; titulos e citacoes em ingles.
Legenda: **Verificado** = lido na fonte primaria (ou 2+ fontes). **Checar** = so fonte secundaria, ou fonte primaria bloqueada para robo, ou conflito.
Alegacao de processo = "alleged / alegou". Nada aqui e decisao de merito, exceto onde dito.

## Fontes primarias (abertas e lidas)
- Queixa do CFPB (91 pp., Doc 1, D. Ariz., 2:24-cv-03652-SMB, 20/12/2024): https://files.consumerfinance.gov/f/documents/cfpb_Zelle-Complaint_2024-12.pdf (o servidor bloqueia curl; texto lido pela copia que o WebFetch baixou)
- Pagina da acao no CFPB (tribunal, docket, datas): https://www.consumerfinance.gov/enforcement/actions/early-warning-services-llc-bank-of-america-na-jpmorgan-chase-bank-na-wells-fargo-bank-na/
- Ordem de extincao com prejuizo (Doc 43, 05/03/2025): https://files.consumerfinance.gov/f/documents/cfpb_early-warning-order-dismissal-prejudice_2025-03.pdf
- Press release do CFPB (arquivo, 20/12/2024): https://www.consumerfinance.gov/archive/newsroom/cfpb-sues-jpmorgan-chase-bank-of-america-and-wells-fargo-for-allowing-fraud-to-fester-on-zelle/
- Fala do diretor Chopra na coletiva (20/12/2024): https://www.consumerfinance.gov/archive/newsroom/prepared-press-call-remarks-of-cfpb-director-rohit-chopra-on-the-zelle-lawsuit-announcement/
- Press release do NY AG (13/08/2025): https://ag.ny.gov/press-release/2025/attorney-general-james-sues-company-behind-zelle-enabling-widespread-fraud
- Queixa do NY AG (NY Supreme Court, NY County, Index 654753/2025): https://ag.ny.gov/sites/default/files/court-filings/people-of-the-state-of-new-york-v-early-warning-services-llc-complaint-2025.pdf
- Regulation E, 12 CFR 1005.2(m) e 1005.6(b) (eCFR, atualizado em 29/10/2026): https://www.ecfr.gov/current/title-12/chapter-X/part-1005/subpart-A/section-1005.2
- Comentario oficial 2(m)-3 da Reg E: https://www.consumerfinance.gov/rules-policy/regulations/1005/interp-2/
- EFTA, 15 U.S.C. 1693 e 1693a(12) (copia Cornell LII; o texto oficial e do US Code, uscode.house.gov): https://www.law.cornell.edu/uscode/text/15/1693a
- S. 4943 (118o Congresso), texto: https://www.govinfo.gov/content/pkg/BILLS-118s4943is/html/BILLS-118s4943is.htm
- FTC, press release 10/03/2025: https://www.ftc.gov/news-events/news/press-releases/2025/03/new-ftc-data-show-big-jump-reported-losses-fraud-125-billion-2024
- PSR, PS24/7 (02/10/2024): https://www.psr.org.uk/ps24-7-app-scams-reimbursement-confirming-max-level/
- PSR, PS25/5 politica consolidada (mai/2025): https://www.psr.org.uk/media/rhelv4op/ps25-5-app-scams-reimbursement-consolidated-policy-statement-may-2025.pdf
- PSR, "One year on" (08/10/2025): https://www.psr.org.uk/news-and-updates/latest-news/news/one-year-on-impact-of-app-reimbursement-on-victims/
- PSR, avaliacao Frontier (01/07/2026): https://www.psr.org.uk/news-and-updates/latest-news/news/payment-fraud-falls-by-73m-following-psr-reimbursement-scheme/
- Zelle, press release 12/02/2025 ($1 trilhao): https://www.zelle.com/press-releases/zelle-shatters-records-1-trillion-sent-single-year
- Zelle, Media Fact Sheet (dez/2025): https://www.zelle.com/sites/default/files/2025-12/Media-Facts-The-Facts-About-Zelle-and-Scams.pdf

**Bloqueio:** hsgac.senate.gov, warren.senate.gov, blumenthal.senate.gov, banking.senate.gov, congress.gov e a pagina de imprensa do NY AG sobre a decisao devolvem 403 / bloqueio de bot. Nao contornei. Os numeros do Senado entram como **Checar** ate alguem abrir o PDF (ou usar a copia no GovInfo, se existir).

---

## 1. Entidades

| # | Entidade | Papel | Trajetoria em 1 linha (fonte) | Foto/logo |
|---|---|---|---|---|
| 1 | **Zelle / Early Warning Services, LLC (EWS)** | Opera a rede Zelle; de propriedade de 7 bancos (queixa CFPB par. 2) | Reu no CFPB (2024, extinto) e no NY AG (2025, em andamento) | SIM zelle_logo.svg (Commons, "Public domain"; marca registrada) |
| 2 | **JPMorgan Chase Bank, N.A.** | Dono de EWS; um dos 3 maiores bancos na rede (73% da atividade em 2023, juntos) | Reu no CFPB | SIM chase_logo.svg (versao 2007 do octogono; marca registrada) |
| 3 | **Bank of America, N.A.** | idem | Reu no CFPB | SIM bofa_logo.svg |
| 4 | **Wells Fargo Bank, N.A.** | idem | Reu no CFPB | SIM wellsfargo_logo.svg |
| 5 | **CFPB** | Agencia federal; autora da acao de 2024 | Processou em 20/12/2024; desistiu em 04/03/2025 | SIM cfpb_seal.svg (PD, selo) |
| 6 | **Rohit Chopra** | Diretor do CFPB quando o processo foi movido | Apresentou a acao em 20/12/2024 (fala na coletiva, pagina do CFPB) | SIM chopra.jpg (FTC, PD; foto de quando era comissario da FTC) |
| 7 | **Russell Vought** | Diretor interino do CFPB na desistencia | Segundo American Banker/imprensa; o aviso foi assinado pelo Chief Legal Officer Mark Paoletta (**Checar** na pagina do Doc 39) | SIM vought.jpg (CFPB, PD, baixa resolucao 455x576) |
| 8 | **Letitia James** | Procuradora-Geral de Nova York | Processou EWS em 13/08/2025 | SIM james.jpg (**CC BY 2.0**, autor Matthew Cohen, Flickr; foto de 2013, ela era Defensora Publica de NYC; exige credito) |
| 9 | **Richard Blumenthal (D-CT)** | Senador; presidente do PSI em 2024; autor do S. 4943 | Relatorio de 23/07/2024; projeto de lei de 01/08/2024 | SIM blumenthal.jpg (PD, Senate) |
| 10 | **Elizabeth Warren (D-MA)** | Senadora; relatorio "Facilitating Fraud" (out/2022); co-autora do S. 4943 | | SIM warren.jpg (PD, Senate, retrato do 114o Congresso) |
| 11 | **Payment Systems Regulator (PSR), Reino Unido** | Regulador de pagamentos; criou a regra de reembolso | PS24/7 (02/10/2024); regra em vigor 07/10/2024 | NAO como arquivo (Commons nao tem o logo). Usar o recorte da pagina (psr_ps24_7.png, mostra o logo PSR). Motivo registrado. |
| 12 | **FTC** | Agencia de defesa do consumidor; Consumer Sentinel | Dado de perdas 2024 | SIM ftc_seal.svg/png (do ep01) |
| 13 | Pay.UK, UK Finance, Frontier Economics | Citados so se couber | | NAO (cartao de texto) |

Pessoa citada sem foto: nenhuma. Vitima do exemplo do NY AG ("Coned Billing", US$ 1.476,89): nao e nomeada; so cartao/T3.
Todos os arquivos e licencas: `entities/credits.json` (11 itens). Logos entram sem recolorir, em cartao `#ece4d0`.

---

## 2. Linha do tempo (cada linha com URL)

| Data | Fato | Fonte | Status |
|---|---|---|---|
| 10/11/1978 | EFTA sancionada (Pub. L. 95-630, tit. XX, par. 2001; 92 Stat. 3728) | https://www.law.cornell.edu/uscode/text/15/1693a (nota de fonte) | Verificado |
| 2015-2017 | Bank of America, Chase e Wells Fargo usam a EWS para criar o Zelle ("by 2015...") | Queixa CFPB par. 2: https://files.consumerfinance.gov/f/documents/cfpb_Zelle-Complaint_2024-12.pdf | Verificado (alegacao) |
| 2017 | Zelle lancado; "Since 2017, hundreds of thousands of consumers complained" | Queixa CFPB par. 5-6 | Verificado (alegacao) |
| jul/2019 | EWS propoe um pacote de "basic network safeguards" e depois o abandona, segundo o NY AG | Queixa NY AG par. 6: https://ag.ny.gov/sites/default/files/court-filings/people-of-the-state-of-new-york-v-early-warning-services-llc-complaint-2025.pdf | Verificado (alegacao) |
| 03/10/2022 | Relatorio da Sen. Warren, "Facilitating Fraud" | https://www.warren.senate.gov/imo/media/doc/ZELLE%20REPORT%20OCTOBER%202022.pdf | Checar (403; numeros so de busca) |
| 16/06/2023 | PSI abre a investigacao (15 meses ate o relatorio) | busca; PDF do PSI bloqueado | Checar |
| mid-2023 (30/06/2023) | Rede Zelle passa a exigir que bancos reembolsem "a limited category of imposter schemes", "a fraction of all induced fraud" | Queixa CFPB par. 50 ("Since mid-2023"). Dia 30/06/2023: NBC/Reuters 13/11/2023 https://www.nbcnews.com/business/personal-finance/zelle-refunds-customers-hurt-by-imposter-scams-rcna124957 | Mes/ano Verificado; dia 30/06 = Checar |
| ago/2023 | Ate agosto/2023, so o Bank of America: 324.000+ queixas de induzidas sem credito (US$ 207 mi), 161.000+ de nao autorizadas sem credito (US$ 85 mi) | Queixa CFPB par. 174-177 | Verificado (alegacao) |
| 02/10/2024 | PSR publica PS24/7: teto de reembolso de 85.000 libras; inicio 07/10/2024 | https://www.psr.org.uk/ps24-7-app-scams-reimbursement-confirming-max-level/ | Verificado |
| 07/10/2024 | Entra em vigor no Reino Unido o reembolso obrigatorio de fraude APP (Faster Payments e CHAPS) | PS25/5 par. 1.1: https://www.psr.org.uk/media/rhelv4op/ps25-5-app-scams-reimbursement-consolidated-policy-statement-may-2025.pdf | Verificado |
| 20/12/2024 | CFPB processa EWS, BofA, Chase e Wells Fargo, D. Ariz., 2:24-cv-03652; CFPA (pratica injusta) contra todos; EFTA/Reg E contra os bancos | Pagina da acao: https://www.consumerfinance.gov/enforcement/actions/early-warning-services-llc-bank-of-america-na-jpmorgan-chase-bank-na-wells-fargo-bank-na/ ; queixa par. 13 | Verificado |
| 04/03/2025 | CFPB protocola aviso de desistencia voluntaria, com prejuizo, contra todos os reus (Doc 39) | Pagina da acao (idem) | Verificado |
| 05/03/2025 | Juiz extingue o caso "with prejudice" (Doc 43) | https://files.consumerfinance.gov/f/documents/cfpb_early-warning-order-dismissal-prejudice_2025-03.pdf | Verificado |
| 10/03/2025 | FTC: perdas reportadas de US$ 12,5 bi em 2024 (+25%) | https://www.ftc.gov/news-events/news/press-releases/2025/03/new-ftc-data-show-big-jump-reported-losses-fraud-125-billion-2024 | Verificado |
| 13/08/2025 | NY AG processa EWS na NY Supreme Court (County of NY), Index 654753/2025, Exec. Law 63(12) | Press release e queixa (URLs acima; carimbo "FILED ... 08/13/2025 10:26 AM") | Verificado |
| 08/10/2025 | PSR, 1o ano: 112 mi de libras reembolsadas em 9 meses | https://www.psr.org.uk/news-and-updates/latest-news/news/one-year-on-impact-of-app-reimbursement-on-victims/ | Verificado |
| 10/04/2026 | EWS pede a extincao do caso do NY AG | ABA Banking Journal (busca) | Checar |
| 20/07/2026 (segunda) | Justice Phaedra Perry-Bond (NY Supreme Court) nega o pedido de extincao; as duas teses do AG seguem; EWS diz que vai recorrer; plano de descoberta ate 08/09/2026 | American Banker https://www.americanbanker.com/news/early-warning-loses-bid-to-toss-ny-zelle-fraud-suit ; Daily Record https://thedailyrecord.com/2026/07/22/zelle-new-york-attorney-general-lawsuit-fraud/ | Checar (so imprensa; sem decisao no ag.ny.gov/NYSCEF). Decisao processual, nao de merito |
| 01/07/2026 | PSR/Frontier: queda estimada de 73 mi de libras por ano nas perdas APP | https://www.psr.org.uk/news-and-updates/latest-news/news/payment-fraud-falls-by-73m-following-psr-reimbursement-scheme/ | Verificado |
| Depois de 08/09/2026 | Estado do caso do NY AG (apelacao, descoberta, acordo) | nao achado | Checar antes de gravar |

---

## 3. Numeros exatos

| Numero | O que significa | Fonte | Status |
|---|---|---|---|
| 143 milhoes de usuarios; 2.200+ bancos e cooperativas; US$ 481 bi em 1,7 bi de transacoes no 1o semestre de 2024 | Rede Zelle, segundo o CFPB | Queixa CFPB par. 3 | Verificado (alegacao) |
| 73% | Parcela dos 3 bancos na atividade da rede em 2023 | Queixa CFPB par. 3 | Verificado |
| 290 mi / 210.000 clientes (BofA); 360 mi / 420.000 (Chase); 220 mi / 280.000 (Wells Fargo) | "complaints of over" esses valores de perda por fraude | Queixa CFPB par. 10 | Verificado (alegacao) |
| **US$ 870 mi** | **Nao esta escrito assim na queixa.** E a soma minha: 290+360+220. Usar "mais de US$ 870 milhoes em queixas de clientes dos tres bancos, somando os numeros da queixa". A fala do Chopra: "over $800 million" | Queixa par. 10; fala de Chopra (URL acima) | Verificado como soma; "$870M" como citacao = NAO usar |
| Periodo dessas queixas | A queixa so data o BofA (ate ago/2023). Chase/Wells: periodo nao conferido | Queixa par. 174 | Checar |
| "More than $1 billion" 2017-2023 | NY AG: golpistas roubaram de usuarios entre 2017 e 2023. Na queixa: "over a billion dollars in consumer losses from reported fraud" ate 2023 | Press release; queixa par. 9 | Verificado (alegacao) |
| US$ 1.476,89 | Usuario de NY perdeu para falso "Coned Billing" (impostor da Con Edison), exemplo do AG | Press release NY AG | Verificado (alegacao) |
| 2,3 bi de pagamentos, US$ 629 bi (2022); alta de quase US$ 200 bi em 2023 | Volume da EWS, segundo o NY AG | Queixa NY AG par. 127 e linha 979 | Verificado (alegacao) |
| US$ 1 trilhao; 3,6 bi de transacoes (2024) | Volume do Zelle, dado do proprio Zelle | Press release Zelle 12/02/2025 | Verificado (fonte do Zelle) |
| 99,95% | Zelle afirma que mais de 99,95% das transacoes sao concluidas sem relato de golpe. Dado do proprio Zelle | Fact sheet do Zelle (dez/2025) | Verificado como afirmacao do Zelle |
| **12 CFR 1005.2(m)** | "an electronic fund transfer from a consumer's account initiated by a person other than the consumer without actual authority to initiate the transfer and from which the consumer receives no benefit" (exclusoes: (1) quem recebeu o dispositivo de acesso do consumidor; (2) fraude do proprio consumidor; (3) banco ou funcionario) | eCFR (URL acima), recorte ecfr_1005_2.png | Verificado |
| 15 U.S.C. 1693a(12) | Mesma definicao na lei: "initiated by a person other than the consumer without actual authority..." | Cornell LII; recorte cornell_efta_1693a.png | Verificado |
| Comentario 2(m)-3 | "An unauthorized EFT includes a transfer initiated by a person who obtained the access device from the consumer through fraud or robbery." Ou seja: o golpista que engana a vitima para entregar a senha/token pode ser "nao autorizado"; o golpista que engana a vitima para ela mesma enviar o dinheiro, nao | CFPB, Interp. 2(m) | Verificado (texto). A leitura "pagamento induzido fica fora" e a leitura geral; a queixa do CFPB, par. 50, diz que os bancos "typically" nao reembolsam transferencias induzidas |
| US$ 50 / 2 dias uteis; US$ 500; 60 dias | Responsabilidade do consumidor em transferencia nao autorizada (1005.6(b)); a regra de 60 dias para avisar o banco do que aparece no extrato | eCFR 1005.6(b) (lido via API do eCFR) | Verificado, mas so vale para o caso "nao autorizado", nao para o induzido |
| S. 4943 | "To amend the Electronic Fund Transfer Act to treat fraudulently induced electronic fund transfers in the same manner as unauthorized electronic fund transfers." Blumenthal e Warren; introduzido 01/08/2024; 118o Congresso | govinfo (URL acima) | Verificado |
| H.R. 9303 | Versao da Camara (Maxine Waters) | busca | Checar (congress.gov bloqueado) |
| Situacao do projeto | Morreu com o 118o Congresso (03/01/2025); nao achei reapresentacao no 119o. **Nao e lei.** O TRAPS Act (S. 2019, 10/06/2025) e outro projeto: forca-tarefa, sem reembolso | billtrack50/busca | Checar no congress.gov antes de afirmar "nenhum projeto vivo" |
| US$ 12,5 bi; +25%; 2,6 mi de consumidores | Perdas reportadas a FTC em 2024 | FTC press release | Verificado |
| US$ 2,089 bi (47.336 relatos) | Perda por "Bank Transfer or Payment" em 2024, 1o entre os metodos; cripto US$ 1,42 bi | Data Book 2024 https://www.ftc.gov/system/files/ftc_gov/pdf/csn-annual-data-book-2024.pdf | Checar (PDF nao aberto; numero de resumo de busca). O press release confirma so: "bank transfers or cryptocurrency" > todos os outros metodos juntos |
| 85.000 libras | Teto por reclamacao, Faster Payments e CHAPS | PS24/7; PS25/5 politica 7 | Verificado |
| 50% | Banco receptor paga ao remetente 50% do reembolso | PS25/5 politica 2 | Verificado. A pagina PS24/7 nao menciona |
| Ate 100 libras | Franquia opcional do banco remetente; nao vale para vulneraveis | PS25/5 politica 5 e 9 | Verificado |
| 5 dias uteis; 13 meses | Prazo para reembolsar; prazo para reclamar | PS25/5 politicas 4 e 8 | Verificado |
| Excecoes | Fraude do proprio cliente; "gross negligence" (padrao de cautela do consumidor); nao cobre disputas civis, pagamentos internacionais, outros sistemas (ex.: cripto) | PS25/5 politicas 1 e 3; par. 3.3 | Verificado |
| 112 mi de libras; 126.000 reclamacoes (out/2024 a jun/2025) | Primeiros 9 meses | PSR "One year on" | Verificado |
| 88% | Do dinheiro perdido em golpes APP e reclamado ao banco, 88% foi devolvido (era 66% no mesmo periodo de 2023/24; a PSR avisa que a metodologia mudou) | PSR "One year on" | Verificado, usar a ressalva |
| 97% das reclamacoes dentro do escopo; 54% -> 65% em todas | Reembolso, avaliacao Frontier | PSR 01/07/2026 | Verificado |
| 459,7 milhoes de libras | Perdas APP em 2023, "segundo a UK Finance" | PSR pagina "APP scams" citando UK Finance | Verificado como citacao |

### Senado (tudo Checar: PDFs do Senado bloqueados)
- PSI, relatorio de maioria, 23/07/2024, "A Fast and Easy Way to Lose Money: Insufficient Consumer Protection on the Zelle Network", ~62 pp.: https://www.hsgac.senate.gov/wp-content/uploads/2024.7.23-PSI-Majority-Staff-Report-on-Zelle.pdf
- Segundo trechos de busca: os 3 bancos reembolsaram 38% das disputas "nao autorizadas" em 2023 (62% em 2019) e 12% das disputas de golpe em 2023; a politica de 30/06/2023 gerou US$ 18,3 mi em reembolsos nos 6 meses seguintes; ~54.000 disputas de impostor de 30/06 a 31/12/2023, ~44% elegiveis; na audiencia (21/05/2024) Blumenthal citou US$ 372 mi disputados em 2023, US$ 270 mi nao reembolsados.
- Warren, "Facilitating Fraud: How Consumers Defrauded on Zelle are Left High and Dry by the Banks that Created It", 03/10/2022: US$ 440 mi de perda em 2021 (estimativa fornecida pela EWS); 4 bancos deram dados (192.878 casos, US$ 213,8 mi, 2021 e 1o sem. 2022; JPMorgan nao deu dados); 47% reembolsado nos casos nao autorizados (US$ 83,06 mi de 176,2 mi).
- Os numeros de 2021-2023 podem confundir (periodos e medidas diferentes). Nao misturar.

---

## 4. Lista "Checar" (nao conferido na fonte primaria)
1. Numeros do relatorio do PSI e do relatorio da Warren (acesso bloqueado). Pedir ao Maiquel para baixar os PDFs, ou usar so os numeros da queixa do CFPB.
2. Dia 30/06/2023 da politica de reembolso de impostor do Zelle (so NBC/Reuters e busca). A queixa so diz "mid-2023". Dica: dizer "desde meados de 2023".
3. Decisao de 20/07/2026 do NY AG vs EWS (so imprensa) e o que aconteceu depois de 08/09/2026.
4. Quem assinou o aviso de 04/03/2025 (Mark Paoletta) e que Russell Vought era diretor interino naquela data (imprensa). Abrir o Doc 39 no PACER/CourtListener.
5. H.R. 9303 (autora Waters), data de extincao do projeto (03/01/2025) e se houve reapresentacao no 119o Congresso.
6. FTC Data Book: US$ 2,089 bi em bank transfer (abrir o PDF).
7. Periodo das queixas de Chase e Wells Fargo (par. 10 da queixa do CFPB).
8. Canal de denuncia do NY AG: o press release convida nova-iorquinos a relatar ao "OAG's Consumer Frauds Bureau" (visto no recorte); o link do formulario nao foi aberto.
9. Se ha projeto de lei estadual de reembolso ou iniciativa do CFPB atual: nao pesquisado.
10. Ordem sob Reg E: o texto da Reg E sobre "induced fraud" nao diz nada; "por que fica fora" = leitura da definicao. Gravar como "A regra so cobre quem iniciou a transferencia sem autoridade" e nao como "a lei diz que golpe induzido nao e coberto".
11. Zelle diz que "banks are required by law to investigate" (fact sheet) e que reembolsa fraude confirmada acima do exigido: afirmacoes do Zelle, nao conferidas.

## 5. Observacoes para o roteiro
- Nao falar "$870 milhoes" como numero oficial: dizer "mais de US$ 290 milhoes, US$ 360 milhoes e US$ 220 milhoes", ou a soma como conta na tela.
- "O CFPB desistiu" e fato (Verificado). Motivo da desistencia: nao ha texto oficial no aviso; nao atribuir motivo.
- Contraste UK x EUA: o UK exige por regra do regulador (PSR) desde 07/10/2024; nos EUA o Zelle reembolsa so "certain qualifying imposter scams" por regra da propria rede, e o projeto S. 4943 nao virou lei.
- Aviso de rigor: EWS, bancos e Zelle negam as alegacoes; Zelle: "political stunt" (resposta ao NY AG, imprensa) e 99,95% sem relato.

## 6. Recortes capturados (assets\clips\, todos de 02/11/2026; cada .png tem .json com URL e caixa)
| Arquivo | URL | O que marca | Capitulo |
|---|---|---|---|
| cfpb_sues_2024.png | https://www.consumerfinance.gov/archive/newsroom/cfpb-sues-jpmorgan-chase-bank-of-america-and-wells-fargo-for-allowing-fraud-to-fester-on-zelle/ | manchete "Allowing Fraud to Fester on Zelle" + data DEC 20, 2024; mostra tambem a faixa "Archived content" e a nota da desistencia (04-05/03/2025) | CASE |
| cfpb_enforcement_page.png | https://www.consumerfinance.gov/enforcement/actions/early-warning-services-llc-bank-of-america-na-jpmorgan-chase-bank-na-wells-fargo-bank-na/ | titulo da acao, texto da alegacao e da desistencia; lateral: tribunal, docket, "Dismissed" | CASE |
| nyag_sues_2025.png | https://ag.ny.gov/press-release/2025/attorney-general-james-sues-company-behind-zelle-enabling-widespread-fraud | manchete + "Users Lost More Than $1 Billion" + 13/08/2025; banner de cookies ocultado por CSS (nao havia botao de recusar, so "Okay") | CASE |
| ecfr_1005_2.png | https://www.ecfr.gov/current/title-12/chapter-X/part-1005/subpart-A/section-1005.2 | definicao (m) "Unauthorized electronic fund transfer"; rolagem para o trecho | RULE |
| cornell_efta_1693a.png | https://www.law.cornell.edu/uscode/text/15/1693a | par. (12) da EFTA + nota Pub. L. 95-630, Nov. 10, 1978. Ha uma faixa de cookies no pe: cortar o rodape na cena | RULE |
| psr_ps24_7.png | https://www.psr.org.uk/ps24-7-app-scams-reimbursement-confirming-max-level/ | "PS24/7 ... maximum level of reimbursement", 02/10/2024, "start date ... 7 October 2024"; banner recusado | RULE (UK) |
| psr_one_year.png | https://www.psr.org.uk/news-and-updates/latest-news/news/one-year-on-impact-of-app-reimbursement-on-victims/ | "One year on", 08/10/2025, "£112 million was reimbursed to victims" | RULE (UK) |
| ftc_12_5b.png | https://www.ftc.gov/news-events/news/press-releases/2025/03/new-ftc-data-show-big-jump-reported-losses-fraud-125-billion-2024 | manchete "$12.5 Billion in 2024", 10/03/2025 | SCAM |

8 recortes, nenhum de imprensa (American Banker e semelhantes ficam atras de assinatura; pode-se adicionar ate 3 manchetes depois, se o Maiquel quiser). Nenhum dado pessoal visivel. Observacoes de captura:
- `tools/web_clip.py` so captura o topo da pagina e nao recusa o banner do PSR ("I Do Not Accept"). Para eCFR, PSR, NY AG e Cornell usei uma copia de trabalho com rolagem ate o texto e recusa do banner, na pasta temporaria da sessao: `C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Documents-Codex-2026-09-10-Dark-YouTube\2ff7f288-0ffd-485a-9fed-0170e9d81589\scratchpad\wc2.py`. O `tools/web_clip.py` nao foi alterado.
- Faltam recortes para: Congress/S. 4943 (congress.gov bloqueia; usar govinfo), Senado (bloqueado). Capturar govinfo S. 4943 no Gate 3 se for usar.
