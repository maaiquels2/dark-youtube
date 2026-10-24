"""python tests/test_qa_gate.py - o portao pega cada erro da Argentina num projeto de mentira."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools")); sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qa_gate

ents = [{"name": "Roberto Lavagna", "kind": "person"}, {"name": "BCRA", "kind": "agency"}]
bad = {"entities": ents, "scenes": [
    {"narration": "Minister Roberto Lavagna offered an exchange.", "ec": {"full": {"type": "flow", "nodes": [1, 2, 3, 4], "edges": []},
     "overlay": [{"type": "lower_third", "name": "Roberto Lavagna"}]}},
    {"narration": "The BCRA acted.", "ec": {"full": {"type": "timeline", "source": "Provided notes, Chapter 8"}, "overlay": [{"type": "callout"}]}},
    {"narration": "Thanks for watching.", "ec": {"full": {"type": "statement", "text": "End"}}}]}
rules = {(f["scene"], f["rule"]) for f in qa_gate.findings(bad, "x")}
for want in [(1, "pessoa_sem_foto"), (1, "lower_third_sem_foto"), (1, "fluxo"), (2, "rascunho"), (2, "foco_unico"), (2, "sem_logo"),
             (3, "cta_falado"), (3, "cta_escrito")]:
    assert want in rules, f"nao pegou {want}: {sorted(rules)}"

good = {"entities": ents, "scenes": [
    {"narration": "Minister Roberto Lavagna offered an exchange.", "ec": {"full": {"type": "pair", "items": [{"file": "entities/roberto-lavagna.jpg"}]}}},
    {"narration": "Subscribe to the channel.", "ec": {"full": {"type": "statement", "text": "End", "outro": True}}}]}
slip = {"entities": [], "scenes": [{"narration": "It fell,, then rose. and so on ."}, {"narration": "Wait... Then it fell, e.g. at 3.5 percent. Subscribe."}]}
hits = {f["scene"] for f in qa_gate.findings(slip, "x") if f["rule"] == "texto_legenda"}
assert hits == {1}, hits
assert not [f for f in qa_gate.findings(good, "x") if f["sev"] == "BLOQUEIA"], qa_gate.findings(good, "x")
print("ok")
