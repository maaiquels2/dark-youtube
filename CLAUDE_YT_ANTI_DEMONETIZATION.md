# CLAUDE_YT_ANTI_DEMONETIZATION.md
# Instruções obrigatórias para o Claude Code — YouTube Partner / monetização

**Raiz do Studio:** `C:\Users\Admin\Documents\Codex\2026-09-10\Dark YouTube`  
**Dono:** Maiquel (Maiqueu). Respostas e notas internas em pt-BR; copy público dos canais em EN.  
**Data desta versão:** 2026-10-26 (America/Sao_Paulo)

Este arquivo é o **manual de sobrevivência YPP** do portfólio. Vale para todo trabalho de roteiro, montagem, kit YouTube, thumb, About, frequência de upload e revisão de canal — em qualquer ferramenta (Claude Code, Codex, scripts).

Em conflito com outros docs:
1. Regras duras deste arquivo (seção 0) + “Nunca publicar sem OK do Maiquel” dos `CLAUDE_WALT*.md` / `CHECKLIST_VIDEO_YOUTUBE.md`
2. Este arquivo (política de monetização / anti–Generic & Repetitive)
3. `CLAUDE_WALT.md` / `CLAUDE_WALT_PRODUCTION.md` / `CHECKLIST_VIDEO_YOUTUBE.md` / `PADRAO_VIDEOS.md` (pipeline de produção)

Fontes que motivaram este doc (ler, não postar, não citar como “hack” na descrição do vídeo):
- [@julianfaceless — How to NEVER Get Your YTA Channels DEMONETIZED](https://x.com/julianfaceless/status/2114421875791090001) (out/2026)
- [@blain_fury — Generic & Repetitive Content em canal CMS de history docs](https://x.com/blain_fury/status/2114310291630772527) (out/2026)

---

## 0. Regras duras (não negociáveis)

1. **Nada é publicado, agendado, apelado em YPP, nem gasto (Grok / TTS pago / ads) sem OK explícito do Maiquel.** Todo episódio/vídeo termina em `approval: awaiting_user`.
2. **YouTube não pune “usar IA”.** Pune canal que **parece** conteúdo genérico, repetitivo, de fábrica ou reutilizado sem valor criativo/educativo claro.
3. **O revisor olha o CANAL INTEIRO**, não o vídeo que você “consertou”. Em poucos minutos: tema, top views, vídeos novos, watch time, títulos/thumbs, About. Um vídeo limpo não salva um canal de fábrica.
4. **CMS / MCN / Partner Manager não protege mais.** Managed O&O caiu no caso Blain (Generic & Repetitive). Trate cada canal como se fosse review humano + automação sem rede.
5. **Appeal falhou + re-review falhou** no caso Blain. Não conte com “depois a gente apela”. Previna no padrão de produção.
6. **Isolar contas.** Um flag pode arrastar o portfólio se Google / AdSense / telefone / browser profile / IP forem compartilhados. Walt ≠ Cracked Ledger ≠ SYW ≠ Fábrica TikTok em identidade de upload.
7. **Nunca** imprimir, logar ou commitar `.env` / chaves. Chrome: só perfil Dark Studio (CDP 9333) ou o perfil que o Maiquel indicar; nunca matar Profile 10 (Livia).
8. **Meta / Facebook / Instagram Reels do SYW estão pausados** (FB banido). Não tocar até o Maiquel avisar.
9. **X/Twitter:** nunca postar autonomamente. Só rascunho; browser só com OK do texto exato.
10. Antes de marcar qualquer etapa de kit/upload como `done`, rodar o **checklist pré-upload do canal** (seção 6) e gravar o resultado no `logs/` do projeto (ou em `production_status`).

---

## 1. Os três juízes (pense neles separados)

| Juiz | O que derruba | Sintoma típico | O que fazer |
|------|----------------|----------------|-------------|
| **1. Community Guidelines** | Strikes (violência, nudez, ódio, spam, etc.) | Strike / remoção | Implicar, não mostrar; EDSA; blecagem no áudio |
| **2. Advertiser-friendly** | Conteúdo “não amigável a anunciante” | Cifrão amarelo / limited ads | Tom, thumb limpa, sem gore na capa, sem clickbait sexual/violento |
| **3. YPP / Inauthentic & reused / Generic & repetitive** | Canal parece fábrica sem valor | Fora do Partner; “Generic or repetitive content”; earnings zerados | Variar template, valor educativo real, ritmo humano, transformar clipes, About de criador |

**Generic or repetitive content** (texto típico do Studio):  
> Content that appears generic or repetitive, or does not deliver significant creative, educational, or other value.

O caso Blain: documentários longos de **história**, automação com **arquivo + imagens**, **só voz de IA**, **3–4 vídeos/dia** no CMS por 6 meses → hit. Não era “IA na cara”; era **padrão de fábrica**.

---

## 2. Sinais de fábrica (evitar em TODOS os canais)

Trate como risco alto se o canal, olhado de fora, tiver vários destes:

- Mesmo layout / intro / lower-third / tipografia / paleta em **quase todos** os vídeos, sem variação perceptível
- Upload em ritmo de CMS (**vários longos por dia**, todo dia, semanas seguidas)
- Narração monótona + B-roll de arquivo / stock / slideshow sem transformação clara
- Títulos e thumbs com a mesma fórmula visual repetida (mesma fonte, mesmos 2 emojis, mesmo enquadramento)
- About vazio, genérico, ou “AI history channel / daily uploads”
- Shorts em massa com o **mesmo template** (mesmo fundo, mesma animação, mesma posição do destaque)
- Clipes reutilizados com mudança cosmética (crop, speed, overlay) sem valor novo
- Canal “dorminhoco / sleep history / 4 docs/day” — exatamente o padrão que está sendo caçado
- Vários canais no mesmo AdSense / mesmo login Google “só pra escalar”

**Não é defesa suficiente:**
- “Tem Partner Manager / CMS”
- “É educativo”
- “Só a voz é IA”
- “Os fatos são reais”
- “Vou apelar”

---

## 3. O que o revisor faria em 5 minutos (simule SEMPRE)

Antes de pedir aprovação de upload, o Claude Code (ou quem estiver no kit) deve responder por escrito no log do episódio:

1. **Tema do canal em uma frase** — soa como criador com ponto de vista, ou dump genérico?
2. **Top 3 vídeos por views** — são distintos entre si ou clones?
3. **5 vídeos mais novos** — mesma capa/estrutura? Ritmo de upload humano?
4. **Watch time / retenção** (se houver número real no Studio; **nunca inventar**) — retenção razoável ou drop imediato?
5. **Títulos + thumbs** — prometem história específica ou “HISTORY DOCUMENTARY #47”?
6. **About** — quem é o canal, o que o espectador ganha, disclaimer de ficção se aplicável?
7. **Valor criativo/educativo óbvio** — o espectador aprende / sente / segue uma narrativa, ou só consome ruído longo?

Se a resposta for “parece fábrica”, **não avançar kit/upload**. Voltar ao roteiro/montagem e variar.

---

## 4. Canais ativos — regras específicas

### 4.1 Grandpa Walt (risco ALTO — nicho history / war storytelling)

**Identidade:** avatar “Grandpa Walt” na varanda conta como conheceu a grandma na guerra (HIMYM-style). Walt e romances = ficção; história = real e checada.  
**Pipeline:** `CLAUDE_WALT.md` + `CLAUDE_WALT_PRODUCTION.md`.  
**Clipes fixos aprovados:**  
- `projects\_characters\grandpa-walt\clips\intro_welcome_lipsync_grok.mp4` (abertura falada)  
- `projects\_characters\grandpa-walt\clips\outro_thanks_lipsync_grok.mp4` (fechamento falado, antes do endcard HyperFrames)  
- backups mudos: `intro_15s.mp4`, `outro_15s.mp4`

**Anti–Generic & Repetitive (Walt):**

| Regra | Detalhe |
|-------|---------|
| Frequência | **Máx. 1 episódio longo bem feito por upload cycle** (meta humana). Proibido ritmo 3–4/dia. Preferir 1–3/semana quando a série estiver no ar — confirmar ritmo com Maiquel. |
| Miolo único | Intro/outro fixos OK. O **miolo** (cenas, gancho, personagem secundário, local, data, carta, objeto) **muda a cada ep**. Não “outro pedaço da guerra” no mesmo template visual. |
| Gancho | Cada ep abre com promessa específica (pessoa, lugar, data, contradição). Sem cold open genérico “during the war…”. |
| Mídia | ~30% varanda (banco Grok) + ~70% cenas de época. Cenas de época = **local (ComfyUI / Wan)**, nunca Grok. Archive puro + narração igual = bandeira. |
| Transformação | Imagens/clips de arquivo (se usar) precisam de framing, ritmo, contexto narrativo — não slideshow. |
| Tom advertiser | Guerra: **implicar** violência; não mostrar gore. EDSA nos primeiros 30s quando o tema for pesado. Thumb limpa (sem sangue, sem corpos, sem texto “KILL/DEAD” gritante). |
| Disclaimer | Em descrição e, se couber, tela: *“Walt is a fictional character. The history is real.”* (já no checklist de Shorts) |
| About | Canal de **storyteller** (“how I fell in love with your grandma during the war”), não “AI WWII documentaries daily”. |
| Conta | Upload/kit só na conta Google que o Maiquel indicar para Walt. **Não** misturar com Cracked Ledger (`UCvmyoFV8fg5fMtoejd82CRA`) nem SYW. Isolar browser profile / AdSense. |
| CMS | **Não** colocar Walt sob CMS/MCN “pra proteger”. Produzir como canal O&O limpo. |

**Checklist pré-montagem Walt (além do PRODUCTION):**
- [ ] Episódio tem gancho e “motivo deste ep” distintos do anterior
- [ ] Pelo menos 1 elemento visual/narrativo novo (local, objeto, personagem, estrutura de atos)
- [ ] Fact check no `.md` preenchido; sem unidade real / gente real nos romances
- [ ] Intro/outro falados corretos; endcard HyperFrames com `next_title`
- [ ] Sem gore explícito; violência só sugerida
- [ ] Disclaimer de ficção no kit
- [ ] Frequência do canal esta semana ainda parece humana
- [ ] `approval: awaiting_user` — sem publicar

### 4.2 The Cracked Ledger / Dark long-form (risco MÉDIO–ALTO — finance / true crime-ish)

**Pipeline:** `CHECKLIST_VIDEO_YOUTUBE.md` + `PADRAO_VIDEOS.md`.  
**Canal Studio a conferir antes do upload:** `studio.youtube.com/channel/UCvmyoFV8fg5fMtoejd82CRA` (parar se cair em `channel-appeal`).

**Anti–Generic & Repetitive (Ledger):**
- Um tema famoso **com ângulo novo**, não “outra falência genérica”.
- Fotos reais de pessoas citadas; logos reais; fontes oficiais — valor investigativo **visível**.
- Gráficos EffectCraft com foco único; proibido kit visual idêntico em todos os vídeos sem variação.
- Ritmo de agenda humana (checklist atual: seg/qua/sex/dom 18:00 BRT) — **não** virar 3 longos/dia.
- Título vende história (personagem + valor + contradição), não catálogo.
- Antes do envio: abrir Studio e confirmar que a conta não está em appeal.
- Isolar AdSense/login deste canal dos outros.

**Advertiser-friendly:**
- Fraude/finanças: fatos + fontes; sem celebrar crime; sem gore.
- Thumb: protagonista / logo / valor — sem sangue, sem “SHOCKING” vazio.

### 4.3 Show Your Work Puzzles — SYW (risco MÉDIO — mass-produced Shorts)

**Formato:** Shorts de enigmas math/lógica em EN (voz Brian/ElevenLabs, animação em código, papel milimetrado, destaque vermelho; 1:00–1:50) + **1 longo/semana**.  
**Contas:** YT `@showyourworkpuzzles` (ID `UCrgIwaM5dsNRgrKqZkOepRg`); TikTok/IG `@syw.puzzles`.  
**Ritmo alvo:** 6 Shorts/semana (seg–sáb YT 13:00 / TikTok 18:00 / IG-FB 19:00 America/Sao_Paulo) + longo domingo. **Reduzir quantidade de envios por dia** quando possível (menos rajadas).  
**Analytics:** `C:\Users\Admin\OpenBot\Shared\show_your_work_analytics\` — só usar números reais de snapshots; **nunca inventar métricas**.  
**Meta/IG Reels:** pausados — não publicar lá.

**Anti–Generic & Repetitive (SYW):**

| Regra | Detalhe |
|-------|---------|
| Variar template | Proibido 40 Shorts com o **mesmo** layout/papel/posição do destaque/vermelho idêntico. Alternar composição, tipografia de apoio, pacing, tipo de enigma. |
| Valor educativo | Cada Short ensina um raciocínio, não só “adivinhe”. O longo semanal é a prova de valor — manter. |
| Não parecer fábrica de puzzle AI | Evitar batch de dezenas de vídeos quase iguais no mesmo dia. Preferir 1 Short/dia no ritmo, não 6 de uma vez se o Studio mostrar padrão robótico. |
| About / branding | Canal de “show your work” (processo), não “1000 puzzles AI”. |
| Conta | Isolar Google/AdSense/browser do Walt e do Ledger. |
| Números | Briefings e `respostas_*.md` só com dados de snapshot; se não houver snapshot, dizer que falta dado. |

**Checklist pré-upload SYW Short:**
- [ ] Enigma / solução / visual distintos do Short anterior
- [ ] Layout não é clone pixel-a-pixel dos últimos 5
- [ ] Voz + legenda sincronizadas; duração 1:00–1:50
- [ ] Copy EN; sem Meta/FB/IG se ainda pausado
- [ ] Não empilhar uploads no mesmo minuto sem necessidade
- [ ] OK do Maiquel antes de publicar

---

## 5. Regras de conteúdo (Guidelines + Advertiser) — portfólio

Aplicar no roteiro, thumb, título e primeiros 30s:

1. **Implicar em vez de descrever/mostrar gore.** Guerra, crime, morte: corte para reação, documento, silêncio, detalhe simbólico.
2. **Citar fonte** quando o tema for sensível (“trial transcript”, “official report”, arquivo datado) — reforça valor educativo (Juiz 3) e reduz “sensacionalismo vazio” (Juiz 2).
3. **Blecagem no áudio**, não asterisco na thumb. Thumb limpa.
4. **EDSA** (context / disclaimer educativo) cedo quando o episódio entrar em zona cinzenta.
5. **Transformar clipes:** se reutilizar arquivo, mudar ritmo, contexto, narração, framing — não reupload com overlay.
6. **Variar template** de série (cores, lower-thirds, pacing) ao longo da temporada, sem perder identidade de marca.
6a. **Revezar o molde do título** (Ledger, Rule Changed, SYW longo): antes de aprovar o título, listar o molde dos 2 últimos vídeos do canal (ex.: "What (Actually) Happened to X", "Who Really Killed X?", pergunta simples, "X: frase", afirmação curta, "A — B" com travessão). O título novo não repete nenhum dos dois, e o molde com travessão ou dois-pontos aparece no máximo 3 vezes a cada 10 vídeos. Sem sufixo fixo ("| History for Sleep") em todo título. No teste A/B de título vale o mesmo para as 3 opções.
6b. **Abertura do roteiro diferente** (Gate 2): comparar os primeiros ~30 s do roteiro novo com os 3 últimos do canal. Se a frase de abertura, o tipo de gancho ou a ordem dos blocos forem iguais, reescrever. Os padrões de retenção dizem *o que* o gancho faz, não *como* começa. Ao usar um roteiro antigo como exemplo, copiar a voz, nunca as frases.
6c. **Ideias pelo que falta:** para escolher tema, dar ao agente a lista completa de vídeos já publicados no canal e pedir as lacunas, não "mais ideias". Proibido refazer um vídeo que foi bem trocando só número ou título.
6d. **Capas vizinhas diferentes:** duas capas seguidas na página do canal nunca têm o mesmo conceito (ver `REGRAS_UNIVERSAIS.md` §12). Conferir olhando a grade dos últimos 6 vídeos antes do upload.
7. **Sem clickbait sexual ou de violência extrema** em título/thumb.
8. Upload config (Ledger checklist): não é para crianças; conteúdo alterado = Sim quando houver IA/avatar; idioma EN; categoria adequada (Educação / Entertainment conforme o canal).

---

## 6. Checklist pré-upload (copiar para o log de cada vídeo)

Preencher e salvar (ex.: `projects/<id>/logs/yt_safety_<data>.md` ou `projects/grandpa-walt/<ep>/logs/yt_safety.md`):

```markdown
# YT safety — <canal> — <id/ep> — <data America/Sao_Paulo>

## Juiz 3 — Generic / repetitive / inauthentic
- [ ] Canal, visto pelos 5 vídeos novos + top views, NÃO parece fábrica
- [ ] Este vídeo tem gancho / visual / estrutura distintos do anterior
- [ ] Ritmo de upload da semana é humano (não CMS 3–4/dia)
- [ ] About do canal está alinhado a “criador com valor”, não dump
- [ ] Há valor criativo ou educativo óbvio (não só duração longa)
- [ ] Conta / AdSense / browser profile isolados dos outros canais do portfólio
- [ ] NÃO estamos dependendo de CMS/MCN como “escudo”

## Juiz 2 — Advertiser-friendly
- [ ] Thumb limpa (sem gore, sem clickbait proibido)
- [ ] Título sem sensacionalismo vazio
- [ ] Primeiros 30s: tom OK; EDSA se zona cinzenta
- [ ] Violência só implicada

## Juiz 1 — Guidelines
- [ ] Sem conteúdo que gere strike óbvio
- [ ] Áudio com blecagem se necessário

## Conta
- [ ] Confirmei no Studio a URL/canal certo (Walt / Ledger / SYW)
- [ ] Não está em channel-appeal / monetization suspended
- [ ] Kit gerado e checado (scripts do canal, se existirem)

## Aprovação
- [ ] Maiquel aprovou por escrito o master + o upload
- [ ] Status: approval awaiting_user → só então upload manual/fila
```

**Se qualquer item crítico do Juiz 3 falhar → não gerar kit de upload; corrigir produção.**

---

## 7. O que fazer se o Studio mostrar “Generic or repetitive” / monetização suspensa

1. **Parar todos os uploads** daquele Google/canal imediatamente.
2. **Não apagar vídeos** se for apelar (o próprio Studio avisa: appeal só se não deletou desde a suspensão).
3. Avisar o Maiquel com: print/data, texto exato do motivo, canal ID, se há prazo de appeal.
4. **Não** abrir appeal em massa em vários canais no mesmo dia sem plano — appeal falho pode arriscar outros canais do mesmo operador (aviso do Studio no caso Blain).
5. Auditar o canal com a seção 3; listar os 10 vídeos mais “fábrica” e o que os torna repetitivos.
6. Plano de remediação (só com OK): variar template, reduzir frequência, reforçar About, produzir 1–2 peças claramente distintas de alto valor **antes** de qualquer appeal — sabendo que appeal pode falhar.
7. Revisar isolamento de contas do portfólio.
8. **Nunca** inventar métricas nem prometer recuperação.

---

## 8. Integração com o pipeline (Claude Code)

### Quando este arquivo é obrigatório
- Qualquer passo `kit`, `upload`, `shorts` publish queue, mudança de About, thumb, título em lote, ou planejamento de calendário de uploads
- QA final de Walt (`approval`) e Ledger (seção 9–10 do checklist)
- Briefings SYW e geração de lote de Shorts

### Comandos / artefatos existentes (não substituir — só acrescentar o gate)
- Walt: `CLAUDE_WALT.md`, `CLAUDE_WALT_PRODUCTION.md`, `python tools/walt_status.py …`
- Ledger: `CHECKLIST_VIDEO_YOUTUBE.md`, `python tools/yt_kit.py`, `python tools/kit_check.py`, `python tools/qa_gate.py`
- SYW: pasta `puzzles\` + analytics em `OpenBot\Shared\show_your_work_analytics\`

### Ao planejar temporada / calendário
- Preferir **qualidade e variação** a volume.
- Explicitar no plano: frequência alvo, o que muda entre episódios, e risco Juiz 3.
- Qualquer proposta de “3–4 vídeos longos por dia” ou “CMS pra escalar” = **rejeitar** e explicar com este doc.

### Ao escrever roteiro
- Incluir no fact-check / notas: “diferença vs ep anterior” (1–3 bullets).
- Marcar zona Guidelines/Advertiser se houver.

---

## 9. Isolamento de contas (checklist operacional)

Para cada canal (Walt, Ledger, SYW, outros Dark):

- [ ] Conta Google própria (ou a que o Maiquel designou), não compartilhada “só pra conveniência”
- [ ] AdSense / pagamento não amarra punição em cascata sem necessidade
- [ ] Browser profile separado (Dark Studio vs Walt vs SYW conforme já existir: ex. `browser_profile`, `browser_profile_walt`)
- [ ] Telefone / 2FA conforme o Maiquel — não reutilizar o mesmo fator em todos se ele pedir isolamento
- [ ] Não logar todos os canais no mesmo Chrome profile no mesmo dia de upload em massa
- [ ] Fábrica TikTok (Micaela) e n8n **não** usam a mesma sessão de upload YT destes canais

Se não souber qual conta usar → **perguntar ao Maiquel**, não adivinhar.

---

## 10. Resumo em uma página (colar no início de uma sessão Claude Code)

```
Você está no Dark YouTube Studio do Maiquel.
Antes de kit/upload/calendário, ler CLAUDE_YT_ANTI_DEMONETIZATION.md.

YouTube caça GENERIC & REPETITIVE / fábrica — CMS não salva.
IA é permitida; parecer massa não é.

Walt = history storytelling → risco alto → 1 ep forte, miolo único, sem gore, disclaimer ficção, conta isolada.
Ledger = investigações → ângulo novo, fontes, ritmo humano, Studio certo.
SYW = puzzles → variar template Shorts, manter longo semanal, sem Meta por enquanto, sem métricas inventadas.

Nunca publicar sem OK. Nunca inventar números. Nunca postar no X sozinho.
Simular review de canal (seção 3) e preencher checklist seção 6 no log.
```

---

## 11. Registro de atualizações

| Data | Mudança |
|------|---------|
| 2026-11-05 | Itens 6a–6d (molde de título revezado, abertura diferente, ideias pelo que falta, capas vizinhas diferentes). Base: @ytajourney, canal de história para dormir desmonetizado por "repetitive content" em 21/10/2026 (x.com/ytajourney/status/2118452265145254022). Aprovado pelo Maiquel. |
| 2026-10-26 | Criação. Base: julianfaceless (3 juízes, review de canal, AI ≠ ban) + blain_fury (Generic & Repetitive em history CMS 3–4/dia; appeal falhou; automação arquivo+voz). Regras por canal: Walt, Ledger, SYW. |

Quando o Maiquel apontar um erro novo de monetização/YPP, **acrescentar neste arquivo no mesmo dia** (como o checklist do Ledger faz com erros de produção).
