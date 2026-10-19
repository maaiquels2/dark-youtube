# Arquivo: scripts de uso único

Scripts feitos para um vídeo específico ou que refaziam o pipeline por conta própria. Saíram do caminho em 19/10/2026 (revisão de arquitetura, melhoria 5) e ficam aqui só como histórico. Não fazem parte da produção: para produzir, use `tools/produce.py`.

- **First Brands** (`fb_*`, `finish.py`, `run_pipe.py`, `research_new.py`, `kit_new.py`, `thumbs_new.py`, `sketch_new.py`, `post_new.py`, `images_fix.py`, `images_retry.py`, `gfx_pass.py`, `progress.py`, `final_sheet.py`, `ds_shot.py`, `_cur.py`, `_scr.py`, `fbsite.py`): dependem de `fb_id.txt` / `<chave>_id.txt` na pasta de trabalho.
- **FTX** (`ftx_*.py`, `tools/ftx_thumbs.py`).
- **Lehman** (`tools/lehman_trim.py`).

Cuidados se for rodar algum de novo:
- `run_pipe.py`, `fb_pipe.py` e `finish.py` refazem pesquisa, validação e a montagem antiga com regras próprias. O `run_pipe.py` zera a mídia de cenas com foto real ou imagem local.
- Os que usam `Path(__file__).parents[1]` como raiz do projeto agora estão um nível mais fundo.
