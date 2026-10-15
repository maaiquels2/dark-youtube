import sys,json
sys.path.insert(0,'.')
import app,pipeline
pid=open('fb_id.txt').read().strip()
d=app.load_project(pid)
cfg=app.pricing()
for s in d['scenes']:
    s['grok_prompt']=app.build_grok_prompt(s,cfg)
pipeline._save(d)
print(d['scenes'][22]['grok_prompt'][-260:])
