# Regras universais (todo vídeo, todo canal)

Criado em 01/11/2026, com a aprovação do Maiquel.

**Como ler:**
- A porta de entrada é [`CLAUDE.md`](CLAUDE.md); o fluxo de cada etapa e canal está em [`ORQUESTRADOR.md`](ORQUESTRADOR.md).
- Leia este arquivo e depois o arquivo do canal em [`canais/`](canais/):
  - [Show Your Work](canais/SHOW_YOUR_WORK.md)
  - [The Cracked Ledger](canais/CRACKED_LEDGER.md)
  - [Grandpa Walt](canais/GRANDPA_WALT.md)
  - [The Rule Changed](canais/RULE_CHANGED.md)
- O processo passo a passo é a skill `video-gate`. A política do YouTube é `CLAUDE_YT_ANTI_DEMONETIZATION.md`, que vence em conflito de monetização.
- Cada regra diz de onde veio. O mapa completo está em [`canais/MAPEAMENTO.md`](canais/MAPEAMENTO.md).
- Regra nova que vale para todos entra aqui. Regra de um canal só entra no arquivo dele.

## 1. Aprovação, contas e segurança
- **Aprovação:** nada é publicado, enviado, agendado nem gasto (Grok, TTS pago, crédito) sem OK do Maiquel. *(CHECKLIST §0, memórias)*
- **Chaves:** nunca imprimir nem commitar o `.env`. *(CHECKLIST §0, CLAUDE_WALT)*
- **Conta:** antes de enviar, conferir a conta e o canal no Studio. Já caiu num canal encerrado. *(memória "Conta do YouTube Studio")*
- **Chrome:** usar o perfil certo de cada canal (memória "Mapa de perfis do Chrome por canal"). Nunca fechar o Chrome da Livia (Profile 10). Um Chrome de automação por vez em cada pasta de perfil.
- **Meta:** nunca automatizar Meta ou Business Suite pelo navegador; o Maiquel agenda à mão. *(memória "Incidente: ban do Facebook")*
- **Um agente por vez em cada projeto.** Antes de mudar um JSON, guardar a cópia `.bak-<motivo>`. *(CHECKLIST §0)*
- **GPU:** um render por vez.

## 2. Verdade
- **Fontes:** todo fato, número e data tem fonte real (URL ou documento). O que não foi conferido fica marcado "Checar" e não vai ao ar. *(CHECKLIST §2)*
- **Números:** nunca inventar. O número narrado é o do fechamento oficial; valor de durante o dia só com "at one point". *(memória "Número da narração = fechamento oficial")*
- **Alegação:** separar alegação de decisão, sempre atribuída ("segundo o FCC", "alegou"). Etiqueta ALLEGED onde couber. Hipótese só com "pode" e nunca no título. *(PADRAO, retenção 7 e 10)*
- **Na tela, sem rascunho:** nada de "Provided notes", "Draft" ou notas internas. A linha de fonte cita a fonte real. Número 1 usa singular. *(CHECKLIST §2, §5; GEMINI §3)*
- **Fatos do ano:** re-pesquisar pela data mais recente antes de escrever. *(registro de erros, eleição 26/10)*

## 3. Pessoas reais, empresas e lugares
- **Visual de quem é citado:** toda pessoa, empresa ou lugar citado tem visual na cena em que é citado. Cena só com texto é reprovada. *(memória "Pessoa/empresa precisa de visual", PADRAO)*
- **Pessoa com foto livre** (Commons, domínio público, arquivo oficial): foto real na proporção original, em moldura, com crédito na linha SOURCE. Nunca esticar retrato vertical em 16:9 nem fazer parallax de retrato. *(PADRAO, GEMINI §1, CHECKLIST §3)*
- **Pessoa sem foto livre** (aprovado em 01/11/2026, substitui o cartão de monograma), nesta ordem:
  1. no documento oficial que a nomeia, com o nome destacado;
  2. num registro público (transcrição de audiência, processo) com o nome;
  3. em lower-third sobre cena reconstruída, marcada como ilustração e sem rosto.
  - Proibido: cartão de iniciais e qualquer texto do tipo "Photo not available".
  - Ficam valendo as exceções já registradas, como Paresh Raja: só o nome, sem foto.
- **Nunca rosto gerado por IA de pessoa real.** Anônimos só de costas, em silhueta ou sem rosto definido. *(PADRAO, PESQUISA)*
- **Empresa e órgão:** logo ou selo real, conferido numa folha de contato. Nunca recolorir nem gerar logo. Sem licença, cartão de texto como exceção registrada. *(CHECKLIST §3, exceções MFS)*
- **Fato grave:** foto histórica real da época. *(GEMINI §4)*

## 4. Imagem e cena
- **Câmera:** imagem parada só com zoom centrado lento, sem deslize lateral, em todos os canais. *(memória "Sem deslize lateral", PADRAO)*
- **Gráfico antes de IA:** número, dinheiro entre partes, ordem no tempo ou queda viram gráfico. Nunca gráfico de uma barra só. *(CHECKLIST §5, §6)*
- **Reconstrução:** realista, na época e no lugar certos; nada simbólico ("analista olhando papéis"). Sem texto gerado dentro da imagem. *(memória "Scene visuals: realism", PADRAO)*
- **Ilustração rotulada:** reconstrução de fato real leva rótulo de ilustração quando pode ser confundida com registro.
- **Clipe de vídeo:** revisar a 6 fps em toda ação e conferir a lógica (mesmo número de pessoas, ninguém surge do nada, carros na pista). *(CHECKLIST §6, memória realism)*
- **Imagem parada:** no máximo 45% do tempo, e nenhum trecho parado passa de 8 s. *(Tricolor, final_sweep)*
- **Composição** (05/11/2026, aprovado pelo Maiquel; ideia de Eian, @EianLu):
  - em foto, reconstrução e clipe, o rosto ou o objeto principal fica perto de 38% ou 62% da largura, não no centro. Gráficos, mapas e cartões seguem o layout do canal;
  - a paleta de cada bloco do vídeo é escolhida antes da primeira imagem e anotada no projeto;
  - teste em preto e branco nos quadros de referência: se o assunto some no fundo, falta contraste e a imagem volta;
  - não emendar várias cenas seguidas com o mesmo enquadramento: alternar plano aberto, médio e fechado.

## 5. Movimento
- **Proibidos:** partículas decorativas, lens flare, degradê roxo ou azul, tudo surgindo junto, fade-and-slide-up em todo elemento, texto que se mexe enquanto é lido. *(PADRAO "Movimento")*
- **Brilho/glow:** proibido, exceto nos números do Ledger (s21_inter), aprovado em 28/10. Ver "Em aberto".
- **Easing:**
  - entrada ease-out-expo (0.16, 1, 0.3, 1);
  - movimento ease-in-out-quart (0.76, 0, 0.24, 1);
  - saída ease-in-expo, 40 a 50% mais curta que a entrada;
  - nunca linear em movimento.
- **Uma ação principal por cena:** o resto entra 100 a 200 ms depois. Texto fica parado no mínimo 0,3 s por palavra + 0,5 s.
- **Foco único:** uma ideia visual por cena. Lower-third só quando acrescenta algo, e nunca o nome de uma pessoa sobre a foto de outra. *(CHECKLIST §5, GEMINI §3)*
- **Som de impacto:** 1 quadro depois da imagem.

## 6. Texto na tela
- **Fontes:** só de licença livre (OFL) em `fonts/`; cada canal escolhe as suas. Nada de Arial, Impact ou Georgia do Windows; a exceção histórica é o Walt (Georgia). *(PADRAO)*
- **Números:** fonte com algarismos alinhados (Inter), nunca serifa ornamentada. *(PADRAO, Tricolor)*
- **Área segura:** texto a pelo menos 5% da borda. A linha de fonte fica acima da barra do YouTube. Texto sempre contido no cartão, sem "…" na tela. *(PADRAO, CHECKLIST §5)*
- **Contraste:** mínimo de 4,5:1; vermelho puro só em forma, não em letra pequena.
- **Legendas:**
  - no máximo 2 linhas de 42 caracteres, sem terminar linha em "the", "of" ou "and";
  - pelo menos ~1,5 s na tela;
  - sem quebra entre número e unidade;
  - o texto vem do roteiro e o tempo, do reconhecimento de voz.
- **Entrega:** a pasta de entrega não leva `.ass` ao lado do `.mp4`. *(memória "Revisar como o usuário vê")*

## 7. Áudio
- **Trilha:** de suspense, nunca cômica; *Investigations* está vetada. Faixas aprovadas: Echoes of Time v2, Stay the Course, Interloper, Darkest Child. Crédito na descrição. *(memória "Trilha: suspense")*
- **Mixagem:** ducking sob a voz. -14 LUFS, pico -1,5 dBTP. Sem silêncio maior que 1,2 s. *(GEMINI §6, CHECKLIST §8)*
- **Voz:** cada canal tem a sua (ver o arquivo do canal). Não trocar a voz de episódio já pronto sem perguntar.

## 8. Processo
- **Skill `video-gate`** antes de qualquer vídeo: Gates 1 (pesquisa) a 6 (Shorts), com relatório em `logs/gate-N.md`.
- **Duração:** piso de 8 min no vídeo longo. Contar palavras a ~136 por minuto. *(memória "Skill video-gate")*
- **Modo orquestrador** em todo vídeo:
  - Opus coordena e revisa os quadros;
  - Sonnet escreve e corrige as cenas;
  - Haiku renderiza e envia. *(memória "Modo orquestrador")*
- **Corrigir a causa:** erro do motor se corrige no motor; erro do roteiro, no roteiro. *(CHECKLIST §0)*
- **Inserir cena:** muda a numeração. Gravar o JSON direto e conferir que todo arquivo existe. *(registro de erros, eleição)*

## 9. QA antes de dizer "pronto"
- **Olhar os quadros:** abrir todas as folhas de quadros e o último quadro de cada gráfico alterado; animação a 6 fps. Relatório e validador não bastam. *(CHECKLIST §7, memórias QA)*
- **O que não foi visto:** o relatório diz o que **não** foi conferido.
- **Final:** o Maiquel assiste o master inteiro e aprova por escrito. Sem isso, nada de kit nem Shorts. *(CHECKLIST §9)*

## 10. YouTube e redes
- **Anti-desmonetização:** ler `CLAUDE_YT_ANTI_DEMONETIZATION.md` e preencher o checklist da seção 6 antes de kit, upload ou calendário. *(memória "Regra anti-desmonetização")*
- **Também ler** `CLAUDE_INTERNATIONAL_REACH.md` e `CLAUDE_ANALYTICS_FEEDBACK.md`.
- **Upload:** não é para crianças; conteúdo alterado/IA = Sim quando há reconstrução ou voz sintética; legenda SRT; capítulos; fontes e créditos.
- **Redes:**
  - legenda + chamada + **exatamente 5 hashtags** nas 4 plataformas;
  - Reels com enquete e até 90 s, mandados pelo Telegram (memória "Enquete obrigatória nos Reels");
  - TikTok pelo Telegram;
  - fila `social/queue.json` só com itens aprovados.
- **Cortes:** Shorts e cortes só depois do final aprovado e só os trechos com nota ≥ 8.

## 11. Erro novo vira regra
- Erro apontado pelo Maiquel vira regra no mesmo dia: aqui, se vale para todos; no arquivo do canal, se é de um só. O caso vai para o registro de erros do canal.

## 12. Ideia, título e capa
Fonte: artigo de Paddy Galloway, "5 Principles That Helped Me Generate 50 Billion Views" (X, 02/11/2026). Aprovado pelo Maiquel em 03/11/2026. As regras do canal sobre título (por exemplo, The Rule Changed sem números) e a seção 2 (Verdade) vencem em caso de conflito.
- **Tempo para a embalagem:** ideia, título e capa decidem cerca de metade do resultado, então ganham tempo de verdade.
  - Antes de escolher o tema, levantar pelo menos 10 ideias e escolher a mais forte.
  - Para cada vídeo, fazer pelo menos 5 títulos e 3 capas e escolher olhando lado a lado, no tamanho do feed do celular.
- **Teste do relance:** ideia, título e capa precisam ser entendidos em menos de 1 segundo. Se não forem, simplificar.
  - Título com menos de 60 caracteres.
  - No máximo 5 palavras na capa.
  - De 1 a 3 pontos de foco na imagem.
  - O texto da capa se destaca do fundo (contraste da seção 6) e não se mistura com a imagem.
- **Vantagem própria:** antes de aprovar uma ideia, perguntar: "qualquer canal poderia dizer isso?". Se a resposta for sim, achar o ângulo que só este canal tem: a fonte primária, o documento, a montagem peça por peça, o personagem.
- **Algo em jogo:** todo vídeo diz no gancho o que o espectador ganha ou perde, mesmo um vídeo educativo. Pode ser uma consequência ("a chave quase certa não gira") ou um adversário real. A consequência precisa ser verdadeira e ter fonte (seção 2). Adversário inventado ou exagerado é proibido, assim como título sensacionalista (`CLAUDE_YT_ANTI_DEMONETIZATION.md`).
- **"Algoritmo" vira "público":** na análise de métricas, não culpar o algoritmo. "O algoritmo não entregou" se escreve "o público não clicou ou não ficou", e a causa vai para a ideia, a embalagem ou o vídeo (`CLAUDE_ANALYTICS_FEEDBACK.md`).

Acrescentado em 05/11/2026, com aprovação do Maiquel (guia de Pierre François, @pierrestories, X, 05/11/2026; só a parte que serve a canal de anúncio):
- **Ideias 70-20-10:** na escolha de temas, ~70% do *tipo* de tema que já funciona no canal, ~20% vizinho a ele e ~10% totalmente novo. Os 70% são o tipo de tema, nunca o mesmo vídeo refeito (`CLAUDE_YT_ANTI_DEMONETIZATION.md` 6c).
- **Padrão, não acaso:** um vídeo que estourou sozinho ensina pouco. Só tirar conclusão comparando vários vídeos acima da média do canal lado a lado e anotando o que se repete em todos.
- **Primeiros 30 s (Gate 2):** cada frase da abertura tem uma função, nesta ordem: por que este vídeo é diferente do que o espectador já viu; por que confiar (a fonte, o documento); o que ele ganha assistindo; o que vem a seguir. Antes de aprovar o roteiro, conferir que os primeiros 30 s entregam o que o título e a capa prometem.
- **Vídeo abaixo do esperado:** primeiro definir o que era "esperado" para ele. Depois investigar na ordem ideia → título e capa → gancho (30 s) → roteiro e edição, parar na primeira etapa que explica e anotar a causa e a correção na ficha do canal ("Deu certo / não deu").
- **Não largar formato por tédio:** formato que funciona continua até os dados dizerem o contrário; mudança de formato só com a análise acima e OK do Maiquel.

Acrescentado em 03/11/2026, com aprovação do Maiquel, e conferido nas fontes primárias:
- Central de Ajuda, "Testar e comparar": support.google.com/youtube/answer/13861714
- entrevista no Creator Insider (27/10/2026) com Todd Beaupré e Rene Ritchie: youtube.com/watch?v=Au_x7IRClH4
- blog do Made on YouTube (23/09/2026)

Detalhes em `research/youtube_ab_2026-11-03/validacao_ab_oficial.md`.
- **Capas no "Testar e comparar"** (já existe):
  - nos vídeos longos, subir até 3 opções no teste A/B do Studio em vez de escolher uma só. Pode ser capa, título ou os dois; o título segue a regra do canal;
  - o teste decide pelo tempo assistido, não pelo clique. Vence a opção que mantém o espectador;
  - a posição 1 é sempre a capa principal do vídeo (o Studio a preenche sozinho) e é ela que fica se o resultado der "Inconclusive". Em vídeo novo, enviar a favorita como capa principal no upload; em vídeo já publicado, a atual fica na posição 1;
  - o teste dura até 2 semanas. Não mexer em título nem em capa nesse período, porque qualquer mudança encerra o teste;
  - só funciona no computador, com recursos avançados ativos. Não vale para Shorts, Premieres, lives nem vídeos para crianças.
- **Nenhuma métrica sozinha:** segundo Rene Ritchie, o YouTube pesa as coisas de forma diferente para cada espectador. Na análise, ler juntos views, retenção e satisfação (curtidas, comentários, inscrições vindas do vídeo). CTR sozinho não decide nada.
- **Título e descrição em linguagem natural:** dizer com clareza, em frases normais, do que o vídeo trata e para quem é. O sistema entende o assunto pelo sentido, não pelo texto literal do título (Todd Beaupré), então lista de palavras-chave não ajuda.
- **Só anunciado (sem data; reavaliar quando sair):** teste A/B de Shorts (2 ou 3 versões, com gráfico de retenção), capas dinâmicas, revisão do catálogo antigo com IA (Ask Studio) e feeds personalizados por linguagem (primeiro nos EUA).
- **Canal novo:** o YouTube mostra vídeos de canais pequenos a alguns espectadores ("exploration") e amplia o alcance quando eles gostam. No Rule Changed e no SYW, manter o tema constante e fazer o primeiro público assistir até o fim vale mais do que olhar o número do Studio.

### Capas com teste A/B (padrão desde 03/11/2026, aprovado pelo Maiquel)
Vale para todo vídeo longo do Ledger e do The Rule Changed. Não vale para o SYW nem para Shorts até o teste de Shorts sair. O primeiro caso foi Binance e Weil, em `canais/CRACKED_LEDGER.md` (03/11). Esta é uma regra de **processo**: o **estilo** que vence só vira regra depois dos resultados (último item).
- **3 capas por vídeo:** a principal e mais 2 variações, cada uma com um conceito diferente. Exemplos de conceito:
  - fundo claro de papel quadriculado com seta verde subindo e vermelha caindo;
  - objeto fundido com a marca (moeda com o símbolo, prédio real da sede);
  - antes e depois;
  - dado desenhado (recibo, barras, linha do tempo, cronômetro);
  - versão escura do canal.
- **Toda capa:**
  - passa no teste do relance acima, com no máximo 5 palavras;
  - tem 1 objeto que mostra o acontecimento (cofre vazio, não cofre fechado; cadeira vazia, não escritório genérico), de preferência fundido com a marca;
  - logo ou foto real conferidos (seção 3);
  - todo número e afirmação estão no vídeo, com fonte (seção 2). Alegação leva ALLEGED ou crédito ("per TRM Labs");
  - no Rule Changed, segue a regra do canal: sem número nem multa na capa.
- **Composição** (lista colada pelo Maiquel em 05/11/2026, sem autor; aprovada por ele):
  - **reviravolta que o título não diz:** a capa completa o título, não repete. Ex.: título "Who Really Killed Red Lobster?" e capa com o prato de camarão vazio e o recibo;
  - **a cor mais forte vai na reviravolta:** o elemento que gera a curiosidade é o primeiro que o olho encontra; o resto fica em tons de apoio;
  - **quebrar só um elemento do visual do nicho** (cor de fundo, ângulo, objeto inesperado); quebrar tudo deixa a capa irreconhecível;
  - **dica, não regra:** o olho tende a ler em Z, então gancho em cima à esquerda e prova embaixo à direita;
  - **variação para o teste A/B:** uma das 3 capas pode fugir de vermelho, branco e preto como cores principais (a página do YouTube usa essas cores). Vira regra só se vencer nos testes.
- **Proibido, mesmo que os concorrentes façam:**
  - rosto de pessoa real gerado por IA;
  - imitar post ou foto de político;
  - "NOW ILLEGAL", multa em dinheiro ou alerta falso na capa;
  - texto gerado dentro da imagem (placa, tela, papel com letras falsas).
- **Revisão:** olhar as 3 lado a lado no tamanho do feed (~400 px) e em tamanho cheio antes de enviar. Depois, converter as 3 para preto e branco no tamanho do feed: se não der para dizer na hora o que importa mais, falta contraste e a capa volta. Procurar texto encostando em seta ou objeto, objeto flutuando sem sombra, recorte com sobra de fundo e logo cortado.
- **Teste no Studio:**
  - "Teste A/B" → "Somente miniatura": a principal fica na posição 1 e as 2 variações nas posições 2 e 3;
  - "Começar teste" e depois **"Salvar"** no topo da página: sem salvar, o teste não fica;
  - conferir reabrindo o "Teste A/B": o aviso "Isso exclui o teste atual" quer dizer que o teste está ativo. Clicar em "Cancelar".
  - Detalhes da automação na memória "Teste A/B de capa no Studio".
- **Resultado:**
  - em até 2 semanas, anotar na ficha do canal o vencedor, o conceito de cada opção e a porcentagem de tempo assistido;
  - depois de uns 5 testes no mesmo canal, o conceito que mais venceu vira o conceito **principal** do canal, por decisão do Maiquel, mas não o único: duas capas vizinhas na página do canal nunca têm o mesmo conceito, e o vencedor se reveza com os outros (cor do texto, o que fica no centro: objeto, mapa, prédio, documento). A identidade do canal fica na paleta e na fonte, não num modelo repetido (`CLAUDE_YT_ANTI_DEMONETIZATION.md` item 6d; corrigido em 05/11/2026).

## Em aberto (o Maiquel decide)
| Tema | Situação |
|---|---|
| Entrada de número N1 (sem contador) nos outros canais | aprovada só para o The Rule Changed |
| Brilho nos números do Ledger | aprovado em 28/10 (s21_inter), mas contraria a lista de proibidos |
| Trilha: faixa única ou deixas | PADRAO pede uma faixa; a memória prefere deixas de suspense. Hoje cada canal decide |
| Upscaler de fotos | ver "Decisões em aberto" do CHECKLIST |
