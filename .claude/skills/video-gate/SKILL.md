---
name: video-gate
description: Roda ANTES de começar e ao FINAL DE CADA ETAPA de qualquer vídeo do canal (The Cracked Ledger): pesquisa, roteiro, narração, imagens/vídeos, montagem, Shorts, kit. Define o pipeline completo e o que cada etapa precisa provar antes de seguir. Use sempre que o pedido for vídeo, roteiro, cena, gráfico, montagem, final.mp4, Shorts ou kit.
---

# video-gate — pipeline por etapas, com revisão obrigatória em cada uma

Nasceu dos erros do Archegos (24/10/2026) e da direção dada pelo Maiquel no mesmo dia. O objetivo é um projeto **robusto e completo, sem ele precisar acompanhar cada passo**. Então:

- As etapas rodam sozinhas e, **no fim de cada uma, esta skill é chamada para revisar** e gravar `projects/<id>/logs/gate-N.md` (o que foi conferido, o que NÃO foi, e o resultado). Só segue se o gate passar.
- **Só paro para o Maiquel** em: vídeo final, publicar/agendar/enviar, gasto novo de dinheiro ou crédito, ação irreversível, e quando falta algo que só ele tem (chave de API, login, foto sem fonte livre). Nada disso é contornado.
- Regra de ouro: nunca dizer "pronto/validado/corrigido" sem ter aberto os frames e sem listar o que não foi conferido.

## Skills de apoio por etapa (ver `SKILLS_PIPELINE.md`)
Gate 1 e 2: `fact-check-workflow`. Gate 2: `technical-video-script` (só revisão). Gate 3: `tools/asr_local.py` (faster-whisper local, grátis). Gate 4: `flux-best-practices`, `comfyui-prompt-engineer`, `comfyui-troubleshooter`. Trilha: `acestep` (só local). Gate 5: `ffmpeg`, `character-animation-qa`. Kit: `youtube-seo`. As regras desta skill vencem as delas.

## Etapa 0 — Pré-voo (sempre)
0. Ler `REGRAS_UNIVERSAIS.md` e o arquivo do canal em `canais/` (SHOW_YOUR_WORK, CRACKED_LEDGER, GRANDPA_WALT ou RULE_CHANGED). Eles valem para todo canal; os itens 1 e 3 abaixo são do Ledger.
1. Ler `CHECKLIST_VIDEO_YOUTUBE.md` inteiro e a memória `video-qa-rules-argentina`.
2. Um agente por projeto (Antigravity fora); `.bak-<motivo>` do JSON antes de editar.
3. Canal e perfil: Cracked Ledger, `chrome_junction`/Profile, porta 9333. Nunca o Grandpa Walt (`chrome-profiles-channels`).

## Etapa 1 — Pesquisa completa de tudo e de todos (GATE 1)
Achado o tema, **buscar a história inteira antes de escrever uma palavra**:
- **Todos os envolvidos**: pessoas (trajetória: de onde vieram, cargos, condenações, relações), empresas, bancos, reguladores, tribunais, órgãos. Se uma pessoa ou empresa aparece na história, entra na lista.
- **Para cada envolvido: foto e/ou logo achados e salvos** em `entities/` com agência/autor/licença/URL em `credits.json` (Commons e domínio público primeiro; foto de agência com crédito é aceita pelo Maiquel; sem fonte = registrar o motivo). Logo grande e legível; conferir numa folha de contato.
- **Linha do tempo dia a dia** das semanas decisivas, cada fato com URL. O que não tem fonte fica "Checar" e fora da narração.
- **Toda queda ou salto de preço** (ação, cripto, índice, câmbio) naquela semana: baixar os fechamentos diários de fonte nomeada e **já deixar o dataset do gráfico pronto** (`chart_line` com valores nos pontos). Se faltar um dia, dizer qual e buscar em outra fonte antes de aceitar 3 pontos.
- Todo número do roteiro tem fonte; disputas viram atribuição ("segundo a Bloomberg").
**Gate 1 passa quando:** lista de entidades 100% com foto/logo ou motivo; todo movimento de preço com gráfico planejado; timeline sem buraco; "Checar" listado.

## Etapa 2 — Roteiro (GATE 2)
- **Gancho de abertura = prévia de TV** (15 a 25 s): por que esta história merece a atenção do espectador. Fala dos 2 ou 3 momentos mais fortes (números, reviravolta) como um "trailer" e promete a resposta. Se a pessoa assistir só isso, tem que querer clicar.
- **Duração: piso 8 min (AdSense), alvo 10 a 12.** Contar palavras por script; ~136 palavras = 1 min (medido no Archegos: 715 palavras = 5 min 29 s). Para 8 min são ≥ 1.100; para 10 min ≥ 1.360. Escrever o número real no relatório. Roteiro abaixo do piso não passa: ampliar com a pesquisa da Etapa 1.
- **Escrito já pensando em Shorts nota ≥ 8:** cada capítulo é um bloco que se sustenta sozinho (30 a 45 s): gancho de até 12 palavras nas duas primeiras frases, 1 número forte, uma virada, e uma frase final que fecha sozinha. Listar os cortes candidatos com nota estimada e o motivo; se um capítulo não daria nota 8, reescrever.
- Capítulo é cena própria narrada ("Chapter two. …"), numeração sequencial. Encerramento com o nome do canal falado.
- Título pela fórmula (5 opções, sem nome da empresa, valor exato).
- **Padrões de retenção (PADRAO_VIDEOS.md, "Padrões de retenção"):** número exato nas 2 primeiras frases; contradição declarada na prévia; um conflito central; trecho "quem paga a conta" perto do fim; uma pausa útil no meio; fato/alegação/decisão separados em voz alta; fecho que espelha o gancho; nada de especulação como fato nem resíduo de roteiro. Listar no relatório onde cada um aparece.
**Gate 2 passa quando:** contagem ≥ piso, prévia de abertura presente, os 8 padrões de retenção presentes, cada capítulo com gancho + número + virada + fecho, fatos todos com fonte, cortes candidatos listados.

## Etapa 3 — Fala completa (GATE 3)
- **Voz fixa do canal (aprovada pelo Maiquel em 24/10/2026): Brian, ElevenLabs, velocidade 0,86.** Já está em `config/montage.json` (`tts_provider: elevenlabs`, `eleven_voice_id: nPczCjzI2devNBz1zQrb`, `eleven_speed: 0.86`); `montage.py --step tts` usa isso sozinho. A chave é `ELEVEN_LABS_KEY` no `.env` (nunca no chat). Orçamento: ~6.600 caracteres por vídeo de 8 min, 90.000 por mês no plano Starter; conferir o saldo antes de gerar e não regenerar sem motivo (cada geração completa gasta ~7%).
- **Duração depende da voz:** a 0,86 o Brian rende ~135 palavras por minuto de áudio. Para 8 min de vídeo (soma das cenas com pausas e capítulos) são ≥ 1.100 palavras; use a duração real do áudio, não a estimativa.
- **Não clonar o Brian em outra ferramenta:** a política da ElevenLabs (seção 12) proíbe usar o Output para treinar ou melhorar outro modelo, e o motor padrão do Voice Studio (OmniVoice) tem pesos CC-BY-NC. Voz local só a partir de gravação do próprio Maiquel e motor de licença comercial.
- `tools/words.py` depois de gerar; ASR com fidelidade ≥ 95%; loudness −14 LUFS e pico −1,5 dB; duração real do áudio ≥ piso.
**Gate 3 passa quando:** duração medida do áudio ≥ 8 min, fidelidade ok, nenhuma frase cortada.

## Etapa 4 — Imagens e vídeos (GATE 4)
- **Realismo e dinamismo.** O Maiquel não quer um vídeo com ~80% de imagem estática com parallax. Meta: a maior parte do tempo com movimento real (gráficos animados, vídeo gerado, câmera com paralaxe de profundidade só como complemento). Medir a fatia por tipo de cena a partir do JSON e escrever no gate: % gráfico animado, % vídeo gerado, % imagem com parallax. Parallax não passa de ~35% do tempo.
- Ferramentas locais: ComfyUI em `tools/ComfyUI` (Juggernaut XL para imagem, Wan 2.2 TI2V-5B para imagem→vídeo: `tools/walt_video_test.py`), FLUX.2 Klein (`tools/local_img.py`), modelos do Hugging Face. **Medido, não suposto:** no teste do Walt, um clipe de 3 s (73 quadros, 1280×704) levou 7 a 8 min na RTX 3070 e o movimento foi mínimo. Qualquer modelo novo (ex.: LTX-Video, CogVideoX, SVD) é testado em 1 cena, com tempo e uma tira a 6 fps no gate, antes de virar padrão. Tempo de processamento alto é aceito se a qualidade compensar; qualidade ruim não.
- Conferir VRAM livre ≥ 5 GB antes (`nvidia-smi`); EffectCraft e FLUX não rodam juntos.
- Regras visuais: empresa nomeada = logo grande (`lineup`, `relmap`, `logo_row`; chip só para 1 logo); pessoa nomeada = foto própria (`person`/`pair`), nunca nome sobre imagem genérica; queda de preço = `chart_line` com valores; comparativo e linha do tempo com logos; nada do estilo antigo `gfx.py`; crédito em inglês "Photo: Agência (via Veículo)"; texto dentro do cartão; sem logo/bandeira desenhado pelo gerador; lugar que sustenta a historia = mapa (`map`, silhueta real + `inset`); o `qa_gate` avisa `lugar_sem_mapa` e a justificativa de cada aviso vai no gate.
- Realismo: reconstrução do fato, na época e no lugar certos; nada simbólico; revisar cada clipe de vídeo a 6 fps (gente que surge, objetos que mudam).
**Gate 4 passa quando:** relatório de fatia de movimento, `qa_gate` 0 bloqueios, tiras a 6 fps dos clipes olhadas, logos/fotos de toda entidade citada na própria cena.

## Etapa 5 — Montagem e revisão (GATE 5)
1. `qa_gate` 0 bloqueios e avisos lidos.
1b. `tools/palette_check.py <id>`: cor fora da paleta so em logo/foto de terceiro; acento unico por video (`IDENTIDADE_CANAL_LEDGER.md`).
2. `qa_sheets.py` e **abrir as 8 folhas inteiras** (todas), mais o último quadro.
3. A folha congela contadores no meio da animação. Em **cada gráfico novo ou alterado**, extrair o quadro de 0,5 s antes do fim e conferir o valor final contra a fonte.
4. Conferir o ritmo de entrada de logos e fotos com a fala, o card de encerramento (6 a 8 s, nome do canal falado e escrito) e o último quadro.
5. Loudness −14 LUFS; duração ≥ 8 min.
5b. `python tools/final_sweep.py <id>` e ler `logs/varredura.md`: imagem parada ≤ 45% (nenhum trecho > 8 s), silêncio ≤ 1,2 s, pico ≤ −1,5 dBFS, legendas sem número separado da unidade, clipes Motion do tamanho da cena. Motion: duração = `timeline.plan()["L"]` + 0,5 s. Lista completa de lições em `CHECKLIST_VIDEO_YOUTUBE.md` (entrada de 28/10/2026).
**Gate 5 passa quando:** tudo acima feito e relatado, inclusive o que não foi visto (movimento contínuo, sincronia fina). Só então chamo o Maiquel para o vídeo final.

## Etapa 6 — Shorts (depois do final aprovado) (GATE 6)
`tools/shorts.py`: só trecho com nota ≥ 8; quadro em largura inteira (sem corte lateral); 20 a 45 s; legenda + chamada para o vídeo completo + exatamente 5 hashtags. Fila `social/queue.json` com horários diferentes por Short. Nada publicado sem OK.

## Inserir cena no meio muda a numeração
Arquivos por cena (`audio/scene-NN.mp3`, `gfx/ec-NN.mp4`, `ecov-NN.mov`, `media/local-NN.jpg`, `parallax-NN.mp4`, `words.json`, `music_cues`, campos `file`/`photo_file`) andam juntos: renomear pelo mapa antigo→novo em duas fases e regerar só o que mudou. Nunca rodar a etapa `converter` depois de editar `ec` à mão.

## Depois de cada erro novo
Entra na tabela "Registro de erros" do `CHECKLIST_VIDEO_YOUTUBE.md` no mesmo dia e, se for padrão, aqui.
