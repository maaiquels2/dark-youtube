# Gera objetos de capa no ComfyUI local (JuggernautXL, fila vazia), 1 job por vez.
import json, time, urllib.request, urllib.parse, sys
from pathlib import Path
API = 'http://127.0.0.1:8188'
OUT = Path(__file__).resolve().parent
NEG = "blank paper text, text, letters, words, logo, watermark, signage, numbers, people, person, face, hands, cartoon, illustration, painting, cgi look, clutter, busy background, deformed"
JOBS = [
 ("w2_chair_0", 100, "product photograph of a black leather executive office chair knocked over, lying on its side on the floor, wheels in the air, abandoned, a few loose legal documents scattered beside it, dramatic low-key studio lighting, isolated on a plain seamless medium gray background, sharp focus, photorealistic, 50mm"),
 ("w2_chair_1", 101, "product photograph of a black leather executive office chair knocked over, lying on its side on the floor, wheels in the air, abandoned, a few loose legal documents scattered beside it, dramatic low-key studio lighting, isolated on a plain seamless medium gray background, sharp focus, photorealistic, 50mm"),
 ("w2_chair_2", 102, "product photograph of a black leather executive office chair knocked over, lying on its side on the floor, wheels in the air, abandoned, a few loose legal documents scattered beside it, dramatic low-key studio lighting, isolated on a plain seamless medium gray background, sharp focus, photorealistic, 50mm"),
 ("w2_chair_3", 103, "product photograph of a black leather executive office chair knocked over, lying on its side on the floor, wheels in the air, abandoned, a few loose legal documents scattered beside it, dramatic low-key studio lighting, isolated on a plain seamless medium gray background, sharp focus, photorealistic, 50mm"),
 ("b2_safe_0", 200, "product photograph of a heavy steel bank safe with its thick door swung wide open, the inside completely empty, a few gold coins spilled on the floor in front of it, dramatic low-key studio lighting, isolated on a plain seamless medium gray background, sharp focus, photorealistic, 50mm"),
 ("b2_safe_1", 201, "product photograph of a heavy steel bank safe with its thick door swung wide open, the inside completely empty, a few gold coins spilled on the floor in front of it, dramatic low-key studio lighting, isolated on a plain seamless medium gray background, sharp focus, photorealistic, 50mm"),
 ("b2_safe_2", 202, "product photograph of a heavy steel bank safe with its thick door swung wide open, the inside completely empty, a few gold coins spilled on the floor in front of it, dramatic low-key studio lighting, isolated on a plain seamless medium gray background, sharp focus, photorealistic, 50mm"),
 ("b2_safe_3", 203, "product photograph of a heavy steel bank safe with its thick door swung wide open, the inside completely empty, a few gold coins spilled on the floor in front of it, dramatic low-key studio lighting, isolated on a plain seamless medium gray background, sharp focus, photorealistic, 50mm"),
]
def post(path, data):
    r = urllib.request.Request(API + path, json.dumps(data).encode(), {'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r))
def get(path): return json.load(urllib.request.urlopen(API + path))
for name, seed, pos in JOBS:
    wf = {"1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "juggernautXL_v9.safetensors"}},
          "2": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
          "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
          "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
          "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0], "seed": seed, "steps": 30, "cfg": 5.0, "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0}},
          "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
          "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "capa_teste_" + name}}}
    pid = post('/prompt', {"prompt": wf})['prompt_id']; t0 = time.time()
    while True:
        h = get('/history/' + pid)
        if pid in h and h[pid].get('outputs'): break
        if time.time() - t0 > 600: sys.exit('timeout ' + name)
        time.sleep(3)
    img = h[pid]['outputs']['7']['images'][0]
    q = urllib.parse.urlencode({'filename': img['filename'], 'subfolder': img['subfolder'], 'type': img['type']})
    (OUT / f'{name}.png').write_bytes(urllib.request.urlopen(API + '/view?' + q).read())
    print(name, round(time.time() - t0), 's', flush=True)
