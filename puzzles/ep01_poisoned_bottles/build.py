"""Ep01 poisoned bottles: ElevenLabs voice (Brian) with word timings -> index.html (HyperFrames).
Usage (from this folder): python build.py [--voice]   (--voice calls the paid API once; without it, reuses assets/timing.json)
"""
import base64, json, re, subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VOICE_ID, SPEED = "nPczCjzI2devNBz1zQrb", 1.08

BLOCKS = [
 "One of these 1,000 bottles is poisoned. You have one hour to find it. How many testers do you need? The answer is smaller than you think.",
 "Here are the rules. The poison kills in exactly one hour. You get one round of testing, and each tester can drink from as many bottles as you like. Whoever drinks the poisoned one dies at the hour mark.",
 "The obvious plan is one tester per bottle. That's 1,000 testers. Too many. With a single tester, you can only split the bottles in two: the ones he drinks, and the ones he doesn't. If he dies, the poison is in the first half. If he lives, it's in the second.",
 "Add a second tester and you get four groups. Three testers, eight groups. Every new tester doubles the groups. So ten testers? Two to the tenth. 1,024 groups. That's more than 1,000 bottles. Ten testers are enough.",
 "Here's how. Give every bottle a number in binary, ten digits long. Bottle 618 is one-zero-zero-one-one-zero-one-zero-one-zero. Tester one drinks every bottle whose first digit is a one. Tester two drinks every bottle whose second digit is a one. And so on, ten testers, ten digits. After an hour, look at who died. Dead is a one. Alive is a zero.",
 "Say testers one, four, five, seven and nine die. That spells one-zero-zero-one-one-zero-one-zero-one-zero. Convert it, and the poisoned bottle is number 618.",
 "Every tester is one yes-or-no question, and ten yes-or-no questions are enough to pick one thing out of a thousand. So next time you need to find something fast, don't search one by one. Ask questions that cut the problem in half.",
]

def env_val(name):
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"')
    sys.exit(f"{name} missing in .env")

def tts(text):
    body = {"text": text, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.25,
                               "use_speaker_boost": True, "speed": SPEED}}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),
        headers={"xi-api-key": env_val("ELEVEN_LABS_KEY"), "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=180).read())

def main():
    assets = HERE / "assets"; assets.mkdir(exist_ok=True)
    text = " ".join(BLOCKS)
    tj = assets / "timing.json"
    if "--voice" in sys.argv:
        r = tts(text)
        (assets / "voice.mp3").write_bytes(base64.b64decode(r["audio_base64"]))
        al = r["alignment"]
        if len(al["characters"]) != len(text):
            sys.exit(f"alignment length {len(al['characters'])} != text {len(text)}")
        words, pos = [], 0
        for m in re.finditer(r"\S+", text):
            a, b = m.start(), m.end() - 1
            words.append({"w": m.group(), "s": round(al["character_start_times_seconds"][a], 3),
                          "e": round(al["character_end_times_seconds"][b], 3)})
        starts, off = [], 0
        for blk in BLOCKS:
            starts.append(round(al["character_start_times_seconds"][off], 3)); off += len(blk) + 1
        tj.write_text(json.dumps({"words": words, "blocks": starts}), encoding="utf-8")
    t = json.loads(tj.read_text(encoding="utf-8"))
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(assets / "voice.mp3")]))
    vend = max(w["e"] for w in t["words"])
    html = (HERE / "src" / "template.html").read_text(encoding="utf-8")
    html = (html.replace("__WORDS__", json.dumps(t["words"])).replace("__BLOCKS__", json.dumps(t["blocks"] + [round(vend + 0.3, 3)]))
            .replace("__VEND__", f"{vend:.3f}").replace("__DUR__", f"{vend + 4.5:.3f}"))
    (HERE / "index.html").write_text(html, encoding="utf-8")
    print(f"voice {dur:.1f}s, speech ends {vend:.1f}s, video {vend + 4.5:.1f}s")

main()
