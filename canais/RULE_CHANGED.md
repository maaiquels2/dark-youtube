# The Rule Changed: identidade do canal

Aprovado pelo Maiquel em 01/11/2026.
- Opção visual: C "Golpe → Regra".
- Números: entrada N1.
- Pessoa sem foto: tratamentos T1, T2 e T3.
- Prova visual: `research/canal_golpes_lei/identidade/proposta_identidade.html`.

Vale junto com [`REGRAS_UNIVERSAIS.md`](../REGRAS_UNIVERSAIS.md). Em conflito, a regra universal vence, exceto onde este arquivo diz "exceção do canal".

## Canal
- **Formato:** golpes contra pessoas comuns e a lei que mudou por causa deles.
  - Vídeo longo horizontal em inglês, para os EUA, de 8 a 12 min.
  - Shorts servem de chamariz.
- **Onde:** no canal de YouTube que era do Grandpa Walt. É um rebranding no mesmo canal; o Walt fica no Facebook e no Instagram.
- **Pesquisa do formato, temas e regras do YouTube:** `research/canal_golpes_lei/PESQUISA.md`.
- **Fica longe do Cracked Ledger:** nada de colapso de empresa ou fraude contábil. Madoff fica de fora.

## Estrutura de cada vídeo
O arco é fixo. A estrutura interna varia de caso para caso (regra anti-fábrica, `CLAUDE_YT_ANTI_DEMONETIZATION.md` §2).

1. **Gancho:** a vítima e o dinheiro, com número concreto na 1ª ou 2ª frase.
2. **THE SCAM:** como o golpe funcionava, em passos, sem receita que dê para repetir.
3. **THE CASE:** quem foi pego, órgão ou tribunal, decisão. Usar "alegou", "segundo o FCC", "foi condenado" só quando for o caso.
4. **THE RULE:** nome e ano da lei. O que ela protege hoje e o que ainda falha.
5. **Como se proteger e onde denunciar:** reportfraud.ftc.gov, ic3.gov, o banco.
6. **Fecho:** espelha o gancho e pede inscrição.

## Voz e música
- **Voz:** Kokoro `am_onyx`, velocidade 0.95, local (memória "Voz oficial: Kokoro am_onyx").
- **Música:** suspense, nunca cômica. Uma faixa sob a narração, com ducking. Piloto: *Interloper* (Kevin MacLeod, CC BY 4.0), ganho 0,14. Crédito na descrição.

## Paleta (fixa em todo vídeo)
| Papel | Cor | Uso |
|---|---|---|
| Fundo | `#111214` grafite neutro, radial sutil até `#1b1d20` | toda cena; sem grade, sem holograma, sem partícula |
| Texto principal | `#ece8e1` | títulos, números, nomes |
| Texto secundário | `#c8c3ba` | frases de apoio, subtítulos |
| Rótulos | `#a8a29a` | rótulos em caixa-alta; não têm cor própria |
| Fonte da informação | `#86817a` | linha "SOURCE · …" |
| **Golpe / perda / dano** | vermelho `#d0402f`; barras `#b8463b` | só no golpe e no que ele custou |
| **Regra nova / proteção** | verde-sálvia `#7fb08a` | só quando a lei ou a proteção entra |
| Neutro de gráfico | `#5a5c60` | barras que não são o destaque |
| Papel de documento | `#ece4d0`, texto `#1d1a14` | trechos de lei, ordem, transcrição |
| Marca-texto | `#f2d24b` | só dentro do papel de documento, sobre o nome ou a frase-chave |

**Regra da cor:** a cor diz em que parte da história estamos. Vermelho é golpe, verde é a regra. Nunca use vermelho e verde como enfeite nem os dois para a mesma coisa.

**Proibido:**
- teal, ciano, magenta, âmbar de holograma, neon;
- brilho (glow), partículas, grade de fundo;
- mais de uma cor por gráfico, fora o destaque;
- logo recolorido.

**Cor de terceiros:** logo, selo e foto entram com a cor original, em cartão `#ece4d0` ou numa moldura.

## Tipografia
| Elemento | Fonte | Peso e tamanho em 1080p | Cor |
|---|---|---|---|
| Títulos (impacto, capítulo, nome grande) | **Anton**, caixa-alta | 120 (título), 76 (subtítulo), 72 (nome) | `#ece8e1`; subtítulo `#c8c3ba` ou a cor do ato |
| Números | **Inter 700**, algarismos tabulares | 150–170 no cartão, 54 nas barras | `#ece8e1`, sem brilho |
| Rótulos | **Inter 600**, caixa-alta, espaçamento 0,2em | 24–26 | `#a8a29a` |
| Frases e textos | **Inter 400** | 30–38 | `#c8c3ba` |
| Lower-third | Inter 600 40 (título) + Inter 400 30 (linha 2) | | `#ece8e1` / `#c8c3ba` |
| Fonte da informação | Inter 500, caixa-alta, espaçamento 0,16em | 20 | `#86817a` |
| Documento (lei, ordem, transcrição) | **Courier Prime** 400/700 | 30 (corpo), 24 (cabeçalho) | `#1d1a14` no papel |

- Números nunca em Anton.
- Courier Prime só dentro do papel de documento.
- Fontes em `fonts/`, licença OFL.

## Marcador de ato (assinatura do canal)
- Fica no canto superior esquerdo (x 96, y 70): `THE SCAM · THE CASE · THE RULE`, em Inter 600 20 px, espaçamento 0,22em.
- O ato atual fica aceso, com uma bolinha: vermelha no SCAM, cinza no CASE, verde no RULE. Os outros ficam a 55% de opacidade.
- Aparece nas cenas de gráfico, número e imagem.
- Não aparece no capítulo, na abertura, no cartão final nem no papel de documento em tela cheia.

## Animação
- **Câmera:** foto e reconstrução só com zoom centrado lento (100→108). Nunca deslize lateral.
- **Entradas:** ease-out-expo (0.16, 1, 0.3, 1). Movimentos: ease-in-out-quart (0.76, 0, 0.24, 1). A saída é 40% mais curta que a entrada.
- **Ordem:** uma ação principal por cena; o resto entra 100 a 200 ms depois.
- **Números (N1):** sem contador. O número já certo sobe 0,4 s de trás de uma máscara, na palavra falada.
  - Logo depois, um traço fino de ~520 px corre por baixo em 0,5 s.
  - A frase entra +0,25 s depois e a linha de fonte, +0,4 s.
- **Contas:** cada termo entra pronto, no tempo da fala (80,000 × $1,000 = $80M).
- **Barras:** a barra cresce em 0,6 s e o valor aparece pronto quando ela para. Uma cor por gráfico: vermelho em dado do golpe, verde em dado da lei, neutro no resto, e um destaque opcional.
- **Lower-third:** fio vertical de 4 px à esquerda (cor do ato; neutro por padrão), sem caixa nem vidro.
- **Reconstrução:** etiqueta `ILLUSTRATION` no canto superior esquerdo da imagem.
- **Proibido:** contador que sobe de zero, brilho, partícula, lens flare, tremor, texto que se mexe enquanto é lido, tudo surgindo junto.

## Recortes de notícia e de página oficial (obrigatório)
Pedido do Maiquel em 02/11/2026, depois do ep01 aprovado: recortes reais dão realismo e dinamismo. Vale também para o The Cracked Ledger, com as diferenças em [`CRACKED_LEDGER.md`](CRACKED_LEDGER.md), seção "Recortes".
- **Quantidade:** pelo menos 1 recorte por capítulo, 6 a 10 por vídeo. Entra nos momentos em que a fala cita um ato com data: multa, ordem, audiência, lei assinada, decisão. Vale também quando a imprensa noticiou o fato.
- **Ordem de preferência:**
  1. página oficial do governo dos EUA (fcc.gov, ftc.gov, govinfo.gov, congress.gov, justice.gov), que é domínio público;
  2. manchete de imprensa.
- **Recorte só da manchete** (Maiquel, 02/11): nunca anúncio, menu, barra lateral ou etiqueta de seção. O `web_clip` sem `crop` já recorta justo na caixa da manchete do .json; a data vai no rótulo de cima (`site` · `date`). `crop` só para outro trecho do documento, e ainda sem propaganda.
- **Imprensa:** só a manchete. Nunca a matéria inteira, a foto da matéria ou o anúncio. Crédito na linha SOURCE com veículo e data. No máximo 3 por vídeo.
- **Captura:** `python tools/web_clip.py <url> <projeto>/assets/clips/<nome>.png "texto a marcar"`.
  - Gera um print em 2x e um .json com a caixa do texto, a URL e a data da captura.
  - Banner de cookies: recusar.
  - Página bloqueada para robô (ex.: commerce.senate.gov): usar a cópia oficial no GovInfo.
- **Na tela:** modelo `web_clip` da ec_lib, com a página como cartão claro sobre o grafite.
  - Marca-texto #f2d24b na manchete ou na data, no tempo da fala.
  - Zoom centrado lento, sem deslize lateral.
  - Linha SOURCE com site e data.
- **Conferir no quadro:** a manchete dá para ler no celular e o recorte é da página certa (URL no .json). Nenhum dado pessoal de terceiros aparece (e-mail, telefone de pessoa física).
- **Não substitui:** foto de pessoa (§3 das Universais), número em cartão N1 e gráfico. O recorte é mais uma camada, não a única.
- **Moldura:** papel `#ece4d0` em volta do recorte (padrão do tema desde 02/11; `"paper": false` volta ao branco).

## Mapas, Motion e Shorts (sempre que possível)
Aprovado pelo Maiquel em 02/11/2026: o mesmo nível de mapas, gráficos e Motion do Tricolor (Ledger), com a identidade deste canal. Parâmetros exatos: `puzzles/ec_lib/README.md`, seção do tema. Exemplo pronto: `scamlaw/_teste_ec_mapa_clip/` (horizontal) e `scamlaw/_teste_ec_mapa_clip_v/` (vertical).
- **Mapa (`us_map`):** em todo vídeo em que a fala cita estados (lei estadual, onde o golpe pegou, onde a regra mudou primeiro). Estados acendem na palavra falada: vermelho = golpe, verde = regra, cinza = neutro. Número N1 e rótulo por estado; `dx`/`dy` em estado pequeno.
  - Uma cor por mapa: se precisar mostrar golpe e regra, faça dois mapas seguidos. O build avisa quando um mapa mistura as duas.
  - Crédito do Census em `entities/credits.json` do episódio.
- **Clipe Motion (`clip`):** cena de explicação feita no HyperFrames entra como .mp4 no `scenes.json`, sem sair da ec_lib. Renderizar o clipe no formato do vídeo (1920x1080 no longo, 1080x1920 no Short) e a 30 fps, na paleta e na tipografia deste canal (não as do Ledger).
- **Recorte com moldura de papel:** ver a seção acima; vale também nos Shorts.
- **Shorts (chamariz do longo):** roteiro e voz próprios, 1080x1920, nunca corte do longo.
  - `"format": "vertical"` e `"lufs": -14` no `scenes.json`.
  - Gancho nos 2-3 s iniciais; 1 número forte, 1 virada, fecho chamando o vídeo completo; 45 a 90 s.
  - Montar e ler os avisos do build. "AVISO 0,3 s" = bloco sem nada na tela nos primeiros 0,3 s: corrigir antes do render.
  - Legenda de 3 palavras e linha SOURCE; todo bloco com imagem, recorte, mapa ou cartão; sem pulsação nem tremida.
  - Só sai Short com nota ≥ 8. Legenda, chamada e exatamente 5 hashtags. Nada é publicado sem OK do Maiquel.

## Pessoa sem foto livre
Segue a regra universal, §3 de `REGRAS_UNIVERSAIS.md`. No canal:
- **T1, nome no documento:** trecho real do documento oficial (ordem, decisão, lei) em papel `#ece4d0`, com o nome em marca-texto.
  - Nome em Anton à direita, com rótulo ("NAMED BY THE FCC") e papel em uma linha.
  - Câmera com zoom centrado no nome.
- **T2, lower-third sobre reconstrução:** nome e uma linha de contexto sobre a cena reconstruída, sem rosto, com `ILLUSTRATION`.
- **T3, registro público:** cabeçalho real da transcrição ou do processo (ex.: "STATEMENT OF …") e a citação exata.
- **Proibido:** cartão de iniciais e qualquer texto do tipo "Photo not available".
- **Réus:** só por documento, cartão ou silhueta. Nunca foto de ficha policial nem rosto gerado.

## Abertura e fecho
- **Abertura:** `intro` com kicker "THE RULE CHANGED" e o título do caso.
- **Fecho:** fala pedindo inscrição e comentário (qual golpe investigar a seguir).
  - Cartão final "THE RULE CHANGED" com SUBSCRIBE e a linha "THE SCAM · THE CASE · THE RULE".
  - Fica parado 6 a 8 s.

## Pipeline e biblioteca
- **Biblioteca:** `puzzles/ec_lib`, horizontal, com o tema `rulechanged`.
  - Tema entregue; parâmetros de cada modelo em `puzzles/ec_lib/README.md`, seção "Tema rulechanged" (`web_clip`, `us_map`, `clip`, `lufs`).
  - Não editar a biblioteca: pedir à sessão dona.
- **Projeto:** `scamlaw/<epNN_tema>/`, com `narration.json`, `scenes.json`, `assets/img`, `entities/credits.json`, `research.md` e `logs/gate-N.md`.
- **Processo:**
  - skill `video-gate` (Gates 1 a 6), em modo orquestrador;
  - imagens: FLUX local (`tools/local_img.py`); retrato oficial só se for domínio público.
- **QA:**
  - folhas de quadros do render final e clipe a 6 fps nas animações;
  - checar a paleta: nenhuma cor fora da tabela, a não ser em logo ou foto de terceiro.
  - Obs.: `tools/palette_check.py` é do Ledger e ainda não lê projeto `scamlaw/`.

## Título, capa e descrição
- **Título e capa vendem o engano que motivou a lei, sem números** (Maiquel, 01/11). A fórmula de "valor exato" do Ledger não vale aqui; os números ficam dentro do vídeo.
  - Ep01: título "The Fake Local Number That Changed the Law", capa "IT LOOKED LOCAL. / IT WASN'T.".
- Seguem também o checklist de `research/canal_golpes_lei/PESQUISA.md`: factual e cumprido pelo vídeo, sem cadáver, choro ou rosto de vítima.
- **Descrição:** fontes primárias, capítulos, "educational, not legal advice" e links de denúncia.
- **Rótulos do upload:** AI use = Sim; checagem de privacidade.
- **Ep01 no YouTube:** `czjOFwcyQjU`, agendado público para 02/11 19:00 ET (versão com recortes de notícia). O envio de 01/11 sem recortes foi apagado.
- **Ep02 no YouTube:** `e8Z_ZhxGjuQ`, "Why Your Bank Says \"You Sent It Yourself\"", agendado público para 03/11 19:00 ET.
- **Tela final:** o Studio exige pelo menos 1 vídeo ou playlist; só o botão de inscrição não salva. Padrão desde 02/11: playlist pública "The Rule Changed" sobre a caixa NEXT VIDEO do cartão final + inscrição sobre o botão SUBSCRIBE, do início do cartão até o fim. Todo episódio novo entra na playlist. O Studio não importa a tela final de outro vídeo: adicionar Playlist e Subscribe, pôr o início no 1º segundo do cartão final e arrastar sobre as caixas (no ep02: playlist a 51%/27% do quadro com 39% de largura; inscrição centrada no botão, 28%/48%).
- **Ritmo (Maiquel, 02/11):** longo às 19h ET e Short às 22h ET, todo dia.
- **Busca no YouTube:** skill principal `youtube-seo` (decisão de 02/11); `claude-youtube` avaliada e não instalada.

## Conta e Chrome
- Canal `UCh9ek7ZsZO3DptaNSPdqRTA` (era do Walt; rebranding em 01/11; vídeos do Walt privados, nunca apagados).
- Chrome de automação `browser_profile_walt`; a porta muda quando o Chrome trava (9337 em 01/11).
- No Studio, o Playwright travou; funcionou CDP direto (Node). Os botões Next e Save só respondem a `.click()` por JS; as tags precisam de Enter para virar etiqueta.
- Navegar com edição não salva abre "Reload site?" nativo e trava a aba: salvar antes de sair da página.
- O YouTube só deixa trocar o nome 2 vezes a cada 14 dias.

## Deu certo / não deu
| Data | Resultado | Lição |
|---|---|---|
| 01/11 | não deu | 1º render do piloto com o visual do SYW (teal, magenta, brilho, contador): reprovado; daí veio a identidade "Golpe → Regra" |
| 01/11 | não deu | título com número e multa na capa: reprovado. Título e capa vendem o engano, sem número |
| 01/11 | não deu | render novo ainda com medidor magenta e contador (7:15), cartão final sem a linha dos atos, linha de fonte apagada: tudo corrigido antes do envio |
| 01/11 | deu certo | ep01 (10:35) enviado privado com kit completo; verificação do YouTube sem problemas |
| 01/11 | deu certo | render da ec_lib em partes retoma de onde parou depois de queda |
| 02/11 | pedido | recortes reais de notícia e página oficial em todo capítulo (seção "Recortes") |
| 02/11 | deu certo | mapa dos EUA, clipe Motion como cena e recorte com moldura de papel aprovados ("incrível"): usar sempre que possível (seção "Mapas, Motion e Shorts") |
| 02/11 | não deu | Kokoro leu "Coned Billing" como "Cone Billing" e "ic3" como "ik3": escrever na narração como se fala ("Con Ed Billing", "I C three") e manter a grafia real na tela; conferir nomes próprios no ASR |
| 02/11 | não deu | envio do master de 1 GB pelo CDP estourou os 30 s do `DOM.setFileInputFiles` e travou a aba; com tempo limite de 10 min passou. Conferir a lista do Studio antes de reenviar |
| 02/11 | deu certo | ep02 (9:06) do pedido ao agendamento na mesma tarde (~4 h): pesquisa e Motion em paralelo com Sonnet, roteiro Opus, troca de imagem no meio de bloco para nenhum plano parado passar de 8 s |
| 02/11 | deu certo | Maiquel assistiu ao ep02: "Estamos chegando a um nível de produção muito bom. Nenhum ajuste identificado." Manter o padrão do ep02 (6 capítulos, 9 recortes oficiais, 2 clipes Motion, mapa, troca de imagem antes de 8 s) |
