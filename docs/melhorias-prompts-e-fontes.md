# Melhorias nos prompts de cena e nas fontes dos vídeos
*17/10/2026 · feito pelo Claude no PC do Dark Studio, sem nenhuma API paga (nada foi gerado no Grok, ChatGPT ou YouTube)*

## Resumo em 1 minuto
- Revisei os prompts de cena dos 5 vídeos (WeWork, FTX, First Brands, SVB e Lehman): 376 cenas no total, com amostras de começo, explicação e clímax de cada um.
- O maior problema: muitas cenas **criam clima mas não explicam** a frase narrada. Em vez de mostrar a ideia (alavancagem, dinheiro saindo, quem deve a quem), mostram "alguém olhando telas e papéis".
- Mudei o programa para os **próximos vídeos**: novas regras para o ChatGPT escrever as cenas, um modelo de prompt do Grok sem contradições e sugestões automáticas de gráfico.
- Nas fontes, troquei tudo o que ainda vinha do Windows (Arial, Impact, Georgia) por **fontes livres (OFL)**, organizei o vídeo em **duas famílias** (Playfair Display para títulos e Inter para o resto) e corrigi números, margens, contraste e legendas.
- Os 4 vídeos prontos **não foram refeitos**. O Lehman (pausado no meio das cenas) já usa o novo modelo nas cenas que faltam, quando o Grok automático for retomado.

---

## Parte 1: prompts de cena

### O que estava fraco (com exemplos reais)

**1. A imagem não explica a frase (o defeito mais comum).**
WeWork, cena 25. Narração: "cerca de 47 bilhões de dólares em aluguéis futuros mínimos, ao longo de anos".
- Antes: *"Dark cinematic 16:9 long corridor of locked office doors receding into darkness, no logos, no text, no people."*
- Um corredor escuro não diz nada sobre 47 bilhões de aluguel. O certo aqui é um **gráfico de escala** com o valor, ou uma metáfora física (ex.: uma mão assina um contrato enquanto uma corrente de chaves iguais se desenrola pela mesa e sai do quadro).

First Brands, cena 18. Narração: promotores dizem que Patrick James recebeu centenas de milhões em contas pessoais.
- Antes: *"Over-the-shoulder ... an anonymous analyst reviewing a contemporary financial workstation ... Two monitors show only abstract, text-free transaction blocks ..."*
- "Um analista olhando telas" apareceu em 13 de 47 cenas do First Brands, 12 de 59 do Lehman e 10 de 54 do SVB. O caminho melhor é o **mapa do dinheiro** (se houver fonte) ou uma metáfora (ex.: moedas numa esteira de fábrica desviam por uma calha lateral para um único cofre trancado).

**2. Coisa demais acontecendo em um clipe de ~6 a 8 segundos.**
SVB, cena 2: clientes de costas com celulares, autoridades entrando pela porta e um funcionário trancando a entrada, tudo no mesmo clipe. O Grok costuma fazer só uma dessas ações direito (ou misturar as três).

**3. O sentido dependia de texto na imagem, e o Grok erra letras.**
Cenas que citam tela, gráfico em monitor, papel, pasta, calendário ou placa: 41 de 47 (First Brands), 49 de 59 (Lehman) e 49 de 54 (SVB). Exemplo: SVB, cena 4, *"three unmarked calendar sheets"* para explicar "48 horas". Sem as datas escritas, o calendário não explica nada. Com datas, o Grok escreveria errado.

**4. Cenário repetido.**
No First Brands, 16 das 47 cenas de IA são tribunal, corredor ou audiência. As cenas 45, 54 e 63 são quase iguais: homens de terno, de costas, em corredor ou sala de tribunal, com lente de 35 a 40 mm.

**5. O modelo de prompt se contradizia.**
- Todo prompt dizia *"Composition: wide cinematic framing"*, até em close-up de 85 mm (Lehman, cena 39).
- Todo prompt dizia *"moody low-key ... cold teal"*, até no ato 1, que pede luz dourada de euforia.
- Em vídeo, vinham dois movimentos ao mesmo tempo: o da cena (*"unsettled handheld drift"*, câmera na mão inquieta) e o genérico *"gentle dolly-in ... smooth and stable"* (aproximação suave e estável). Exemplo: Lehman, cena 55.
- Sem humor definido, toda cena recebia *"tense, investigative"*, até nas de euforia.
- Nos projetos antigos, aparecia *"Story beat: True."* (um campo vazio virava a palavra "True") e pontos duplos (*"deadline.."*).
- O texto do arco emocional falava de *"busy warehouses and trucks"* (do First Brands) para todos os vídeos, inclusive Lehman e SVB.

**6. Proibições dentro da descrição.**
Média de 1 a 3 "no/without" por cena (WeWork: 3 por cena). Exemplo do Lehman, cena 55: *"No recognizable officials, readable text, agency emblems, or corporate logos."* Isso já está no bloco "Avoid" do fim. Repetido no meio da descrição, rouba atenção da ação e às vezes faz o Grok desenhar justamente o que foi proibido.

**7. Grok gerando cena que vira gráfico.**
Cenas com mapa do dinheiro ou queda animada viram gráfico em tela cheia, mas mesmo assim iam para o Grok. No SVB, as cenas 40 e 55 foram geradas no Grok e depois substituídas pelo gráfico: limite gasto à toa.

**8. Botão "Copiar prompt completo"** (tela de cenas): ainda montava o prompt antigo com **"Netflix-style"**, que o seu padrão proíbe. O servidor já não usava o termo, mas o botão sim.

### O que mudou (vale para os próximos vídeos)

**Na etapa "Prompts Grok" (o ChatGPT escrevendo cada cena), regras novas:**
1. **Explicar, não decorar:** com o som desligado, a imagem tem que explicar a frase. Para cada cena, ele escolhe um recurso: reconstrução (o fato real, no lugar e na época certos), metáfora física, impacto humano ou ambientação.
2. **Ideias financeiras viram objetos.** Exemplos dados a ele: 31 caixas em cima de uma tábua fina para "31 para 1"; água passando de um tanque para outro para dinheiro que sai; uma chave emprestada que vai e volta para um repo.
3. **Um assunto e uma ação** que cabem no clipe, dizendo como a imagem muda do começo ao fim.
4. **Nada que dependa de texto:** papel e tela só em branco, desfocados ou de costas.
5. **Uma lente e um movimento de câmera**, ligados à emoção. Nunca o mesmo plano nem o mesmo cenário em mais de 2 cenas seguidas, inclusive na passagem de um lote de 20 cenas para o outro (antes cada lote era escrito sem saber do anterior).
6. **Época certa** de objetos, carros e roupas.
7. **Bíblia visual:** no começo, ele descreve a silhueta do protagonista, a sede e os lugares que se repetem, e reaproveita as mesmas palavras em todas as cenas (assim as cenas parecem do mesmo filme).
8. **Sugestão de gráfico:** quando a frase seria melhor explicada por linha do tempo, barras, escala, mapa do dinheiro, queda de valor ou mapa de relações, ele marca a cena e diz quais números ou datas o gráfico precisa. Aparece na Validação como "N sugestão(ões) de gráfico" (só aviso: o gráfico nunca é inventado sem fonte).
9. Descrições de 40 a 70 palavras (antes 60 a 90), sem as frases "no logos / no text".

**No modelo do prompt do Grok (vale também para as cenas que faltam no Lehman):**
- O enquadramento segue o tipo de plano: close-up, macro, aéreo, de cima, travelling etc.
- Luz e cor seguem o ato: dourado (1), azul acinzentado (2), duro e dessaturado (3), suave no final.
- Em vídeo, **um movimento só** (o da cena) e "uma ação simples que termina dentro do clipe, sem cortes, sem deformar".
- Frases de proibição saem da descrição (o bloco "Avoid" continua igual). Tudo o que vem depois de "STRICT:" (suas correções manuais) fica intacto.
- Nova frase de proteção: papéis, telas e placas em branco, desfocados ou de costas; pessoas só de costas ou em silhueta.
- O botão "Copiar prompt completo" agora gera exatamente o mesmo prompt do servidor. Conferi nas 376 cenas: 0 diferenças.
- Ao iniciar o Grok automático, as cenas **sem mídia** recebem o prompt no modelo novo. As prontas guardam o prompt com que foram feitas.
- O Grok automático pula todas as cenas que viram gráfico em tela cheia (inclusive mapa do dinheiro e queda animada).
- A Validação avisa **gráfico com uma barra só**, que a sua regra proíbe. O Lehman tem 3 (cenas 16, 25 e 69) e o SVB, já publicado, tem 6.
- Mantido como você escolheu: a divisão vídeo/imagem, a regra de 30+ cenas em vídeo e o ato 3 em vídeo.

### Lehman: 3 exemplos antes e depois (gerados aqui, sem API)
Só o modelo mudou. A descrição de cada cena é a mesma que o ChatGPT já tinha escrito. Mostro só as partes que mudaram:

**Cena 39 (imagem, close-up 85 mm, regulador britânico trava a venda ao Barclays)**
- Antes: *"... No likenesses or logos. Mood: A regulatory requirement becomes an insurmountable deadline.. Camera: ... Composition: wide cinematic framing, strong leading lines ... Style: dark cinematic documentary, moody low-key lighting ... cold teal-and-amber contrast ..."*
- Depois: *"... Mood: A regulatory requirement becomes an insurmountable deadline. Camera: ... Composition: close-up, one subject filling most of the frame, shallow depth of field, soft background. Style: photorealistic cinematic documentary reconstruction ... Light and color: cool blue-grey light, low-key contrast, deepening shadows ... Papers, screens and signs are blank, blurred or turned away; people only from behind or in silhouette."*

**Cena 55 (vídeo, empréstimo de emergência à AIG)**
- Antes: *"... No recognizable officials, readable text, agency emblems, or corporate logos. ... Camera move: 28mm lens, unsettled handheld drift. Motion: slow cinematic camera movement (gentle dolly-in or slow parallax pan) ... smooth and stable ..."* (dois movimentos que se contradizem)
- Depois: a frase de proibição sai. *"... Light and color: hard light and deep shadows, desaturated cold palette with small red accents. Camera move: one continuous move only: 28mm lens, unsettled handheld drift. One simple, clearly visible subject action that completes within the clip, subtle atmospheric motion, realistic physics, no cuts, no morphing."*

**Cena 67 (vídeo, o que é um repo)**
- Antes: *"Composition: wide cinematic framing"* num close-up de 85 mm, mais o movimento genérico por cima do *"slow lateral tabletop move"*.
- Depois: *"Composition: close-up ... Camera move: one continuous move only: 85mm lens, slow lateral tabletop move. One simple, clearly visible subject action ..."*
- Com as regras novas da etapa "Prompts Grok", a própria descrição também mudaria. Exemplo escrito por mim (o ChatGPT não foi chamado): *"Close-up on a 2008 desk: one anonymous hand slides a locked case of bonds across to another hand, which pushes back a thick envelope of cash; moments later the case slides back and the envelope returns. 85mm, slow lateral move. A loan secured by the case, not a sale."* Uma ação, que explica o repo sem nenhum texto na tela.

Observação honesta: o prompt completo ficou um pouco mais longo (cerca de 10 a 25 palavras a mais), porque ganhou a linha de luz e cor e a frase de proteção. A descrição da cena ficou mais curta e sem contradições. Não testei no Grok, porque gerar gastaria o seu limite.

---

## Parte 2: fontes

### O que havia
| Onde | Fonte | Problema |
|---|---|---|
| Gráficos e cartões (estilo v2) | Playfair Display, Inter, Courier Prime, Caveat, Bebas Neue | 5 famílias misturadas; valores grandes em Playfair, cujos algarismos sobem e descem ("$639" desalinhado) |
| Contadores animados | Playfair | Os números mudavam de largura e o valor "balançava" durante a contagem |
| Logo e cartões de reserva (gfx.py) | Arial, Impact e Georgia do Windows | Fontes da Microsoft, sem licença livre para distribuir |
| Capas (tools/thumbs_new.py) | Impact (Windows) | Mesmo problema de licença |
| Legenda queimada | Arial 22, contorno 2 | Grande demais e com fonte do Windows |
| Legendas SRT | – | Linhas de até 47 caracteres (28 acima de 42) e a numeração recomeçava em cada cena (defeito antigo) |
| Fonte da informação no rodapé | 3,7% da borda | Fora da área segura (5%), embaixo da barra do YouTube |

### O que ficou (todas SIL OFL: livres para uso comercial no YouTube)
| Uso | Fonte | Por quê |
|---|---|---|
| Títulos (capítulo, nome de pessoa, manchete, citação) | **Playfair Display** | Serifada de revista, dá o ar documental "premium" que o canal já tinha |
| Todo o resto: rótulos, textos, fontes, legendas e **todos os números** | **Inter** | Feita para telas, legível pequena, algarismos alinhados; agora desenhados em largura fixa (o contador não balança) |
| Só dentro de objetos de cena | Courier Prime (documento datilografado), Caveat (anotação à mão), Bebas Neue (carimbo "EXHIBIT") | Fazem parte do objeto, não da interface |
| Capa | **Anton** (nova, baixada do repositório oficial do Google Fonts) | Parecida com a Impact, mais limpa e livre |

As fontes ficam em `fonts/`, com a licença de cada uma em `fonts/licenses/`.

**Outras correções de tipografia:**
- Rótulos em caixa alta (CHAPTER 1, SOURCE, títulos de gráfico) com espaçamento entre letras, como nos documentários profissionais.
- "CHAPTER 1" passou de Bebas para Inter espaçada, e as datas da linha do tempo para Inter com algarismos de largura fixa.
- Título de capítulo com linhas equilibradas: antes "Act I — A Name Built to / Last" deixava uma palavra sozinha na última linha.
- Margens: fonte da informação e selo de fonte subiram para dentro da área segura de 5%. O destaque de valor saiu da borda direita (de 3,6% para 5,2%).
- Contraste: o título vermelho da queda animada ficou num vermelho mais claro (5,4:1 em vez de 3,7:1). Os demais textos já passavam (branco 15,6:1, âmbar 9,2:1, fonte 9,4:1).
- "31times" virou "31×", e as unidades em palavra ganharam espaço.
- O contador mostra as casas decimais do valor final durante toda a contagem ($0.97, e não $0.3 no meio).
- Legendas: no máximo 2 linhas de 42 caracteres, sem terminar linha em "the/of/and", quebra preferindo vírgula e numeração corrigida. Resultado nos 5 vídeos: linhas acima de 42 caíram de 28 para 6 (máximo 45), e as legendas com menos de 1,5 s ficaram iguais (20 de 1.036, porque a narração é rápida).
- Legenda queimada (só se `burn_subtitles` estiver ligado; o YouTube usa o SRT com a fonte dele): Inter branca com contorno e sombra, ~10% acima da borda de baixo.
- Defeito pequeno corrigido: quando a Validação encurtava o nome de uma fonte, punha "â€¦" em vez de "…".

### Imagens de teste (feitas offline)
- `output_yt/fontes_teste_1_titulo.png`: cartão de capítulo
- `output_yt/fontes_teste_2_grafico.png`: gráfico de barras com números alinhados
- `output_yt/fontes_teste_2b_callout.png`: destaque de valor + nome da pessoa + selo de fonte sobre uma cena real do Lehman
- `output_yt/fontes_teste_2c_contador.png`: queda animada (quadro final)
- `output_yt/fontes_teste_3_legenda.png`: legenda queimada + nome da pessoa, com as linhas de área segura (5% e 10%) desenhadas só para conferir
- `output_yt/fontes_teste_4_capa.png`: texto de capa em Anton

Também rodei todos os 145 gráficos e cartões do First Brands, SVB e Lehman numa pasta temporária, com 0 erros (nada nos projetos foi alterado).

---

## O que você precisa fazer
1. **Reiniciar o app:** feche a janela do servidor e abra o `iniciar.bat` de novo. No navegador, aperte **Ctrl+F5** na página do Dark Studio, para carregar o botão de copiar prompt novo.
2. **Lehman:** é só retomar o Grok automático. As cenas que faltam recebem o prompt novo sozinhas, sem custo (as que viram gráfico continuam fora do Grok).
   - Opcional: rodar de novo a etapa "Prompts Grok" no Lehman reescreve as descrições com as regras novas (metáforas, bíblia visual, sugestões de gráfico). Usa o ChatGPT só para texto (poucos centavos) e reescreve a descrição de todas as cenas, mas as mídias já prontas ficam como estão.
3. **Lehman, cenas 16, 25 e 69:** gráfico com uma barra só. Trocar por um gráfico de escala ou comparar com outro valor real.
4. **Próximo vídeo:** é só seguir o fluxo normal. As regras novas entram sozinhas na etapa "Prompts Grok".
5. **Para desfazer**, os arquivos originais estão em `backups/pre-prompts-fontes-20261017/`.

Arquivos alterados: `app.py`, `pipeline.py`, `grok_worker.py`, `static/app.js`, `gfx.py`, `gfx2.py`, `gfx_anim.py`, `montage.py`, `tools/thumbs_new.py` e `PADRAO_VIDEOS.md` (novas seções "Prompts de cena" e "Fontes e tipografia"). Novos: `fonts/Anton-Regular.ttf`, `fonts/licenses/` e este relatório. Nada foi enviado ao GitHub (sem commit).
