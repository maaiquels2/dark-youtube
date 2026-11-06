"""Cliente mínimo da YouTube Data API v3 (só leitura). A chave vem do .env e nunca é impressa."""
import json, urllib.request, urllib.parse, urllib.error
from pathlib import Path

ROOT = Path(r"D:\DarkYouTube")
OUT = ROOT / "research" / "youtube_ab_2026-11-03"
QUOTA_FILE = OUT / "raw" / "quota.json"
COST = {"search": 100, "videos": 1, "channels": 1, "playlistItems": 1}


def _key():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("YOUTUBE_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("YOUTUBE_API_KEY ausente")


KEY = _key()


def _quota_add(endpoint):
    q = json.loads(QUOTA_FILE.read_text()) if QUOTA_FILE.exists() else {"units": 0, "calls": {}}
    q["units"] += COST[endpoint]
    q["calls"][endpoint] = q["calls"].get(endpoint, 0) + 1
    QUOTA_FILE.write_text(json.dumps(q, indent=1))
    return q["units"]


def call(endpoint, **params):
    params["key"] = KEY
    url = f"https://www.googleapis.com/youtube/v3/{endpoint}?" + urllib.parse.urlencode(params)
    used = _quota_add(endpoint)
    if used > 4000:
        raise SystemExit("orçamento de cota estourado")
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300].replace(KEY, "***")
        raise RuntimeError(f"HTTP {e.code} em {endpoint}: {body}") from None
