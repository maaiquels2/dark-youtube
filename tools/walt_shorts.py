"""Walt vertical cuts (Reels / Shorts / TikTok) from an episode's montage work files.
Usage: python tools/walt_shorts.py <episode> [--only 1,4] [--no-render] [--send]
Needs projects/grandpa-walt/<episode>/shorts_plan.json (row ranges, headline, title, caption, 5 tags) and the
projects/grandpa-walt/work/v.mp4 + mix.wav left by the LAST walt_montage.py run of that episode.
Cuts fall on scene boundaries. Output: projects/grandpa-walt/out/<episode>_shorts/short-NN.mp4 (videos only);
working .ass files go to projects/grandpa-walt/<episode>/shorts_work/."""
import argparse, json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import walt_script  # noqa: E402

R = Path("projects/grandpa-walt")
LEAD, TAIL = 0.6, 1.7           # same as walt_montage.py
NOTE = "Walt is a fictional character. The history is real."
WEAK = set("a an the of to in on at for by and or but it its is was as that with from his her their this".split())


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)


def timeline(ep):
    rows = walt_script.rows(Path("projects/_characters/grandpa-walt") / f"{ep}.md"); A = R / ep / "audio"
    t = dur(Path("projects/_characters/grandpa-walt/clips/intro_15s.mp4")); tl = {}
    for k, _, _, text in rows[2:-1]:
        ad = dur(A / f"{k}.mp3"); D = round(LEAD + ad + TAIL, 2)
        tl[int(k)] = dict(start=t, end=t + D, speech=(t + LEAD, t + LEAD + ad), text=text); t += D
    return tl


def chunks(text):
    """Blocks of up to 3 words that break on punctuation and do not end on a weak word."""
    ws, out, cur = text.split(), [], []
    for i, w in enumerate(ws):
        cur.append(w); punct = re.search(r"[.,;:?!]$", w)
        if len(cur) >= 3 or punct:
            if not punct and w.lower().strip("'\"") in WEAK and len(cur) > 1 and i + 1 < len(ws):
                last = cur.pop(); out.append(cur); cur = [last]
            else: out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def caption_events(row):
    """Timing is proportional to letters (+ pause weight on punctuation) inside the row's speech window."""
    cs = chunks(row["text"])
    wt = [sum(len(re.sub(r"\W", "", w)) + 1 for w in c) + (6 if re.search(r"[.?!]$", c[-1]) else 3 if re.search(r"[,;:]$", c[-1]) else 0) for c in cs]
    s0, s1 = row["speech"]; t = s0; ev = []
    for c, w in zip(cs, wt):
        e = t + (s1 - s0) * w / sum(wt); ev.append([t, e, " ".join(c).upper()]); t = e
    return ev


def ass(rows, t0, t1, headline, path):
    def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,"
            "ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
            "Style: Head,Georgia,76,&H00C4E2F0,&H00C4E2F0,&H00141414,&H96000000,1,0,0,0,100,100,0,0,1,3,2,8,70,70,260,1\n"
            "Style: Cap,Georgia,88,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,1,0,0,0,100,100,0,0,1,6,3,2,60,60,440,1\n"
            "Style: Note,Georgia,34,&H00C4E2F0,&H00C4E2F0,&H00101010,&H96000000,0,1,0,0,100,100,0,0,1,2,1,2,60,60,90,1\n\n"
            "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    ev = [f"Dialogue: 0,{ts(0)},{ts(t1 - t0)},Head,,0,0,0,,{headline}", f"Dialogue: 0,{ts(0)},{ts(t1 - t0)},Note,,0,0,0,,{NOTE}"]
    flat = [e for r in rows for e in caption_events(r)]
    for i, e in enumerate(flat):
        if i + 1 < len(flat): e[1] = min(e[1] + 0.15, flat[i + 1][0])
        else: e[1] += 0.2
    assert all(b > a for a, b, _ in flat) and all(flat[i][1] <= flat[i + 1][0] + 1e-6 for i in range(len(flat) - 1)), "legenda sobreposta"
    ev += [f"Dialogue: 1,{ts(a - t0)},{ts(b - t0)},Cap,,0,0,0,,{txt}" for a, b, txt in flat]
    Path(path).write_text(head + "\n".join(ev) + "\n", encoding="utf-8")


def render(t0, t1, sub, out):
    """Smart Vertical Framing as in tools/shorts.py: blurred background, 1080x740 centered picture, captions below it."""
    sp = Path(sub).as_posix()
    fc = ("[0:v]split=2[a][b];"
          "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=32,eq=brightness=-0.20[bg];"
          "[b]scale=1316:740:flags=lanczos,crop=1080:740[fg];"
          f"[bg][fg]overlay=0:(H-h)/2-55,subtitles='{sp}'[v];"
          f"[1:a]afade=t=in:d=0.3,afade=t=out:st={max(0.1, t1 - t0 - 0.6):.2f}:d=0.6,loudnorm=I=-14:TP=-1.5:LRA=11[au]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(R / "work/v.mp4"),
                    "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(R / "work/mix.wav"), "-filter_complex", fc,
                    "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "22", "-maxrate", "5M", "-bufsize", "10M", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], check=True, cwd=ROOT)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("episode"); ap.add_argument("--only", default=""); ap.add_argument("--send", action="store_true")
    ap.add_argument("--no-render", action="store_true", help="reuse the mp4s already in out/")
    a = ap.parse_args(); ep = a.episode
    plan = json.loads((R / ep / "shorts_plan.json").read_text(encoding="utf-8")); tl = timeline(ep)
    od = R / "out" / f"{ep}_shorts"; wd = R / ep / "shorts_work"; od.mkdir(parents=True, exist_ok=True); wd.mkdir(exist_ok=True)
    only = {int(x) for x in a.only.split(",") if x}; used = set(); made = []
    for n, p in enumerate(plan, 1):
        rr = list(range(p["from_row"], p["to_row"] + 1))
        assert all(r in tl for r in rr), f"short {n}: linhas fora do corpo do episodio"
        assert not used & set(rr), f"short {n}: sobreposto"; used |= set(rr)
        assert len(p["tags"]) == 5, f"short {n}: sao exatamente 5 hashtags"
        t0, t1 = tl[rr[0]]["start"] + 0.3, tl[rr[-1]]["end"] - 1.0
        assert 20 <= t1 - t0 <= 58, f"short {n}: {t1 - t0:.0f}s fora de 20-58s"
        out = od / f"short-{n:02d}.mp4"
        if (not only or n in only) and not a.no_render:
            ass([tl[r] for r in rr], t0, t1, p["headline"], wd / f"short-{n:02d}.ass"); render(t0, t1, wd / f"short-{n:02d}.ass", out)
            print(f"short-{n:02d}: linhas {rr[0]}-{rr[-1]} ({t1 - t0:.0f}s, {out.stat().st_size / 1e6:.0f} MB) {p['title']}", flush=True)
        made.append((n, out, p))
    if a.send:
        from meta_publish import tg_env, tg_send
        tg = tg_env()
        if not tg: sys.exit("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID faltando no .env")
        for n, out, p in made:
            if only and n not in only: continue
            text = f"{n}/{len(plan)} - {p['title']}\n\n{p['caption']}\n{NOTE}\n\n{' '.join(p['tags'])}"
            tg_send(tg, ROOT / out, text); print("telegram ok", out.name, flush=True); time.sleep(2)


if __name__ == "__main__":
    main()
