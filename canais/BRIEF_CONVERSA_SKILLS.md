Esta é a conversa fixa de SKILLS do projeto Dark YouTube. Tudo que for teste de skill, protótipo de ferramenta ou avaliação de repositório passa por aqui.

Tarefa agora: montar o registro único de skills.
1. Ler `SKILLS_PIPELINE.md`, `PLANO_MELHORIAS_SKILLS.md`, `research/skills_sh_varredura_2026-11-01.md`, `TOOLS_MOTION.md`, as pastas `.claude/skills/*` (cada uma tem `SOURCE.md` e `LICENSE`) e as memórias de skills e ferramentas (`video-skills-installed`, `project-skills-review-qa-tools`, `ace-step-music`, `local-image-gen`, `kokoro-voice-onyx`, `motion-standard-ledger`).
2. Criar `skills/REGISTRO.md` com uma linha por skill ou ferramenta: nome; para que serve; etapa do pipeline (video-gate 1 a 6, kit, publicação); repositório/URL e commit; licença; onde está instalada; status (em uso / aprovada / reprovada / só lida / não instalar); o que deu certo e errado no teste, com data e projeto; quais canais usam. Incluir as ferramentas locais (FLUX Klein, Kokoro, ACE-Step, faster-whisper, EffectCraft/ec_lib, HyperFrames, ComfyUI/Wan) e as descartadas, com o motivo.
3. Criar `skills/TESTE_MODELO.md` (objetivo, comando, tempo, resultado, quadros/medidas olhados, decisão) e a pasta `skills/testes/` para os relatórios.
4. Fazer `SKILLS_PIPELINE.md` apontar para `skills/REGISTRO.md` como fonte única.

Regras: não instalar nem rodar scripts de terceiros sem meu OK; não editar `puzzles/ec_lib`; só mexer em `skills/` e `SKILLS_PIPELINE.md`. Onde não houver evidência, escrever "não conferido".
