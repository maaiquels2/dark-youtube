# ec_lib — vídeos verticais no EffectCraft a partir de uma lista de cenas

Você escreve **um JSON curto** (`scenes.json`) dizendo, para cada bloco da narração, quais modelos de cena usar e em que palavra cada coisa acontece. O `build.py` gera o script, monta o projeto, tira quadros de teste, renderiza e mixa (voz + trilha + efeitos sonoros ligados às cenas). Exemplo completo e aprovado: `puzzles/bigbang/scenes.json` (o vídeo do Big Bang).

## Passo a passo (vídeo novo)

1. Crie a pasta `puzzles/<projeto>/` com `narration.json`: `{"blocks": ["frase do bloco 1...", "bloco 2...", ...]}` (inglês; 1 bloco ≈ 1 cena, 6–10 s cada).
2. Voz (Kokoro `am_onyx`, local):
   `tools/ComfyUI/python_embeded/python.exe puzzles/ec_lib/voice.py puzzles/<projeto>`
   → `assets/voice.wav` e `assets/timing_raw.json` (tempo de cada palavra).
3. Imagens (se usar `clumps_stars`/`recede`/`body_map`/`organ_focus`): ponha em `puzzles/<projeto>/assets/img/` (1080x1920 ou 864x1536, .jpg).
4. Escreva `puzzles/<projeto>/scenes.json` (formato abaixo). Precisa ter **o mesmo número de blocos** da narração.
5. Teste por quadros (barato, ~1 min): `python puzzles/ec_lib/build.py puzzles/<projeto> --frames`
   → abra `puzzles/<projeto>/ec_build/sheet.png` e **olhe de verdade** (texto cortado? tela estourada em branco? cena vazia?).
   Para ver instantes exatos: `--frames 12.5,13,13.5`.
6. Só quando os quadros estiverem bons: `python puzzles/ec_lib/build.py puzzles/<projeto> --render`
   (~12 min por minuto de vídeo; rode em segundo plano) → `puzzles/<projeto>/renders/<out>.mp4` e `<out>_share.mp4`.
   Só remixar o som: `--mix`. Folha de contato do vídeo pronto (2 quadros/s): `--sheet puzzles/<projeto>/renders/<out>.mp4`.

## Formato do `scenes.json`

```json
{
  "comp": "main",                 // nome da composição (opcional)
  "out": "meu_video",             // renders/meu_video.mp4
  "music": "library/music/incompetech/echoes-of-time-v2.mp3",   // CC-BY: crédito obrigatório na descrição
  "music_gain": 0.22,
  "tail": 3.0,                    // segundos depois da última palavra
  "captions": true,               // legendas automáticas (3 palavras, y=1560)
  "finish": {"glow": 1.1, "shake": 22, "grain": 3, "vignette": 75},   // opcional
  "blocks": [
    {"scenes": [ {"t": "bang", "at": 0.8} ]},
    {"cut": "whoosh", "scenes": [ {"t": "impact_title", "at": "thirteen", "lines": [{"text": "13.8 BILLION"}]} ]}
  ]
}
```

- `blocks[i]` = bloco `i` da narração. Dentro, `scenes` é uma lista de modelos que rodam juntos (a ordem = ordem das camadas; o último fica por cima).
- `cut` = transição na entrada do bloco: `"both"` (padrão: clarão 35 + whoosh), `"flash"`, `"whoosh"`, `"none"`. O bloco 0 não tem.

### Tempos (vale para todo parâmetro de tempo)

| Valor | Significa |
|---|---|
| `"stretched"` | início da palavra "stretched", procurada **a partir do início do bloco** (pode cair num bloco seguinte) |
| `"hot-0.3"`, `"fuse+0.5"` | a palavra com deslocamento em segundos |
| `0.8` (número) | 0,8 s depois do início do bloco |
| `"start"`, `"end"` | início/fim do bloco (`"end+0.3"` também vale) |
| `"vend"`, `"dur"` | fim da última palavra / fim do vídeo |

A palavra é comparada sem pontuação e em minúsculas ("13.8" vira "138"; números falados aparecem como o Kokoro os escreveu — confira em `timing_raw.json`). Se a palavra não existir, o build para com "palavra nao encontrada". Cuidado: `start`, `end`, `vend`, `dur` são palavras reservadas.

## Modelos de cena

Cores são `[r, g, b]` de 0 a 1. Todo parâmetro tem padrão (os do Big Bang); só `t` e os marcados com * são obrigatórios. "fim" padrão = fim do bloco + 0,3 s.

| Modelo | O que faz | Parâmetros | Som / tremida |
|---|---|---|---|
| `bang` | ponto brilhante que explode: onda de choque, gás laranja, faíscas; grade opcional (o espaço se expandindo) | `at` (0.8), `until`, `grid_at` (sem = sem grade), `grid_cell` 90, `grid_color`, `gas_dark`, `gas_light`, `spark`, `spark_end`, `ring`, `core` | boom + subida; tremida |
| `starfield` | estrelas passando pela câmera (fundo) | `from` ("start"), `until`, `speed` 1.2 (negativo = afastando), `size` 22, `peak` 85, `fade` [0.5,0.6] | — |
| `impact_title` | 1+ linhas de título com "pop" de escala | `lines`* (abaixo), `at` ("start"), `until` ("end"), `pop` 0.2, `fade` [entra, sai] (sem = corte seco), `hit` (true = tremida), `sfx` `{"k":"thud","g":0.7}` | o `sfx` que você pedir |
| `dive_into` | átomo (órbitas + núcleo); câmera mergulha no núcleo, que vira bola quente e estoura em `until` | `at`, `hot`*, `until`*, `orbits` 3, `orbit`, `nucleus`, `hot_dark`, `hot_light` | thud; tremida |
| `grid_expand` | grade explode para fora (expansão súbita) + riscos + desfoque radial + clarão 85 | `at`*, `until`, `cell` 36, `color`, `streak`, `streak_end`, `flash` 85 | subida + boom; tremida |
| `counter` | número/relógio que corre de 0 a `to` | `at` (0.2), `reach`* (quando chega em `to`), `until`, `to` 180, `format` `"clock"` (m:ss) ou `"number"` (1,234), `prefix`, `suffix`, `y` 560, `size` 120, `color`, `label`, `label_y`, `label_color` | — |
| `collide` | fundo de plasma com bolinhas; 4 bolas voam e se juntam em `at`+0.5 (clarão) | `at`*, `until`, `x` 760, `y` 1080, `c1`, `c2`, `plasma`, `bg` (false = sem fundo), `solo` `{text, at, x 320, ball, color}` (bola sozinha com rótulo), `label` `{text, at, color}` (rótulo do grupo) | thud no choque, sino em cada rótulo; tremida |
| `fog_clear` | névoa laranja que se dissipa em `at` com clarão e luz escapando | `at`*, `electrons` (palavra: pontinhos azuis entram), `light_until` (`at`+2.5), `dark`, `light` | sino grave; tremida |
| `oval_map` | mapa oval colorido tipo radiação cósmica de fundo, com anel e rótulo | `at`*, `until`, `rx` 490, `ry` 260, `tones` (5 cores, do quente ao frio), `label`, `label_at`, `label_y` 620 | whoosh |
| `clumps_stars` | gás azul que se aglomera, estrelas acendendo em `at`, imagem de textura (tela) por cima | `at`*, `until`, `gas`, `image` (arquivo em assets/img), `image_at` | sino agudo |
| `recede` | recortes redondos de uma imagem se afastando do centro (com estrelas e grade); ficam vermelhos em `redshift_at` | `image`*, `until` ("dur"), `count` 7, `crop` [x,y,raio,suavização] na imagem (432,768,210,150 para 864x1536), `redshift_at`, `tint`, `grid` (false = sem), `center_label` ("US" = pontinho no centro) | — |

### Corpo humano, medicina e dados (estilo holograma médico)

Fundo escuro teal com grade fraca (`bg: false` desliga, use quando empilhar dois modelos no mesmo bloco, ex.: `organ_focus` + `meter`), ciano/teal com acentos âmbar e magenta. Cores padrão: CYAN `[0.3,0.9,1]`, TEAL `[0.12,0.72,0.7]`, AMBER `[1,0.7,0.22]`, MAGENTA `[1,0.3,0.72]`. Textos longos encolhem sozinhos para caber (nada passa de ~980 px). Coordenadas `x`/`y` de **imagem** são em pixels da imagem original (ex.: 864x1536); a imagem é escalada para cobrir 1080x1920. Imagens com fundo preto (holograma) entram em modo *screen* (o preto some); `screen: false` para foto comum.

| Modelo | O que faz | Parâmetros | Som / tremida |
|---|---|---|---|
| `body_map` | imagem do corpo com leve respiração; pontos acendem (anel pulsando + brilho) e uma linha-guia leva ao rótulo na margem; `focus` = câmera mergulha num ponto (transição para a cena do órgão) | `image`*, `spots` `[{x, y, at, label, color, side "left"/"right" (padrão: lado do ponto), dy (rótulo acima −/abaixo +, px), size 46}]`, `focus` `{spot 0, at, zoom 4}` (zoom termina em `until`; rótulos somem), `color` CYAN, `glow` 22, `scale` 1, `until`, `bg`, `screen` | sino a cada ponto (tom sobe); subida no `focus` |
| `organ_focus` | imagem do órgão com zoom lento, brilho pulsando e varredura; partículas saindo de um ponto; sinal de bloqueio; título no topo | `image`*, `zoom` [100,116], `emit` `{at*, until ("end"), from:[x,y]* (px da imagem), dir [0,-1] (para cima), color AMBER, type 2 (bolas) ou 3 (estrelas), rate 4}`, `hold` `{at*, x, y (px da imagem; padrão abaixo do centro), color MAGENTA, text, dir, flow (false = sem o fluxo que para no bloqueio)}`, `label` `{text, at, y 440}`, `color`, `glow` 30, `bg`, `screen` | sino na emissão; thud + tremida no bloqueio |
| `molecule_dock` | membrana da célula (faixa curva com textura) e receptores em U; ligantes chegam voando e encaixam em `at`; ondas de sinal brilham para dentro da célula | `ligands`* `[{at*, label, color (alterna CYAN/MAGENTA), receptor (índice), persist}]`, `receptors` (n.º de ligantes), `dissolve_at` (os sem `persist` viram partículas e somem), `y` 1080, `bend` 70, `color` TEAL, `until`, `bg` | thud + tremida em cada encaixe; sino ao dissolver |
| `molecule_build` | corrente de contas: metade `c1` + metade `c2` se juntam em `at`; cauda ondulada amarela em `tail_at`; em `ride_at` a molécula encolhe e viaja num vaso com glóbulos vermelhos | `at`*, `tail_at`, `ride_at`, `labels` `{a, b (cada metade, somem após juntar), joined, tail, ride}`, `c1` CYAN, `c2` MAGENTA, `tail_color`, `beads` 5 (por metade), `gap` 190, `y` 820, `until`, `bg` | thud + tremida ao juntar; thud + sino na cauda; whoosh no vaso |
| `flow_valve` | tubo com partículas passando; em `slow_at` a válvula fecha, o fluxo desacelera e metade das partículas some | `slow_at`, `label` `{text, at}`, `y` 960, `h` 240, `x` 700 (válvula), `gap` 0.3 (abertura final), `speed` [520,110] px/s, `count` 24, `color` (tubo), `dots` (cor), `until`, `bg` | thud ao fechar |
| `meter` | medidor arredondado (vertical ou horizontal) com rótulo e valor; vai de `from` a `to` entre `at` e `reach`; cor muda com o nível. Até 2 lado a lado: `meters: [{...}, {...}]` (campo de cada medidor sobrepõe o de fora) | `label`*, `from` 0, `to` 100, `max` 100 (cheio), `at` ("start+0.4"), `reach` (at+1.6), `suffix`, `prefix`, `decimals` 0, `colors` [baixo, meio, alto] (padrão CYAN→AMBER→MAGENTA), `value` (false = sem número), `dir` "v"/"h", `y` (centro: 900 horizontal, 840 vertical; 2 horizontais ficam em y−120 e y+180), `show` (quando aparece; "start"), `until`, `bg` | sino no `reach`; whoosh se `show` for depois do início |
| `bars` | gráfico de barras (2 a 4): barras crescem e o número conta junto; rótulos, título, fonte no rodapé (y 1420) | `bars`* `[{label, value, color}]`, `title`, `source`, `at` ("start+0.5"), `reach` (at+1.6), `stagger` 0.3, `suffix` "%", `prefix` (ex.: "-"), `decimals` 0, `max` (auto), `down` (true = barras para baixo, perda), `show`, `until`, `bg` | subida enquanto cresce; sino no fim |
| `end_card` | cartão de aviso: círculo com "!" e 1-3 linhas; entra suave subindo | `lines`* (`["NOT MEDICAL ADVICE", "linha 2", ...]`; 1ª em Anton 80, demais Inter 46; ou `{text, size, font, color}`), `at` ("start+0.2"), `until` (use `"dur"` no último bloco), `color` AMBER, `y` 900, `icon` (false = sem), `bg` | sino suave |

Exemplo (pâncreas: insulina sai e o açúcar desce no mesmo bloco; medidor embaixo, sem fundo próprio):

```json
{"scenes": [
  {"t": "organ_focus", "image": "03_pancreas.jpg", "label": {"text": "PANCREAS"},
   "emit": {"at": "insulin", "from": [430, 600], "dir": [0.3, -1]}},
  {"t": "meter", "bg": false, "dir": "h", "y": 1260, "label": "BLOOD SUGAR", "from": 180, "to": 100, "max": 250,
   "suffix": " mg/dL", "at": "sugar", "reach": "down"}
]}
```

Outros exemplos prontos (os 8 modelos): `puzzles/ec_lib/demo_med/scenes.json` (narração do Mounjaro; folha em `demo_med/ec_build/sheet.png`).

Linha do `impact_title`: `{"text", "size" 150, "y" 960, "x" (centro), "color", "font" ("Anton" ou "Inter"), "track" 0, "delay" 0, "scale" [início, pico, fim]}`. Títulos em Anton; números e rótulos pequenos em Inter.

### Exemplo (bloco com título + átomo)

```json
{"cut": "whoosh", "scenes": [
  {"t": "starfield", "until": "smaller+0.3"},
  {"t": "impact_title", "at": "thirteen", "until": "smaller-0.3", "pop": 0.25, "lines": [
    {"text": "13.8 BILLION", "size": 170, "y": 900, "color": [1, 0.93, 0.8], "track": 20, "scale": [80, 104, 118]},
    {"text": "YEARS AGO", "size": 86, "y": 1010, "color": [1, 0.6, 0.25], "track": 300, "scale": [80, 100, 112]}]},
  {"t": "dive_into", "at": "smaller-0.3", "hot": "hot-0.3", "until": "stretched"}
]}
```

## Armadilhas (já custaram tempo)

- **Olhe os quadros antes de renderizar o vídeo.** Render completo é caro (~12 min/min); quadros custam segundos. Só diga "ficou bom" depois de ver.
- **Clarões somados estouram a tela em branco.** `fog_clear` + `flash` + `cut` no mesmo instante já está no limite: não ponha outro `grid_expand`/`bang` no mesmo segundo. Clarão de corte ~25–35; Lens Flare ≤ 80.
- **Texto largo estoura 1080 px.** Tracking alto (`track` 300–400) só em palavras curtas. Rótulos com menos de 60 px saem com contorno fino automático. Confira as bordas nos quadros.
- **Área das legendas:** y ≈ 1500–1620. Títulos entre y 400 e 1100.
- **Palavra que se repete** ("trillionth" 3×): pega a primeira depois do início do bloco. Para outra, use deslocamento (`"trillionth+1.2"`) ou um número.
- Mensagens normais do CLI saem em stderr (o PowerShell mostra como erro): veja se a última linha diz `saved video.ecproj`.
- Partículas (CC Particle World): tipos 1 riscos, 2 bolas, 3 estrelas; 8+ sai quadrado.
- Expressão com início de bloco negativo: `"time-" + a` vira `time--0.1` (erro silencioso, a camada fica parada). Escreva `"time-(" + a + ")"`.
- Não existe `app.project.save` nem `Folder.current` no script; o `build.py` já cuida disso.
- Trilha da Incompetech é CC-BY: crédito "Music: Kevin MacLeod (incompetech.com), CC BY 4.0" na descrição.
- Loudness final -16 LUFS (o `--render`/`--mix` já normaliza).

## Arquivos

- `ec_lib.jsx` — funções auxiliares (solid, shape, text, noise, particles, grid, flash, photo, circle/oval, fade, K, P, fx; e para as cenas médicas: `vec` formas vetoriais, `label` rótulo que encolhe para caber, `KS` chaves suavizadas, `rig` null que move um grupo, `holoBg`/`holoScan`/`holoGlow`, `cover` foto + mapa de pixels) + modelos (`TPL.nome`) + `buildVideo()` (fundo, cortes, acabamento glow/tremida/grão/vinheta, legendas). Modelo novo: escreva `TPL.meu_modelo = function (sc) {...}` usando `T(sc, sc.at)` para tempos e `sfx(t, "boom"|"whoosh"|"rise"|"thud"|"chime", ganho)` para som.
- `build.py` — lê `scenes.json` + voz, gera `ec_build/video.jsx`, `video.ecproj`, `events.json` (sons), quadros, vídeo e mixagem.
- `voice.py` — narração → voz + tempos por palavra.
