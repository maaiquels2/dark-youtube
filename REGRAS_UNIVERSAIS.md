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

## Em aberto (o Maiquel decide)
| Tema | Situação |
|---|---|
| Entrada de número N1 (sem contador) nos outros canais | aprovada só para o The Rule Changed |
| Brilho nos números do Ledger | aprovado em 28/10 (s21_inter), mas contraria a lista de proibidos |
| Trilha: faixa única ou deixas | PADRAO pede uma faixa; a memória prefere deixas de suspense. Hoje cada canal decide |
| Upscaler de fotos | ver "Decisões em aberto" do CHECKLIST |
