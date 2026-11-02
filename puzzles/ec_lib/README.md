# ec_lib — vídeos no EffectCraft a partir de uma lista de cenas (Short vertical e vídeo longo horizontal)

Você escreve **um JSON curto** (`scenes.json`) dizendo, para cada bloco da narração, quais modelos de cena usar e em que palavra cada coisa acontece. O `build.py` gera o script, monta o projeto, tira quadros de teste, renderiza e mixa (voz + trilha + efeitos sonoros ligados às cenas). Exemplos aprovados: `puzzles/bigbang/scenes.json` e `puzzles/mounjaro/scenes.json` (Shorts verticais); `puzzles/ec_lib/demo_long/scenes.json` (longo horizontal, todos os modelos novos; tempo sintético, sem voz).

> Esta versão (pasta `ec_lib_next` até a troca) acrescenta o formato horizontal. Os Shorts verticais saem **iguais pixel a pixel** aos da versão anterior (conferido em mounjaro e bigbang). Os caminhos abaixo usam `puzzles/ec_lib/`, o nome depois da troca.

## Formato: vertical (Short) ou horizontal (longo)

`"format": "vertical"` (padrão, 1080x1920) ou `"format": "horizontal"` (1920x1080), no topo do `scenes.json`. Todos os modelos funcionam nos dois; o que muda sozinho no horizontal:

- **Imagens 864x1536** (`body_map`, `organ_focus`) ocupam a altura toda num painel (~700 px de largura, bordas suaves). `organ_focus` fica à **esquerda** (centro x 560) e o título vai para a **coluna da direita** (x 1360); `body_map` fica no **centro** com os rótulos dos dois lados. Troque com `"img_x"` (centro da imagem, px de tela) e `"panel"` (largura do painel). As coordenadas de imagem (`spots`, `emit.from`, `hold.x/y`) são em pixels da imagem, então **servem aos dois formatos sem mudar**.
- `meter` com `"bg": false` (empilhado sobre uma imagem) vai para a coluna da direita (x 1360, y 560). Outra posição: `"x"`, `"y"`.
- **Legendas**: vertical = 3 palavras, Anton 78, y 1560; horizontal = até 5 palavras numa linha só, Anton 50, linha de base y 1012 (nunca passam da largura; encolhem se preciso). Mude com `"caption_words"`.
- Zona livre de texto no horizontal: títulos de cena em y ≈ 130–360; conteúdo entre 150 e 900; **não ponha nada abaixo de y 940** (legenda).
- Textos do `impact_title` que passariam da largura encolhem sozinhos no horizontal.

**Mesmo bloco nos dois formatos:** qualquer modelo aceita `"horizontal": {...}` e `"vertical": {...}` — parâmetros que só valem naquele formato (o resto é comum). Ex.: `{"t": "meter", "bg": false, "label": "BLOOD SUGAR", ..., "vertical": {"y": 1300}}`. Coordenada de tela (`x`, `y`, `label_y`, `lines[].y/x`) fora do quadro faz o build parar com "fora da tela 1920x1080; use horizontal: {...}" — é quase sempre um número do vertical copiado.

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
  "format": "vertical",           // ou "horizontal" (1920x1080, vídeo longo)
  "comp": "main",                 // nome da composição (opcional)
  "out": "meu_video",             // renders/meu_video.mp4
  "music": "library/music/incompetech/echoes-of-time-v2.mp3",   // CC-BY: crédito obrigatório na descrição
  "music_gain": 0.22,
  "tail": 3.0,                    // segundos depois da última palavra
  "captions": true,               // legendas automáticas (vertical 3 palavras y=1560; horizontal 5 palavras y=1012)
  "caption_words": 3,             // opcional: palavras por legenda
  "part_max": 150,                // opcional (longo): parte nova a cada capítulo ou a cada 150 s
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

Fundo escuro teal com grade fraca (`bg: false` desliga, use quando empilhar dois modelos no mesmo bloco, ex.: `organ_focus` + `meter`), ciano/teal com acentos âmbar e magenta. Cores padrão: CYAN `[0.3,0.9,1]`, TEAL `[0.12,0.72,0.7]`, AMBER `[1,0.7,0.22]`, MAGENTA `[1,0.3,0.72]`. Textos longos encolhem sozinhos para caber (nada passa da largura − 100 px). Coordenadas `x`/`y` de **imagem** são em pixels da imagem original (ex.: 864x1536); a imagem é escalada para cobrir 1080x1920 (no horizontal: altura toda num painel, ver acima). Imagens com fundo preto (holograma) entram em modo *screen* (o preto some); `screen: false` para foto comum.

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

### Modelos do vídeo longo (funcionam também no vertical)

Todos entram com `at` e saem em `until` (padrão "fim do bloco + 0,3"). Fundo próprio de holograma, exceto onde dito; `image` = foto de fundo escurecida (35%, `image_opacity`) em vez do holograma; `bg: false` = sem fundo.

| Modelo | O que faz | Parâmetros | Som |
|---|---|---|---|
| `intro` | abertura ≤ 5 s: nome do canal pequeno entre duas linhas que se abrem, título do vídeo (até 3 linhas, equilibradas) entrando em foco, faixa de luz atravessando. Sem logo | `title`*, `kicker` (ex.: "SHOW YOUR WORK"), `sub`, `at` ("start"), `until` (fim do bloco, **corta em 5 s**), `size`, `color`, `image` | subida + boom leve; tremida |
| `chapter_card` | cartão de capítulo: número grande "fantasma" ao fundo, "CHAPTER 2", linha que se abre do centro e título entrando em foco (~1 s de animação; o bloco narrado "Chapter two. The numbers." dá os 2–3 s) | `title`*, `num` (1 → "01" + "CHAPTER 1"), `kicker` (troca o "CHAPTER n"), `sub`, `at`, `until`, `size`, `color`, `image`, `y` | subida + thud + sino grave |
| `lower_third` | rótulo de fonte/dado no canto: barra colorida + caixa escura + 1–2 linhas, desliza 40 px. **Sem fundo, vai por cima** de outra cena do bloco; é montado depois da vinheta (fica nítido) | `text`*, `sub` (ex.: "Source: NEJM 2022"), `at` ("start+0.5"), `until` ("end"), `corner` "bl" (padrão) / "br" / "tl" / "tr", `color` | — |
| `fact_card` | número/frase grande com brilho, frase de apoio (até 3 linhas) e fonte embaixo de um filete. Respiro entre cenas densas | `big` (texto, ex.: "1 in 3") **ou** `to` (número que conta de `from` 0 até `to` em `reach`, com `prefix`, `suffix`, `decimals`), `text`, `source`, `at` ("start+0.2"), `until`, `size` (220), `color` AMBER, `y` | thud; tremida; sino quando o número chega |
| `quote_card` | aspas grandes, citação (até 4 linhas, equilibradas), autor e fonte | `quote`*, `by`, `source`, `at`, `until`, `size` (56), `color` | sino |
| `timeline` | linha do tempo com 3–6 marcos: a linha se acende até cada marco quando ele aparece (ponto que pulsa, ano em Anton, rótulo de até 3 linhas). Horizontal no 16:9; vertical (de cima para baixo) no 9:16 | `items`* `[{date, label, at, color}]`, `title`, `at` (1º marco, "start+0.5"), `step` 0.8 (s entre marcos sem `at`), `until`, `color` | sino a cada marco (tom sobe) |
| `outro` | fechamento: frase curta + botão "SUBSCRIBE" (texto num botão arredondado que pulsa, sem logo) à esquerda; quadro 16:9 "NEXT VIDEO" com o título do próximo vídeo à direita (no vertical: um embaixo do outro). O quadro serve de lugar para o elemento de tela final do YouTube | `next`* (título do próximo vídeo), `next_label` ("NEXT VIDEO"), `cta` ("SUBSCRIBE"), `line`, `button` [r,g,b] (vermelho), `at` ("start+0.2"), `until` ("dur"), `color` | sino + whoosh |

Exemplo (bloco com imagem + rótulo de fonte):

```json
{"scenes": [
  {"t": "body_map", "image": "01_body.jpg", "spots": [{"x": 432, "y": 150, "at": "brain", "label": "BRAIN"}]},
  {"t": "lower_third", "text": "Tirzepatide (Mounjaro, Zepbound)", "sub": "Source: FDA prescribing information, 2022"}
]}
```

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

## Tema "rulechanged" (canal The Rule Changed)

`"theme": "rulechanged"` no topo do `scenes.json`. Sem esse parâmetro nada muda (Show Your Work continua igual). Com ele:
- **Fundo e cores:** grafite liso #111214 com radial sutil. Sem grade, partículas, brilhos, varredura nem Glow final. Toda cor passa pela paleta do canal (`pal()`): escuro vira grafite, neutro vira texto #ece8e1, verde vira verde-sálvia #7fb08a, ciano/azul vira rótulo #a8a29a, âmbar vira texto secundário #c8c3ba, o resto vira vermelho #d0402f.
- **Fontes e cortes:** Anton só nos títulos (impact_title, chapter_card, intro, 1ª linha do end_card, próximo vídeo do outro, nome do doc_excerpt). Todo o resto em Inter, números em Inter 700. Legendas em Inter Bold. Corte entre blocos sem clarão (padrão `whoosh`).
- **Linha de fonte** (`source` do fact_card, bars, doc_excerpt e web_clip; termina no fim do próprio bloco): Inter Medium 24, caixa-alta, cor #a8a29a, tracking 0,12em. É desenhada depois da vinheta, para o canto não apagar a cor. Fica acima da legenda; no doc_excerpt, embaixo da coluna do nome (texto longo encolhe para caber).
- **`fact_card`:** o número entra pronto, sem contador, subindo de trás de uma máscara em 0,4 s no `at`. Depois um traço de 520 px (`color`, padrão vermelho) e a frase, e por fim a fonte no canto inferior esquerdo. Alinhado à esquerda (x 170). `reach` é ignorado.
- **`bars`:** uma cor por gráfico (`color`, padrão #b8463b). `highlight`: índice da barra em cor cheia, as outras em cinza. Cada barra cresce em 0,6 s e o valor aparece pronto quando ela para. Sem grade. `down` não existe no tema.
- **`act`:** "scam" | "case" | "rule", no bloco ou numa cena. Desenha THE SCAM · THE CASE · THE RULE no canto superior esquerdo. Quando o bloco tem `organ_focus` com a foto à esquerda, o marcador vai para x = 48% da tela. Blocos seguidos com o mesmo ato formam uma faixa contínua.
- **`lower_third`:** fio vertical de 4 px na cor do ato (cinza sem ato; `color` troca), título Inter 600 40, sub Inter 30, sem caixa.
- **`quote_card`:** aspas e texto em Inter. Opcional `header`: cabeçalho do registro em Courier Prime acima das aspas (este também funciona fora do tema).
- **`organ_focus`:** `"illustration": true` põe o selo ILLUSTRATION no canto superior esquerdo da imagem (este também funciona fora do tema).

- **Modelo novo `doc_excerpt`:** trecho de documento (pessoa sem foto). Folha de papel com cabeçalho e corpo em Courier Prime. O marca-texto amarelo corre da esquerda para a direita em `hl_at`, o trecho final fica em 40%, e uma coluna à direita mostra o nome. Câmera: só zoom centrado lento. **Só horizontal.** Precisa da fonte Courier Prime instalada (`fonts/CourierPrime-*.ttf`) Parâmetros: `text`*, `header` `["Federal Communications Commission", "FCC 18-58"]`, `highlight` (trecho exato do text), `hl_at` ("start+1.0"), `hl_dur` 0.8, `fade` (trecho do text; dele até o fim fica em 40%), `kicker`, `name`, `role`, `source`, `at`, `until`, `zoom` [100, 106]. Som: whoosh na entrada e no marca-texto.
- **Cena que entra depois de outra no mesmo bloco** (2ª cena em diante, com `at` ou `show` depois do início do bloco): fundo e partes fixas começam no próprio `show`/`at` (−0,1 s). O `until` corta tudo. Assim a cena de trás não é coberta desde o começo do bloco. Vale para todos os modelos. Conferido: demo_long e Big Bang com quadros idênticos.
- **Modelo novo `web_clip`:** print real de página (notícia, ordem, registro) num cartão claro sobre o fundo, sem moldura de navegador. Cantos 8 px, sombra, até 1500 px de largura, centrado. Sobe 30 px em 0,5 s (ease-out-expo) e sai com fade. Câmera só com zoom centrado. Parâmetros: `image`* (procura em assets/img/ e depois em assets/clips/), `crop` [x,y,w,h] em px da imagem. **Sem crop (o padrão certo): mostra só a manchete**, pela caixa `box` do .json ao lado do print (assets/clips/<nome>.json), com recorte justo e uma moldura desenhada: `paper` (no tema, papel #ece4d0; fora dele, branco; "#rrggbb" ou [r,g,b] troca a cor; com `crop`, `paper` liga a moldura; `paper: false` = sem moldura no crop, branca no automático). Assim não entra menu, etiqueta nem propaganda. Use `crop` só para um trecho que não seja a manchete. Marcas fora do recorte são ignoradas, `site` e `date` (rótulo "FCC.GOV · MAY 10, 2018" em cima do cartão), `marks` [{`box` [x,y,w,h] em px da imagem original, `at`, `color`}] até 3 (marca-texto #f2d24b em multiplicar a 45%, corre em 0,5 s), `source`, `at` ("start"), `until` ("end+0.3"), `zoom` [100, 108], `bg`. Serve de `news_clip` (recorte de site oficial ou de mídia): `site` = veículo, `marks` = trechos marcados. Testado nos dois formatos (no vertical o cartão tem até 880 px de largura).
- **Modelo novo `us_map`:** mapa dos EUA (fronteiras do US Census, domínio público, de `library/maps/us-states.json`; o build gera `puzzles/ec_lib/assets/us_states.json` uma vez, Alasca a 35% e Havaí em encarte embaixo à esquerda, sem Porto Rico). Estados não citados ficam grafite #2a2c30, com fio #111214. Cada estado citado acende em 0,4 s (ease-out-expo), sem brilho. Parâmetros: `states`* [{`code` (sigla: "CA"), `at` (padrão: start+0.6, depois +`step` 0.25 por estado), `tone` "scam" (#d0402f) | "rule" (#7fb08a) | "neutral" (#5a5c60), `value` (número N1 em Inter Bold, sobe 0,4 s de trás de máscara, sem contador), `label` (caixa-alta, Inter 20), `dx`/`dy` (afasta o rótulo do centro do estado e liga com um fio; use em estado pequeno)}], `title`, `source`, `at` ("start"), `until` ("end+0.3"), `zoom` [100, 100] (só zoom centrado), `bg`. O marcador de ato vem do `act` do bloco. Área: horizontal x 230–1690, y 210 até acima da fonte; vertical x 70–1010, centro em y ≈ 880. O rótulo nunca sai pela borda. O build avisa ("AVISO … scam e rule no mesmo mapa") quando um mapa mistura vermelho e verde, porque a regra do canal é uma cor por gráfico; não para o build. **Crédito:** quem usar o mapa põe em `entities/credits.json` do episódio: U.S. Census Bureau, cartographic boundary files, domínio público (exemplo em `scamlaw/_teste_ec_mapa_clip/entities/credits.json`).
- **Modelo novo `clip`:** vídeo pronto (clipe do HyperFrames ou outro .mp4) como cena, mudo (a mixagem continua voz + trilha + efeitos). Parâmetros: `file`* (procura em assets/img/ e depois em assets/clips/), `from` 0 (segundo do clipe que aparece no início da cena), `at` ("start"), `until` ("end+0.3"), `fit` "cover" (cobre a tela) | "contain" (inteiro, com o fundo do tema em volta), `hold` true (cena mais longa que o clipe: para no último quadro), `fade` [0.15, 0.15], `source`, `bg`. Renderize o clipe no formato do vídeo (1920x1080 no longo, 1080x1920 no Short) e a 30 fps; um clipe 16:9 num Short com `cover` perde as laterais. Trocar o .mp4 refaz só a parte dele no `--render` (o hash inclui tamanho e data do arquivo).
- **`lufs`** no topo do `scenes.json` (padrão -16): volume final da mixagem. Shorts do canal: `"lufs": -14` (pico continua em -1,5 dBFS).
- **Aviso dos 0,3 s:** ao montar, o build lista os blocos em que nada aparece nos primeiros 0,3 s ("AVISO 0,3 s: … 3 (+1.0s)"; "só sobreposição" = o bloco só tem lower_third). Fundo e o que já vinha do bloco anterior não contam. Não para o build.
- **Linha de fonte no vertical** fica 110 px acima da linha de base da legenda (era 74; encostava na legenda de 3 palavras).
- **Teste dos modelos novos:** `scamlaw/_teste_ec_mapa_clip/` (horizontal) e `scamlaw/_teste_ec_mapa_clip_v/` (vertical), tempo sintético, sem voz.

## Como fazer um vídeo longo (8–12 min, horizontal)

1. `narration.json` com ~60–80 blocos (1 bloco ≈ 1 cena de 6–10 s). Comece com o bloco da abertura (só o título falado, ≤ 5 s), depois um bloco curto narrado para cada capítulo ("Chapter two. Caffeine."), e termine com o bloco do fechamento ("Next week… Subscribe…").
2. Voz e imagens como no Short (as mesmas imagens 864x1536 dos Shorts servem).
3. `scenes.json` com `"format": "horizontal"`. Estrutura sugerida:
   - bloco 0: `intro`;
   - cada capítulo: um bloco só com `chapter_card` (nunca cartão de capítulo por cima de gráfico — regra do canal), seguido dos blocos do capítulo;
   - nos blocos com dado/estudo: `lower_third` com a fonte por cima da cena (ou `source` do `bars`/`fact_card`);
   - a cada 4–6 blocos densos, um `fact_card`/`quote_card` de respiro; história de um remédio = `timeline`;
   - penúltimo: `end_card` (aviso médico); último: `outro` (`until` "dur").
   - Para reaproveitar um bloco de um Short: copie o modelo e mova as coordenadas de tela do vertical para `"vertical": {...}` (as de imagem ficam).
4. **Partes**: o build corta o vídeo em partes no início de cada bloco com `chapter_card` (e a cada `part_max` = 150 s se não houver capítulo). Cada parte vira uma pré-composição própria (montagem rápida) e é renderizada separada.
5. Quadros: `python puzzles/ec_lib/build.py puzzles/<projeto> --frames` → **uma folha por parte** (`ec_build/sheet_part01.png`, …; 2 quadros por bloco, a 35% e 80% dele; ~1 min para 140 quadros). Para olhar uma parte de perto: `--frames part4` (1 quadro/s, `sheet_part04.png`). Instantes exatos: `--frames 312.5,313`.
6. Render: `python puzzles/ec_lib/build.py puzzles/<projeto> --render` (em segundo plano; ~12 min por minuto → ~2 h para 10 min). Renderiza parte por parte em `ec_build/parts/visual_NN.mp4`, **refaz só as partes que mudaram**. Cada parte tem uma impressão digital, guardada em `ec_build/parts/hashes.json`. Ela junta biblioteca, tema e cabeçalho do `scenes.json`, e mais os blocos, palavras, legendas e imagens da janela da parte, com 1 s de folga. A parte cujo hash não mudou é pulada. Mudar 1 texto num bloco refaz só a parte dele. Já mudar a biblioteca, o tema ou a voz (que desloca tempos) refaz todas. Também retoma de onde parou se cair. Exceção: cena com `until` que passa mais de 1 s do próprio bloco não entra no hash da parte seguinte. Nesse caso rode `--render --part N`, junta com `ffmpeg concat` sem recodificar (corte em quadro inteiro, testado: sem quadro repetido nem perdido) e mixa. Só uma parte: `--render --part 3` (dá para rodar 2 partes em paralelo em janelas diferentes; depois `--render` junta). A trilha repete sozinha se for mais curta que o vídeo.

### Limites medidos (70 blocos, 9,3 min, 1920x1080)

- Montagem do projeto: ~45 s, pico ~250 MB de RAM (numa comp só seriam ~6,5 min e 1,4 GB — por isso as partes). `video.ecproj` ~75 MB.
- Quadros: ~0,5 s cada no lote do horizontal.
- O tempo de render (~12 min/min) não muda com as partes; elas só permitem retomar e paralelizar.
- Uma cena que dura mais que o próprio capítulo (ex.: `until: "dur"` no meio do vídeo) continua aparecendo por baixo dos capítulos seguintes — use `until: "dur"` só no último bloco.
- No horizontal, cada imagem é importada uma vez só (no vertical continua como antes, para os Shorts saírem idênticos).

## Armadilhas (já custaram tempo)

- **Olhe os quadros antes de renderizar o vídeo.** Render completo é caro (~12 min/min); quadros custam segundos. Só diga "ficou bom" depois de ver.
- **Clarões somados estouram a tela em branco.** `fog_clear` + `flash` + `cut` no mesmo instante já está no limite: não ponha outro `grid_expand`/`bang` no mesmo segundo. Clarão de corte ~25–35; Lens Flare ≤ 80.
- **Texto largo estoura 1080 px.** Tracking alto (`track` 300–400) só em palavras curtas. Rótulos com menos de 60 px saem com contorno fino automático. Confira as bordas nos quadros.
- **Área das legendas:** vertical y ≈ 1500–1620 (títulos entre y 400 e 1100); horizontal y ≈ 960–1030 (nada abaixo de 940).
- **Ordem das camadas:** o último modelo do bloco fica por cima. `lower_third` é a exceção (sempre por cima de tudo, menos da legenda).
- **Palavra que se repete** ("trillionth" 3×): pega a primeira depois do início do bloco. Para outra, use deslocamento (`"trillionth+1.2"`) ou um número.
- Mensagens normais do CLI saem em stderr (o PowerShell mostra como erro): veja se a última linha diz `saved video.ecproj`.
- Partículas (CC Particle World): tipos 1 riscos, 2 bolas, 3 estrelas; 8+ sai quadrado.
- Expressão com início de bloco negativo: `"time-" + a` vira `time--0.1` (erro silencioso, a camada fica parada). Escreva `"time-(" + a + ")"`.
- Não existe `app.project.save` nem `Folder.current` no script; o `build.py` já cuida disso.
- Trilha da Incompetech é CC-BY: crédito "Music: Kevin MacLeod (incompetech.com), CC BY 4.0" na descrição.
- Loudness final -16 LUFS (o `--render`/`--mix` já normaliza).

## Arquivos

- `ec_lib.jsx` — funções auxiliares (solid, shape, text, noise, particles, grid, flash, photo, circle/oval, fade, K, P, fx; e para as cenas médicas: `vec` formas vetoriais, `label` rótulo que encolhe para caber, `KS` chaves suavizadas, `rig` null que move um grupo, `holoBg`/`holoScan`/`holoGlow`, `cover` foto + mapa de pixels) + modelos (`TPL.nome`) + `buildVideo()` (fundo, cortes, acabamento glow/tremida/grão/vinheta, legendas). Modelo novo: escreva `TPL.meu_modelo = function (sc) {...}` usando `T(sc, sc.at)` para tempos e `sfx(t, "boom"|"whoosh"|"rise"|"thud"|"chime", ganho)` para som.
- No `ec_lib.jsx`, `W`/`H`/`CX`/`CY` valem para o formato do vídeo e `vh(v, h)` devolve o valor do vertical ou do horizontal; modelo novo deve usar isso em vez de números fixos de 1080x1920. Partículas: posições/raios/tamanhos em unidades de 1080 px (`particles()` converte). Modelo com `TPL.x.overlay = true` é montado depois da vinheta.
- `build.py` — lê `scenes.json` + voz, gera `ec_build/video.jsx`, `video.ecproj`, `events.json` (sons), quadros, vídeo (por partes no longo) e mixagem.
- `demo_long/` — teste horizontal (14 blocos, todos os modelos novos e vários antigos; `make_timing.py` gera tempo sintético a partir de `narration.json`). `demo_long_v/` — o mesmo `scenes.json` no vertical.
- `voice.py` — narração → voz + tempos por palavra.
