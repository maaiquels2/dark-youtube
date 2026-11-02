# Skills do pipeline de vídeo — quem faz o quê (01/11/2026)

> **Fonte única: [`skills/REGISTRO.md`](skills/REGISTRO.md).** Status, licença, testes e descartes de cada skill ou ferramenta ficam lá; testes novos seguem `skills/TESTE_MODELO.md` e vão para `skills/testes/`. Este arquivo é só o resumo por etapa; se divergir, vale o registro.

Vale para todos os canais (Show Your Work, Cracked Ledger, Grandpa Walt, The Rule Changed). As regras da casa vencem as das skills: `video-gate`, `CHECKLIST_VIDEO_YOUTUBE.md`, `CLAUDE_YT_ANTI_DEMONETIZATION.md` e as memórias. As skills de fora são guias. Se uma delas mandar usar serviço pago, nuvem ou instalar algo, isso só vale com OK do Maiquel.

Skills instaladas em `.claude/skills/`. Cada pasta tem `SOURCE.md` (repositório, commit, licença) e `LICENSE`. Nenhum script de terceiros foi executado.

| Etapa (video-gate) | Skill | Função no nosso pipeline | Cuidado |
|---|---|---|---|
| 1 Pesquisa | **fact-check-workflow** | Checagem estilo jornalismo: cada afirmação do roteiro vira item com fonte, nota (verdadeiro / precisa de contexto / sem fonte) e decisão. Rodar no fim do Gate 1 e de novo no roteiro (Gate 2). | Saída vai para `logs/gate-1.md` e `logs/gate-2.md`. |
| 2 Roteiro | **technical-video-script** | Revisar o roteiro como "folha de cenas" (tela à esquerda, narração à direita): gancho de 30 s, ritmo por capítulo, orçamento de tempo, lista de cortes e descrição com 1 chamada. Usar para revisar, não para trocar a estrutura. | Foi feita para screencast técnico. Nossas regras de retenção (PADRAO_VIDEOS.md) e a skill `cortes-verticais` têm prioridade. |
| 3 Fala | **faster-whisper** (biblioteca, não a skill) | `tools/asr_local.py <projeto>`: transcrição local e grátis da narração contra o roteiro, no lugar da checagem paga da OpenAI (`tools/words.py`). | A skill do skills.sh é só Linux/Mac e roda scripts próprios; instalei só o pacote `faster-whisper` no `.venv`. |
| 3 Fala (teste 01/11) | | Piloto robocalls: fidelidade 98,1% (sem números), contra 94,4% bruto no Whisper da OpenAI. Na CPU levou ~15 min. Com `nvidia-cublas-cu12` 12.9 e `nvidia-cudnn-cu12` 9.27 no `.venv` (instalados em 01/11, com OK do Maiquel), roda na GPU em 1 min 32 s (fidelidade 98,2%), mesmo com um render do EffectCraft ao mesmo tempo. O script acha as DLLs sozinho. | |
| 4 Imagens | **flux-best-practices** | Como escrever prompt para o FLUX.2 Klein local (`tools/local_img.py`, `flux_vertical.py`): ordem dos elementos, luz, câmera, época, sem texto na imagem. | Licença AGPL-3.0 no repositório (uso interno ok; não redistribuir). |
| 4 Imagens | **comfyui-prompt-engineer** | Prompt certo para cada modelo do ComfyUI (Juggernaut XL, Wan 2.2) e negativos. | Só local; nada de nuvem paga. |
| 4 Imagens | **comfyui-troubleshooter** | Quando um workflow do ComfyUI falhar (erro, nó faltando, VRAM). | Instalar nó novo ou modelo = perguntar antes. |
| 4/5 Trilha | **acestep** | Gerar trilha de suspense com o ACE-Step local (memória `ace-step-music`) ou separar faixas. | A skill usa por padrão a nuvem acemusic.ai com chave. Para nós, só o modo local. Trilha da casa: suspense, nunca cômica. |
| 5 Montagem | **ffmpeg** | Receitas de conversão, corte, compressão, áudio, legenda queimada. Usar junto com as ferramentas do repo (`montage.py`, `tools/final_sweep.py`). | As partes de Remotion não se aplicam. |
| 5 Revisão | **character-animation-qa** | Roteiro de QA de animação: amostra de quadros, prévia no navegador (HyperFrames) e ffprobe do arquivo final. Complementa as folhas de contato. | Repo AGPL-3.0; o SKILL.md diz MIT. |
| Kit YouTube | **youtube-seo** | Título, descrição, capítulos, tags e miniatura pensando em busca e em citação por IA. Usar no `tools/yt_kit.py` / kit de cada vídeo. | Sempre depois do checklist anti-desmonetização (seção 6). |

## Ficaram de fora (e por quê)
- **faceless-explainer** e **embedded-captions** (HeyGen): aposentadas pela HeyGen em 21/10/2026 e incorporadas às skills HyperFrames que já temos (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`).
- **motion-broll** (barty-bart): o repositório não tem licença (todos os direitos reservados), teve aviso em 2 das 3 auditorias e depende de um `setup.sh` com motor próprio. Instalar só se o autor publicar uma licença e depois de ler o código.
