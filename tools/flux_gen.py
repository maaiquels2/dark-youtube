# -*- coding: utf-8 -*-
"""Dark Studio - gerador FLUX.2 Klein 4B (Apache 2.0). Roda no ambiente proprio do modelo, chamado por tools/local_img.py:
  %LOCALAPPDATA%/DarkStudio/flux/.venv/Scripts/python.exe tools/flux_gen.py <jobs.json>
jobs.json = [{"out": caminho .jpg, "prompt": "...", "seed": 1}]. 4 bits NF4 (o 8 bits do bitsandbytes gerou so ruido: estouro
em float16); ~5 GB de placa e ~10 s por imagem na RTX 3070. Gera em 1536x864 e entrega em 1920x1080.
"""
import json, sys, time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline, PipelineQuantizationConfig

jobs = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
t0 = time.time()
q = PipelineQuantizationConfig(quant_backend="bitsandbytes_4bit",
                               quant_kwargs={"load_in_4bit": True, "bnb_4bit_quant_type": "nf4", "bnb_4bit_compute_dtype": torch.bfloat16},
                               components_to_quantize=["transformer", "text_encoder"])
pipe = Flux2KleinPipeline.from_pretrained("black-forest-labs/FLUX.2-klein-4B", torch_dtype=torch.bfloat16, quantization_config=q)
pipe.enable_model_cpu_offload()
print(f"modelo carregado em {time.time() - t0:.0f}s", flush=True)
for k, j in enumerate(jobs, 1):
    t = time.time(); out = Path(j["out"]); out.parent.mkdir(parents=True, exist_ok=True)
    img = pipe(prompt=j["prompt"], height=864, width=1536, guidance_scale=1.0, num_inference_steps=4,
               generator=torch.Generator("cuda").manual_seed(int(j.get("seed", 1)))).images[0]
    img.resize((1920, 1080)).save(out, quality=95)
    print(f"ok {k}/{len(jobs)} {out.name} {time.time() - t:.0f}s", flush=True)
