# The Cracked Ledger — Manual de Regras de Produção, Visual e Publicação

> **Porta de entrada da pasta (4 canais):** [`CLAUDE.md`](CLAUDE.md), depois [`ORQUESTRADOR.md`](ORQUESTRADOR.md). Este manual vale só para o The Cracked Ledger.

> **Regras organizadas em 01/11/2026:** o que vale para todo canal está em [`REGRAS_UNIVERSAIS.md`](REGRAS_UNIVERSAIS.md); a identidade de cada canal está em [`canais/`](canais/) (mapa em [`canais/MAPEAMENTO.md`](canais/MAPEAMENTO.md)). Este arquivo continua valendo como detalhe do The Cracked Ledger.

> **LEIA ANTES DE AGIR: [CHECKLIST_VIDEO_YOUTUBE.md](CHECKLIST_VIDEO_YOUTUBE.md).** Abra e leia o arquivo inteiro antes de começar qualquer vídeo, correção ou publicação. Ele é o processo único, na ordem do pipeline; este manual traz os detalhes visuais do EffectCraft.
>
> **Em caso de conflito entre este manual e o checklist, vale o `CHECKLIST_VIDEO_YOUTUBE.md`** (exceto nos itens da tabela "Decisões em aberto", que só o Maiquel decide). Erro novo vira regra no checklist.

Este documento estabelece as regras estritas e inegociáveis para a produção de roteiros, imagens, gráficos animados no EffectCraft, sound design, montagem e publicação de vídeos do canal **The Cracked Ledger**. Todo script, agente e pipeline DEVE seguir rigorosamente este manual.

---

## 1. Figuras Históricas e Personalidades (A Regra de Ouro)

- **Presença Visual Mandatória:** Toda e qualquer figura histórica (presidentes, ministros, juízes, secretários de tesouro, executivos de fundos) citada pelo nome na narração **DEVE ter sua face real exibida na tela**. Nunca citar uma personalidade histórica sem exibir sua foto autêntica.
- **Proibição de Zoom/Esticamento em Fundo Parallax:** **NUNCA** esticar fotos de retratos (fotos 3:4 ou verticais) em tela cheia 16:9 como fundo de parallax 2.5D ou plano aberto. Isso causa zoom digital agressivo, perda drástica de nitidez, desfoque e cortes anatômicos (olhos, queixo, testa ou ternos).
- **Template Documental Obrigatório (`person`):**
  - Retratos em tela cheia devem usar o template documental `person` do EffectCraft (`ec["full"] = {"type": "person", ...}`).
  - **Fotografia:** Foto real de arquivo histórico em preto e branco de alto contraste documental (`entities/...-bw.jpg`), restaurada/nítida e apresentada em sua proporção original dentro de uma moldura de card Polaroid inclinada (-3°) com sombra natural e zoom de entrada sutil.
  - **Tipografia:** Nome da personalidade em destaque na tipografia Playfair Display.
  - **Kicker / Cargo:** Em caixa alta e dourado/âmbar (`track: 240`, `color: COL.amber`).
  - **Tópicos Factuais:** Descrição da atuação e fatos históricos com marcadores em âmbar (`points`).
  - **Rodapé:** Crédito da foto e fonte histórica oficial (ex.: FCIC, SEC, corte judicial, presidência).
  - Cenas com card `person` em tela cheia **não** recebem overlay de `lower_third` redundante.
- **Duplas Políticas / Econômicas (`pair`):**
  - Quando duas figuras históricas atuam em conjunto na mesma tese (ex.: Presidente e Ministro da Economia, como Javier Milei & Luis Caputo), utilizar o template `pair`.
  - **Conexão Editorial:** A ligação visual entre os dois retratos deve ser um divisor refinado com medalhão âmbar contendo o símbolo `&` em Playfair Display e a doutrina econômica acima. **NUNCA** utilizar linhas grossas com pontos de laser pulsando ou correndo entre pessoas.
- **Lower-Third com Foto Obrigatória:**
  - Se uma personalidade histórica for introduzida em overlay sobre uma cena ou infográfico, o template `lower_third` DEVE conter a fotografia documental em moldura (`file: "entities/..."`).
  - **NUNCA** exibir um lower-third de pessoa apenas com texto em fundo vazio.
- **Desacoplamento e Proibição de Sobreposição Conflitante:**
  - **NUNCA** exibir o nome ou cargo de uma pessoa sobreposto à fotografia de outra personalidade histórica (ex.: lower-third de Domingo Cavallo sobreposto ao retrato de Carlos Menem). Cada personalidade deve ter seu momento visual exclusivo.
- **Proibição Absoluta de Upscalers AI Plásticos:**
  - Utilizar sempre imagens RAW autênticas de alta resolução (Wikimedia Commons, arquivos governamentais, agências oficiais). Nunca aceitar fotos pixeladas de baixa qualidade com interpolação que deforme feições.

---

## 2. Infográficos e Fluxos Financeiros (EffectCraft)

- **Confinamento Estrito de Texto em Caixas (`fit`):**
  - Todo e qualquer rótulo de nó, caixa ou painel retangular DEVE ser confinado dinamicamente (`fit(lb, w - 48)`).
  - **Nenhuma palavra ou letra pode transbordar as bordas de um retângulo**, independentemente do tamanho do texto ou idioma.
- **Fluxos Bidirecionais em Canais Paralelos Independentes (`isDual`):**
  - Em diagramas de fluxo (`flow`), se houver duas transferências entre o mesmo par de nós (ex.: transferência de ativos públicos vs. recebimento de dinheiro, ou entrega de títulos velhos vs. emissão de novos bônus):
    - O fluxo de ida DEVE ser posicionado no canal superior (`y = Y - 48`), com o rótulo posicionado **acima** da linha e animação correndo na direção correta.
    - O fluxo de volta DEVE ser posicionado no canal inferior (`y = Y + 48`), com o rótulo posicionado **abaixo** da linha e animação correndo na direção inversa.
    - **JAMAIS sobrepor dois fluxos opostos na mesma linha horizontal central**.
- **Topologia Limpa em Liminares e Relações Triangulares:**
  - Em situações com três entidades onde uma rota é bloqueada e outra exigida (ex.: Liminar *Pari Passu* entre devedor soberano, credores reestruturados e credores holdouts):
    - O devedor soberano fica no centro (`x = 960`).
    - O canal à esquerda direciona o pagamento reestruturado com alerta visual vermelho de bloqueio (*"BLOCKED BY COURT"*).
    - O canal à direita direciona a exigência dos holdouts (*"PARI PASSU DEMAND"*).
    - **NUNCA** criar linhas que atravessem por baixo de caixas intermediárias com textos colidindo nas bordas inferiores.
- **Capítulo e tela cheia (alinhado ao `CHECKLIST_VIDEO_YOUTUBE.md`, blocos 2 e 5, e ao `PADRAO_VIDEOS.md`):**
  - O capítulo é uma **cena própria narrada** ("Chapter two. Title."), com `hold`, e **nunca** recebe `ec.full` na mesma cena. `callout`, `lower_third` e `logo` só entram depois de 3,6 s.
  - Corrigir o roteiro (mover o gráfico para a cena seguinte) em vez de deixar o `readcheck` ou o validador descartar a diretiva `full`. O validador nunca apaga um `full` para forçar fundo de rascunho; se houver conflito, ele avisa e o roteiro é corrigido.

---

## 3. Hierarquia Visual e Prevenção de Poluição (Anti-Clutter)

- **Regra do Foco Único:** Cada cena tem duração curta (8 a 12 segundos). Deve haver **uma única ideia visual dominante** por cena:
  - Se a cena exibe uma linha do tempo (`timeline`), ela **não** deve receber callouts laterais e lower-thirds simultâneos concorrentes.
  - Se a cena exibe um card `person`, ela **não** deve ter caixas de texto flutuantes redundantes.
  - Eliminar qualquer elemento que dispute a atenção do espectador com o objeto central da cena.
- **Filtro Absoluto Anti-Rascunho:**
  - **NUNCA** exibir textos internos de produção ou placeholders na tela (ex.: *"Provided notes"*, *"No source URL supplied"*, *"Draft"*, *"User-provided"*).
  - Toda menção de fonte (`source`) deve exibir estritamente fontes documentais reais e auditadas (ex.: *"Official Records / Ministry of Economy"*, *"U.S. District Court, S.D.N.Y."*, *"INDEC"*, *"Banco Central de la República Argentina"*).

---

## 4. Rigor Arquivístico e Documental

- **Instituições Oficiais Exigem Logo / Brasão Real:**
  - Menções a Bancos Centrais (ex.: BCRA, Federal Reserve), instituições multilaterais (FMI, Banco Mundial) ou agências reguladoras exigem a exibição do brasão/logo oficial de alta resolução com transparência.
- **Fatos Históricos Graves Exigem Fotos Históricas Reais:**
  - Protestos, mortes em repressões policiais (ex.: Dezembro de 2001 na Plaza de Mayo), renúncias presidenciais e fugas de helicóptero DEVEM conter registros fotográficos autênticos da época, sem cortes abruptos no assunto principal.
- **Fenômenos Exponenciais Exigem Gráficos de Linha (`chart_line`):**
  - Trajetórias de hiperinflação, colapso de reservas cambiais ou dívida pública explosiva devem ser materializadas graficamente através de curvas animadas baseadas em dados oficiais.

---

## 5. Encerramento Obrigatório do Vídeo (Call to Action & Outro)

- **Chamada de Ação Falada (Spoken CTA):**
  - Todo documentário longo deve encerrar com a narração oficial do locutor principal realizando uma chamada clara e envolvente para:
    1. Se inscrever no canal **The Cracked Ledger**.
    2. Deixar a curtida (*like*).
    3. Comentar no vídeo qual próxima crise ou quebra financeira deseja ver investigada.
- **Outro Card Oficial Animado:**
  - A cena final deve transicionar da citação de encerramento para o card oficial animado da marca:
    - Logotipo e Nome: **THE CRACKED LEDGER** em Playfair Display.
    - Slogan: *"DEEP-DIVE FINANCIAL INVESTIGATIONS"*.
    - Botão em destaque âmbar com *"SUBSCRIBE"*.
    - Chamada para interação: *"LIKE · COMMENT · NOTIFICATIONS"*.
    - Sustentação em tela por no mínimo 6 a 8 segundos com cauda musical elegante.

---

## 6. Mixagem de Áudio e Acabamento Sonoro (Padrão Broadcast)

- **Loudness Padrão YouTube:** `-14.0 LUFS` integrado e `-1.5 dB True Peak`.
- **Sound Design Sincronizado:** Todo impacto visual (entrada de Polaroid, carimbos, gráficos preenchidos, alertas de corte judicial) deve ter seu evento sonoro correspondente (whoosh, papel, impacto sutil, gavel, registradora).
- **Sidechain Ducking:** A trilha sonora deve baixar automaticamente de volume (`ducking`) sempre que a voz da narração estiver ativa, garantindo inteligibilidade absoluta.

---

## 7. Publicação em Redes Sociais: Legenda + 5 Hashtags

Todo vídeo vertical publicado nas redes sociais do canal (**TikTok**, **Instagram Reels**, **Facebook Reels / Vídeos** e **YouTube Shorts**) DEVE seguir rigorosamente a estrutura:
- **Estrutura Obrigatória:** `[Legenda descritiva e concisa]` + `[Chamada / Link do documentário completo]` + `[Exatamente 5 hashtags]`.
- **Regra Estrita das 5 Hashtags:**
  - Todo post deve conter **obrigatoriamente e exatamente 5 hashtags** no rodapé (nem 4, nem 6).
  - **Composição recomendada:**
    - 2 a 3 hashtags contextuais do tema do vídeo (ex.: `#Argentina`, `#Economy`, `#DebtCrisis`, `#WallStreet`, `#Inflation`).
    - 2 a 3 hashtags de nicho / canal (`#TheCrackedLedger`, `#Finance`, `#BusinessHistory`, `#Documentary`, `#shorts`).
  - Válido sem exceções em todas as 4 plataformas:
    1. **TikTok**: legenda + 5 hashtags.
    2. **Instagram Reels**: legenda + 5 hashtags (com indicação "link in bio").
    3. **Facebook Reels / Vídeos**: legenda + 5 hashtags (com link clicável do YouTube).
    4. **YouTube Shorts**: legenda/descrição + 5 hashtags (com link do documentário).
