# Plano de melhoria: o que levar dos 11 repositórios (29/10/2026)

Base: li o código dos repositórios (clones só para leitura, nada instalado ou executado) e comparei com `PADRAO_VIDEOS.md`, `CHECKLIST_VIDEO_YOUTUBE.md`, `tools/qa_gate.py`, `tools/qa_sheets.py`, `tools/shorts.py` e `tools/ec_montage.py`.
Regra do plano: **não instalar nenhuma skill**. Só portar ideias e checagens, uma por vez, cada uma com critério de aceite.

## 1. O que cada repositório tem de útil (aprofundado)

| Repo | Veredito | O que realmente serve | Por que não instalar |
|---|---|---|---|
| **win4r/video-director** | Fonte principal de ideias | Critic independente (rejeita por padrão, nota por eixo, P0/P1/P2, "ship" só com todos os eixos >= 8); gancho legível em 3 s com texto >= 84 px e CTA >= 48 px; zona segura 9:16 (x 60-1020, y 250-1500); quadro 0 acabado; "fix card" + diff de quadros fora do escopo; tabela sintoma -> mecanismo -> correção; lista de cacoetes de IA | É para vídeo feito em código (HTML/Remotion). Seu fluxo é documental com Grok + EffectCraft + HyperFrames; a skill inteira brigaria com o `video-gate` |
| **Pocock/skills** | Boa ideia para os documentos | `retro` (revisar o que o agente errou e melhorar o ambiente), `writing-for-agents` (divulgação progressiva, cortar regra que não muda comportamento) | São skills de engenharia de software; auto-atualização por padrão |
| **Addy Osmani/agent-skills** | Duas ideias | `constraint-driven-development` (piso de qualidade escrito, com número, checável por máquina); `doubt-driven-development` (revisor de contexto limpo, no máximo 3 ciclos) | 25 skills de engenharia; hooks e comandos `/build auto` |
| **Superpowers** | Uma frase | `verification-before-completion`: sem alegação de pronto sem evidência nova. Você já tem isso no checklist (§7) | Hook de início de sessão, logo de terceiros no companheiro visual |
| **Karpathy** | Nada novo | 4 princípios que o Ponytail e o seu uso de Claude já cobrem | Origem divergente (multica-ai x forrestchang) |
| **Ponytail** | Já em uso | Manter | - |
| **Caveman** | Descartar | `caveman-compress` mandaria seus documentos (em português, com regras exatas) para um modelo e perderia precisão | Telemetria para Supabase; `curl | bash` |
| **Graphify** | Descartar por ora | Mapa de código local é possível, mas o Ponytail já dá o mapa do repositório | Hooks `PreToolUse`, HTTP em vários módulos, nome do repositório divergente |
| **UI UX Pro Max** | Não serve | Tem `charts.csv`, `colors.csv`, `motion.csv`, mas é para UI de web/app | npm que escreve em projetos |
| **Taste Skill** | Não serve | `inspect.mjs` (renderiza a página em 3 larguras, mede, sai com código 1) é o mesmo padrão que o HyperFrames CLI já faz | Baixa imagens da web; instalação por symlink |
| **Anthropic/skills** | Não serve | Nenhuma é de vídeo (`slack-gif-creator` é GIF de 128-480 px) | - |
| **8 sites** | Não servem | Galerias de design para landing page; 3dicons é CC0 | - |

## 2. Lacunas reais no seu pipeline

1. **Quadro 0 preto em todo vídeo longo.** Medido nos dois vídeos aprovados que testei. Provável causa: `tools/ec_montage.py:63` aplica `fade=in:st=0:d=0.9:color=black` na primeira cena.
2. **Ninguém mede o MP4.** `qa_gate` lê o plano, `qa_sheets` gera quadros para olhar, `loudnorm` aplica -14 LUFS mas nada confere o resultado. Já resolvido em parte pelo `tools/qa_render.py` (ligado ao `produce.py`).
3. **Quem revisa é quem montou.** Hoje o Claude que construiu o vídeo dá a nota por minuto. Falta revisor independente.
4. **Correção sem prova de escopo.** Casos registrados: Argentina ("36 pontos validados" e 6 errados). Falta provar que a correção não mexeu no resto.
5. **Shorts/Reels sem zona segura 9:16 medida.** `shorts.py` usa 1080x608 centralizado e título fixo no alto; não comparei com y 250-1500 nem com os ~20% de baixo.
6. **Regras duplicadas.** Cerca de 88 KB em 7 documentos de regras; a regra do capítulo, por exemplo, aparece em `PADRAO_VIDEOS`, `CHECKLIST` e `GEMINI.md`.
7. **Fábrica do TikTok:** não vi o código dela, só os nomes dos arquivos (`tools/tiktok_upload.py`, `tools/walt_tiktok.py`, `social/queue.json`). Os itens abaixo para ela são hipóteses até eu ler o código.

## 3. Fases (cada uma: o que muda, aceite, risco)

### Fase 0: quadro 0 (30 min)
- **Mudar:** `ec_montage.py:63`, primeira cena sem fade preto (ou 0,15 s a partir de uma imagem já com o gancho).
- **Aceite:** `python tools/qa_render.py <final.mp4>` sem FAIL de `quadro0` em um projeto novo renderizado.
- **Risco:** vídeos já aprovados não são refeitos. Cenas depois da primeira não mudam.

### Fase 1: medir mais, sem custo (1 a 2 h)
- Acrescentar ao `qa_sheets.py`: folha dos 3 primeiros segundos (um quadro a cada 0,5 s) e folha a 360 px de largura, para olhar sem som e em tamanho de celular.
- No `qa_render.py`: `--short` com zona segura 9:16 e texto mínimo (verificar com quadros reais, não só pelo plano).
- **Aceite:** as duas folhas saem em `logs/qa_video/` e o `qa_render --short` roda em um Short real.
- **Risco:** baixo (só leitura).

### Fase 2: revisor independente (2 h, sem código)
- Criar `tools/critico_prompt.md` com o rubrico do video-director adaptado a vocês (gancho, clareza, legibilidade, ritmo, composição, verdade/fontes, som) e a regra "padrão = reprovar".
- No checklist §7: depois das folhas, um **subagente novo**, que não viu a montagem, recebe só folhas, roteiro e este rubrico. Ship com todos os eixos >= 8 e nenhum P0. Uma rodada de correção e uma conferência (limite de 3 ciclos, ideia do Addy).
- **Aceite:** testar no próximo vídeo e comparar com a nota que o Claude da montagem daria. Guardar as duas.
- **Risco:** o subagente repete as mesmas fraquezas do modelo; o olhar do Maiquel no master continua obrigatório.

### Fase 3: correção com prova de escopo (investigar primeiro, 1 h)
- Descobrir se os clipes por cena ficam em cache. Se sim: guardar um hash por cena antes e depois de cada correção; só as cenas apontadas podem mudar.
- **Aceite:** relatório "cenas alteradas: 12, 30; as outras idênticas".
- **Risco:** se não houver cache por cena, descartar a fase.

### Fase 4: Shorts e Fábrica do TikTok (depende da leitura do código)
- Ler `shorts.py`, `walt_shorts.py`, `tiktok_upload.py` e a fila antes de decidir.
- Candidatas: zona segura, gancho >= 84 px, quadro 0 acabado, `qa_render --short` antes de entrar em `social/queue.json`.
- **Aceite:** definir depois da leitura. Nada vai para a fila sem aprovação (regra já existente).

### Fase 5: faxina dos documentos (2 a 3 h)
- Usar o método do `retro` e do `writing-for-agents`: uma fonte única por regra e os outros documentos só apontam para ela; cortar regra que não muda comportamento.
- Cada regra nova ganha uma coluna "como se checa" (comando ou olhar nos quadros). Regra sem checagem possível fica marcada como "julgamento".
- **Aceite:** nenhuma regra perdida (lista antes/depois conferida por diff) e o `video-gate` continua lendo o mesmo caminho.
- **Risco:** perder regra por erro. Fazer em branch e conferir com o Maiquel.

## 4. O que não fazer
- Não instalar nenhum dos 11 repositórios.
- Não rodar `caveman-compress` nos documentos.
- Não ligar o `qa_render` como bloqueio antes da Fase 0; senão todo vídeo novo trava.
- Não trocar o HyperFrames/EffectCraft pelo fluxo "tudo em código" do video-director.

## 5. O que não foi verificado
- Estrelas e benchmarks dos repositórios.
- Comportamento real do `video-director` rodando (só li o código).
- Quanto do ruído de "imagem parada" do `qa_render` é Ken Burns intencional.
- O código da Fábrica do TikTok.
