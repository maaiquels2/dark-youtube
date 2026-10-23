"""Walt narration via OpenAI gpt-4o-mini-tts (PAID, run only with approval).
Usage: python walt_tts.py <episode.md>   -> projects/grandpa-walt/<episode>/audio/NN.mp3 + lines.json"""
import json, urllib.request, sys
from pathlib import Path
sys.path.insert(0,"."); import montage, walt_script
md=Path(sys.argv[1]); A=Path("projects/grandpa-walt")/md.stem/"audio"; A.mkdir(parents=True,exist_ok=True)
L={k:t for k,_,_,t in walt_script.rows(md)}
print(len(L),"lines,",sum(map(len,L.values())),"chars",flush=True)
key=montage.env_key()
INS="Voice of an 80-year-old man from rural Ohio, born in 1924, a World War Two veteran telling a story to his grandkids on the porch. Warm, slightly raspy and gravelly, slow unhurried pace with natural pauses, gentle Midwestern accent, dry humor, quiet emotion. Never theatrical, never announcer-like."
for k,t in L.items():
    o=A/f"{k}.mp3"
    if o.exists(): continue
    body={"model":"gpt-4o-mini-tts","voice":"ash","input":t,"instructions":INS,"response_format":"mp3"}
    r=urllib.request.Request("https://api.openai.com/v1/audio/speech",data=json.dumps(body).encode(),headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    o.write_bytes(urllib.request.urlopen(r,timeout=120).read()); print(k,"ok",flush=True)
(A/"lines.json").write_text(json.dumps(L,indent=1),encoding="utf-8")
