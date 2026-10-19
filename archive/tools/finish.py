import sys, json, subprocess, time
sys.path.insert(0, "."); import app, pipeline
key = sys.argv[1]; steps = sys.argv[2:] or ["validate", "montage", "thumbs", "kit"]
pid = open(f"{key}_id.txt").read().strip(); PY = r".venv\Scripts\python.exe"
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
for st in steps:
    log("START", st)
    if st == "validate":
        r = pipeline.validate(pid)
        log("ok", r["ok"]); log(json.dumps({k: v for k, v in r.items()}, default=str, ensure_ascii=False)[:6000])
        if not r["ok"]: log("VALIDATION FAILED - stop"); break
        log("gfx", app.gfx_render(pid))
    elif st == "montage":
        p = subprocess.run([PY, "montage.py", pid, "--step", "all"]); log("montage rc", p.returncode)
        if p.returncode: break
    elif st == "thumbs": subprocess.run([sys.executable, "tools/thumbs_new.py", key])
    elif st == "kit": subprocess.run([sys.executable, "tools/kit_new.py", key])
log("DONE")
