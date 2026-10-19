import json, sys, os
sys.path.insert(0, os.getcwd())
import pipeline
for k in ("svb","lehman"):
    pid=open(f"{k}_id.txt").read().strip()
    r=pipeline.script_from_dossier(pid)
    d=pipeline._load(pid); sc=d["scenes"]
    print(k, len(sc), sum(len(s["narration"].split()) for s in sc), d.get("title"))
