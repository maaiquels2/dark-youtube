import sys, json; sys.path.insert(0, "."); import app, pipeline
pid = open("lehman_id.txt").read().strip(); d = pipeline._load(pid); sc = d["scenes"]
w0 = sum(len(s["narration"].split()) for s in sc)
if w0 > 1600:
    for st in range(0, len(sc), 20):
        part = {str(i): sc[i]["narration"] for i in range(st, min(st + 20, len(sc)))}
        r = app.chat_json("You are a documentary script editor. Reply only in json.",
            "Shorten each narration line by about 20% for a tighter 11-minute video. Keep EVERY person name, company, agency, acronym, date and dollar amount exactly as written, keep attribution words (alleged, according to), keep the storytelling tone. "
            "Return json {\"n\":{\"<index>\":\"shortened text\"}}.\n" + json.dumps(part, ensure_ascii=False), 8000)
        for k, v in (r.get("n") or {}).items():
            if v and int(k) < len(sc): sc[int(k)]["narration"] = v
    f = pipeline._load(pid)
    for a, b in zip(f["scenes"], sc): a["narration"] = b["narration"]
    pipeline._save(f)
print("words", w0, "->", sum(len(s["narration"].split()) for s in pipeline._load(pid)["scenes"]))
