# ACE-Step 1.5: uma faixa instrumental por ato, mesma tonalidade (ré menor) para soarem como uma trilha so.
# Uso: cd %LOCALAPPDATA%/DarkStudio/ace-step; .venv/Scripts/python.exe -u -X faulthandler <este arquivo> <pasta_saida> act2
# Um ato por processo (a VRAM nao e liberada entre geracoes); precisa de ~5 GB livres na GPU (nvidia-smi).
# Saida aprovada em 18/10/2026: library/music/ace-step/trilha-<ato>.mp3
import sys, time
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from acestep.model_downloader import ensure_main_model
from acestep.handler import AceStepHandler
from acestep.inference import GenerationParams, GenerationConfig, generate_music

BASE = "dark cinematic documentary underscore, instrumental, no drums, no vocals, minimal, restrained, never playful"
ACTS = {  # ato: (descricao, bpm, segundos) - espelha ACT_VOICE do montage.py
    "act1": ("rise: warm low strings, slow arpeggiated piano, a hint of wonder and ambition, steady forward momentum, "
             "subtle dark undertone", 80, 180),
    "act2": ("growing suspicion: muted ticking clock texture, low sustained cello drone, sparse piano notes, "
             "quiet tension, uneasy pauses", 70, 180),
    "act3": ("collapse: grave slow deep cello and contrabass, heavy low brass swells, pulsing sub bass, "
             "ominous weight, controlled tension", 60, 180),
    "after": ("aftermath: soft reflective solo piano with faint distant strings, unhurried, lots of space, "
              "unresolved ending", 60, 120),
}

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
ok, msg = ensure_main_model(ROOT / "checkpoints", prefer_source="huggingface"); assert ok, msg
dit = AceStepHandler()
msg, ok = dit.initialize_service(project_root=str(ROOT), config_path="acestep-v15-turbo", device="cuda", offload_to_cpu=True)
assert ok, msg

cfg = GenerationConfig(batch_size=1, use_random_seed=False, audio_format="wav")
for act in (sys.argv[2:] or ACTS):  # um ato por processo: a VRAM nao e liberada entre geracoes
    desc, bpm, secs = ACTS[act]
    p = GenerationParams(caption=f"{BASE}, {desc}", lyrics="[Instrumental]", instrumental=True, duration=secs, bpm=bpm,
                         keyscale="D minor", inference_steps=8, shift=3.0, seed=7, thinking=False,
                         use_cot_metas=False, use_cot_caption=False, use_cot_language=False)
    t = time.time()
    r = generate_music(dit, None, p, cfg, save_dir=str(out)); assert r.success, r.error
    dst = out / f"trilha_{act}.wav"
    dst.unlink(missing_ok=True); Path(r.audios[0]["path"]).rename(dst)
    print(f"OK {act} {secs}s em {time.time()-t:.0f}s -> {dst}", flush=True)
