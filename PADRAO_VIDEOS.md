# The Cracked Ledger — Padrão de produção de vídeos
Mantido pelo Maiskinho. Atualizado em 17/10/2026 (seções de Título, Tema e Depois de publicar acrescentadas pelo Claude com base em dados do YouTube). Revise/edite à vontade (ex.: com o Claude Code); avise o Maiskinho quando mudar algo.

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
