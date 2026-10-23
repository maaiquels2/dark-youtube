"""Reads a Grandpa Walt episode script (projects/_characters/grandpa-walt/<ep>.md)."""
import re
from pathlib import Path

def rows(md):
    """[(key 'NN', shot, visual, narration)] from the scene table."""
    out = []
    for line in Path(md).read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 5 and re.fullmatch(r"\d+", c[0]):
            out.append((f"{int(c[0]):02d}", c[2], c[3], c[4]))
    if not out: raise SystemExit(f"no scene table in {md}")
    return out

def next_episode(md):
    """(number, title) from a 'Next episode: Ep02 "Title"' line, or None."""
    m = re.search(r'Next episode:\s*Ep(\d+)\s*"([^"]+)"', Path(md).read_text(encoding="utf-8"))
    return (int(m.group(1)), m.group(2)) if m else None
