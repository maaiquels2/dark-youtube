# Notas visuais — longo "What Medicines Actually Do Inside Your Body" (16:9)

Uma linha por bloco de `long_narration.json` (69 blocos, numerados na ordem). Formato: **n. modelo(s) — o que aparece**.
Modelos de `puzzles/ec_lib/README.md` (holograma médico: fundo teal escuro, ciano/âmbar/magenta). Os modelos novos do formato horizontal usam os nomes que já estão em `puzzles/ec_lib_next/ec_lib.jsx`: `chapter_card`, `timeline`, `fact_card`, `quote_card`, `lower_third`, `intro`, `outro`. Esses nomes podem mudar enquanto o outro agente trabalha. **Rodapé de fonte** = `lower_third` ou o parâmetro `source`, no canto inferior, sempre que aparecer número ou estudo.

Paleta por capítulo, para o vídeo não virar template repetido: cafeína = âmbar/café · ibuprofeno = vermelho-alarme suave · insulina = ciano · Mounjaro = magenta · mRNA = verde-teal · antibiótico = violeta. A "fechadura" (receptor em U do `molecule_dock`) é o motivo visual que aparece em todos os capítulos.

Regra de tela limpa: nada de seringa enfiando na pele, nada de sangue, nada de comprimido "milagroso" em close. Remédio aparece como embalagem genérica ou molécula, sem marca, exceto o nome "Mounjaro" falado (usar a fórmula estrutural, não a caneta da Lilly).

## The Lock and the Key (abertura)
1. `intro` + `dive_into` adaptado — um comprimido genérico gira no escuro e a câmera mergulha nele até virar uma nuvem de moléculas caindo num corpo-holograma.
2. `fact_card` em sequência rápida — seis ícones acendem um por um (cadeado travado, fio de alarme cortado, chave, carta com selo falso, sirene de treino, parede rachada); fica a grade 3×2 = sumário visual do vídeo.
3. `molecule_dock` — membrana da célula com receptores em U; uma molécula-sinal chega pela corrente sanguínea e encaixa.
4. `molecule_dock` (mesmo cenário) — o encaixe gira como chave e uma onda de sinal entra na célula; rótulos "RECEPTOR = LOCK", "SIGNAL = KEY".
5. `molecule_dock` com 3 ligantes — um encaixa e acende, outro encaixa e fica cinza (travado), o terceiro voa para uma bactéria no canto.
6. `end_card` — "HOW THEY WORK, NOT ADVICE" / "Treatment decisions belong to you and your doctor."

## Caffeine: The Key That Jams the Lock
7. `chapter_card` — "01 · CAFFEINE · jams the lock"; fundo de grão de café em holograma âmbar.
8. `organ_focus` (cérebro) — partículas âmbar (adenosina) surgem entre os neurônios e se acumulam; relógio no canto avançando de manhã à noite.
9. `molecule_dock` + `meter` horizontal "SLEEP PRESSURE" — cada adenosina que encaixa sobe o medidor.
10. `molecule_dock` — a molécula de cafeína (estrutura lado a lado com a adenosina, mostrando a semelhança) entra no receptor; o receptor fica cinza com um cadeado; adenosinas batem e voltam.
11. `meter` "SLEEP PRESSURE" escondido atrás de um véu, ainda subindo; quando a cafeína sai, o véu cai e o medidor aparece cheio (tremida leve).
12. `timeline` horizontal 14h → 24h — curva de cafeína no sangue caindo pela metade a cada ~5 h; marcador "BEDTIME" ainda com metade/um quarto. Rodapé: "NIH/NCBI · IOM 2001".
13. `fact_card` — "400 mg / day" com "FDA: amount not generally linked to harmful effects in most healthy adults"; rodapé "FDA Consumer Update".
14. Transição — o receptor travado vira, num morph, uma fábrica (engrenagem) soltando sinais; texto "BLOCK A RECEPTOR → STOP THE SIGNAL BEING MADE?".

## Ibuprofen: Cutting the Alarm Wire
15. `chapter_card` "02 · IBUPROFEN · cuts the alarm wire" + `timeline` curta: 1899 (frasco de aspirina antigo, genérico) → 1971 ("JOHN VANE: HOW IT WORKS"); contador de anos "72".
16. `body_map` — tornozelo acende em vermelho; zoom (`focus`) até células; uma molécula longa (ácido graxo) entra numa enzima-máquina rotulada "CYCLOOXYGENASE" e sai como pequenas sirenes "PROSTAGLANDINS".
17. `organ_focus` (tornozelo/tecido) — sirenes se espalham, a área incha e avermelha; nervo de dor brilha mais forte; `meter` "PAIN SENSITIVITY" sobe.
18. `organ_focus` (cérebro, hipotálamo) — prostaglandinas chegam; termômetro holograma sobe de 37 para 38,5 °C (só ilustrativo, sem número falado).
19. `molecule_dock` adaptado — a molécula de ibuprofeno entra no "bolso" da enzima; a esteira de produção para (`hold` com sinal de bloqueio); três `meter` pequenos descem: PAIN, SWELLING, FEVER.
20. `timeline` — concentração de ibuprofeno no sangue caindo pela metade em ~2 h; o tornozelo continua torcido (ícone de lesão ainda lá, alarme baixo).
21. Duas enzimas lado a lado: "COX-1" (escudo sobre a parede do estômago) e "COX-2" (sirene na inflamação).
22. `organ_focus` (estômago) — ibuprofeno bloqueia as duas; o escudo do estômago afina e aparece uma pequena erosão (sem sangue explícito, só área magenta).
23. `fact_card` — "FDA WARNING: heart attack & stroke risk ↑ with higher dose and longer use"; rodapé "FDA Drug Safety Communication, 2015".
24. Transição — chave quebrando/sumindo de um chaveiro; texto "WHAT IF THE KEY IS MISSING?".

## Insulin: Replacing a Lost Key
25. `chapter_card` "03 · INSULIN · replaces a lost key" + `timeline` "JAN 1922 · TORONTO"; silhueta genérica de um menino num leito (sem rosto real, ou foto de arquivo de domínio público com crédito).
26. `fact_card` — "BEFORE 1922: TYPE 1 DIABETES = FATAL"; frasco de vidro de extrato; `meter` "BLOOD SUGAR" descendo depois do 23 de janeiro.
27. `quote_card`/`fact_card` — "NOBEL PRIZE 1923 · Banting & Macleod · 'for the discovery of insulin'"; rodapé "nobelprize.org".
28. `body_map` → `organ_focus` (pâncreas) — açúcar (pontos âmbar) entra no sangue; células beta acendem e soltam insulina (pontos ciano) — igual à cena aprovada do Mounjaro.
29. `molecule_dock` em célula muscular — insulina encaixa; portinhas (transportadores) sobem do interior para a membrana; açúcar entra; `meter` "BLOOD SUGAR" desce.
30. `organ_focus` (pâncreas) — células imunes (pontos magenta) atacam as células beta, que apagam uma a uma; o açúcar se acumula no vaso (`flow_valve` entupindo).
31. Frasco genérico de insulina + estômago-holograma "digerindo" uma molécula de proteína (corrente de contas se partindo); seta "INJECTED, NOT SWALLOWED".
32. `molecule_build` adaptado — bactéria holograma com um gene humano destacado produzindo cadeias A e B que se juntam; `timeline` "1982 · FIRST RECOMBINANT DRUG APPROVED BY FDA".
33. `meter` "BLOOD SUGAR" com faixa segura no meio e zona vermelha embaixo; o ponteiro passa da faixa e volta; ícone de médico/estetoscópio.
34. Transição — a chave ciano da insulina vira, com efeito de "falsificação", uma chave magenta com selo; texto "FORGE THE MESSAGE".

## Mounjaro: The Forged Message
35. `chapter_card` "04 · MOUNJARO · forges a message" → `body_map` do intestino acendendo; dois mensageiros saem: "GLP-1" e "GIP".
36. `organ_focus` (pâncreas) recebendo os mensageiros + `counter` "≈ 2 MIN" (meia-vida do GLP-1 natural), com tesouras (enzima) picotando os mensageiros.
37. `molecule_build` — metade ciano (GLP-1) + metade magenta (GIP) se juntam numa molécula só: "TIRZEPATIDE".
38. `molecule_build` (`tail_at`, `ride_at`) — a cauda amarela de gordura aparece e gruda numa bola grande "ALBUMIN"; a molécula viaja no vaso.
39. `timeline` semanal (SEG→SEG) — curva de meia-vida de ~5 dias; ícone de uma injeção por semana (caneta genérica, sem logo).
40. `organ_focus` (pâncreas) — insulina sai quando o `meter` de açúcar está alto; glucagon (âmbar) diminui; legenda "GLUCOSE-DEPENDENT".
41. `flow_valve` (estômago) — a válvula fecha e a comida sai mais devagar; depois o cérebro com um medidor "APPETITE" baixando.
42. `bars` — "TIRZEPATIDE 15 mg: −20.9%" vs "PLACEBO: −3.1%" (barras para baixo, `down: true`); rodapé "SURMOUNT-1, NEJM 2022 · 72 weeks · adults with obesity or overweight".
43. `end_card` — "COMMON: nausea, GI side effects" / "BOXED WARNING on label" / "PRESCRIPTION ONLY · doctor decides".
44. Transição — a fechadura sai de cena; entra uma folha de papel com uma receita escrita em letras de RNA (A, U, G, C).

## mRNA Vaccines: A Fire Drill for Your Immune System
45. `chapter_card` "05 · mRNA VACCINES · run a fire drill" → células imunes holograma "estudando" um alvo de treino.
46. Simulação de treino: alvo de papelão no formato de vírus; células imunes praticam; legenda "REHEARSAL".
47. Comparação lado a lado: "OLDER VACCINES: the piece itself" (vírus enfraquecido/proteína) vs "mRNA: the recipe" (fita).
48. `molecule_build` adaptado — fita de mRNA é envolta por uma bolha de lipídio ("LIPID NANOPARTICLE") que se funde com a membrana da célula.
49. Ribossomo holograma lendo a fita (cursor andando) e montando a proteína spike conta por conta.
50. A célula mostra a spike na superfície; anticorpos (Y) e células T chegam e "memorizam" o formato; selo "TRAINED".
51. A fita se desfaz em partículas no citoplasma; o núcleo fica intacto, com escudo e rótulo "DNA — NOT ENTERED"; rodapé "CDC".
52. `meter` "INFLAMMATION" alto com RNA comum → troca de uma conta da fita (U → Ψ, destaque) → medidor cai; nomes "Karikó & Weissman".
53. `timeline` "2005: modified RNA paper → 2023: NOBEL PRIZE"; rodapé "nobelprize.org".
54. `end_card` — "Recommendations depend on age & health" / "Ask your doctor".
55. Transição — o escudo imune se afasta e entra uma bactéria com parede em malha brilhante; texto "A LOCK YOU DON'T HAVE".

## Antibiotics: Breaking a Wall You Don't Have
56. `chapter_card` "06 · ANTIBIOTICS · break a wall" + `timeline` "1928 · LONDON"; placa de Petri holograma: mofo verde no centro e um halo vazio de bactérias em volta.
57. `timeline` 1928 → 1940s (Oxford) → 1945 "NOBEL: Fleming, Florey, Chain"; frasco antigo genérico de penicilina.
58. Bactéria em close — parede em malha (peptidoglicano) tipo rede; legenda "PEPTIDOGLYCAN".
59. Enzimas-"costureiras" ligando os fios da malha; a penicilina (formato de chave com anel quadrado) entra na enzima e trava (`hold`).
60. A malha abre buracos; água (partículas azuis) entra; a bactéria incha e estoura (`fog_clear`/`bang` pequeno, sem gore — só partículas).
61. Split screen: célula humana (sem malha) intacta vs bactéria estourando; selo "SELECTIVE TOXICITY".
62. Vírus de gripe holograma ao lado da penicilina: a chave não acha fechadura nenhuma (ícone "NO TARGET").
63. Bactéria mutante soltando tesourinhas (betalactamase) que cortam a penicilina; colônia resistente crescendo com setas.
64. `fact_card` "≈1.27 MILLION deaths directly caused by resistant bacteria (2019)" + mapa-múndi holograma pulsando; rodapé "The Lancet, 2022 (GRAM/IHME)".
65. `end_card` — "Only when prescribed. Exactly as prescribed."

## One Idea, Six Tricks (fechamento)
66. Volta a grade 3×2 do bloco 2: cafeína (cadeado), ibuprofeno (fio cortado), insulina (chave) acendem conforme são citados.
67. Os outros três acendem: Mounjaro (carta com selo + relógio de 5 dias), mRNA (receita), penicilina (parede rachada).
68. As seis cenas se fundem num receptor só; uma chave falsa "escorrega" para um segundo receptor em outro órgão (efeito colateral); legenda "SAME LOCK, MORE THAN ONE PLACE".
69. `outro` — logo Show Your Work + "SUBSCRIBE" discreto + cartão do próximo vídeo; fundo em grade de caderno (identidade do canal), não holograma.
