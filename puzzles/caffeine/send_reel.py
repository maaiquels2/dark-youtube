"""Envia o Reel da cafeina + enquete ao Telegram do usuario (ele agenda no Meta a mao)."""
import os, requests
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"'))
API = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}"
CHAT = os.environ["TELEGRAM_CHAT_ID"]
CAPTION = ("REEL SYW How It Works #2 (cafeina) - agendar 31/10 20:30 no IG/FB\n\n"
           "Coffee doesn't give you energy. It hides how tired you are. Here's the molecule trick.\n"
           "Up to 400 mg a day is considered safe for most healthy adults (U.S. FDA). Not medical advice.\n"
           "Music: \"Stay the Course\" by Kevin MacLeod (incompetech.com), CC BY 4.0.\n"
           "#howitworks #science #caffeine #coffee\n\n"
           "ENQUETE: Does coffee give you energy? | Yes, it does | It hides tiredness")
with open(ROOT / "puzzles/caffeine/renders/caffeine_yt.mp4", "rb") as f:
    r = requests.post(f"{API}/sendVideo", data={"chat_id": CHAT, "caption": CAPTION, "supports_streaming": True},
                      files={"video": ("caffeine_reel.mp4", f, "video/mp4")}, timeout=600)
print("video:", r.json().get("ok"), r.json().get("description", ""))
r = requests.post(f"{API}/sendPoll", json={"chat_id": CHAT, "question": "Does coffee give you energy?",
                                           "options": ["Yes, it does", "It hides tiredness"]}, timeout=60)
print("poll:", r.json().get("ok"), r.json().get("description", ""))
