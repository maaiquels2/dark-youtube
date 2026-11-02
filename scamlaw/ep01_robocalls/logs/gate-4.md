# Gate 4 — Imagens e cenas (ep01_robocalls) — 01/11/2026

Resultado: PASSA.

## Feito por agente Sonnet; revisão Opus
- 34 imagens em assets/img:
  - Reconstruções FLUX locais, sem rosto de pessoa real e sem texto gerado.
  - Fotos oficiais em domínio público: Pai, O'Rielly, Thune, Blumenthal, Pallone.
  - Selos FCC e FTC; grade de marcas (TripAdvisor, Expedia, Marriott e a palavra HILTON).
  - Cartão com monograma para Abramovich (sem foto livre).
- scenes.json com 75 blocos:
  - fact_card 12, impact_title 15, organ_focus 26, chapter_card 5, bars 5, end_card 5, timeline 3, meter 1, quote_card 1, intro 1, outro 1, lower_third 31.
  - Música: interloper.mp3, ganho 0,14.
- Fatia de tempo: painéis de imagem com zoom centrado 37% (235 s de 632 s); modelos animados ~63%.

## Revisão Opus
- Rodada 1: abri as folhas 01 a 06 e pedi 8 correções.
  - "%" no gráfico em bilhões e "1 YEARS".
  - Logos cobrindo o título e Hilton cortada.
  - Nome do Abramovich cortado e monograma atrás da citação.
  - "task force" na tela.
  - Rótulos de fonte e fim do vídeo.
- Rodada 2: o agente abriu as folhas 01 a 07. Conferi eu mesmo os quadros 62, 88, 267, 361, 423, 533 e 634,1 s: tudo corrigido.
  - O "3" em 361 s é o contador no meio da animação; ele vai até 4.
  - O SUBSCRIBE e "COMING SOON: THE NEXT CASE" aparecem nítidos no último quadro.

## Não conferido
- Só quadros parados: não vi a animação contínua nem a sincronia fina com a fala.
- Não ouvi a mixagem.
- Foto do Blumenthal um pouco macia (original de 791x1002).
- O qa_gate e o final_sweep são do pipeline do Ledger (projects/*.json) e não se aplicam a projetos ec_lib. Depois do render: folha de contato a 2 quadros/s e picos de áudio.
