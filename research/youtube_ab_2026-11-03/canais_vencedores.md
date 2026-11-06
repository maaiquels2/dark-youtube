# Canais vencedores nos 4 nichos (YouTube Data API v3, 03/11/2026)

Pesquisa somente leitura. Todos os números vêm da YouTube Data API v3, coletados em 03/11/2026. Views/dia = views ÷ dias desde a publicação (mínimo 1 dia). Views/inscritos = views do vídeo ÷ inscritos atuais do canal.

## Método e limites (ler antes das tabelas)
- **Descoberta:** 37 buscas `search.list` (ordem por views, publicados desde 05/08/2026, `relevanceLanguage=en`, `regionCode=US`), com 7 a 10 consultas por nicho. O nicho C e parte do B e do D usaram `videoDuration=short`. Saíram 1.688 vídeos únicos e os canais deles (`dados_A.csv` … `dados_D.csv`).
- **Escolha dos canais:** feita à mão, por relevância ao nicho, entre os que cumprem pelo menos um critério: canal com ≤ 548 dias (18 meses), vídeo ≥ 3x os inscritos, ou poucos vídeos com muitas views. Para cada canal escolhido baixei os **últimos 50 uploads** (`playlistItems` + `videos.list`), para medir o canal todo e não só o vídeo achado na busca.
- **Vencedores:** 11 ou 12 vídeos por nicho, publicados nos últimos 90 dias, no máximo 2 por canal e sempre no tema (excluí vídeos fora do nicho de canais mistos, como os Shorts de joias e espaço do Mason Mignanelli ou os de curiosidade do Ricks Clips).
- **Amostra pequena:** são cerca de 11 vídeos e 10 canais por nicho, o que mostra tendência mas não prova nada. A busca por views favorece quem já é grande. Os vídeos de 1 a 2 dias têm views/dia inflado (Mike Rafi, Night Drive Thoughts, Tale Time66).
- **Capas de Shorts:** a API devolve um **quadro do vídeo**, não a capa escolhida no Studio. Por isso, nas folhas C e D (e nos Shorts do B), o que se analisa é o quadro de abertura.
- **Fora da lista:** Podclips1, porque o vídeo de 1,38 M achado na busca ficou fora dos últimos 50 uploads e a mediana recente é de 252 views. Gigantes como Zack D. Films (29,5 M inscritos) e fern entram só como referência.
- **Cota usada:** **3.929 unidades** (37 search = 3.700; 117 videos.list; 30 channels.list; 82 playlistItems). Umas 83 unidades se perderam porque um script falhou e teve de rodar de novo.

Arquivos: dados brutos em `raw/`, scripts em `scripts/`, capas em `thumbs/` e folhas de contato `contato_A.jpg` … `contato_D.jpg`, todos em `D:\DarkYouTube\research\youtube_ab_2026-11-03\`.

**Nichos:** A = escândalos e colapsos financeiros (The Cracked Ledger) · B = leis que mudaram, golpes e direito do consumidor (The Rule Changed) · C = Shorts de how it works, engenharia e enigmas (Show Your Work) · D = avô, idosos e histórias de vida (Grandpa Walt).

## Tabelas

### Nicho A: canais

| Canal | Criado em | Idade (dias) | Inscritos | Vídeos | Views totais | Mediana views (últimos 50 uploads) | Shorts na amostra | Uploads ≤90 d | Vídeos ≤90 d com ≥3x inscritos | Melhor views/dia ≤90 d |
|---|---|---|---|---|---|---|---|---|---|---|
| [OBF](https://www.youtube.com/channel/UCK1XzxcKXB_v_dcw_tflC1A) | 2014-12-06 | 4349 | 741.000 | 166 | 131.742.441 | 310.158 | 4/50 | 12 | 1 | 408.276 |
| [Mason Mignanelli](https://www.youtube.com/channel/UCDz2F9qBLuUpI7ZIIcxEAEg) | 2026-02-05 | 271 | 210.000 | 131 | 154.705.896 | 358.840 | 49/50 | 29 | 8 | 108.761 |
| [Damon Cassidy](https://www.youtube.com/channel/UCvBy3qcISSOcrbqPhqmG4Xw) | 2022-12-05 | 1429 | 339.000 | 171 | 46.325.143 | 362.517 | 0/50 | 8 | 2 | 80.565 |
| [Bagholder Association](https://www.youtube.com/channel/UCaMJ003hQXcETQIs2_ppVLQ) | 2026-05-18 | 169 | 10.200 | 55 | 7.690.529 | 49.421 | 1/50 | 40 | 30 | 25.421 |
| [Paul McAllister](https://www.youtube.com/channel/UCdKg7c7M8mpavVhr0jIrsGg) | 2024-11-19 | 714 | 119.000 | 400 | 40.831.822 | 33.780 | 0/50 | 50 | 2 | 23.262 |
| [The American Shoe Archive](https://www.youtube.com/channel/UC9eHJgqXkFDf1sgb51xTyTw) | 2026-08-31 | 63 | 3.370 | 60 | 980.033 | 968 | 0/50 | 50 | 11 | 18.562 |
| [Old Glory Iron](https://www.youtube.com/channel/UCIG0iylwBroJOiY2uwA3pmQ) | 2026-05-07 | 179 | 2.590 | 88 | 1.653.359 | 10.802 | 1/50 | 46 | 28 | 18.198 |
| [Old American Empires](https://www.youtube.com/channel/UCHCHcGMkCZt0TbchB5umlnA) | 2026-07-10 | 115 | 6.520 | 80 | 2.462.012 | 10.005 | 0/50 | 50 | 18 | 8.387 |
| [Persimmon Archive](https://www.youtube.com/channel/UCY-irETA7i1cuKPg2_XNTyg) | 2026-07-05 | 120 | 4.080 | 56 | 1.872.196 | 9.060 | 1/50 | 43 | 19 | 7.854 |
| [ALPHA DECODES](https://www.youtube.com/channel/UCZgo0tAX7oE0Bw-tXN60jyQ) | 2026-03-21 | 226 | 15.500 | 24 | 4.410.337 | 94.355 | 3/23 | 4 | 1 | 5.171 |

### Nicho A: vídeos vencedores (últimos 90 dias)

| # | Vídeo | Canal | Data | Duração (s) | Views | Views/dia | Inscritos | Views/inscritos | Views/mediana do canal | Chars título |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [Which Rich Country Goes Bankrupt First?](https://www.youtube.com/watch?v=zhQVjly5Gos) | OBF | 2026-10-13 | 1055 | 8.600.152 | 408.276 | 741.000 | 11.61x | 27.73x | 39 |
| 2 | [The (Overdue) Collapse Of The AI Bubble](https://www.youtube.com/watch?v=XEMvG2vulKg) | Damon Cassidy | 2026-10-07 | 1416 | 2.212.651 | 80.565 | 339.000 | 6.53x | 6.1x | 39 |
| 3 | [America Can't Go Bankrupt. Here's What Happens Instead](https://www.youtube.com/watch?v=FVxmNVMSAhU) | OBF | 2026-10-16 | 1100 | 974.226 | 54.119 | 741.000 | 1.31x | 3.14x | 54 |
| 4 | [De Beers: The Death of the Diamond Empire](https://www.youtube.com/watch?v=1-vw4UPDgU8) | Mason Mignanelli | 2026-08-26 | 1272 | 2.045.279 | 29.442 | 210.000 | 9.74x | 5.7x | 41 |
| 5 | [Pepsi Is (Finally) Getting What They Deserve…](https://www.youtube.com/watch?v=3Hp03-lSQRw) | Bagholder Association | 2026-09-12 | 1012 | 1.318.220 | 25.421 | 10.200 | 129.24x | 26.67x | 45 |
| 6 | [Gillette Is (Finally) Getting What They Deserve...](https://www.youtube.com/watch?v=Stz7bzbHRV4) | Bagholder Association | 2026-10-08 | 1104 | 620.254 | 23.975 | 10.200 | 60.81x | 12.55x | 50 |
| 7 | [What Happened to Eastbay? The Sneaker Catalog Foot Locker Shut Down After Four Decades](https://www.youtube.com/watch?v=fycTftKbOTA) | The American Shoe Archive | 2026-10-11 | 2408 | 423.752 | 18.562 | 3.370 | 125.74x | 437.53x | 86 |
| 8 | [The Rise and Fall of Harvestore: The Blue Silo Every Farmer Wanted](https://www.youtube.com/watch?v=PZ-DYHQMYsY) | Old Glory Iron | 2026-10-10 | 1517 | 431.433 | 18.198 | 2.590 | 166.58x | 39.94x | 66 |
| 9 | [Why America Stopped Shopping at Kmart](https://www.youtube.com/watch?v=zqFOMrzSr9g) | Paul McAllister | 2026-10-15 | 3245 | 329.266 | 17.292 | 119.000 | 2.77x | 9.75x | 37 |
| 10 | [What Happened to Mizuno? The Irons Tiger Won the Masters With While Titleist Paid $20 Million](https://www.youtube.com/watch?v=AtTZ2j9dWeg) | Persimmon Archive | 2026-10-16 | 1528 | 140.390 | 7.854 | 4.080 | 34.41x | 15.5x | 93 |
| 11 | [How One Fraud Destroyed New York's Biggest Electronics Chain: Crazy Eddie](https://www.youtube.com/watch?v=hYSm3KuL5HE) | Old American Empires | 2026-10-05 | 2078 | 205.311 | 7.162 | 6.520 | 31.49x | 20.52x | 73 |
| 12 | [$4.5 Billion Stolen / The Biggest Financial Scandal](https://www.youtube.com/watch?v=SIgfV-qz06o) | ALPHA DECODES | 2026-08-11 | 2239 | 433.155 | 5.171 | 15.500 | 27.95x | 4.59x | 51 |

### Nicho B: canais

| Canal | Criado em | Idade (dias) | Inscritos | Vídeos | Views totais | Mediana views (últimos 50 uploads) | Shorts na amostra | Uploads ≤90 d | Vídeos ≤90 d com ≥3x inscritos | Melhor views/dia ≤90 d |
|---|---|---|---|---|---|---|---|---|---|---|
| [Ricks Clips](https://www.youtube.com/channel/UC_VeFWlNnRIg558hAeIpJ4w) | 2025-08-26 | 433 | 136.000 | 146 | 366.813.988 | 988.898 | 50/50 | 24 | 22 | 7.291.066 |
| [Mike Rafi - Personal Injury Attorney](https://www.youtube.com/channel/UC04RYGK0kWq2GJH7uKuvdFg) | 2015-12-25 | 3965 | 1.010.000 | 1481 | 2.249.185.068 | 1.795.537 | 50/50 | 50 | 10 | 1.031.142 |
| [Frank USA](https://www.youtube.com/channel/UCWahu7-uoeJpMjPyCk21Wxw) | 2025-10-07 | 391 | 116.000 | 218 | 11.944.303 | 7.822 | 12/50 | 50 | 1 | 94.669 |
| [Jonathan Funk, RSSA® | Social Security Expert](https://www.youtube.com/channel/UCzYtu-Ru3MyTFrjM9SalqNA) | 2021-10-01 | 1859 | 4.670 | 18 | 972.566 | 512 | 0/18 | 6 | 2 | 21.806 |
| [Better Call Kal](https://www.youtube.com/channel/UCdTAA3TxJBMI4AjM33WpPSA) | 2023-07-04 | 1218 | 44.800 | 96 | 3.185.247 | 1.880 | 1/50 | 6 | 3 | 19.499 |
| [Penguin History](https://www.youtube.com/channel/UCOS34vlQabZvm53dzHMr8hA) | 2014-06-18 | 4520 | 318.000 | 62 | 46.202.244 | 40.500 | 40/50 | 2 | 1 | 15.690 |
| [VAR Exposed TV](https://www.youtube.com/channel/UCQfMOCSfBdCIWx3JFzJKtiA) | 2024-10-05 | 759 | 4.980 | 46 | 1.796.644 | 18.952 | 0/46 | 46 | 25 | 15.062 |
| [David Grant](https://www.youtube.com/channel/UCHrmtG8qEjDdz8eBckxO_4g) | 2026-08-18 | 77 | 8.670 | 40 | 1.555.774 | 765 | 0/40 | 40 | 4 | 14.172 |
| [The Texas Retiree](https://www.youtube.com/channel/UCFAkyyGi9HVs9I0bcqf8KQA) | 2026-06-18 | 137 | 9.720 | 45 | 2.039.897 | 15.055 | 1/45 | 30 | 15 | 12.752 |
| [Noah Tech](https://www.youtube.com/channel/UCTiJrl2XQu0XrRherUPke6w) | 2026-10-13 | 21 | 1.090 | 13 | 157.803 | 3.154 | 0/14 | 14 | 7 | 9.258 |

### Nicho B: vídeos vencedores (últimos 90 dias)

| # | Vídeo | Canal | Data | Duração (s) | Views | Views/dia | Inscritos | Views/inscritos | Views/mediana do canal | Chars título |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [A Judge Jailed Two Kids](https://www.youtube.com/watch?v=LBwJ14rnS9E) | Mike Rafi - Personal Injury Attorney | 2026-11-02 | 123 | 1.031.142 | 1.031.142 | 1.010.000 | 1.02x | 0.57x | 23 |
| 2 | [The Window That Breaks Japan's Gambling Law](https://www.youtube.com/watch?v=eQR3pgMiUF0) | Ricks Clips | 2026-10-15 | 46 | 13.593.098 | 727.542 | 136.000 | 99.95x | 13.75x | 43 |
| 3 | [The Roller Coaster Loophole](https://www.youtube.com/watch?v=1pTBLKdOijA) | Mike Rafi - Personal Injury Attorney | 2026-10-14 | 108 | 3.496.085 | 174.902 | 1.010.000 | 3.46x | 1.95x | 27 |
| 4 | [🌟️️️️️️ New I-95 and Highway Rules Begin NOW — Millions of Drivers Could Be Hit With Instant Fines!](https://www.youtube.com/watch?v=ObrbEBbHX0k) | Frank USA | 2026-10-21 | 623 | 1.233.029 | 94.669 | 116.000 | 10.63x | 157.65x | 99 |
| 5 | [Full Social Security at 60? New Bill Explained.](https://www.youtube.com/watch?v=uQB9hVNXvLo) | Jonathan Funk, RSSA® | Social Security Expert | 2026-09-26 | 423 | 837.997 | 21.806 | 4.670 | 179.44x | 1638.31x | 47 |
| 6 | [The Trillion Dollar Scam](https://www.youtube.com/watch?v=gkqQe0qp3SM) | Penguin History | 2026-08-22 | 646 | 1.145.375 | 15.690 | 318.000 | 3.6x | 28.28x | 24 |
| 7 | [Scammers Target a 100-Year-Old for $10,000 — But Police Are Already Inside Her Home](https://www.youtube.com/watch?v=PgSAg9HAoec) | VAR Exposed TV | 2026-10-10 | 1905 | 361.571 | 15.062 | 4.980 | 72.6x | 19.08x | 83 |
| 8 | [Massive UK Parking Law Changes Just Dropped! — IMMEDIATE FINES!](https://www.youtube.com/watch?v=5SI7rzF8TII) | Better Call Kal | 2026-08-23 | 829 | 1.041.472 | 14.515 | 44.800 | 23.25x | 554.12x | 63 |
| 9 | [New Laws Start OCTOBER 1st — Is Your State on the List? (Share With Family!)](https://www.youtube.com/watch?v=uuPrcgwt6xg) | David Grant | 2026-09-23 | 862 | 582.825 | 14.172 | 8.670 | 67.22x | 761.86x | 76 |
| 10 | [16 Things ELDERLY Drivers Don’t Know Are ILLEGAL in Australia (2026–2027)](https://www.youtube.com/watch?v=HhGThyikhxs) | Noah Tech | 2026-11-02 | 962 | 11.183 | 9.258 | 1.090 | 10.26x | 3.55x | 73 |
| 11 | [These 12 New Texas Laws Are Insane (In A GOOD Way)!](https://www.youtube.com/watch?v=zVaIaqRxEyw) | The Texas Retiree | 2026-10-05 | 1778 | 195.951 | 6.836 | 9.720 | 20.16x | 13.02x | 51 |

### Nicho C: canais

| Canal | Criado em | Idade (dias) | Inscritos | Vídeos | Views totais | Mediana views (últimos 50 uploads) | Shorts na amostra | Uploads ≤90 d | Vídeos ≤90 d com ≥3x inscritos | Melhor views/dia ≤90 d |
|---|---|---|---|---|---|---|---|---|---|---|
| [Zack D. Films](https://www.youtube.com/channel/UCvz84_Q0BbvZThy75mbd-Dg) | 2021-06-07 | 1974 | 29.500.000 | 4168 | 82.175.332.073 | 7.867.392 | 50/50 | 50 | 0 | 11.307.021 |
| [OddFrame](https://www.youtube.com/channel/UC87Re_9sXZzkbVJm41Hs_zQ) | 2025-11-09 | 359 | 180.000 | 60 | 250.454.836 | 1.836.572 | 49/50 | 50 | 36 | 1.632.528 |
| [Things Opened](https://www.youtube.com/channel/UCIF5FWPogXDvzpKAInS2eLA) | 2026-10-15 | 18 | 19.600 | 48 | 16.421.152 | 33.986 | 48/48 | 48 | 17 | 566.177 |
| [Inside Machines-TK](https://www.youtube.com/channel/UCbK3I-X6f7WQrQ0fOfX0qFw) | 2026-08-27 | 68 | 6.180 | 168 | 4.869.535 | 3.844 | 49/50 | 50 | 7 | 166.766 |
| [How Things Work](https://www.youtube.com/channel/UCKkvTzcxADWP9flCTnOAkAA) | 2026-09-17 | 47 | 5.570 | 27 | 4.620.676 | 1.809 | 27/27 | 27 | 1 | 144.747 |
| [LeauFilms](https://www.youtube.com/channel/UC-omXnvBb7pdgNhfGM6gWrA) | 2026-04-09 | 207 | 84.600 | 68 | 10.093.141 | 42.958 | 50/50 | 35 | 6 | 143.658 |
| [Made Ordinary](https://www.youtube.com/channel/UCSZF1m2BcjouqEj7t36LErg) | 2026-10-01 | 32 | 3.570 | 70 | 5.091.639 | 5.720 | 41/50 | 50 | 16 | 136.003 |
| [You Built A...](https://www.youtube.com/channel/UCrzEugGqfsfHTdq-IM910KA) | 2026-10-18 | 16 | 8.970 | 17 | 4.296.593 | 183.654 | 17/17 | 17 | 15 | 130.410 |
| [GYMM-MC](https://www.youtube.com/channel/UCKZnzKNc8SJcy2qquaR5FOA) | 2026-06-10 | 146 | 26.300 | 74 | 18.719.160 | 24.262 | 50/50 | 50 | 11 | 96.275 |
| [Torque & Theory](https://www.youtube.com/channel/UC1XojYfY_7EMZiqgzRIwljg) | 2026-08-10 | 84 | 7.600 | 78 | 3.669.832 | 7.088 | 50/50 | 50 | 7 | 10.962 |
| [Knowhow](https://www.youtube.com/channel/UCMCRfQwGDPDaSjTGfhsVfaA) | 2026-08-21 | 74 | 20.700 | 180 | 6.570.819 | 1.412 | 34/50 | 50 | 1 | 5.585 |

### Nicho C: vídeos vencedores (últimos 90 dias)

| # | Vídeo | Canal | Data | Duração (s) | Views | Views/dia | Inscritos | Views/inscritos | Views/mediana do canal | Chars título |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [Why Dobermans Have Cropped Ears 😞](https://www.youtube.com/watch?v=gyOZv_ckZQU) | Zack D. Films | 2026-10-30 | 32 | 40.747.676 | 11.307.021 | 29.500.000 | 1.38x | 5.18x | 33 |
| 2 | [Why Air Force One Never Has to Land #shorts](https://www.youtube.com/watch?v=qwwf2Dp-DTw) | OddFrame | 2026-10-10 | 99 | 38.885.993 | 1.632.528 | 180.000 | 216.03x | 21.17x | 43 |
| 3 | [How Does a Helicopter Pilot Eject Without Hitting the Rotor?](https://www.youtube.com/watch?v=w65jbQSq1io) | OddFrame | 2026-10-13 | 88 | 29.596.624 | 1.426.039 | 180.000 | 164.43x | 16.12x | 60 |
| 4 | [How a USB-C Cable Really Works 🔌 #shorts](https://www.youtube.com/watch?v=1Ug_sjO1zrA) | Things Opened | 2026-10-21 | 73 | 7.336.690 | 566.177 | 19.600 | 374.32x | 215.87x | 40 |
| 5 | [How a Hole at the Edge of Town Becomes a Landfill #shorts](https://www.youtube.com/watch?v=--tDx15MD1k) | Things Opened | 2026-10-21 | 71 | 4.015.100 | 300.203 | 19.600 | 204.85x | 118.14x | 57 |
| 6 | [How a Manual Gearbox Works: Clutch and Gear Shift Explained](https://www.youtube.com/watch?v=gmA6wSPwjSQ) | Inside Machines-TK | 2026-10-15 | 11 | 3.127.108 | 166.766 | 6.180 | 506.0x | 813.61x | 59 |
| 7 | [How Drilling Finds Water Underground](https://www.youtube.com/watch?v=QiTdwT9mjpg) | How Things Work | 2026-10-02 | 30 | 4.630.347 | 144.747 | 5.570 | 831.3x | 2559.62x | 36 |
| 8 | [How Does Tesla's Roadster Hang Upside Down?](https://www.youtube.com/watch?v=ejh9GG17mA0) | Made Ordinary | 2026-10-17 | 59 | 2.357.362 | 136.003 | 3.570 | 660.33x | 412.09x | 43 |
| 9 | [How a Sledgehammer Becomes a Building Implosion 💥 #animation #explanation #engineering #howitworks](https://www.youtube.com/watch?v=JakW-D2qSqw) | You Built A... | 2026-11-01 | 121 | 204.512 | 130.410 | 8.970 | 22.8x | 1.11x | 98 |
| 10 | [How do you solve the two guards riddle? 😱...](https://www.youtube.com/watch?v=ahGr0xaEVUg) | GYMM-MC | 2026-10-12 | 63 | 2.140.087 | 96.275 | 26.300 | 81.37x | 88.21x | 44 |
| 11 | [Can You Solve This Impossible Riddle? 🧠](https://www.youtube.com/watch?v=YWbFyy6mHSY) | LeauFilms | 2026-10-28 | 29 | 333.842 | 54.692 | 84.600 | 3.95x | 7.77x | 39 |

### Nicho D: canais

| Canal | Criado em | Idade (dias) | Inscritos | Vídeos | Views totais | Mediana views (últimos 50 uploads) | Shorts na amostra | Uploads ≤90 d | Vídeos ≤90 d com ≥3x inscritos | Melhor views/dia ≤90 d |
|---|---|---|---|---|---|---|---|---|---|---|
| [Nomad Soul Studio](https://www.youtube.com/channel/UCv7UbDGYRcDU7MQrC04YpGQ) | 2025-08-22 | 438 | 80.000 | 104 | 32.523.504 | 281.364 | 50/50 | 50 | 26 | 825.047 |
| [Tale Time66](https://www.youtube.com/channel/UCJbgvbXt3LRtru6z4dUu9gw) | 2019-02-18 | 2814 | 2.850.000 | 581 | 866.467.508 | 5.804 | 38/50 | 50 | 0 | 233.821 |
| [Night Drive Thoughts](https://www.youtube.com/channel/UCcSqXbX1iyKtSRaFTo_wt3w) | 2015-05-30 | 4174 | 21.300 | 450 | 43.309.638 | 80.469 | 50/50 | 50 | 30 | 153.705 |
| [the mind unlocked 🔓](https://www.youtube.com/channel/UCAb66L4CDp3-3LO3gXlArTQ) | 2026-09-10 | 53 | 10.900 | 131 | 8.279.257 | 12.964 | 47/50 | 50 | 12 | 40.466 |
| [Rob Osborne Reports](https://www.youtube.com/channel/UCkQJNU6Ms10OnNM-TIUH7wQ) | 2011-08-29 | 5545 | 891 | 17 | 479.318 | 148 | 8/17 | 14 | 1 | 32.075 |
| [Everydays Dignity](https://www.youtube.com/channel/UCCZp-9dCHCSVjiXQ_2I_IMw) | 2022-09-19 | 1506 | 5.060 | 22 | 1.676.260 | 14.881 | 22/22 | 22 | 11 | 30.752 |
| [Foresight 20-20](https://www.youtube.com/channel/UC3UY7U4Va-tX_6Cc8MDrtPw) | 2026-08-05 | 90 | 28.300 | 125 | 7.399.024 | 4.072 | 36/50 | 50 | 9 | 26.973 |
| [Health Vibe](https://www.youtube.com/channel/UCpqPL7eofzCyiQVbJVYXDqg) | 2024-08-05 | 820 | 72.700 | 233 | 35.744.325 | 2.233 | 21/50 | 24 | 1 | 19.090 |
| [Son Le](https://www.youtube.com/channel/UC1UBxQnINQUu9kZKDANSgRA) | 2025-03-25 | 588 | 3.040 | 63 | 803.951 | 2.892 | 0/50 | 50 | 13 | 17.592 |
| [Podclips1](https://www.youtube.com/channel/UCTgHesiTcGXrk_D7yKa7DKw) | 2026-09-12 | 52 | 2.570 | 66 | 1.428.475 | 252 | 50/50 | 50 | 0 | 215 |

### Nicho D: vídeos vencedores (últimos 90 dias)

| # | Vídeo | Canal | Data | Duração (s) | Views | Views/dia | Inscritos | Views/inscritos | Views/mediana do canal | Chars título |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [He Thought It Was Just a Cheap Silver Locket #inspirational](https://www.youtube.com/watch?v=ZfayyZZ29Yc) | Nomad Soul Studio | 2026-10-30 | 167 | 3.208.266 | 825.047 | 80.000 | 40.1x | 11.4x | 59 |
| 2 | [Grocery CEO Fired a Single Dad for Wanting Thanksgiving Off—By Sunrise, Her Whole Night Crew Quit](https://www.youtube.com/watch?v=RWw_xsonAR4) | Tale Time66 | 2026-11-02 | 1638 | 233.821 | 233.821 | 2.850.000 | 0.08x | 40.29x | 97 |
| 3 | [Do Not Look Into Other People's Homes In Old Age #shorts #wisdom #oldage](https://www.youtube.com/watch?v=DcLfSIcbeT8) | Night Drive Thoughts | 2026-11-02 | 11 | 153.705 | 153.705 | 21.300 | 7.22x | 1.91x | 72 |
| 4 | [A Manager Humiliated an Old Farmer Over $8.50—Until the Owner Saw the Hinge #emotionalstory](https://www.youtube.com/watch?v=i1S7HJTPaY4) | Nomad Soul Studio | 2026-10-31 | 179 | 349.861 | 135.259 | 80.000 | 4.37x | 1.24x | 91 |
| 5 | [Foolish Mistakes People Make In Old Age #shorts #oldage #lifelessons #mindfulness](https://www.youtube.com/watch?v=b98ZBMjPkwE) | Night Drive Thoughts | 2026-10-31 | 11 | 308.670 | 111.407 | 21.300 | 14.49x | 3.84x | 81 |
| 6 | [Life Lessons From a 107-Year-Old (Born 1919)](https://www.youtube.com/watch?v=GsFAL6-2akA) | Rob Osborne Reports | 2026-10-19 | 848 | 488.020 | 32.075 | 891 | 547.72x | 3297.43x | 44 |
| 7 | [The Doorman Told the Old Man His Violin Was Firewood… Until the Conductor Opened the Case #shorts](https://www.youtube.com/watch?v=p32tBCJ2fGk) | Everydays Dignity | 2026-10-13 | 176 | 646.288 | 30.752 | 5.060 | 127.72x | 43.43x | 97 |
| 8 | [5 Habits of People Who Age Fast and Die Early](https://www.youtube.com/watch?v=Y1LbT8mR7ps) | Foresight 20-20 | 2026-10-24 | 120 | 265.233 | 26.973 | 28.300 | 9.37x | 65.13x | 45 |
| 9 | [13 Ugly Habits in Old Age That Make People Avoid You (But They Are Afraid to Tell You)](https://www.youtube.com/watch?v=71sPZwVD3Fg) | Health Vibe | 2026-09-24 | 645 | 763.449 | 19.090 | 72.700 | 10.5x | 341.89x | 86 |
| 10 | [My Billionaire Grandfather Left Me Just $2—Then the Bank Manager Turned Pale](https://www.youtube.com/watch?v=wqcLSSa8C_M) | Son Le | 2026-10-13 | 2304 | 368.880 | 17.592 | 3.040 | 121.34x | 127.53x | 76 |
| 11 | [7 Powerful Life Lessons My Grandpa Taught Me ❤️ / Life Advice #Shorts #lifestrategies #lifedecisions](https://www.youtube.com/watch?v=y-onkwEvqwA) | the mind unlocked 🔓 | 2026-10-24 | 14 | 142.265 | 14.360 | 10.900 | 13.05x | 10.97x | 100 |

## Padrões de capa por nicho (lidos nas folhas de contato)

### A: colapsos e escândalos (contato_A.jpg, 12 capas, todas de vídeo longo)
- **Elementos:** 1 a 3. Um objeto ou marca no centro (garrafa de Pepsi, aparelho Gillette, anel sem a pedra, silo, fachada da Kmart ou da Crazy Eddie) mais um gráfico ou seta. O mapa com o país em destaque aparece em 2 de 12 (OBF).
- **Rosto:** em 4 de 12, sempre de executivo ou testemunha mais velha, com cara de ilustração ou IA (Eastbay, Harvestore, Mizuno, ALPHA DECODES). Os 3 primeiros em views/dia não têm rosto.
- **Palavras na capa:** de 0 a 5. Exemplos: "It's starting.", "They pay.", "THEY'RE DONE", "Diamonds aren't forever.", "NOBODY BUYS", "BLUE LIE", "EASTBAY / CATALOG GONE", "THE RISE AND FALL OF KMART". A frase da capa **não repete o título**: completa o título.
- **Cores e contraste:** fundo escuro (preto, azul-noite) com vermelho e amarelo, ou papel quadriculado claro com seta vermelha (Bagholder). Contraste alto em todas.
- **Setas e círculos:** seta vermelha para baixo em 4 de 12; seta amarela para cima em 1; elipse ou círculo amarelo em 2 (OBF, Harvestore). A linha verde subindo e depois a vermelha caindo faz o **antes/depois** num quadro só (Pepsi, Gillette).
- **Modelo de série:** a Bagholder Association usa o mesmo layout em todo vídeo ("NOBODY BUYS" + produto + gráfico) e tem 30 de 40 uploads recentes acima de 3x os inscritos. Os canais novos de "o que aconteceu com a marca X" (Old American Empires, American Shoe Archive, Persimmon Archive, Old Glory Iron) usam cena nostálgica realista com o logo da marca.

### B: leis, regras e golpes (contato_B.jpg, 11 capas)
- **Elementos:** 3 a 5 nas capas de vídeo longo (rosto, objeto oficial e selo de alerta). Os Shorts mostram o quadro do vídeo: advogado de terno à mesa com legenda (Mike Rafi) ou desenho 2D (Ricks Clips).
- **Rosto:** em 6 de 11. Político conhecido em 2 (Trump); apresentador apontando ou de braços cruzados em 2 (Better Call Kal, Noah Tech); idosa vítima em 1 (VAR Exposed).
- **Palavras na capa:** muitas, de 3 a 8, em CAIXA ALTA amarela ou branca sobre faixa vermelha ou preta: "NEW I-95 AND HIGHWAY RULES BEGIN TOMORROW", "FULL BENEFITS AT AGE 60? NO REDUCTION!", "NOW ILLEGAL!", "NEW LAWS JUST PASSED!", "STOP PARKING LIKE THIS!".
- **Sinais de urgência:** selos "BREAKING NEWS", "EMERGENCY ALERT" e "NEW", valor da multa num selo ("FINE UP TO A$2,200"), ícone de alerta. Há seta curva em 1 (I-95) e mapa com o estado brilhando em 1 (Texas). Objeto oficial em 2: cartão do Social Security e uma imitação de post do Trump.
- **Cópia de modelo:** Noah Tech (canal de 21 dias) repete título e capa da Better Call Kal e trocou o Reino Unido pela Austrália. Esse formato se copia de um país para outro.
- **Cuidado:** a capa do David Grant imita um post do Trump. Para nós isso é proibido (imita pessoa real e pode enganar). Ver `CLAUDE_YT_ANTI_DEMONETIZATION.md`.

### C: Shorts de how it works e enigmas (contato_C.jpg, 11 quadros)
- Todos são Shorts, e o que se vê é **o quadro do vídeo**, não a capa.
- **Elementos:** 1 objeto em 3D no centro (avião em raio-X, cadeira de ejeção, cabo USB-C aberto, câmbio transparente, broca entrando no chão). Fundo limpo: grade escura, azul-claro ou paisagem simples.
- **Rosto:** em 0 de 9 no how it works. Os enigmas usam personagem (boneco de Roblox, recorte de filme).
- **Texto:** de 0 a 4 palavras. Rótulo pequeno em minúsculas numa etiqueta preta ("e-marker.", "liner.") ou legenda curta embaixo ("pushes from below"). Só 2 de 11 têm manchete grande no quadro: "WHERE IS THE WATER?" (How Things Work) e "WINGS CAN'T DO THIS" (Made Ordinary).
- **Cores:** escuras e frias (azul e preto) nas de engenharia militar e mecânica; claras e naturais nas de construção.
- **Setas e círculos:** quase nenhum. Seta fina em 1. O corte em raio-X faz o papel da seta.
- **Antes/depois:** está no título, não na imagem ("How a Sledgehammer Becomes a Building Implosion", "How a Rope Over a Branch Became a Tower Crane").

### D: idosos, histórias e conselhos (contato_D.jpg, 11 capas e quadros)
- **Três formatos:**
  - **História curta dramatizada** (Nomad Soul Studio, Everydays Dignity; de 150 a 180 s): close de idoso emocionado, realista e feito com IA, luz quente sobre fundo escuro, uma legenda de fala ("GOD BLESS YOU SON", "I've got eight dollars.").
  - **Cartão de lista** (Night Drive Thoughts, the mind unlocked; de 11 a 15 s): fundo escuro, título em vermelho e amarelo ("DO NOT LOOK INTO OTHER PEOPLE'S HOMES IN OLD AGE") e lista numerada de 6 a 7 itens. O modelo é idêntico em todo vídeo.
  - **Vídeo longo narrado** (Tale Time66, Son Le, Health Vibe): Tale Time66 usa cena de confronto com 3 palavras amarelas ("THEY ALL QUIT"). Son Le escreve na capa o gancho inteiro, umas 55 palavras com trechos coloridos, mais o rosto da protagonista. Health Vibe usa só texto (11 palavras brancas com contorno preto sobre fundo verde desfocado).
- **Rosto:** em 7 de 11, quase sempre de idoso ou de quem foi injustiçado.
- **Número grande:** "107" em amarelo (Rob Osborne) e "13 ugly habits" (Health Vibe).
- **Setas e círculos:** nenhum. O contraste vem da emoção do rosto e do texto.

## Padrões de título por nicho

| Nicho | Títulos | Chars (mín / mediana / máx) | ≤ 60 chars | Pergunta | Número | How… | Why… | What… | Colapso ou queda | Consequência (multa, prisão, perda) | Reviravolta (—, …, Then, Until) | Personagem ou adversário | Emoji |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 12 | 37 / 50,5 / 93 | 8 | 3 | 2 | 1 | 1 | 2 | 5 | 2 | 2 | 0 | 0 |
| B | 11 | 23 / 51 / 99 | 6 | 2 | 6 | 0 | 0 | 0 | 0 | 4 | 4 | 2 | 1 |
| C | 11 | 32 / 43 / 60 | 11 | 4 | 0 | 8 | 2 | 0 | 0 | 0 | 1 | 0 | 5 |
| D | 11 | 39 / 61 / 97 | 5 | 0 | 6 | 0 | 0 | 0 | 0 | 2 | 4 | 4 | 1 |

O comprimento foi contado sem hashtags; a contagem de estruturas foi feita por regex em `scripts/titles.py`.

- **A.** Palavras que se repetem: bankrupt, finally/getting/deserve, happened, biggest, America.
  - Estruturas vencedoras:
    - pergunta de ranking ("Which Rich Country Goes Bankrupt First?", 39 chars, 11,6x os inscritos);
    - "(Overdue)" ou "(Finally)" entre parênteses, que dão julgamento e sensação de "eu avisei";
    - "What Happened to [marca]?" mais o detalhe que dói;
    - "Why Nobody [faz X] [lugar ou marca] Anymore";
    - "How One Fraud Destroyed [empresa]".
  - O título nomeia a marca. O adversário é a própria empresa.
- **B.** Palavras: new, law(s), drivers, fines.
  - Dois estilos opostos dão certo:
    - **Shorts de 2 a 5 palavras** (Mike Rafi: "Self-Defense?", "A Judge Jailed Two Kids", "The Roller Coaster Loophole"; Ricks Clips: "The Window That Breaks Japan's Gambling Law");
    - **título longo de alerta** (80 a 99 chars) com data, público atingido e multa: "New I-95 and Highway Rules Begin NOW — Millions of Drivers Could Be Hit With Instant Fines!".
  - Seis de 11 têm número ou data.
  - O público mais velho aparece muito: Social Security, "ELDERLY Drivers", "(Share With Family!)", The Texas Retiree.
- **C.**
  - Todos ≤ 60 chars, mediana 43.
  - 8 de 11 começam com "How…".
  - Modelos:
    - "How a [coisa comum] Really Works";
    - "How a [coisa simples] Becomes a [coisa enorme]";
    - "Why [fato curioso]".
  - Emoji no fim em 5 de 11.
  - Enigma: "Can You Solve This Impossible Riddle?" e "How do you solve the two guards riddle?" ficaram abaixo dos how it works nesta amostra.
- **D.** Palavras: old, age, people, life, lessons, habits, manager, until.
  - Dois modelos:
    - **lista para a velhice:** "Foolish Mistakes People Make In Old Age", "5 Habits of People Who Age Fast and Die Early", "13 Ugly Habits in Old Age That Make People Avoid You";
    - **história de injustiça com virada:** "[Alguém com poder] Humiliated an Old Farmer Over $8.50—Until the Owner Saw…", em que o "—Until/Then" aparece em 4 de 11.
  - O título de história é longo (mediana 61, até 97 chars) e não cabe inteiro no celular.

**O que se repete entre todos os vencedores:**
1. Uma coisa concreta com nome: marca, lei, objeto ou idade.
2. Uma tensão: queda, multa, injustiça, mistério.
3. Capa que **não repete** o título.
4. Nos canais novos que crescem, um **modelo fixo** de capa e título repetido vídeo após vídeo: Bagholder, Night Drive Thoughts, Better Call Kal/Noah Tech, You Built A…, Things Opened.

## Recomendações para os nossos canais
1. **Ledger: modelos de título de até 60 chars, nomeando a marca.**
   - "What Happened to [Marca]? [detalhe que dói]"
   - "How One Fraud Destroyed [Empresa]"
   - "Why Nobody Buys [Marca] Anymore"
   - "[Marca] Is (Finally) Paying for It"
   - "Which [Bank/Company] Collapses First?"

   Nos vencedores do A, a mediana é de 50,5 chars e 8 de 12 ficam em até 60.
2. **Ledger: capa com 2 a 4 palavras que completam o título.** Exemplos: "THEY'RE DONE", "Diamonds aren't forever.", "NOBODY BUYS". A capa leva 1 objeto ou logo e 1 seta vermelha para baixo ou a linha que sobe e depois cai. Rosto só se for o protagonista real e houver foto livre (regra do canal). Vale fixar **um layout de série**, como faz a Bagholder (30 de 40 uploads recentes acima de 3x os inscritos).
3. **Ledger: testar a série "marca que todo mundo lembrava".** Os canais mais novos do nicho cresceram assim: Old American Empires (115 dias), American Shoe Archive (63 dias), Persimmon Archive (120 dias) e Old Glory Iron (179 dias). Todos tiveram entre 11 e 28 vídeos recentes acima de 3x os inscritos, com cena realista nostálgica e logo. Crazy Eddie, Kmart e Eastbay são exemplos de tema com fraude ou colapso.
4. **Rule Changed, vídeo longo: alerta com data e público.** Modelo de até 60 chars: "New [Driving/Benefit] Rules Start [Data] — Check Yours". Na capa, o objeto oficial (cartão, placa, multa) mais um selo "NEW" ou "NOW ILLEGAL".
   - **Conflito com a regra atual do canal** ("título psicológico, sem números"): 6 de 11 vencedores do B têm número ou data. Sugiro um teste A/B (Test & Compare no Studio). Quem decide é o Maiquel.
5. **Rule Changed, Shorts: o modelo do Mike Rafi e do Ricks Clips.** Título de 2 a 5 palavras: "The [Objeto] Loophole", "The [Objeto] That Breaks [Lei]", "A Judge [verbo] [pessoa]". O Mike Rafi tem mediana de 1,8 M views nos últimos 50 Shorts; a "Window That Breaks Japan's Gambling Law" teve 100x os inscritos.
6. **Rule Changed: mirar o público de 60+.** Social Security, motoristas idosos e "Share With Family!" aparecem em 5 de 11 vencedores. David Grant (77 dias) e The Texas Retiree (137 dias) cresceram com esse público. Nada de imitar post de político ou usar o rosto dele como isca (risco de enganar e de perder a monetização).
7. **SYW How It Works: títulos de 35 a 50 chars começando com "How".** Modelos: "How a [objeto do dia a dia] Really Works" e "How a [coisa simples] Becomes [coisa enorme]", com 1 emoji no fim. Canais de 16 a 68 dias (Things Opened, You Built A…, Made Ordinary, How Things Work, Inside Machines-TK) passaram de 100 mil views/dia num vídeo cada. No quadro 0: o objeto em corte 3D centralizado, fundo limpo e 1 rótulo curto, ou uma pergunta grande como "WHERE IS THE WATER?". Isso confirma a regra do quadro 0 que já temos.
8. **SYW Puzzles:** nesta amostra, os enigmas renderam bem menos que o how it works: o melhor teve 96 mil views/dia, contra 1,6 M do melhor how it works. Vale pôr o enigma dentro de um "how" (por exemplo "How do you solve the two guards riddle?") e usar personagem ou cena no quadro 0.
9. **Walt (FB e IG; o YouTube aqui só serve de termômetro):** dois formatos para testar nos Reels.
   - **Cartão de lista de 10 a 15 s:** "Foolish Mistakes People Make In Old Age", "Do Not ___ In Old Age". A Night Drive Thoughts teve 30 de 50 uploads recentes acima de 3x os inscritos com um modelo idêntico.
   - **História de 150 a 180 s** com virada "—Until…/Then…" e close do idoso. A Nomad Soul Studio tem mediana de 281 mil views nos últimos 50 vídeos.

   O Walt pode ser o narrador: "Grandpa's Rule: …", "The Day a Manager Laughed at Me…".
10. **Comprimento:** quando o título passa de 60 chars (D e B longo), as primeiras 5 a 7 palavras precisam conter o gancho, porque o celular corta o resto.
