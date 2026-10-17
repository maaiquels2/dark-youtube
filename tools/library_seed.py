"""Preenche library/entities/ com logos, selos e fotos ja baixados nos projetos (sem internet, sem API).
Uso: python tools/library_seed.py"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT))
import entities as E
tot = 0
for f in sorted((ROOT / "projects").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8")); pdir = ROOT / "projects" / f.stem
    for e in d.get("entities") or []:
        sv = E.library_save(e, pdir)
        if sv: tot += len(sv); print(f"{f.stem[:24]:24} {e['name']}: {', '.join(sv)}")
print(f"\n{tot} arquivos na biblioteca; {len(list(E.LIBRARY.glob('*/meta.json')))} entidades em {E.LIBRARY}")
