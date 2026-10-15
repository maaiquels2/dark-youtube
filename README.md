# Dark YouTube

Protótipo local para produzir vídeos longos (8–15 min) de canais "dark" sem rosto, em línguas estrangeiras (inglês, espanhol, alemão...). Roteiro pela API do ChatGPT, cenas pelo Grok Imagine.

## Como rodar (Windows)
1. Precisa de Python 3.10+ (sem dependências extras).
2. Copie `.env.example` para `.env` e coloque sua `OPENAI_API_KEY` (o `.env` nunca vai pro GitHub).
3. Rode `python app.py` (ou dê dois cliques em `iniciar.bat`).
4. Abra http://127.0.0.1:8765

## Telas
1. **Ideia** – nicho, língua e tema → o ChatGPT sugere títulos. ✅
2. **Roteiro** – roteiro completo dividido em cenas (narração + prompt visual), editável, salvo em `projects/<id>.json`. ✅
3. **Cenas** – por cena: modo (vídeo ou imagem animada) e origem (API xAI ou Site do Grok). Gancho e retenção saem em vídeo (`grok-imagine-video-1.5-lite`), o resto em imagem (`grok-imagine-image`). Custo estimado ao vivo (preços em `config/pricing.json`), ações em massa, "Gerar todas pendentes" (3 em paralelo), regenerar e enviar arquivo manual. Arquivos vão para `projects/<id>/media/`. Precisa de `XAI_API_KEY` no `.env` para a API. ✅
4. **Montagem** – TODO: narração inteira via OpenAI TTS + ffmpeg (MP4 16:9, trilha, legendas).
5. **Publicação** – TODO: thumbnail, título, descrição e tags na língua do vídeo.

Modelo padrão: `gpt-6.1-sol` (mude com `OPENAI_MODEL` no `.env`).
