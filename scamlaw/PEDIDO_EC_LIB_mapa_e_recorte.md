# Pedido à sessão ec-lib: dois modelos novos no tema `rulechanged`

De: sessão Ferramentas (02/11/2026), a pedido do Maiquel. Para: sessão dona de `puzzles/ec_lib`. Não editei a biblioteca.

## Contexto
O Maiquel gostou dos mapas, gráficos e Motion do vídeo Tricolor (Cracked Ledger) e quer o mesmo nível no The Rule Changed, com recortes de notícias de sites oficiais do governo ou da mídia. Os canais têm identidade própria (`canais/RULE_CHANGED.md`); só a prática comprovada é compartilhada. No Ep01 (`scamlaw/ep01_robocalls`, 55 cenas por tipo: lower_third 29, organ_focus 25, impact_title 15, fact_card 12, bars 6...) há 1 `doc_excerpt` e nenhum mapa.

## Modelo 1: `news_clip` (recorte de fonte oficial ou de mídia)
Hoje o `doc_excerpt` só cobre texto de lei/ordem em Courier. Falta um recorte de **página real** (captura de site `.gov` ou de veículo).
- `image`* (captura em `assets/img/`), `crop` [x, y, w, h] na imagem, `highlight` [{x, y, w, h}] com marca-texto animado (amarelo `#f2d24b`) em `hl_at`.
- Moldura de papel `#ece4d0`, cabeçalho com nome da fonte e data (`outlet`, `date`), linha `source` no padrão do canal.
- Câmera: só zoom centrado lento; sem deslize lateral. Sem brilho, sem tremida.
- Só horizontal, como o `doc_excerpt`.
- Regra de uso: recorte curto, creditado, nunca a matéria inteira.

## Modelo 2: `us_map` (mapa de estados)
Mapa dos EUA, que serve a leis estaduais e à lei federal que mudou.
- `states` [{code, at, tone}] para acender estados; `tone`: `scam` (vermelho `#d0402f`), `rule` (verde `#7fb08a`) ou neutro `#5a5c60`.
- `label` e `value` opcionais por estado (número em Inter 700, sem contador, entrada N1).
- Marcador de ato (`THE SCAM · THE CASE · THE RULE`) como nos gráficos.
- Geometria de fonte livre (domínio público, como o US Census), com crédito em `entities/credits.json`.

## Restrições do tema (de `canais/RULE_CHANGED.md`)
Fundo `#111214`; uma cor por gráfico; sem brilho, partícula, grade ou holograma; entradas ease-out-expo; números em Inter, nunca em Anton.

## Pergunta em aberto
O Maiquel gostou do Motion (HyperFrames, `tools/hyperframes/tricolor-s21`). Dá para o `ec_lib` renderizar um clipe HyperFrames como cena (um `t` que aponta para um .mp4 pronto, na duração da cena), ou isso fica fora do `ec_lib`?

## Entrega esperada
Parâmetros exatos dos dois modelos em `puzzles/ec_lib/README.md` e um teste curto (3 a 5 s cada) em `scamlaw/`, para o Maiquel aprovar o visual antes do Ep02.
