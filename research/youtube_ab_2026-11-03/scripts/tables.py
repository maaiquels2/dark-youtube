"""Gera raw/tabelas.md (canais + vencedores por nicho) só com números da API."""
import json
from pathlib import Path
RAW = Path(r"D:\DarkYouTube\research\youtube_ab_2026-11-03\raw")
ch = json.load(open(RAW / "channels_summary.json", encoding="utf-8")); w = json.load(open(RAW / "winners.json", encoding="utf-8"))
f = lambda x: f"{x:,}".replace(",", ".") if isinstance(x, int) else str(x)
out = []
for n in "ABCD":
    out.append(f"\n### Nicho {n}: canais\n\n| Canal | Criado em | Idade (dias) | Inscritos | Vídeos | Views totais | Mediana views (últimos {50} uploads) | Shorts na amostra | Uploads ≤90 d | Vídeos ≤90 d com ≥3x inscritos | Melhor views/dia ≤90 d |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for c in sorted([c for c in ch if c["niche"] == n], key=lambda c: -c["best_vpd"]):
        out.append(f"| [{c['channel']}]({c['url']}) | {c['created']} | {c['age_days']} | {f(c['subs'])} | {c['total_videos']} | {f(c['total_views'])} | {f(c['median_views_sample'])} | {c['shorts_in_sample']}/{c['sample']} | {c['recent90']} | {c['outliers3x']} | {f(c['best_vpd'])} |")
    out.append(f"\n### Nicho {n}: vídeos vencedores (últimos 90 dias)\n\n| # | Vídeo | Canal | Data | Duração (s) | Views | Views/dia | Inscritos | Views/inscritos | Views/mediana do canal | Chars título |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for i, v in enumerate(w[n], 1):
        t = v["title"].replace("|", "/")
        out.append(f"| {i} | [{t}](https://www.youtube.com/watch?v={v['videoId']}) | {v['channel']} | {v['publishedAt']} | {v['dur']} | {f(v['views'])} | {f(v['vpd'])} | {f(v['subs'])} | {v['ratio']}x | {v['x_median']}x | {len(v['title'])} |")
(RAW / "tabelas.md").write_text("\n".join(out), encoding="utf-8")
