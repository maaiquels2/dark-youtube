"""Grandpa Walt montage. Default: intro_15s at start (hook narration over it), outro_15s at end with end card.
Usage: python walt_montage.py [out_name] [episode]   (defaults: pilot_ep04_teaser_v2, pilot_ep04_teaser)
Period scenes come ONLY from local ComfyUI images: projects/grandpa-walt/<episode>/scenes/sceneNN_seedK.png
(seed from picks.json, default 1). Porch scenes (06,10,15) still use scenes/sKK.jpg until the Grok clip bank exists."""
import json, re, subprocess, sys
from pathlib import Path
R=Path("projects/grandpa-walt"); S=R/"scenes"; A=R/"audio"; W=R/"work"; O=R/"out"; W.mkdir(exist_ok=True); O.mkdir(exist_ok=True)
CL=Path("projects/_characters/grandpa-walt/clips"); INTRO=CL/"intro_15s.mp4"; OUTRO=CL/"outro_15s.mp4"
NAME=sys.argv[1] if len(sys.argv)>1 else "pilot_ep04_teaser_v2"
EP=sys.argv[2] if len(sys.argv)>2 else "pilot_ep04_teaser"
LS=R/EP/"scenes"; PICKS=json.loads((LS/"picks.json").read_text(encoding="utf-8")) if (LS/"picks.json").exists() else {}
if (R/EP/"audio").is_dir(): A=R/EP/"audio"   # per-episode narration; pilot keeps the shared audio/ folder
sys.path.insert(0,"."); import walt_script
MD=Path("projects/_characters/grandpa-walt")/f"{EP}.md"; ROWS=walt_script.rows(MD); NEXT=walt_script.next_episode(MD)
INTRO_LINES=[(ROWS[0][0],1.8),(ROWS[1][0],7.4)]; OUTRO_LINE=(ROWS[-1][0],1.0); END_AT=9.0   # seconds inside the clip
PORCH={k for k,sh,_,_ in ROWS[2:-1] if sh.lower().startswith("porch")}
# porch pose (from "Porch clip <pose>" in the script) -> existing pilot still, until the Grok clip bank exists
POSE_STILL={"hook_close":"s01","rocking_wide":"s02","laugh_3q":"s06","serious_close":"s10","screen_door":"s15","dusk_lamp":"s17"}
POSE={k:re.search(r"clip (\w+)",v).group(1) for k,_,v,_ in ROWS if re.search(r"clip (\w+)",v)}
def scene_img(k):
    if k in PORCH: return S/f"{POSE_STILL.get(POSE.get(k),'s'+k)}.jpg"
    p=LS/f"scene{k}_seed{PICKS.get(k,1)}.png"
    if not p.exists(): sys.exit(f"missing {p} - run: python tools/walt_local.py <script.md> --scenes {k}")
    return p
L=json.loads((A/"lines.json").read_text(encoding="utf-8"))
MUSIC=Path("archive/projects/crash-2008-3min-20261019/music/echoes-of-time-v2.mp3")
FPS=30; LEAD=0.6; TAIL=1.7
# crop boxes (x,y,w as fractions; h follows 16:9) to avoid generic close-up faces (pilot images only)
CROP={"12":(0.40,0.30,0.60),"14":(0.0,0.42,0.58)} if EP=="pilot_ep04_teaser" else {}
def run(a): subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error"]+a,check=True)
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout)
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".",",")
srt=[]; clips=[]; auds=[]; t=0.0
def subs(k,st,ad):
    words=L[k].split(); parts=[L[k]] if len(L[k])<70 else [" ".join(words[:len(words)//2])," ".join(words[len(words)//2:])]
    seg=ad/len(parts)
    for p in parts: srt.append((st,st+seg,p)); st+=seg
def clip_seg(src,name,lines,length):
    c=W/f"{name}.mp4"
    run(["-i",str(src),"-t",str(length),"-vf",f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps={FPS},fade=in:0:10,fade=out:st={length-0.35}:d=0.35,format=yuv420p","-an","-c:v","libx264","-preset","veryfast","-crf","18",str(c)])
    ins=[]; flt=[]
    for j,(k,at) in enumerate(lines):
        ins+=["-i",str(A/f"{k}.mp3")]; flt.append(f"[{j}:a]adelay={int(at*1000)}:all=1[a{j}]")
        subs(k,t+at,dur(A/f"{k}.mp3"))
    a=W/f"{name}.wav"
    run(ins+["-filter_complex",";".join(flt)+";"+"".join(f"[a{j}]" for j in range(len(lines)))+f"amix=inputs={len(lines)}:normalize=0,apad,atrim=0:{length}","-ar","48000","-ac","2",str(a)])
    clips.append(c); auds.append(a)
clip_seg(INTRO,"intro",INTRO_LINES,dur(INTRO)); t+=dur(INTRO)
keys=[k for k in sorted(L) if k not in {x for x,_ in INTRO_LINES}|{OUTRO_LINE[0]}]
for n,k in enumerate(keys):
    img=scene_img(k); ad=dur(A/f"{k}.mp3"); D=round(LEAD+ad+TAIL,2); fr=int(D*FPS)
    porch=k in PORCH
    z=f"'min(1+0.08*on/{fr},1.08)'" if n%2==0 else f"'max(1.08-0.08*on/{fr},1.0)'"
    x="'iw/2-(iw/zoom/2)+%s'"%("(on/%d)*iw*0.015"%fr if n%3==1 else "0")
    pre="scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160"
    if k in CROP:
        cx,cy,cw=CROP[k]; pre+=f",crop=iw*{cw}:ih*{cw}:iw*{cx}:ih*{cy},scale=3840:2160"
    look="" if porch else ",eq=contrast=1.04,noise=alls=8:allf=t"
    c=W/f"c{k}.mp4"
    run(["-loop","1","-i",str(img),"-vf",f"{pre},zoompan=z={z}:x={x}:y='ih/2-(ih/zoom/2)':d={fr}:s=1920x1080:fps={FPS}{look},vignette=PI/5,fade=in:0:8,fade=out:{fr-8}:8,format=yuv420p","-frames:v",str(fr),"-c:v","libx264","-preset","veryfast","-crf","18",str(c)])
    a=W/f"a{k}.wav"
    run(["-i",str(A/f"{k}.mp3"),"-af",f"adelay={int(LEAD*1000)}:all=1,apad,atrim=0:{D}","-ar","48000","-ac","2",str(a)])
    clips.append(c); auds.append(a); subs(k,t+LEAD,ad); t+=D
end_start=t+END_AT
clip_seg(OUTRO,"outro",[OUTRO_LINE],dur(OUTRO)); t+=dur(OUTRO)
srt=[(a,min(b,end_start-0.3),p) for a,b,p in srt]
(W/"v.txt").write_text("".join(f"file '{c.resolve().as_posix()}'\n" for c in clips)); (W/"a.txt").write_text("".join(f"file '{a.resolve().as_posix()}'\n" for a in auds))
run(["-f","concat","-safe","0","-i",str(W/"v.txt"),"-c","copy",str(W/"v.mp4")])
run(["-f","concat","-safe","0","-i",str(W/"a.txt"),str(W/"narr.wav")])
sp=O/f"{NAME}.srt"; sp.write_text("".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{p}\n\n" for i,(a,b,p) in enumerate(srt)),encoding="utf-8")
T=t
run(["-i",str(W/"narr.wav"),"-stream_loop","-1","-i",str(MUSIC),"-filter_complex",
 f"[1:a]atrim=0:{T},volume=0.11,afade=in:0:2,afade=out:st={T-4}:d=4[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[0:a][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5[o]","-map","[o]","-ar","48000",str(W/"mix.wav")])
CARD=f"NEXT\\: EPISODE {NEXT[0]} - {NEXT[1].upper()}" if NEXT else "NEXT\\: EPISODE 5 - OMAHA BEACH"   # no 'Next episode:' line = old pilot card
srtp=str(sp.resolve()).replace("\\","/").replace(":","\\:")
e=end_start; al=f"alpha='min(1,(t-{e})*1.5)'"
vf=(f"subtitles='{srtp}':force_style='FontName=Georgia,FontSize=17,PrimaryColour=&H00E8F4FA,OutlineColour=&H00000000,BorderStyle=1,Outline=1.6,Shadow=0.6,MarginV=34',"
 "drawtext=fontfile='C\\:/Windows/Fonts/georgia.ttf':text='Walt is a fictional character. The history is real.':fontsize=30:fontcolor=0xF0E2C4:shadowcolor=black:shadowx=2:shadowy=2:x=(w-tw)/2:y=60:enable='between(t,15.5,20.5)',"
 f"drawbox=x=0:y=ih*0.30:w=iw:h=ih*0.26:color=black@0.55:t=fill:enable='gte(t,{e})',"
 f"drawtext=fontfile='C\\:/Windows/Fonts/georgiab.ttf':text='{CARD}':fontsize={66 if len(CARD)<=32 else 52}:fontcolor=0xF0E2C4:x=(w-tw)/2:y=h*0.35:enable='gte(t,{e})':{al},"
 f"drawtext=fontfile='C\\:/Windows/Fonts/georgiai.ttf':text='Subscribe - Grandpa Walt Remembers':fontsize=42:fontcolor=0xF0E2C4:x=(w-tw)/2:y=h*0.35+95:enable='gte(t,{e})':{al}")
fin=O/f"{NAME}.mp4"
run(["-i",str(W/"v.mp4"),"-i",str(W/"mix.wav"),"-vf",vf,"-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","20","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",str(fin)])
run(["-i",str(fin),"-filter_complex","[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.15[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2","-c:v","libx264","-preset","medium","-crf","23","-c:a","copy","-movflags","+faststart",str(O/f"{NAME}_9x16.mp4")])
run(["-i",str(fin),"-c:v","libx264","-preset","medium","-b:v","2600k","-maxrate","3200k","-bufsize","6400k","-c:a","aac","-b:a","128k","-movflags","+faststart",str(O/f"{NAME}_preview.mp4")])
run(["-i",str(fin),"-vf",f"fps=1/{T/16:.2f},scale=480:-2,tile=4x4","-frames:v","1",str(O/f"{NAME}_frames.jpg")])
print("total",round(T,1))
