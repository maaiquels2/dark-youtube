# Grandpa Walt: identidade do canal

Vale junto com [`REGRAS_UNIVERSAIS.md`](../REGRAS_UNIVERSAIS.md).

**Detalhe operacional** (fica onde está):
- `CLAUDE_WALT.md`: comandos e regras;
- `CLAUDE_WALT_PRODUCTION.md`: runbook, status, QA e agenda.

## Canal
- Histórias da 2ª Guerra contadas por um avô **fictício**. A história é real.
- **Plataformas** (decisão de 01/11/2026):
  - Facebook e Instagram (Página do Walt), com vídeo completo e Reels;
  - o YouTube do Walt passa a ser o The Rule Changed (rebranding no mesmo canal).
- **Arco atual:** os 10 episódios de "como conheceu a vovó". Depois, histórias gerais da guerra, com nova abertura e novo fecho pedindo para seguir a Página e comentar.

## Voz
- Abertura e fecho falados fixos: `projects/_characters/grandpa-walt/clips/` (`intro_welcome_lipsync_grok.mp4`, `outro_thanks_lipsync_grok.mp4`).
- Meio: narração OpenAI TTS, voz ash, estilo HIMYM (`spoken_bookends: true`).
- TTS pago só com OK.

## Visual
- Imagens de época geradas no local (ComfyUI, Juggernaut XL, `tools/walt_local.py`); 3 a 6 clipes Wan por episódio.
- **Nunca Grok em cena de época.** Grok só na varanda ou nos clipes, com OK de crédito.
- Varanda com quadros dos clipes padrão (pasta `porch/`).
- Fonte: Georgia (exceção histórica à regra das fontes OFL; ver CHECKLIST "Decisões em aberto").
- Câmera: zoom centrado, sem deslize (`walt_montage.py`).

## Estrutura e regras do canal
- Romance fictício sem unidade militar real e sem pessoa real.
- Aviso em todo Short e Reel: "Walt is a fictional character. The history is real."
- Risco anti-desmonetização ALTO (`CLAUDE_YT_ANTI_DEMONETIZATION.md` §4.1).

## Música
Suspense ou emotiva, nunca cômica (regra universal §7).

## Pipeline
- Montagem: `walt_tts.py` e `walt_montage.py`.
- Status: `tools/walt_status.py`.
- Facebook longo: `tools/walt_fb_long.py`; Chrome do Walt via CDP (porta muda quando o Chrome trava).
- Meta: o Maiquel agenda à mão (regra universal §1).

## Deu certo / não deu
| Data | Resultado | Lição |
|---|---|---|
| até 01/11 | deu certo | roteiros "Where To, Son?" (79% de retenção) e "Nobody Told Us Where the Train Was Going" (74%) são os modelos |
| até 01/11 | não deu | a maioria dos Shorts segura só 20–40%: conflito no 1º segundo, até ~47 s |
| 01/11 | não deu | no YouTube, público BR assiste pouco vídeo em inglês; o YouTube do Walt virou o The Rule Changed |
| 01/11 | deu certo | Facebook: Ep01 e Ep02 longos publicados (a Meta trata como Reel de 10 min); ~660–1.160 views/dia na Página |
| 25/10 | não deu | automação do Business Suite levou a bloqueio no Facebook: nunca automatizar a Meta |
