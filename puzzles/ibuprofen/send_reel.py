"""Envia o Reel do ibuprofeno + enquete ao Telegram do usuario (ele agenda no Meta a mao)."""
import os, requests
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"'))
API = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}"
CHAT = os.environ["TELEGRAM_CHAT_ID"]
CAPTION = ("REEL SYW How It Works #3 (ibuprofeno) - agendar 01/11 20:30 no IG/FB\n\n"
           "Ibuprofen doesn't fix the pain. It mutes the alarm. Here's the enzyme it shuts down.\n"
           "Not medical advice: read the label and ask a pharmacist or doctor.\n"
           "Music: \"Interloper\" by Kevin MacLeod (incompetech.com), CC BY 4.0.\n"
           "#howitworks #science #health #ibuprofen\n\n"
           "ENQUETE: Does ibuprofen fix what's causing the pain? | Yes, it heals it | No, it mutes the alarm")
with open(ROOT / "puzzles/ibuprofen/renders/ibuprofen_yt.mp4", "rb") as f:
    r = requests.post(f"{API}/sendVideo", data={"chat_id": CHAT, "caption": CAPTION, "supports_streaming": True},
                      files={"video": ("ibuprofen_reel.mp4", f, "video/mp4")}, timeout=600)
print("video:", r.json().get("ok"), r.json().get("description", ""))
r = requests.post(f"{API}/sendPoll", json={"chat_id": CHAT, "question": "Does ibuprofen fix what's causing the pain?",
                                           "options": ["Yes, it heals it", "No, it mutes the alarm"]}, timeout=60)
print("poll:", r.json().get("ok"), r.json().get("description", ""))
