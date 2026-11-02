# Gate 4 — Imagens e cenas (ep02_zelle) — 02/11/2026

Resultado: PASSA.

## Feito
- Executor Sonnet: scenes.json (65 blocos), composições de pessoa e logo (p_chopra, p_james, p_senators, l_banks, l_zelle), crops e marcas dos recortes, quadros de teste. Revisão Opus nas 7 folhas.
- Clipes Motion HyperFrames (Sonnet): `assets/clips/two_transfers.mp4` (11 s, regra autorizado × não autorizado, textos conferidos na Reg E 1005.2(m), 1005.6, 1005.11) e `money_path.mp4` (9 s, textos do FAQ do Zelle). 1920x1080, 30 fps, paleta e fontes do canal.
- 26 reconstruções FLUX locais (sem rosto, texto ou logo); uma refeita porque mostrava o rosto de perfil.
- Modelos usados: intro, chapter_card 6, fact_card, impact_title, organ_focus, web_clip 9 (CFPB 2, NY AG, eCFR, Cornell, PSR 2, FTC, GovInfo), us_map (NY), clip 3, bars 2, timeline, quote_card, end_card, lower_third, outro.
- Build: nenhum aviso (palavra, fora da tela, 0,3 s, mapa).

## Correções da revisão Opus
- 13 blocos tinham uma só foto por 8,4 a 11,3 s (regra: nenhum trecho parado > 8 s). Cada um troca de imagem no meio do bloco; os logos (27) e a foto dos senadores (49) ficam até o fim dos nomes falados. Cópia: scenes.json.bak-troca-8s.
- Crédito da foto da Letitia James (CC BY 2.0) na tela, no lower-third do bloco 32.
- Capa e cena com o celular gerado: na capa a foto foi desfocada (o app falso mostrava "73").

## Fatia de tempo (do executor, antes da troca; a troca não muda os tipos)
- Imagem com zoom 31,3%; cartões e títulos 41,6%; recortes 15,7%; mapa, gráfico e linha do tempo 6,3%; clipes 5,1%.
- Imagem parada ≤ 45%. Depois da troca, nenhum plano de foto passa de ~7,4 s.

## Desvios aceitos
- Bloco 46: barras na ordem falada (88% depois 66%), 88% em verde, 66% em cinza.
- Bloco 37 (99,95% do Zelle): traço quase branco, nem vermelho nem verde (afirmação do Zelle).
- Bloco 27: logos em cartão de papel sobre grafite, com a base escura para a legenda.
- A tela mostra "CONED BILLING" (grafia do processo); a voz diz "Con Ed Billing" (para a Kokoro pronunciar certo).

## Não conferido
- Clipes Motion só por folha a 1 fps (não a 6 fps).
- Foto da Letitia James é de 2013, com letras soltas de cartaz ao fundo.
- Recortes eCFR (18), PS24/7 (41) e GovInfo (50) ficam com letra pequena no celular; legíveis em 1080p.
- Bug da ec_lib (não mexi): "palavra-com-hífen-0.2" dá "tempo invalido". Avisar a sessão ec-lib.
