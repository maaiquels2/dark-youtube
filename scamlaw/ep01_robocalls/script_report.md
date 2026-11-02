# Ep01 Robocalls - relatorio do roteiro (GATE 2)

- Palavras de narracao: **1614** (mais 4 do titulo falado, bloco 0 = 1618 no total). Meta 1.450-1.650: ok.
- Blocos: **75** (bloco 0 = titulo falado + 74 blocos). Tempo estimado a ~2,6 palavras/s: cerca de 10.4 min de fala, mais pausas = 10-11 min.
- Blocos de capitulo (5) e o titulo (bloco 0) sao curtos de proposito. Os outros 69 ficam entre 15 e 28 palavras (conferido por script).
- Cold open: blocos 1-3 (~65 palavras, ~25 s).
- `CHANNELNAME` aparece uma vez, no bloco 74. Substituir antes da voz.

## Capitulos (cada um e candidato a Short)
| # | Titulo | Blocos |
|---|---|---|
| 1 | The Call | 4-14 |
| 2 | The Fine | 15-26 |
| 3 | The Hearing | 27-37 |
| 4 | The Law | 38-49 |
| 5 | Still Ringing | 50-60 |
| - | Who pays the bill (sem cabecalho) | 61-65 |
| - | O que voce pode fazer + denuncia | 66-71 |
| - | Fecho que espelha o gancho | 72-73 |
| - | Pedido de inscricao | 74 |

## Padroes de retencao (PADRAO_VIDEOS.md tem 12; os 8 centrais estao em 1-8)
1. Numero concreto na 1a/2a frase: blocos 1, 16, 39, 51 (96 milhoes; 120 milhoes; 48 bilhoes; 58,5 bilhoes).
2. Contradicao como motor: bloco 3 (multa recorde + lei nova + o telefone ainda toca), retomada nos blocos 52-54 e 72.
3. Conflito central unico (confianca no numero da tela): blocos 5-14, 66, 74 (sem desvio para outro assunto).
4. Culpa deslocada: blocos 22-24 (a defesa dele de que so ha dano se atender 5 min contra a decisao do FCC) e 33-34 (nega ser o kingpin; FCC nao achou prova de que a operadora sabia).
5. Quem paga a conta: blocos 61-65 (donos dos numeros falsos, marcas, quem apertou 1, o publico que reclamou).
6. Pausa util no meio: blocos 46-47 (STIR SHAKEN como assinatura digital) e 66-71 (o que fazer).
7. Honestidade explicita: blocos 11 e 12 ("the FCC says"), 22-23 (alegacao x decisao), 25 (civil, nao criminal), 31-32 (Quinta Emenda nao e prova), 54 (sem contrafactual, YouMail e estimativa), 59 (ruling, nao lei nova), 65.
8. Fecho que espelha o gancho: blocos 72-74 repetem 1-3 (tres meses, 96 milhoes, multa, lei, telefone ainda toca) e terminam pedindo inscricao.
9. Tese cedo + licao no fim de cada capitulo: tese no bloco 3; licoes nos blocos 14, 26, 37, 49, 60.
10. Sem especulacao como fato: bloco 54 admite que nao se sabe o contrafactual; bloco 65 diz que o order nao da contagem de vitimas.
11. Sem residuo no texto falado: sem 'TTS script', sem 'watch next'. Cabecalhos 'Chapter N.' seguem o padrao do canal.
12. Sem anuncio no meio: pedido de inscricao so no bloco 74.

## Candidatos a Short (nota estimada 0-10)
| Capitulo | Nota | Por que |
|---|---|---|
| 2 The Fine (15-26) | 8,5 | Numero forte (120 mi) na 1a frase, reviravolta da amostra de 80 mil, fecho curto |
| 1 The Call (4-14) | 8 | Gancho de 'seu celular toca', numero 96,7 mi, fecho 'o truque inteiro'. Cena familiar para todos |
| 5 Still Ringing (50-60) | 8 | Contradicao (lei nova, mesmo volume), numeros de grafico, fecho forte; precisa cortar para 45 s |
| 3 The Hearing (27-37) | 7 | Citacao 'not the kingpin' e conta de 2 milhoes; mais denso e menos universal |
| 4 The Law (38-49) | 6,5 | Bom, mas tecnico (STIR SHAKEN); cortar a pausa explicativa para virar Short |

## Opcoes de titulo (sem nome de empresa, valor exato, <= 60 caracteres)
- He Made 96,758,223 Calls. The Fine: $120,000,000 (48)
- The $120,000,000 Robocall Fine, Explained Simply (47)
- Why a $120,000,000 Fine Did Not Silence Your Phone (50)
- What Actually Happened After the $120,000,000 Fine (49)
- 96,758,223 Fake Calls in 3 Months: The Law That Followed (56)
Recomendada: a 2 (formula 3, 'Explained Simply'; serie reconhecivel). O bloco 0 falado ('Ninety-Six Million Fake Calls.') funciona com qualquer uma.

## Duvidas / pontos que precisam de decisao
1. Bloco 12: 'ninety-six million, seven hundred fifty-eight thousand' omite os 223 finais de proposito (TTS fica melhor); o card em tela mostra 96,758,223. Se preferir o numero completo, ajustar.
2. Blocos 46-47 (STIR SHAKEN como assinatura digital) usam a explicacao simples do research.md sec.6, cujo texto tecnico esta marcado Checar. E correta em termos gerais, mas conferir em fcc.gov/call-authentication antes de gravar.
3. Blocos 67-69 e 71 (nao apertar 1, nao devolver, falar com a operadora): as dicas gerais estao marcadas Checar no research.md sec.8 e nao atribui a nenhum orgao. Conferir nas paginas FCC/FTC.
4. Bloco 41: 'about seventeen months' e conta nossa (31/dez/2016 a 10/mai/2018). Bloco 41 tambem afirma que a lei de 2010 'worked after the fact' - e leitura, nao fato da fonte; suavizar se o Gate de revisao pedir.
5. Bloco 26 e 60 trazem inferencia moderada (o volume nao caiu). Sustentada pelos dados YouMail, e o bloco 54 avisa que nao se sabe o contrafactual.
6. Desfecho da multa: o roteiro NAO diz se foi paga, nem condenacao. Bloco 25 diz so que foi multa civil.
7. Bloco 56: 'removed fourteen providers' segue o research (14 removidas desde 2023); o research nao da a data exata da 14a remocao.
8. Bloco 57: 'two Texas telemarketers' sem nomes; 'fined' = ordem final de marco/2021 (research diz proposta jun/2020, final mar/2021).
9. Os 'Checar' evitados: placar 97-1 e 417-3, dia exato do NAL, data 30/jun/2021 do STIR SHAKEN, desfecho da multa, Clyburn, task force, FTC por ano.
10. Tipo de cartao para Rosemary Harold e Lois Greisman: monograma (sem foto).

## Fonte e imagem por bloco
Fontes referem-se a secoes do research.md (sec.N). Linha `V:` = visual sugerido.

**0** (4 palavras) - Ninety-Six Million Fake Calls.
- Fonte: titulo falado (FCC 18-58 par.1, sec.3)
- V: title card: titulo em tela, fundo escuro
**1** (24 palavras) - Three months. Ninety-six million phone calls. The FCC says the callers faked their numbers, so they looked like they came from your own neighborhood.
- Fonte: sec.3 96.758.223; sec.5.1 neighbor spoofing; FCC 18-58 par.1
- V: fact card 96,758,223 + reconstrucao: celular tocando na mesa da cozinha 2016, numero local na tela
**2** (25 palavras) - Then a record fine. Then a Senate hearing, where the man behind the calls said, I am not the kingpin of robocalling that is alleged.
- Fonte: sec.2 18/abr/2018 (Hearing 115-806); sec.3 US$120 mi
- V: cartao monograma: Adrian Abramovich + documento: trecho da transcricao do Senado
**3** (20 palavras) - Then a brand new law. And yet, your phone still rings. Here is what really changed, and what did not.
- Fonte: sec.2 30/dez/2019; sec.4.1 YouMail
- V: foto card: Thune + Pallone, depois reconstrucao: celular tocando de novo (2026)
**4** (4 palavras) - Chapter one. The Call.
- Fonte: titulo de capitulo
- V: chapter card: 1 The Call
**5** (19 palavras) - Your phone rings. The number looks local. It even starts with the same six digits as your own number.
- Fonte: sec.5.1 (FCC 18-58 n.108)
- V: reconstrucao: celular tocando, tela mostra numero vizinho (digitos destacados)
**6** (24 palavras) - That trick is called neighbor spoofing. The caller fakes the number on your screen, copying the first six digits of the number being called.
- Fonte: sec.5.1 (FCC 18-58 n.108)
- V: diagrama animado: dois numeros com os 6 primeiros digitos iguais
**7** (25 palavras) - You pick up. A recording says you have been chosen for an exclusive travel offer, from a brand you know. Press one to claim it.
- Fonte: sec.5.2 (FCC 18-58 par.4,16)
- V: reconstrucao: mao atendendo, legenda da gravacao 'Press 1'
**8** (27 palavras) - According to the FCC, the callers used the names TripAdvisor, Expedia, Marriott and Hilton. Those companies did not make the calls. Their names were used without permission.
- Fonte: sec.1 #17-20; sec.9.7; FCC 18-58 par.4,15
- V: logos: TripAdvisor, Expedia, Marriott; cartao monograma Hilton (sem logo livre)
**9** (22 palavras) - If you pressed one, you were connected to a call center. There, operators sold vacation packages, usually with a timeshare sales presentation.
- Fonte: sec.5.3 (FCC 18-58 par.16,37)
- V: fluxo simples: ligacao > Press 1 > call center > pacote timeshare
**10** (26 palavras) - Those packages were for Mexico and the Caribbean. The operators had no connection to the brands whose names were used to get you on the line.
- Fonte: sec.5.3-5.4 (par.16); nao dizer que o call center era no Mexico
- V: fluxo simples (continuacao) + mapa Mexico/Caribbean so do pacote
**11** (15 palavras) - The FCC says the man behind the recordings was Adrian Abramovich, a businessman from Miami.
- Fonte: sec.1 #1; FCC 18-58
- V: cartao monograma: Adrian Abramovich (sem foto) com legenda 'according to the FCC'
**12** (26 palavras) - From October to December of twenty sixteen, the FCC counted ninety-six million, seven hundred fifty-eight thousand calls. That is more than a million calls a day.
- Fonte: sec.2 1/out-31/dez/2016; sec.3 96.758.223 e >1 mi/dia; sec.4.2
- V: grafico de barras: chamadas por mes (36,5 / 30,7 / 29,5 mi) com valores
**13** (23 palavras) - And the harm did not stop with the people who answered. The real owners of those faked numbers began getting angry calls back.
- Fonte: sec.5.6 (FCC 18-58 par.16,18,37)
- V: reconstrucao: celular tocando de novo na cozinha, pessoa confusa (sem rosto realista)
**14** (23 palavras) - A local number on your screen is not proof of where a call comes from. In this case, that was the whole trick.
- Fonte: sec.8 'fala segura'; sec.3 80.000 amostradas spoofed
- V: tela de celular com numero local + carimbo 'FAKE' sobre ele
**15** (4 palavras) - Chapter two. The Fine.
- Fonte: titulo de capitulo
- V: chapter card: 2 The Fine
**16** (24 palavras) - One hundred twenty million dollars. That was the fine. In June twenty seventeen, the FCC proposed it against Adrian Abramovich and his two companies.
- Fonte: sec.2 22/jun/2017; sec.1 #2; gate-1 'June 2017'
- V: fact card US$120,000,000 + cartoes monograma: Marketing Strategy Leaders / Marketing Leaders
**17** (21 palavras) - In May twenty eighteen, the FCC made it final. He and both companies were held responsible together, for the full amount.
- Fonte: sec.2 10/mai/2018 (FCC 18-58)
- V: documento: capa FCC 18-58 Forfeiture Order, data em destaque; selo FCC
**18** (25 palavras) - FCC Chairman Ajit Pai called it the largest fine in the agency's history. It was also the first under the Truth in Caller ID Act.
- Fonte: sec.1 #5 (Pai statement); sec.2 10/mai/2018
- V: foto card: Ajit Pai + selo FCC
**19** (24 palavras) - Here is the odd part. The FCC did not count all ninety-six million calls. It sampled eighty thousand, about a thousand for each day.
- Fonte: sec.3 80.000 (par.7,25,28)
- V: infografico: 96.758.223 vs 80.000 amostradas (1.000/dia)
**20** (24 palavras) - It counted each sampled call at one thousand dollars, which is eighty million. Then it added forty million more. That makes one hundred twenty.
- Fonte: sec.3 US$1.000 + US$40 mi (par.25,33)
- V: calculo animado: 80.000 x 1.000 = 80 mi, +40 mi = 120 mi
**21** (23 palavras) - The FCC found that every one of those eighty thousand sampled calls used a spoofed number. The fine was built on that sample.
- Fonte: sec.3 80.000; sec.8; FCC 18-58 par.7
- V: documento: trecho do order sobre a amostra, destaque 80,000
**22** (19 palavras) - Abramovich argued that no one is harmed unless they answer and stay on the line for about five minutes.
- Fonte: sec.5.7 (par.27,35-38) - argumento dele
- V: cartao monograma Abramovich + legenda 'his argument'
**23** (24 palavras) - The FCC ruled otherwise. Under the law, what matters is whether he intended to cause harm, not whether harm was proven for each call.
- Fonte: sec.5.7 (par.27,35-38)
- V: documento: citacao do order sobre 'intent' + selo FCC
**24** (22 palavras) - Commissioner Michael O'Rielly agreed in part and disagreed in part. He doubted there is harm when a consumer never hears the message.
- Fonte: sec.1 #7
- V: foto card: Michael O'Rielly
**25** (22 palavras) - One more thing. This was a civil fine from a federal agency. It was not a criminal verdict. Those are different things.
- Fonte: sec.9.1 (administrativa, sem condenacao)
- V: comparacao em tela: 'FCC forfeiture (civil)' vs 'criminal conviction' (texto)
**26** (16 palavras) - A record fine. And a lesson: one fine does not change how the phone network works.
- Fonte: sec.3 120 mi; sec.4.1 plato (inferencia)
- V: grafico de linha: robocalls por ano 2016-2025 (comeca a aparecer) com valores
**27** (4 palavras) - Chapter three. The Hearing.
- Fonte: titulo de capitulo
- V: chapter card: 3 The Hearing
**28** (25 palavras) - Abramovich said no to the Senate. In October twenty seventeen, the Commerce Committee wrote to him. In November, his lawyer declined. Then came a subpoena.
- Fonte: sec.2 10/out/2017 e 3/nov/2017 (Hearing 115-806)
- V: timeline: out/2017 carta > nov/2017 recusa > intimacao; cartao Senate Commerce Committee
**29** (19 palavras) - On April eighteenth, twenty eighteen, he testified. The hearing was titled Abusive Robocalls and How We Can Stop Them.
- Fonte: sec.2 18/abr/2018
- V: documento: titulo do hearing 115-806 (govinfo)
**30** (28 palavras) - Abramovich claimed fewer than two percent of people called interacted with the message. Senator John Thune did the math: two percent of a hundred million is two million.
- Fonte: sec.3 ~2% (Hearing 115-806)
- V: foto card: John Thune + calculo animado: 2% de 100 mi = 2 mi
**31** (22 palavras) - He answered some questions. On others he invoked the Fifth Amendment. That is his right, and it is not proof of anything.
- Fonte: sec.9.5 (transcricao govinfo)
- V: documento: trecho da transcricao + cartao Abramovich
**32** (24 palavras) - Senator Richard Blumenthal asked the chairman to consider holding him in contempt after he invoked the Fifth. That was a request, not a ruling.
- Fonte: sec.1 #11
- V: foto card: Richard Blumenthal
**33** (23 palavras) - He also said, I am not the kingpin of robocalling that is alleged. The kingpin label came from others, and he denied it.
- Fonte: sec.2 18/abr/2018; sec.9.2
- V: documento: citacao 'I am not the king pin of robocalling that is alleged'
**34** (26 palavras) - He also said the resorts were real, offering real vacation packages. The FCC found no evidence that the carrier or the clients knew about the spoofing.
- Fonte: sec.9.3-9.4 (par.42)
- V: cartao: 'resorts were real' (his words) e 'FCC: no evidence' (lado a lado)
**35** (24 palavras) - Other witnesses gave the scale. Lois Greisman of the FTC reported more than seven million complaints about unwanted calls in fiscal year twenty seventeen.
- Fonte: sec.1 #10; sec.3 >7 mi (Hearing 115-806)
- V: selo FTC + fact card '7,000,000+ complaints' (sem foto)
**36** (17 palavras) - Rosemary Harold, the FCC's enforcement chief, told senators that robocalls were the agency's largest source of complaints.
- Fonte: sec.1 #9
- V: selo FCC + cartao monograma Rosemary Harold (sem foto)
**37** (20 palavras) - He denied being the kingpin. Senator Thune went on to co-write the law that came next, with Representative Frank Pallone.
- Fonte: sec.1 #3-4
- V: fotos lado a lado: Thune e Pallone
**38** (4 palavras) - Chapter four. The Law.
- Fonte: titulo de capitulo
- V: chapter card: 4 The Law
**39** (22 palavras) - Nearly forty-eight billion robocalls in one year. That was twenty eighteen, according to YouMail, up more than half from the year before.
- Fonte: sec.4.1 (2018 = 47,8 bi, +56,8% sobre 30,5 bi; YouMail)
- V: grafico de linha: 2016-2018 com valores 29,1 / 30,5 / 47,8
**40** (27 palavras) - A law already existed. The Truth in Caller ID Act of twenty ten bans spoofing that is meant to defraud, cause harm, or get something of value.
- Fonte: sec.2 22/dez/2010 (P.L. 111-331)
- V: documento: Truth in Caller ID Act, P.L. 111-331, trecho
**41** (28 palavras) - But it worked after the fact, case by case. Abramovich's calls ended in December twenty sixteen. The fine became final in May twenty eighteen, about seventeen months later.
- Fonte: sec.2 datas 31/dez/2016 e 10/mai/2018 (17 meses = conta nossa)
- V: timeline: dez/2016 ultima chamada > jun/2017 proposta > mai/2018 final (17 meses)
**42** (21 palavras) - So Congress wrote a new one. The Pallone-Thune TRACED Act passed almost unanimously and was signed on December thirtieth, twenty nineteen.
- Fonte: sec.2 30/dez/2019 (P.L. 116-105); gate-1 'almost unanimously'
- V: documento: P.L. 116-105 capa + fotos Pallone e Thune
**43** (22 palavras) - First, bigger penalties. For an intentional violation, the FCC can add up to ten thousand dollars on top of the base fine.
- Fonte: sec.3 Ate US$10.000; sec.6 Sec.3
- V: fact card US$10,000 + trecho da lei
**44** (23 palavras) - Second, more time. For intentional violations, the FCC now has four years to act. For the base fine, the window is one year.
- Fonte: sec.3 1 ano / 4 anos; sec.6 Sec.3
- V: barra comparando 1 ano x 4 anos
**45** (20 palavras) - Third, and most important, caller authentication. The law gave the FCC eighteen months to require a system called STIR SHAKEN.
- Fonte: sec.3 18 meses; sec.6 Sec.4
- V: fact card '18 months' + titulo STIR/SHAKEN
**46** (24 palavras) - Think of it as a digital signature. The carrier that starts the call signs the number. The carrier that receives it checks the signature.
- Fonte: sec.6 STIR/SHAKEN simples (texto tecnico marcado Checar)
- V: diagrama animado: operadora A assina > operadora B confere
**47** (28 palavras) - If the signature is missing or fake, the call can be flagged or blocked. The law also protects carriers that block, and bans charging you extra for it.
- Fonte: sec.6 Sec.4 (taxa proibida; safe harbor)
- V: icone de chamada marcada/bloqueada + trecho da Sec.4
**48** (28 palavras) - The law also created a group of federal agencies to study how to prosecute these cases criminally, and told the FCC to pass evidence to the Attorney General.
- Fonte: sec.6 Sec.5 (270 dias) e Sec.11; chamar 'interagency working group'
- V: documento: Sec.5 da lei, destaque 'interagency working group'
**49** (22 palavras) - The old law punished a fake number after the damage was done. The new one tried to catch it before you answer.
- Fonte: sec.6 (sintese)
- V: tela de celular: chamada com selo 'blocked' antes de tocar
**50** (4 palavras) - Chapter five. Still Ringing.
- Fonte: titulo de capitulo
- V: chapter card: 5 Still Ringing
**51** (22 palavras) - Fifty-eight and a half billion robocalls in twenty nineteen. About fifty-two and a half billion in twenty twenty-five. Those are YouMail's estimates.
- Fonte: sec.4.1 (58,5 bi / 52,5 bi)
- V: grafico de linha completo 2016-2025 com valores; 2019 e 2025 destacados
**52** (22 palavras) - In between, the number fell to nearly forty-six billion in twenty twenty, the pandemic year. Then it climbed back above fifty billion.
- Fonte: sec.4.1 (45,9 bi 2020; 50,5 bi 2021)
- V: grafico de linha: destaque queda 2020 e retorno 2021
**53** (25 palavras) - It reached fifty-five billion in twenty twenty-three, then fifty-two point eight billion in twenty twenty-four. The law did not shrink the problem. It leveled off.
- Fonte: sec.4.1 (55,0 bi; 52,8 bi); leitura honesta do sec.4.1
- V: grafico de linha: faixa 50-55 bi sombreada
**54** (27 palavras) - To be fair, no one can say how high those numbers would be without the law. And YouMail is a private company, so treat these as estimates.
- Fonte: sec.10 item 11; sec.4.1
- V: cartao de fonte: YouMail Robocall Index + aviso 'estimate'
**55** (27 palavras) - What did the law fix? Carriers must now sign calls. The FCC has bigger penalties, a longer deadline, and a database where providers certify their robocall defenses.
- Fonte: sec.6-7; sec.2 (Robocall Mitigation Database)
- V: lista animada de 3 itens + selo FCC
**56** (27 palavras) - The FCC has used that power. In twenty twenty-three, it removed fourteen providers from the database. In September twenty twenty-five, another was removed for a false certification.
- Fonte: sec.2 2023 (14 removidas); 15/set/2025
- V: timeline 2023 > 2025 com contagem 14
**57** (26 palavras) - The next big case was bigger. In twenty twenty-one, the FCC fined two Texas telemarketers two hundred twenty-five million dollars, for about one billion spoofed calls.
- Fonte: sec.1 #21; sec.4.3; sec.2 mar/2021
- V: grafico de barras: 120 mi vs 225 mi com valores
**58** (24 palavras) - What still fails? Smaller carriers got more time to comply, and in December twenty twenty-one the FCC had to shorten some of those deadlines.
- Fonte: sec.2 dez/2021 (tlp.law)
- V: timeline: prazo grande x prazo pequenas operadoras; selo FCC
**59** (28 palavras) - And technology moves. In February twenty twenty-four, the FCC ruled that AI-generated voices count as artificial voices under the old robocall law. A ruling, not a new law.
- Fonte: sec.2 8/fev/2024; sec.7
- V: documento: titulo do declaratory ruling FCC 24-17 + selo FCC
**60** (17 palavras) - The law made the fake number harder to hide. It did not make your phone go quiet.
- Fonte: sec.4.1 (sintese)
- V: celular tocando de novo (reconstrucao 2026) com grafico plano ao fundo
**61** (23 palavras) - So who pays the bill? Start with people who never made a call at all: the owners of the numbers that were faked.
- Fonte: sec.5.6
- V: reconstrucao: pessoa olhando o celular com muitas chamadas perdidas (sem rosto)
**62** (15 palavras) - The FCC order says they received angry calls from strangers, over calls they never made.
- Fonte: sec.5.6 (par.16,18,37)
- V: documento: trecho do order sobre consumidores devolvendo ligacoes
**63** (20 palavras) - Then the brands. In April twenty sixteen, TripAdvisor reported several consumer complaints to the FCC about calls using its name.
- Fonte: sec.2 abr/2016; sec.1 #17
- V: logo TripAdvisor + selo FCC
**64** (26 palavras) - Then everyone who pressed one. By Thune's math, that could be about two million people. The FCC order does not give a total count of victims.
- Fonte: sec.3 ~2%; sec.5 ultima linha (sem contagem total)
- V: fact card '~2,000,000' com legenda 'Thune math, not a victim count'
**65** (28 palavras) - In the first three months of twenty eighteen alone, the FTC logged about one point four million complaints about unwanted calls. About nine hundred thousand were about robocalls.
- Fonte: sec.3 1,4 mi / ~900 mil (Hearing 115-806)
- V: grafico de barras: 1,4 mi total vs 900 mil robocalls, com valores; selo FTC
**66** (24 palavras) - Now, what can you do? First, remember this case. A local number on your screen proves nothing. Every call the FCC sampled was faked.
- Fonte: sec.8 'fala segura'; sec.3
- V: tela de celular com numero local + carimbo 'FAKE'
**67** (21 palavras) - If a recording offers an exclusive deal you never asked for and says press one, do not press anything. Hang up.
- Fonte: sec.5.2 (sinais de alerta); dicas gerais = Checar
- V: lista de sinais de alerta (3 itens) em cartao
**68** (21 palavras) - Do not call the number back. It may belong to a stranger, just as those faked numbers belonged to real people.
- Fonte: sec.5.6 (inferencia)
- V: cartao: 'Do not call back' + icone de telefone riscado
**69** (21 palavras) - Ask your phone carrier what call-blocking tools it offers. The TRACED Act says carriers cannot charge you extra for call authentication.
- Fonte: sec.6 Sec.4 (taxa proibida)
- V: cartao: 'Ask your carrier' + trecho da Sec.4
**70** (19 palavras) - To report a robocall, go to donotcall dot gov. To report fraud, go to reportfraud dot ftc dot gov.
- Fonte: sec.8 links oficiais
- V: cartao de links: donotcall.gov, reportfraud.ftc.gov, consumercomplaints.fcc.gov; selos FTC e FCC
**71** (22 palavras) - You can also file a complaint at consumercomplaints dot fcc dot gov. The FCC explains spoofing at fcc dot gov slash spoofing.
- Fonte: sec.8 fcc.gov/spoofing; sec.1 #9 (reclamacoes = maior fonte)
- V: cartao de link: fcc.gov/spoofing; selo FCC
**72** (22 palavras) - Three months. Ninety-six million calls. A record fine, a Senate hearing, and a brand new law. And yet your phone still rings.
- Fonte: espelho do gancho (sec.3, sec.2)
- V: reprise: fact card 96,758,223 + celular tocando
**73** (27 palavras) - But now you know what a local number is worth, what the law fixed, and what it did not. That is how you stay one step ahead.
- Fonte: sintese (sec.4.1, sec.6)
- V: grafico de linha final 2016-2025 + lista fixed/not fixed
**74** (24 palavras) - If you want more cases like this, the scam, the case, and the new rule, subscribe to CHANNELNAME. The next case is coming soon.
- Fonte: pedido de inscricao; CHANNELNAME substituir antes da voz
- V: end card: subscribe + CHANNELNAME
