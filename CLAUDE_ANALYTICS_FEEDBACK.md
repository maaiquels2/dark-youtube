# CLAUDE_ANALYTICS_FEEDBACK — usar os números reais para melhorar os próximos vídeos

Vale para **Grandpa Walt (walt)**, **Show Your Work (syw)** e **The Cracked Ledger (ledger)**.

## Regra obrigatória (antes de roteirizar ou editar QUALQUER vídeo desses canais)
1. Leia `yt-analytics/reviews/LATEST.md` (e, se precisar de dados estruturados, `yt-analytics/reviews/LATEST.json`).
2. Confira a data do snapshot no topo. Se tiver mais de 3 dias, avise que a revisão está velha (rodar `yt-analytics/daily.ps1`) e siga com cautela.
3. Vá na seção **🎯 AÇÕES PARA OS PRÓXIMOS VÍDEOS** do canal do vídeo e aplique as ações que couberem ao formato (gancho, duração, título/termos de busca, formato a repetir/evitar).
4. Se o relatório disser "poucos dados", trate as ações como pista: aplique as baratas (gancho, duração) e não reescreva o formato do canal com base nelas.

## Prioridade
- **`CLAUDE_YT_ANTI_DEMONETIZATION.md` prevalece sempre.** Se uma ação do relatório conflitar com ele (ex.: "repetir formato" virar template repetitivo, título clickbait, termos de busca enganosos, aumentar volume), **não aplique** e registre o motivo.
- Depois vêm as regras do canal (`CLAUDE_WALT.md`, `CLAUDE_WALT_PRODUCTION.md`, `CHECKLIST_VIDEO_YOUTUBE.md`), depois este arquivo.
- "Repetir formato" = repetir a estrutura que funcionou com história/ângulo novo, nunca clonar vídeo.
- Termos de busca só entram no título/descrição se forem verdadeiros para o conteúdo.

## Registrar
No changelog do projeto do vídeo (ou no `CHANGELOG`/notas da pasta do episódio), adicione:
```
[AAAA-MM-DD] Analytics LATEST.md (snapshot AAAA-MM-DD)
- Aplicado: <ação> — motivo: <número citado no relatório>
- Não aplicado: <ação> — motivo: <conflito com anti-demonetização / não se aplica / poucos dados>
```

## Proibido
- Publicar, agendar, postar ou responder em qualquer plataforma. Só gerar arquivos locais; a publicação é da Maiskieu.
- Inventar métricas. Só use números que estão no relatório. CTR de miniatura não vem pela API (só no Studio).
- Editar os snapshots ou o relatório para "melhorar" números.

## Como atualizar os dados
`powershell -ExecutionPolicy Bypass -File yt-analytics\daily.ps1` (coleta YouTube + Meta, gera `report.html` e `reviews/LATEST.md`; log em `yt-analytics/logs/`).

> Alcance internacional: leia tambem CLAUDE_INTERNATIONAL_REACH.md antes de roteirizar ou preparar upload.


> Lições dos dados reais (ler antes de roteirizar/publicar): [CLAUDE_ANALYTICS_LESSONS.md](CLAUDE_ANALYTICS_LESSONS.md)

