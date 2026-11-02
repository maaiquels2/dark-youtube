# Gate 5 — Montagem e revisão (ep01_robocalls) — 01/11/2026

Resultado: PASSA. Aguarda aprovação do Maiquel.

- Render: renders/ep01_robocalls.mp4 (1920x1080, 10:34, 1,2 GB) e ep01_robocalls_share.mp4 (66 MB).
  - Houve dois renders ao mesmo tempo. Com OK do Maiquel, encerrei o antigo (de antes das correções) e apaguei as partes 4, 5 e 6 que ele gravou. As 7 partes finais são do render novo (15:13–16:58), feito depois da remontagem do projeto (15:03).
- Áudio:
  - −16,1 LUFS integrado (padrão do ec_lib), pico −3,0 dBFS.
  - Os 3 picos de efeito mais altos ficam +4 dB acima do nível típico da voz (109 s, 165 s, 311 s).
- Narração (tools/asr_local.py, faster-whisper local na GPU): fidelidade 98,2% contra o roteiro.
- Folha de contato do vídeo final, 1 quadro a cada 8 s (logs/final/sheet_01.jpg e sheet_02.jpg), e o último quadro (logs/final/last.jpg): abertos.
  - Nada cortado ou vazando, nenhuma foto trocada.
  - Contadores congelados no meio (22,022, 41.3B, 14.7B) e imagens meio apagadas (2:32, 9:36) são animação e transição.
  - O último quadro mostra SUBSCRIBE e "COMING SOON: THE NEXT CASE" nítidos.

## Não conferido
- Não assisti o vídeo inteiro em tempo real nem ouvi a mixagem (trilha "Interloper" com ganho 0,14).
- Sincronia fina entre a fala e as entradas de cena.
- Kit do YouTube (título, descrição, checklist anti-desmonetização) ainda não foi feito.
- O "next video" do fim é um texto genérico até existir o episódio 2.
