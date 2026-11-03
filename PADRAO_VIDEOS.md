# The Cracked Ledger — Padrão de produção de vídeos

> **Regras organizadas em 01/11/2026:** o que vale para todo canal está em [`REGRAS_UNIVERSAIS.md`](REGRAS_UNIVERSAIS.md); a identidade de cada canal está em [`canais/`](canais/) (mapa em [`canais/MAPEAMENTO.md`](canais/MAPEAMENTO.md)). Este arquivo continua valendo como detalhe do The Cracked Ledger.

> **Antes de qualquer vídeo, siga o checklist único: [CHECKLIST_VIDEO_YOUTUBE.md](CHECKLIST_VIDEO_YOUTUBE.md).** Ele junta este padrão e o `GEMINI.md` na ordem do pipeline. Erro novo vira regra lá.
Mantido pelo Maiskinho. Atualizado em 17/10/2026 (seções de Título, Tema e Depois de publicar acrescentadas pelo Claude com base em dados do YouTube). Revise/edite à vontade (ex.: com o Claude Code); avise o Maiskinho quando mudar algo.

## REGRA DE OURO N.º 1 (OBRIGATÓRIA ANTES DE QUALQUER CRIAÇÃO DE VÍDEO)
- **SEMPRE TENHA IMAGENS REAIS DAS PESSOAS ANTES DE CRIAR QUALQUER VÍDEO:** Antes de iniciar a renderização de qualquer projeto, **todas as pessoas citadas na narrativa** (cientistas, professores, técnicos, executivos, políticos, juízes, fundadores) devem ter suas fotos reais baixadas e preparadas em `entities/` (preferencialmente em preto e branco de alto contraste documental com restauração/upscale 4x Real-ESRGAN) e vinculadas aos templates `person`, `evidence_doc` (`photo` + `photo_caption`) e `statement` (`photo` + `photo_caption`). Nenhum quadro sobre uma pessoa ou citação de uma pessoa pode ir ao ar sem a foto real dela.

## Canal
- Documentários de Business & Finance em inglês, @thecrackedledger.
- Duração alvo: 10–12 min. Agenda: seg/qua/sex/dom às 18:00 BRT.
- Nada é publicado se a Validação falhar.

## Pipeline (ordem obrigatória)
Ideia → Pesquisa → Roteiro → Imagens reais → Prompts Grok → Cenas → Validação → Montagem → Publicação
1. **Pesquisa** completa por capítulo, com fontes: pessoas (inclusive juízes e promotores), empresas, órgãos, valores e linha do tempo.
2. **Roteiro** escrito pelo ChatGPT a partir da pesquisa.
3. **Imagens reais** das pessoas e empresas, de fontes válidas e licenciadas. Consultar primeiro a biblioteca local de entidades.
4. **Prompts Grok** ricos, cena a cena, baseados no roteiro.
5. **Validação**: todo nome, sigla e valor narrado precisa ter um visual correspondente naquele momento. Também barra logos, selos, bandeiras e símbolos religiosos dentro das cenas do Grok, e erros de digitação no texto da tela.

## Ferramentas
- ChatGPT/OpenAI: só texto, narração (voz onyx) e checagem de imagens na Validação (só análise, não gera nada).
- Grok Imagine: todas as imagens e vídeos, em 1080p (1920x1080), com 720p de reserva.
- Só automatizar o perfil do Chrome do Dark Studio (CDP na porta 9333). Nunca fechar o Chrome da Livia (Profile 10). Nunca imprimir nem commitar chaves.

## Visuais obrigatórios
- Toda empresa, órgão ou pessoa citada aparece na tela: cartão com logo, foto licenciada da sede, selo oficial, ou foto/cartão de nome. Sempre que existir, usar o logo de todas as empresas envolvidas.
- **Fotos de pessoas:** preferir licença livre (ex.: Wikimedia Commons, domínio público). Se não houver, usar foto de jornal com crédito, em uso justo: breve, só dentro do cartão da pessoa. Nunca rosto gerado por IA de pessoa real.
- Também entram: linhas do tempo, gráficos com dados reais, trechos de documentos destacados, citações com fonte, mapas de relações, comparações de escala, cartões de capítulo, recriação de manchetes, fontes no canto da tela, mapa animado do fluxo do dinheiro e gráfico animado da queda de valor. Nunca gráfico com uma barra só.
- Estilo dos cartões: artístico e documental, com texturas de papel e documento, recortes orgânicos, luz e sombra, e animação de entrada. Nada de caixas quadradas simples.
- Um cartão por nome em cada cena, sem duplicados.

## Cenas do Grok
- A maioria das cenas é vídeo: 30 ou mais de cerca de 47.
- A emoção acompanha o impacto financeiro: euforia no começo, tensão no meio, impacto humano no colapso.
- Só pessoas anônimas: de costas, silhuetas, sem rosto definido.
- Sem logos, emblemas ou bandeiras, com paredes lisas e sem marca. Nunca escrever "Netflix-style" nos prompts.

## Prompts de cena (17/10/2026)
Cada prompt do Grok precisa **explicar** a frase narrada, não só criar clima. Teste: com o som desligado, dá para entender a frase olhando a imagem?
- **Um assunto, uma ação.** Cada clipe tem ~6 a 8 s: uma pessoa ou objeto principal fazendo uma coisa visível, com começo e fim. Nada de três ações ao mesmo tempo.
- **Ideia financeira abstrata vira objeto concreto.** Alavancagem, dívida, depósitos, dinheiro saindo, quem deve a quem: usar uma metáfora física (ex.: 31 caixas em cima de uma tábua fina para "31 para 1"; água passando de um tanque para outro para dinheiro que sai). Nunca "um analista olhando telas ou papéis".
- **Quando tem número, data em sequência ou dinheiro entre partes, o gráfico explica melhor** (linha do tempo, barras, escala, mapa do dinheiro, queda de valor). O programa sugere isso na Validação ("sugestão de gráfico"), sem bloquear.
- **O sentido nunca depende de texto na imagem.** O Grok erra letras: papel, tela, placa e calendário só aparecem em branco, desfocados ou de costas.
- **Câmera:** lente e **um** movimento só, ligado à emoção (parado, aproximação lenta, travelling lateral, recuo revelando, câmera na mão). O enquadramento escrito no prompt segue o tipo de plano (close-up não recebe mais "plano aberto").
- **Variedade:** nunca o mesmo tipo de plano nem o mesmo cenário em mais de 2 cenas seguidas (ex.: nada de três corredores de tribunal em sequência).
- **Luz e cor seguem o ato:** ato 1 dourado e quente, ato 2 azul acinzentado, ato 3 duro e dessaturado, final suave e calmo.
- **Continuidade:** cada vídeo ganha uma "bíblia visual" (como é a silhueta do protagonista, a sede, os lugares que se repetem), reaproveitada com as mesmas palavras.
- **Época certa:** celulares, carros, telas e roupas da data narrada.
- Cenas que viram gráfico em tela cheia (inclusive mapa do dinheiro e queda animada) não vão para o Grok (não gastam o limite).

## Fontes e tipografia (17/10/2026)
- **Só fontes de licença livre (SIL OFL)**, guardadas em `fonts/` com a licença em `fonts/licenses/`. Nada de Arial, Impact ou Georgia do Windows no vídeo.
- **Duas famílias no vídeo:** **Playfair Display** para títulos (capítulo, nome de pessoa, manchete) e **Inter** para todo o resto (rótulos, textos, fontes, legendas e números).
- Courier Prime (documento datilografado), Caveat (anotação à mão) e Bebas Neue (carimbo) só aparecem **dentro de objetos de cena**, nunca como texto de interface.
- **Capa:** Anton (parecida com a Impact, mas livre) para o texto grande.
- **Números de dinheiro** sempre na Inter, com algarismos alinhados e de largura fixa (os contadores não "dançam"). A Playfair tem algarismos que sobem e descem: boa em texto, ruim em valores grandes.
- **Tamanhos em 1080p:** título 132/96/76, subtítulo 48 a 60, texto 30 a 38, rótulo 24 a 30, crédito de foto 16 ou mais.
- **Rótulos em caixa alta** (CHAPTER, SOURCE, títulos de gráfico) com espaçamento entre letras. Nunca negrito falso nem fonte esticada.
- **Margens:** todo texto fica a pelo menos 5% da borda (área segura). Fonte da informação acima do rodapé, onde fica a barra do YouTube.
- **Contraste:** texto claro sobre fundo escuro com contraste de pelo menos 4,5:1 (o vermelho puro só em formas, não em letra pequena).
- **Legendas (SRT e legenda queimada):** no máximo 2 linhas de 42 caracteres, sem terminar linha em "the/of/and", pelo menos ~1,5 s na tela, Inter branca com contorno e sombra, ~10% acima da borda de baixo.
- **Títulos de capítulo** com linhas equilibradas (sem uma palavra sozinha na última linha).

## Narrativa
Gancho forte, protagonista humanizado, tensão crescente, 3 atos, emoção autêntica, mostrar em vez de contar, ritmo variado e narração expressiva.

### Padrões de retenção (24/10/2026, de 10 vídeos do nicho com 8+ min, últimos 90 dias)
Os que mais retêm (Sriracha, Jaguar, Dollar Shave Club, AirAsia, transporte na Austrália) repetem isto; os fracos (lista genérica, venda disfarçada, especulação) não têm nada disso.
1. **Número concreto na primeira ou segunda frase** (ex.: "49 carros na Europa inteira", "um anúncio de US$ 4.500"). Valor exato, com fonte.
2. **Contradição como motor:** o que a empresa disse contra o que aconteceu. A prévia de abertura já mostra a contradição e promete resolvê-la.
3. **Um conflito central com personagens claros** (vilão e vítima, ou decisão e consequência), num único tema (ex.: confiança). Nada de desvio para assunto vizinho.
4. **Culpa deslocada:** quando a empresa culpa clima, combustível ou mercado, mostrar o que decisão própria causou.
5. **"Quem paga a conta"** tem um trecho próprio perto do fim: trabalhadores, fornecedores, contribuintes, credores, na ordem em que recebem.
6. **Uma pausa útil no meio** que explica algo prático ao espectador (um direito, um mecanismo, uma regra). Não vale repetir pedido de like.
7. **Honestidade explícita:** separar fato, alegação e decisão judicial em voz alta ("é alegação, não decisão"; "aqui o registro é fraco"). Corrigir a manchete quando ela exagera (ex.: "nada foi protocolado").
8. **Fecho que espelha o gancho** (mesma frase, número ou imagem, agora com outro peso) e termina pedindo inscrição, como já manda a regra de QA.
9. **Capítulos com tese dita cedo** (uma frase que diz por que a história deu errado) e uma lição nomeada no fim.
10. **Nada de especulação como fato.** Hipótese só com "pode", atribuída a alguém, e nunca no título nem no gancho. Sem opinião política ou macro sem fonte.
11. **Sem resíduo no texto falado** (marcadores como "TTS script", "Chapter 8" fora do padrão, links de "assista a seguir").
12. **Sem anúncio no meio.** O vídeo não tem patrocinador nem venda de serviço, e pedido de like/inscrição só no fim.

## Áudio
- **Uma música calma só, o vídeo inteiro, sem trocar entre os atos.**
- A música fica sempre bem mais baixa que a narração (abaixa quando a voz entra).
- Música royalty-free, com crédito na descrição (ex.: Kevin MacLeod, CC BY 4.0).

## Título (baseado em dados do YouTube, 17/10/2026)
Fonte: análise de ~2.000 vídeos do nicho (`pesquisa/por-que-canais-dark-dao-views.md` no projeto do Claude).
- **O título vende uma história, não um assunto.** Nada de formato manchete "Empresa: como X aconteceu".
- **Esconder o nome da empresa no título.** O nome vai na descrição, nas tags e na capa (logo). O clique vem da curiosidade de descobrir quem é.
- Fórmulas que mais estouram (escolher uma por vídeo):
  1. **Personagem + valor exato + contradição:** "The $63 BILLION Company That Sold Nothing", "The Fake Genius: a $30 BILLION Fraud", "The Homeless Teen Who Created Louis Vuitton".
  2. **Pergunta direta e informal, com "Actually":** "WTF Did Lehman Brothers Actually Do?", "How Jeff Bezos Actually Built Amazon".
  3. **Promessa de facilidade:** "Explained Simply" / "Explained Like You're 5".
- Valor sempre exato e em destaque ($11.6 BILLION, $477,000,000), e sempre conferido no roteiro.
- O título tem no máximo ~60 caracteres. Capa e título se completam e não repetem as mesmas palavras.
- Gerar 5 opções de título e escolher pela fórmula. Nunca usar o título sugerido pelo roteiro sem passar por esta regra.

## Escolha de tema
- **Prioridade: histórias famosas com ângulo novo** (Enron, Theranos, Madoff, 2008, Wolf of Wall Street, FTX). O público busca esses temas há anos, e canais com menos de 300 mil inscritos fizeram mais de 2 milhões de views com eles.
- Temas pouco conhecidos (ex.: First Brands) só quando o canal já tiver inscritos, ou com um título muito forte, porque quase ninguém pesquisa por eles.
- Notícia quente só vale se sair na mesma semana do fato. Depois disso, tratar como tema histórico com ângulo próprio.
- Criar uma **série com nome fixo** (ex.: "...Explained Simply" ou "What Actually Happened to..."). O público reconhece a série e o YouTube entende o tipo de vídeo. É o que fez o Crayon Capital, canal de 2025, chegar a 274 mil inscritos com 32 vídeos.

## Depois de publicar
- Após 48 h, ver o **CTR** (cliques na capa) no YouTube Studio. Abaixo de 4%, trocar o título ou a capa e usar o teste de 3 capas do YouTube.
- Não julgar o canal pelos primeiros vídeos: até nos canais grandes, 3 a 5 vídeos trazem a maior parte das views.

## Para decidir (recomendação dos dados, ainda não é regra)
- **Duração:** os sucessos do nicho têm de 13 a 30 min, e o canal mais parecido acerta com 13 a 16 min. Sugestão: subir de 10–12 para **13–16 min**.
- **Frequência:** os canais que crescem postam a cada 7 a 16 dias. Sugestão: testar **2 vídeos por semana com mais capricho no título e na capa**, em vez de 4. Isso também economiza o limite do Grok.

## Capa (thumbnail)
Foto real do CEO da empresa em destaque (licença livre), o logo da empresa e o valor perdido (ex.: "$8 BILLION"). Fazer 3 versões e escolher a melhor (subir as 3 no teste de capas do YouTube). A capa mostra quem é; o título cria a curiosidade.

## Upload no YouTube
Não é conteúdo para crianças, conteúdo alterado = Sim, idioma inglês, categoria Educação, tags, legenda SRT em inglês, capítulos, fontes e créditos (incluindo a nota de uso justo) na descrição. Depois de recarregar a página, conferir tudo e marcar como Agendado no Dark Studio.

## Economia de uso
- O PC faz o trabalho pesado localmente. Para revisão, só a folha de quadros final vai para o computador do bot.
- Acompanhar a geração com pouca frequência, sem checar cena por cena.
- Biblioteca local de entidades em `library/entities/<nome>/` (logo, fotos, selo e meta.json com licença e crédito), reaproveitada entre os vídeos.

## Revisão do Claude (17/10/2026): onde o programa ainda não segue este padrão
Conferi cada regra com o código e os projetos. O resto bate (voz onyx, 1080p com reserva 720p, Chrome na porta 9333, upload com Educação/conteúdo alterado, checagem de imagens pela OpenAI na Validação, nenhum "Netflix-style" nos prompts atuais).
- [x] **Música:** *(corrigido 17/10: a montagem agora usa uma faixa só, a primeira da lista, com ducking. Para voltar a trilha por ato, `"single_music": false` em `config/montage.json`.)* a regra pede uma música só no vídeo inteiro, mas First Brands e SVB foram montados com 4 faixas, uma por ato (Floating Cities, Investigations, Darkest Child, Heartbreaking). O programa precisa passar a usar uma faixa só por padrão.
- [ ] **Quantidade de cenas:** os projetos têm de 70 a 85 cenas, não cerca de 47. Vídeos por projeto: First Brands 33/72, SVB 36/80, Lehman 35/83, FTX 20/74 e WeWork 20/67. Ou seja, "a maioria em vídeo" ainda não acontece (fica perto de 45%). Decidir se a meta é "30 ou mais vídeos" ou "mais da metade em vídeo".
- [x] **Biblioteca de entidades:** *(criada 17/10: `library/entities/` já tem 54 entidades dos 5 vídeos. A etapa Imagens reais consulta a biblioteca primeiro e salva nela o que achar de novo. Para repovoar: `python tools/library_seed.py`.)* a pasta `library/entities/` ainda não existe, e o código não a usa. Hoje cada vídeo guarda as fotos e logos na própria pasta (`projects/<vídeo>/entities/`), e nada é reaproveitado entre vídeos.
- [x] **Regras de clique no programa** *(17/10)*: a etapa Ideia agora pede ao ChatGPT títulos nas fórmulas A/B/C, sem o nome da empresa no início, com até 60 caracteres, texto de capa que completa o título, nota de procura do tema (alta/média/baixa) e uma série sugerida. Títulos fora do padrão aparecem com ⚠ na lista e na Validação (só aviso, não bloqueia). O roteiro mantém o título escolhido e entrega a promessa dele nos primeiros 15 segundos.
- [x] **"Netflix-style" no botão Copiar prompt** *(corrigido 17/10)*: o código do servidor já não usava, mas o botão "Copiar prompt completo" da tela de cenas ainda montava o prompt antigo com "Netflix-style". Agora ele monta exatamente o mesmo prompt do servidor. (FTX e WeWork, já publicados, ainda têm o termo guardado; não foram refeitos.)
- [ ] **Gráfico com uma barra só** *(a Validação avisa desde 17/10, sem bloquear)*: a regra diz "nunca", mas o SVB (publicado) tem 6 e o Lehman tem 3 (cenas 16, 25 e 69: alavancagem de 31 para 1, prejuízo do 2º trimestre e os US$ 50 bilhões do Repo 105). Para o Lehman: trocar por um gráfico de escala (`scale`) ou comparar com outro valor real.

## Regras de Acabamento Visual, Mapas, Fotos P&B e Logos nos Gráficos (22/10/2026)
- **Retratos de Pessoas e Figuras Históricas (`person`):**
  - **NUNCA** esticar retratos de pessoas (fotos 3:4 ou verticais) em tela cheia 16:9 como fundo de parallax 2.5D ou plano aberto. Isso causa zoom digital agressivo, perda drástica de nitidez, desfoque e cortes bizarros em olhos, queixo ou ternos.
  - **SEMPRE** utilizar o template documental `person` do EffectCraft (`ec["full"] = {"type": "person", ...}`). A foto real em preto e branco de alto contraste documental é apresentada em sua proporção original dentro de uma moldura de card Polaroid inclinada (-3°) com sombra natural, nome em destaque em Playfair Display, kicker/cargo em caixa alta e dourado/âmbar (`track: 240`), texto de mandato/papel histórico e tópicos factuais com marcadores em âmbar (`points`), além de crédito e fonte oficial no rodapé (padrão de referência visual: Ben Bernanke na Cena 35 do documentário Lehman Brothers).
  - Cenas que utilizam o card `person` em tela cheia não recebem overlay de `lower_third` redundante.
- **Lugar citado sem mapa (30/10/2026):** o `qa_gate` avisa (`lugar_sem_mapa`, nunca bloqueia) quando pais, estado ou cidade aparece na fala e nao ha cena `map` ate 2 cenas de distancia. So vale mapa se o lugar sustenta a historia; citacao de passagem pode ficar sem, anotando no gate.
- **Mapas (`map`):** Nunca exibir apenas uma grade vazia com pontos soltos. Sempre mostrar a silhueta cartográfica real do país e estado (`map_img`, ex.: mapa dos EUA com a Flórida destacada ou mapa do Brasil com estados demarcados), marcando a cidade no mapa do país e abrindo um quadro de zoom (`inset`) para os pontos locais.
- **Parallax 2.5D (`tools/parallax.py`):** Objetos apoiados em superfícies no primeiro plano (capacetes num banco, frascos numa bancada, documentos numa mesa) nunca podem ter deslocamento horizontal oposto ao fundo nem sair do quadro (`grounded_zoom` / `camera: "zoom"`).
- **Fotos Reais em Preto e Branco (`evidence_doc`, `statement`, `person`):** Sempre buscar foto histórica real (preferencialmente em preto e branco de alto contraste documental) dos personagens citados (cientistas, professores, técnicos, executivos, juízes) e exibi-la em moldura de arquivo (`photo` + `photo_caption`) ao lado do documento (`evidence_doc`) ou da citação (`statement`).
- **Logos Reais nos Gráficos (`breakdown`, `chart_line`, `versus`):** Sempre incluir os logos reais das equipes, universidades e empresas envolvidas (`logo` / `logos`, ex.: Florida Gators, Gatorade, PepsiCo) dentro dos próprios gráficos comparativos e curvas de evolução (`Valuation Curve`) para identificação imediata do espectador.
- **Alinhamento de Valores em Barras (`breakdown`):** Os números e unidades das barras horizontais ficam alinhados em coluna à direita fora do trilho escuro (`BX + BW + 28`), nunca sobrepostos à barra de fundo.
- **Abertura de Capítulo (`chapter`):** o capítulo é uma cena própria narrada ("Chapter two. Title.") com `hold`. Cenas com `chapter` nunca recebem gráfico de tela cheia (`ec.full`) ao mesmo tempo, e qualquer `callout`/`lower_third`/`logo` só entra após `t >= 3.6s` (verificado automaticamente pelo `readcheck`). Mesma regra do `CHECKLIST_VIDEO_YOUTUBE.md` e do `GEMINI.md`.

## Acrescentado em 22/10/2026 (Maiskinho, aprovado pelo usuário)

### Retratos (vindo do GEMINI.md)
- Nunca esticar foto vertical de pessoa em 16:9 com parallax. Sempre usar o card `person` do EffectCraft, com foto tratada no Real-ESRGAN na proporção original, nome em Playfair Display, cargo em âmbar e crédito da foto no rodapé. Cena com card `person` não leva `lower_third`.

### Publicação
- **Regra Mandatória de Legendas e Hashtags (TikTok, Instagram Reels, Facebook e YouTube Shorts):** Todo vídeo publicado nas 4 plataformas deve conter **legenda descritiva concisa + exatamente 5 hashtags** (mix de tema e nicho do canal, como #TheCrackedLedger). Nem mais, nem menos.
- TikTok vai pelo Telegram: o vídeo e a legenda chegam no seu Telegram e você baixa e posta pelo celular. Nada sobe pro TikTok pelo PC (config/publish.json, tiktok_mode).
- Nenhum Short ou Reel vai pro TikTok, Facebook ou Instagram sem aprovação do usuário. A fila `social/queue.json` só publica itens marcados como aprovados; o `meta_publish.py --run` não deve postar nada sem esse ok.

### Movimento (gráficos e cenas em código)
- **Lista de proibidos:** sem brilho/glow, partículas decorativas, lens flare, degradê roxo ou azul, tudo surgindo junto, fade-and-slide-up em todo elemento, layout todo centralizado, texto que se mexe enquanto é lido. Depois de cada render, nomear o padrão que apareceu mesmo assim e acrescentar aqui.
- **Números em vez de adjetivos:** entradas com ease-out-expo (0.16, 1, 0.3, 1), movimentos com ease-in-out-quart (0.76, 0, 0.24, 1), saídas com ease-in-expo (0.7, 0, 0.84, 0) e 40–50% mais curtas que a entrada. Molas com damping 0.7–0.85. Nunca easing linear em movimento (só em rotação e barra de progresso).
- **Uma ação principal por cena:** o resto entra 100–200 ms depois e se move 50–70% do caminho. Texto fica parado pelo menos 0,3 s por palavra + 0,5 s.
- **Revisão por frame:** contact sheet antes do render final, notas sempre com número de frame (ex.: frame 84 atrasado). Som de impacto 1 frame depois da imagem, nunca antes.

## Motion (HyperFrames) nos vídeos longos (28/10/2026, aprovado pelo Maiquel no vídeo do Tricolor)
- Usar HyperFrames para as cenas de explicação: diagramas de níveis/fluxo, contas (parcela, juros), barras comparativas, "quem paga", fechamento. 14 cenas, ~4 min num vídeo de 11 min funcionaram. Gerador de referência: `tools/hyperframes/make_tricolor_scenes.py`; modelo visual: `tools/hyperframes/tricolor-s21`.
- **Tipografia fixa (a do s21_inter):** números grandes em Inter 700 com brilho; rótulos em Inter 500 caixa-alta com espaçamento largo, cor âmbar; legendas/frases em Playfair Display itálico; linha "SOURCE · fonte" embaixo à esquerda em toda cena. Nunca Playfair nos números (o "$" fica ornamentado e os traços finos somem com o brilho).
- **Identidade do canal (30/10/2026): ver `IDENTIDADE_CANAL_LEDGER.md`** (paleta fixa, uma cor de acento por video em `accent`, proibicoes). Conferir com `tools/palette_check.py <id>`.
- Paleta: fundo #0b0e14, creme #f6f2ea, âmbar #f4b042, vermelho #d63a34 (só alegação/perda), cartões #ece4d0.
- Tempos de cada elemento vêm de `audio/words.json` (palavra falada -> instante). Alegação sempre com etiqueta ALLEGED; ilustração sempre rotulada.
- Revisão: quadros-chave no mínimo; clipe inteiro a 6 fps no Gate 4.
- **Mistura de formatos (decisão do Maiquel, 28/10/2026):** em cada vídeo longo, escolher por cena o formato de Motion que serve ao conteúdo. F2 = SVG + curvas (fluxos, ligações, setas desenhadas); F3 = tipografia cinética (números e frases de impacto, valores que mudam); F4 = câmera virtual com paralaxe e profundidade (vários blocos em sequência, cartões lado a lado). No Tricolor: F2 em 13, 17, 18, 39, 44; F3 em 5, 14, 19, 36, 45; F4 em 15, 38, 40; 21 fica com barras simples. Gerador: `tools/hyperframes/make_tricolor_final.py`.

## Shorts nativos verticais (padrão desde 30/10/2026, aprovado pelo Maiquel)
- Não recortar o vídeo longo. Montar cada Short do zero em 1080x1920 (HyperFrames), reaproveitando as falas já gravadas (cortadas pelo words.json) e os blocos visuais do longo.
- Estrutura: frase-gancho que se sustenta sozinha nos 2-3 s iniciais (pode ser fala nova curta) + desenvolvimento com 1 número forte e 1 virada + fecho + chamada "full story on the channel". 45 a 90 s (Reels da Meta: até 90 s e com enquete).
- Legendas grandes por fala (blocos de até 3 palavras, números em âmbar), mesma tipografia do longo (números Inter 700, títulos Playfair), créditos na linha SOURCE.
- Áudio: voz + trilha com ducking, -14 LUFS, pico <= -1,5 dBFS. Gerador: `scratch/short_native.py` (piloto: Tricolor native-1).
- Shorts nativos: o primeiro elemento de cada bloco entra nos primeiros 0,3 s do bloco (nunca esperar a palavra falada com a tela só com o rótulo); os demais entram na palavra. Nenhum bloco fica mais de 4 s sem elemento novo: trecho longo de fala vira dois blocos (`end_before`/`start`). Toda empresa ou órgão citado no trecho aparece com logo (`logos`); sem logo licenciado, cartão de texto `"text:Nome"` (02/11/2026, Shorts da Binance). Backlog de Shorts antigos (recorte horizontal) em `social/queue.json` deve ser refeito no formato nativo antes de publicar (gerador `scratch/short_native.py`, `SHORT_PID=<projeto>`).

- **Sem deslize lateral (30/10/2026, pedido do Maiquel, todos os canais):** nenhuma imagem parada anda para o lado. Foto/fundo so faz zoom centrado lento (aproximar ou recuar). Aplicado em tools/parallax.py, montage.py (Ken Burns) e walt_montage.py. Conferir ao olhar os quadros: o assunto nao pode "escorregar".

- **Shorts proprios, nao cortes do audio do longo (01/11/2026, pedido do Maiquel; vale para videos futuros):** depois do longo pronto, escrever 3 roteiros NOVOS de Short (45 a 60 s cada) com o que a pesquisa e o video descobriram (numero forte, virada, quem paga), com narracao gerada so para o Short (TTS proprio, voz do canal), e nao reaproveitar as falas gravadas do longo. Cada Short: gancho nos 3 primeiros segundos, nenhum bloco de mais de ~3 s sem elemento novo na tela (foto de fundo, logo, cartao de pessoa, barras, bolinhas), sem pulsacao/tremida, trilha bem baixa (0,045) e barra de progresso. Meta: 3 Shorts "campeoes" nota >= 8, revisados quadro a quadro antes de mostrar. Weil: weil-1 e weil-3 aprovados com audio reaproveitado (excecao); weil-2 refeito.
- Shorts: quadro de capa e primeiro quadro (02/11/2026). O YouTube escolhe sozinho um quadro do meio como capa se ninguem definir (Weil Short 3 saiu com o cartao "MA / And"). Regra de geracao: (1) o quadro 0 ja mostra o gancho (frase ou numero legivel, nunca so fundo); (2) o quadro 0,5 s deve se sustentar como capa (texto grande, sem legenda cortada como "And"); (3) o Short so conta como enviado depois de abrir o Studio e fixar a capa em "Miniatura > Selecionar no video" num quadro dos 2 primeiros segundos; (4) conferir a capa na lista do Studio antes de dizer "agendado".
