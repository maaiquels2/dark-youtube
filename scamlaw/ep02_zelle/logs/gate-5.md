# Gate 5 — Montagem e revisão (ep02_zelle) — 02/11/2026

Resultado: PASSA. Aguarda aprovação do Maiquel.

- Render: renders/ep02_zelle.mp4 (1920x1080, 30 fps, 9:05,7, ~1,0 GB) e renders/ep02_zelle_share.mp4 (52 MB). 7 partes, render de 02/11 ~14:45–16:26.
- A ec_lib.jsx foi corrigida pela sessão ec-lib durante o render (tempo com hífen); o render usou o projeto gerado antes da mudança. Um novo `--render` refaria as partes.
- Áudio: remixado com "lufs": -14 (regra universal §7). Medido: −14,0 LUFS integrado, pico −1,5 dBFS. Único silêncio > 1,2 s: a cauda do cartão final (2,5 s).
- Folhas do vídeo final, 1 quadro a cada 6 s (logs/final/sheet_01 a 04.jpg) e último quadro (logs/final/last.jpg): abertos.
  - Nada cortado ou vazando, nenhuma foto trocada, marcador de ato certo em cada capítulo.
  - Trocas de imagem no meio dos blocos longos aparecem (ex.: 0:36 medidor, 1:12 relógio, 3:48 saguão do banco, 7:24 livros, 7:54 teclado).
  - Barras dos bancos entram uma por vez na fala (3:54 vazio, 4:00 só Chase): animação, não erro.
  - Último quadro: SUBSCRIBE e "MORE CASES: THE RULE CHANGED" nítidos; o cartão fica ~8 s.
- Fidelidade da voz: 96,97% (Gate 3).

## Não conferido
- Não assisti em tempo real nem ouvi a mixagem inteira (trilha Interloper, ganho 0,14).
- Sincronia fina fala × entrada de cada cena; clipes Motion a 6 fps.
- final_sweep e palette_check são do Ledger e não leem projetos scamlaw/.
