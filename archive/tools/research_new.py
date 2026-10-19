import json, sys, os
sys.path.insert(0, os.getcwd())
import app, pipeline
out = {}
for key, title, theme in [
  ("svb", "Silicon Valley Bank: The 48-Hour Collapse", "Channel 'The Cracked Ledger'. Angle: how the startup world's bank died in 48 hours. Civil FDIC claims are allegations; no criminal charges. Target 10-12 min."),
  ("lehman", "Lehman Brothers: The Weekend Wall Street Broke", "Channel 'The Cracked Ledger'. Angle: 158-year-old bank, Repo 105, the weekend at the NY Fed, the largest bankruptcy in U.S. history. No criminal charges were filed. Target 10-12 min.")]:
    notes = open(f"research/{key}_notes.txt", encoding="utf-8").read()
    pid_file = f"{key}_id.txt"
    if os.path.exists(pid_file): pid = open(pid_file).read().strip()
    else:
        saved = app.save_project({"title": title, "niche": "Business & Finance documentary (rise and fall)", "language": "English", "minutes": 11,
                                  "theme": theme, "channel": "The Cracked Ledger", "scenes": [], "research_notes": notes, "facts": notes})
        pid = saved["id"]; open(pid_file, "w").write(pid)
    d = pipeline._load(pid); d["research_notes"] = notes; d["facts"] = notes; pipeline._save(d)
    dos = pipeline.research(pid)
    out[key] = {"id": pid, "chapters": len(dos.get("chapters") or []), "facts": sum(len(c.get("facts") or []) for c in dos.get("chapters") or []),
                "sources": f"{dos.get('sources_ok')}/{dos.get('sources_checked')}"}
    bad = sorted({f["url"] for c in dos["chapters"] for f in c.get("facts") or [] if f.get("url_ok") is False})
    out[key]["bad_urls"] = bad
print(json.dumps(out, indent=1))
