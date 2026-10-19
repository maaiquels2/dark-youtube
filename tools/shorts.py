# -*- coding: utf-8 -*-
"""Dark Studio - Shorts verticais a partir do video longo (sem gerar nada novo).
1. O ChatGPT escolhe ate N trechos de 20-45 s 100% autonomos, com gancho sustentado por frase literal do roteiro
   (conferida no codigo), sempre em limites de cena; criterios da skill cortes-verticais.
2. Vertical 1080x1920: video 16:9 no centro, o mesmo video desfocado de fundo, titulo fixo no alto e legenda
   palavra por palavra (a palavra falada em ambar), com os tempos de audio/words.json (tools/words.py).
3. Kit de cada Short (titulo, legenda de ate 100 caracteres + link do video completo, sem hashtags, gancho, frase
   literal, por que se sustenta sozinho, ordem de publicacao) em output/shorts/shorts.json.
Uso: python tools/shorts.py <project_id> [--n 4] [--full-url https://youtu.be/...]
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import app, words as Wd  # noqa: E402

FONTS = (ROOT / "fonts").as_posix().replace(":", "\\:")
MIN_S, MAX_S = 20.0, 45.0  # cortes de 20-45 s retem melhor que os de quase 1 min


def timeline(pdir, sc):
    """Duracao e inicio de cada cena: timeline.py (a pausa vem da configuracao; antes era 0,3 fixo aqui)."""
    import timeline as T
    tl = T.plan(pdir, len(sc))
    return tl["D"], tl["starts"]


def _plain(t):
    return re.sub(r"[^a-z0-9$%. ]", "", re.sub(r"\s+", " ", (t or "").lower().replace("’", "'").replace("'", ""))).strip()


def pick(pj, D, n):
    """Criterios do editor de cortes (skill cortes-verticais): trecho 100% autonomo, gancho especifico sustentado por
    uma frase LITERAL do roteiro (conferida aqui), so fatos da narracao, sem clickbait, menos cortes se nao houver bons.
    Os 'timestamps' sao numeros de cena: o corte cai na fronteira exata da narracao, sem o deslocamento de segundos
    que o modelo comete com minutagem."""
    sc = pj["scenes"]
    lines = "\n".join(f"{i+1} [{D[i]:.1f}s]: {s['narration']}" for i, s in enumerate(sc))
    r = app.chat_json(
        "You are an experienced editor of vertical short videos (YouTube Shorts, Reels, TikTok) focused on retention, "
        "working for a business documentary channel. Reply in JSON.",
        f"Video: {pj.get('title')}\nFull narration by scene (scene number [seconds]: text):\n{lines}\n\n"
        f"Find UP TO {n} segments of {MIN_S:.0f}-{MAX_S:.0f} seconds, each a run of CONSECUTIVE scenes, that make sense 100% on their own, "
        "with no dependence on earlier parts of the video (no 'this', 'that figure', 'he' pointing to something not inside the segment). "
        "Never cut a line of reasoning in the middle: the segment ends where the idea is complete. Segments must not overlap.\n"
        "For each segment return:\n"
        "- from_scene, to_scene (the scene numbers above, literally)\n"
        "- headline: opening hook of at most 12 words (and at most 45 characters), shown on screen during the first seconds: direct, "
        "promising something concrete the segment really delivers or creating curiosity about what it shows\n"
        "- quote: the exact sentence copied word for word from the narration of these scenes that delivers on the hook\n"
        "- title: YouTube title, at most 60 characters\n"
        "- caption: post description, at most 100 characters\n"
        "- why_standalone: one short sentence on why the idea is complete by itself\n"
        "- rank: 1 = the most specific, concrete, well-bounded idea (published first)\n"
        "Mandatory rules: use only statements, numbers and facts present in the narration, never invent or infer; no clickbait "
        "that the segment does not fulfill; no hashtags; English. If there are not enough strong, complete segments, return only "
        "the good ones and explain why in 'skipped_reason'.\n"
        'Return {"shorts":[{"from_scene":int,"to_scene":int,"headline":"","quote":"","title":"","caption":"","why_standalone":"","rank":1}],'
        '"skipped_reason":""}', 4000)
    out, used = [], set()
    for s in sorted(r.get("shorts") or [], key=lambda x: int(x.get("rank") or 99)):
        a, b = int(s["from_scene"]), int(s["to_scene"]); why = None
        if not 1 <= a <= b <= len(sc) or used & set(range(a, b + 1)): why = "cenas invalidas ou sobrepostas"
        elif not MIN_S <= sum(D[a - 1:b]) <= MAX_S: why = f"{sum(D[a - 1:b]):.0f}s fora de {MIN_S:.0f}-{MAX_S:.0f}s (nao corto: quebraria o raciocinio)"
        elif _plain(s.get("quote")) not in _plain(" ".join(x["narration"] for x in sc[a - 1:b])): why = "frase do gancho nao esta no roteiro do trecho"
        elif len(s.get("headline", "").split()) > 12: why = "gancho com mais de 12 palavras"
        if why: print(f"  descartado (cenas {a}-{b}): {why}", flush=True); continue
        used |= set(range(a, b + 1))
        out.append(dict(s, from_scene=a, to_scene=b, description=s.get("caption", "")[:100], title=s.get("title", "")[:60]))
    if r.get("skipped_reason"): print("  modelo:", r["skipped_reason"], flush=True)
    return out


def ass(words_abs, t0, t1, headline, path):
    """Legenda ASS 1080x1920: titulo fixo no alto + blocos de ate 3 palavras, a palavra falada em ambar."""
    def ts(t):
        t = max(0.0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
        return f"{h}:{m:02d}:{s:05.2f}"
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,"
            "ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
            "Style: Head,Playfair Display,78,&H00EAF2F6,&H00EAF2F6,&H00141414,&H96000000,0,0,0,0,100,100,0,0,1,3,2,8,70,70,250,1\n"
            "Style: Cap,Inter,92,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,1,0,0,0,100,100,0,0,1,6,3,2,60,60,420,1\n\n"
            "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    ev = [f"Dialogue: 0,{ts(0)},{ts(t1 - t0)},Head,,0,0,0,,{headline}"]
    for a, b, txt in caption_events([w for w in words_abs if t0 <= w["s"] < t1]):
        ev.append(f"Dialogue: 1,{ts(a - t0)},{ts(b - t0)},Cap,,0,0,0,,{txt}")
    Path(path).write_text(head + "\n".join(ev) + "\n", encoding="utf-8")


WEAK = set("a an the of to in on at for by and or but it its is was as that with from his her their this".split())
UNITS = set("billion million thousand trillion percent dollars years days months".split())


def chunks_of(ws):
    """Blocos de ate 3 palavras / 16 letras, que respeitam a frase: quebram na pontuacao do roteiro e nas pausas,
    e nunca terminam em palavra fraca ('it', 'of', 'the' passam para o bloco seguinte)."""
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w); nxt = ws[i + 1] if i + 1 < len(ws) else None
        gap = nxt["s"] - w["e"] if nxt else 9.0
        full = len(cur) >= 3 or len(" ".join(x["w"] for x in cur)) >= 16
        if full and nxt and nxt.get("p") and gap <= 0.35:  # a proxima palavra fecha a frase: nunca fica sozinha no bloco
            if len(" ".join(x["w"] for x in cur + [nxt])) <= 22: continue          # cabe: entra aqui ("THE OFFICES WERE REAL")
            if len(cur) > 1: out.append(cur[:-1]); cur = [cur[-1]]; continue       # nao cabe: quebra antes ("STARTUP STORIES")
        if w.get("p") or gap > 0.35 or not nxt: out.append(cur); cur = []
        elif full:
            num_unit = re.fullmatch(r"[$\d.,]+", w["w"]) and Wd.norm(nxt["w"]) in UNITS  # '8 | BILLION' nao se separa
            if (Wd.norm(w["w"]) in WEAK or num_unit) and len(cur) > 1: cur.pop(); out.append(cur); cur = [w]
            else: out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def caption_events(ws):
    """Um evento por palavra (o bloco com a palavra falada em ambar), SEM sobreposicao: no ASS dois eventos ao mesmo
    tempo sao empilhados um em cima do outro. Na pausa da narracao a legenda some."""
    ev = []
    for c in chunks_of(ws):
        for k, w in enumerate(c):
            b = c[k + 1]["s"] if k + 1 < len(c) else c[-1]["e"] + 0.2
            txt = " ".join(("{\\c&H42B0F4&}" + x["w"].strip().upper() + "{\\c&HFFFFFF&}") if j == k else x["w"].strip().upper() for j, x in enumerate(c))
            ev.append([w["s"], b, txt])
    out = []
    for i, e in enumerate(ev):
        if out and e[0] < out[-1][1]: e[0] = out[-1][1]               # comeca depois do anterior
        if i + 1 < len(ev): e[1] = min(e[1], ev[i + 1][0])            # termina antes do seguinte
        if e[1] - e[0] >= 0.04: out.append(e)                         # sem evento de duracao zero (o libass some com o titulo)
        elif out: out[-1][1] = max(out[-1][1], e[1])
    assert all(b > a for a, b, _ in out) and all(out[i][1] <= out[i + 1][0] + 1e-6 for i in range(len(out) - 1)), "legenda sobreposta"
    return out


def punctuate(words, narration):
    """TEXTO do roteiro, TEMPO do Whisper. O Whisper erra nomes ('Bankman-Fried' -> 'Bankman Freed', 'U.S.' -> 'U S'):
    alinha as duas sequencias e usa a palavra do roteiro; so numeros ditos ficam como o Whisper escreveu ('47' le
    melhor que 'forty-seven'). A pontuacao do roteiro marca o fim dos blocos de legenda."""
    from difflib import SequenceMatcher
    toks = narration.split(); P = (".", ",", "?", "!", ";", ":", "—")
    def tok(t):
        w = t.strip("\"'“”‘’()")
        w = w.rstrip(",;:!?—") if re.search(r"\w\.\w", w) else w.rstrip(".,;:!?—")  # 'U.S.' mantem o ponto
        return {"w": w, "p": t.rstrip("\"'”’)").endswith(P)}
    def dig(s): return any(c.isdigit() for c in s)
    out = []
    sm = SequenceMatcher(None, [Wd.norm(w["w"]) for w in words], [Wd.norm(t) for t in toks], autojunk=False)
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        ws, ts = words[a0:a1], toks[b0:b1]
        if op == "equal":  # 'eight' no roteiro e '8' no Whisper: na tela vai o algarismo
            out += [dict(w, **dict(tok(t), w=w["w"].strip(".,") if dig(w["w"]) and not dig(t) else tok(t)["w"])) for w, t in zip(ws, ts)]
        elif op == "replace" and ws:
            if any(dig(w["w"]) for w in ws) and not any(dig(t) for t in ts):  # numero por extenso no roteiro: algarismos do Whisper
                out += [dict(w, w=w["w"].strip(".,"), p=(k == len(ws) - 1 and tok(ts[-1])["p"])) for k, w in enumerate(ws)]
            else:  # mesmas palavras do roteiro, distribuidas no tempo que o Whisper ouviu
                s0, e0 = ws[0]["s"], ws[-1]["e"]; step = (e0 - s0) / len(ts)
                out += [dict(tok(t), s=round(s0 + k * step, 3), e=round(s0 + (k + 1) * step, 3)) for k, t in enumerate(ts)]
        elif op == "insert" and out:  # palavra do roteiro que o Whisper nao separou: cola no tempo da anterior
            for t in ts: out.append(dict(tok(t), s=out[-1]["e"], e=out[-1]["e"] + 0.12))
        # "delete": palavra que so o Whisper ouviu -> fica fora da legenda
    return out


def render(src, t0, t1, sub, out):
    sp = Path(sub).as_posix().replace(":", "\\:")
    fc = (f"[0:v]split=2[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.18[bg];"
          f"[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2-60,subtitles='{sp}':fontsdir='{FONTS}'[v];"
          f"[0:a]afade=t=in:d=0.3,afade=t=out:st={t1 - t0 - 0.6:.2f}:d=0.6,loudnorm=I=-14:TP=-1.5:LRA=11[au]")
    subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(src),
                    "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--n", type=int, default=4); ap.add_argument("--full-url", default="")
    ap.add_argument("--repick", action="store_true", help="escolhe outros trechos (por padrao reaproveita output/shorts/shorts.json)")
    a = ap.parse_args()
    pfile, pdir = ROOT / "projects" / f"{a.project}.json", ROOT / "projects" / a.project
    pj = json.loads(pfile.read_text(encoding="utf-8")); sc = pj["scenes"]
    if not (pdir / "audio" / "words.json").is_file(): Wd.run(a.project)
    wj = Wd.load(pdir); D, st = timeline(pdir, sc)
    words_abs = [dict(w, s=w["s"] + st[i], e=w["e"] + st[i]) for i in range(len(sc))
                 for w in punctuate([dict(x) for x in (wj.get(str(i + 1)) or {}).get("words", [])], sc[i].get("narration") or "")]
    od = pdir / "output" / "shorts"; od.mkdir(parents=True, exist_ok=True)
    kits = []
    prev = od / "shorts.json"  # reaproveita a escolha dos trechos: nao paga o ChatGPT de novo a cada renderizacao
    picks = json.loads(prev.read_text(encoding="utf-8")) if prev.is_file() and not a.repick else pick(pj, D, a.n)
    for k, s in enumerate(picks, 1):
        s = dict(s, title=s.get("pick_title") or s["title"], description=s.get("pick_description") or s["description"])
        t0 = st[s["from_scene"] - 1]; t1 = st[s["to_scene"] - 1] + D[s["to_scene"] - 1]
        # o .ass NAO fica ao lado do .mp4 com o mesmo nome: o player do Windows/VLC carrega sozinho e desenha a legenda de novo por cima
        (od / "_legendas").mkdir(exist_ok=True)
        sub, out = od / "_legendas" / f"short-{k}.ass", od / f"short-{k}.mp4"
        ass(words_abs, t0, t1, s["headline"], sub)  # no ASS a virgula no texto nao precisa de escape
        render(pdir / "output" / "final.mp4", t0, t1, sub, out)
        link = f"\n\nFull documentary: {a.full_url}" if a.full_url else "\n\nFull documentary on the channel."
        kits.append({"file": out.name, "title": s["title"][:60], "from_scene": s["from_scene"],  # sem hashtags (o YouTube reconhece o Short pelo formato)
                     "to_scene": s["to_scene"], "seconds": round(t1 - t0, 1), "rank": s.get("rank"),
                     "headline": s["headline"], "quote": s.get("quote"), "why_standalone": s.get("why_standalone"),
                     "pick_title": s["title"], "pick_description": s["description"],
                     "description": s["description"] + link})
        print(f"short-{k}: cenas {s['from_scene']}-{s['to_scene']} ({t1 - t0:.0f}s) {s['title']}", flush=True)
    (od / "shorts.json").write_text(json.dumps(kits, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
