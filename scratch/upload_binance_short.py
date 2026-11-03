"""Sobe UM Short da Binance e agenda, com o texto de output/shorts/shorts.json.
Uso: YT_CDP_PORT=9336 python scratch/upload_binance_short.py <n>   (data e hora: yt_date / yt_time do shorts.json)"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import yt_upload as Y
P = "binance-hack-north-korea-20261102-150000"; SD = ROOT / "projects" / P / "output" / "shorts"
n = int(sys.argv[1]); s = next(x for x in json.loads((SD / "shorts.json").read_text(encoding="utf-8")) if x["file"] == f"binance-{n}.mp4")
kit = {"title": s["title"], "description": s["description"], "tags": s["tags"] + ["The Cracked Ledger"]}
rv = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--resume-vid=")), None)
vid = Y.upload(P, None, s["yt_date"], s["yt_time"], video=SD / s["file"], kit=kit, srt=None, resume="--resume" in sys.argv, resume_vid=rv)
print("SHORT binance", n, s["yt_date"], s["yt_time"], "https://youtube.com/shorts/" + vid)
