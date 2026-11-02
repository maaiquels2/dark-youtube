# Show Your Work Puzzles: identidade do canal

Vale junto com [`REGRAS_UNIVERSAIS.md`](../REGRAS_UNIVERSAIS.md). Escrito em 01/11/2026 a partir das memórias "Terceiro canal: enigmas animados", "Série How It Works no SYW", "Rumo dos canais" e "Roteiro didático, visual adulto".

## Canal
- Enigmas de matemática e física, e a série **How It Works** (corpo, remédios, tecnologia, ciência).
- Inglês. Shorts e Reels verticais de até 90 s, mais 1 longo horizontal no domingo, de 8 a 12 min, sobre o tema da semana.
- **Plataformas** (decisão de 01/11):
  - YouTube Shorts: 1 vídeo por dia, muito bem produzido;
  - volume extra no TikTok, Instagram e Facebook;
  - Reels manuais, com enquete.
- Conta do YouTube: syw.puzzles@gmail.com; canal `UCrgIwaM5dsNRgrKqZkOepRg`; Chrome Profile 6.

## Voz
Kokoro `am_onyx` (local). Episódios antigos usavam ElevenLabs Brian a 1.08; não trocar sem perguntar.

## Visual
- **Puzzles** (`puzzles/_engine`):
  - papel milimetrado, fundo creme `#f4ecd8`, traço `#1c1c1c`, destaque vermelho `#d62828`;
  - paleta própria, nunca o azul blueprint do @mathomaly;
  - área segura do vertical: conteúdo em x 130–950; título em y≈292; legenda em y 1124–1244.
- **How It Works** (`puzzles/ec_lib`): estilo holograma médico, com fundo escuro, ciano/teal, âmbar e magenta, grade e brilho.
  - Esse visual é deste canal e **não** deve ir para o The Rule Changed nem para o Ledger.
  - Outros estilos testados ficam em `puzzles/_styles/`.
  - Visual realista e adulto; desenho infantil foi reprovado em 31/10.
- **Fontes:** Anton (títulos) e Inter (resto), as da `ec_lib` e do `_engine`.
- **Números:** contador animado é parte do estilo deste canal. A entrada N1 sem contador foi aprovada só para o The Rule Changed.

## Estrutura
- **Puzzle (~1:45):**
  - gancho com promessa em 0–5 s;
  - regras;
  - escalada de exemplos;
  - revelação;
  - explicação;
  - fecho que generaliza.
- **How It Works (≤ 90 s):**
  - pergunta no gancho;
  - uma metáfora do começo ao fim;
  - no máximo um termo técnico, explicado na hora;
  - fato com fonte na tela;
  - aviso quando o tema for saúde.

## Música
Suspense ou neutra, nunca cômica (regra universal §7).

## Pipeline
- Motores: `puzzles/_engine/build.py <dir>` e `puzzles/ec_lib` (dona: sessão ec-lib).
- Projetos em `puzzles/<tema>/`.
- Agendas e scripts: `puzzles/youtube_schedule.md`, `yt_schedule.py`, `yt_long.py`, `social_schedule.md`.
- Risco anti-desmonetização MÉDIO (`CLAUDE_YT_ANTI_DEMONETIZATION.md` §4.3): variar o visual entre episódios.
- Chrome de automação: `browser_profile_syw`, porta 9335 (o Maiquel faz o login lá dentro), ou a extensão Claude in Chrome. Nunca o Profile 6 real com porta de depuração (abriu deslogado em 30/10).

## Deu certo / não deu
| Data | Resultado | Lição |
|---|---|---|
| até 01/11 | deu certo | puzzles no Instagram fazem ~1.800+ views (Moser 2.439); garrafas envenenadas teve 119% de retenção no YouTube (reassistido) |
| 31/10 | não deu | estilo de desenho infantil reprovado: visual adulto e realista |
| 28–29/10 | não deu | o mesmo episódio saiu em 2 Reels no Instagram: nunca repetir |
| 01/11 | não deu | Ep 3 (aniversário) com 94 s fez só 457 views: sempre menos de 90 s |
| 01/11 | decisão | manter 2 vídeos por dia no formato desafio, com a resposta no fim |
