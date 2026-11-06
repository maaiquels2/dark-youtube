# Gera objetos de capa no ComfyUI local (JuggernautXL, fila vazia), 1 job por vez.
import json, time, urllib.request, urllib.parse, sys
from pathlib import Path
API = 'http://127.0.0.1:8188'
OUT = Path(__file__).resolve().parent
NEG = "engraving, emblem, portrait, symbol, blank paper text, text, letters, words, logo, watermark, signage, numbers, people, person, face, hands, cartoon, illustration, painting, cgi look, clutter, busy background, deformed"
JOBS = [
 ("r4_hg_0", 600, "product photograph of a single tall glass hourglass with an elegant dark wood frame, small gold coins falling through the narrow neck instead of sand, the top bulb almost empty, the bottom bulb piled with gold coins, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_hg_1", 601, "product photograph of a single tall glass hourglass with an elegant dark wood frame, small gold coins falling through the narrow neck instead of sand, the top bulb almost empty, the bottom bulb piled with gold coins, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_hg_2", 602, "product photograph of a single tall glass hourglass with an elegant dark wood frame, small gold coins falling through the narrow neck instead of sand, the top bulb almost empty, the bottom bulb piled with gold coins, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_ice_0", 610, "product photograph of a single clear solid block of ice, cube shaped, frosty edges, a few cracks, slightly melting, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_ice_1", 611, "product photograph of a single clear solid block of ice, cube shaped, frosty edges, a few cracks, slightly melting, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_ice_2", 612, "product photograph of a single clear solid block of ice, cube shaped, frosty edges, a few cracks, slightly melting, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_box_0", 620, "product photograph of a single plain brown cardboard moving box, open flaps, filled with office items: a desk lamp, a small potted plant, a framed photo seen from behind, a coffee mug, rolled papers, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_box_1", 621, "product photograph of a single plain brown cardboard moving box, open flaps, filled with office items: a desk lamp, a small potted plant, a framed photo seen from behind, a coffee mug, rolled papers, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_box_2", 622, "product photograph of a single plain brown cardboard moving box, open flaps, filled with office items: a desk lamp, a small potted plant, a framed photo seen from behind, a coffee mug, rolled papers, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_dom_0", 630, "product photograph of a row of tall black dominoes with white dots toppling over in a chain reaction, several mid-fall, the first ones already flat, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_dom_1", 631, "product photograph of a row of tall black dominoes with white dots toppling over in a chain reaction, several mid-fall, the first ones already flat, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_dom_2", 632, "product photograph of a row of tall black dominoes with white dots toppling over in a chain reaction, several mid-fall, the first ones already flat, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_gav_0", 640, "product photograph of a wooden judge gavel broken in two pieces, the handle snapped with splinters, lying on its sound block, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_gav_1", 641, "product photograph of a wooden judge gavel broken in two pieces, the handle snapped with splinters, lying on its sound block, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
 ("r4_gav_2", 642, "product photograph of a wooden judge gavel broken in two pieces, the handle snapped with splinters, lying on its sound block, isolated on a plain seamless light gray background, dramatic studio lighting, soft shadow, sharp focus, photorealistic"),
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
