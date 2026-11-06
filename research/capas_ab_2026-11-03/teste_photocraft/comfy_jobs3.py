# Gera objetos de capa no ComfyUI local (JuggernautXL, fila vazia), 1 job por vez.
import json, time, urllib.request, urllib.parse, sys
from pathlib import Path
API = 'http://127.0.0.1:8188'
OUT = Path(__file__).resolve().parent
NEG = "coins, gold, money, cash, banknotes, treasure, jewelry, objects inside, blank paper text, text, letters, words, logo, watermark, signage, numbers, people, person, face, hands, cartoon, illustration, painting, cgi look, clutter, busy background, deformed"
JOBS = [
 ("b3_safe_0", 300, "product photograph of a heavy steel safe with its thick door swung fully open ninety degrees, the inside completely empty and bare, empty metal shelves, nothing inside, dramatic low-key studio lighting with a warm rim light, isolated on a plain seamless medium gray background, sharp focus, photorealistic, three-quarter view, 50mm"),
 ("b3_safe_1", 301, "product photograph of a heavy steel safe with its thick door swung fully open ninety degrees, the inside completely empty and bare, empty metal shelves, nothing inside, dramatic low-key studio lighting with a warm rim light, isolated on a plain seamless medium gray background, sharp focus, photorealistic, three-quarter view, 50mm"),
 ("b3_safe_2", 302, "product photograph of a heavy steel safe with its thick door swung fully open ninety degrees, the inside completely empty and bare, empty metal shelves, nothing inside, dramatic low-key studio lighting with a warm rim light, isolated on a plain seamless medium gray background, sharp focus, photorealistic, three-quarter view, 50mm"),
 ("b3_safe_3", 303, "product photograph of a heavy steel safe with its thick door swung fully open ninety degrees, the inside completely empty and bare, empty metal shelves, nothing inside, dramatic low-key studio lighting with a warm rim light, isolated on a plain seamless medium gray background, sharp focus, photorealistic, three-quarter view, 50mm"),
 ("b3_safe_4", 304, "product photograph of a heavy steel safe with its thick door swung fully open ninety degrees, the inside completely empty and bare, empty metal shelves, nothing inside, dramatic low-key studio lighting with a warm rim light, isolated on a plain seamless medium gray background, sharp focus, photorealistic, three-quarter view, 50mm"),
 ("b3_safe_5", 305, "product photograph of a heavy steel safe with its thick door swung fully open ninety degrees, the inside completely empty and bare, empty metal shelves, nothing inside, dramatic low-key studio lighting with a warm rim light, isolated on a plain seamless medium gray background, sharp focus, photorealistic, three-quarter view, 50mm"),
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
