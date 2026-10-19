# -*- coding: utf-8 -*-
"""Dark Studio - o que cada cena e. Unico dono das listas de tipos de grafico (termos em GLOSSARY.md).
Duas perguntas, nada mais:
  kind(cena)                    -> "grafico" | "foto_real" | "local" | "ia"
  needs_media(cena, pasta)      -> True se a cena ainda nao tem o arquivo da sua midia
"ia" vale tambem para cena ainda vazia: o motor (FLUX local, Grok, Flow) e escolha de quem gera, nao da cena; depois de
gerada, o campo source diz qual foi. Sem dependencias pesadas: app, pipeline, grok_worker e tools importam este modulo.
"""
from pathlib import Path

# tipo do roteiro -> (tela_cheia, desenha_pil, vai_para_ec)
#   tela_cheia : vira a midia da cena (a cena e "grafico"); False = sobreposicao, nunca muda o tipo da cena
#   desenha_pil: gfx.py / gfx_anim.py sabem desenhar em tela cheia (caminho antigo e o que sobra no caminho novo)
#   vai_para_ec: tools/remake.py convert traduz para o EffectCraft (tools/ec_gfx.py)
TYPES = {
    "timeline": (True, True, True), "chart": (True, True, True), "quote": (True, True, True), "relmap": (True, True, True),
    "document": (True, True, False), "headline": (True, True, False), "scale": (True, True, False),
    "photo": (True, True, False), "entity_full": (True, True, False),
    "moneyflow": (True, True, False), "collapse": (True, True, False),   # animados (gfx_anim.py)
    "flow": (True, False, True), "stack": (True, False, True), "list": (True, False, True), "takeaway": (True, False, True),
    "real_photo": (False, False, True),  # o convert troca pela foto da entidade (source real_photo); sem foto vira recusado
    "chapter": (False, False, True), "lower_third": (False, False, True), "callout": (False, False, True),
    "citation": (False, False, True), "entity": (False, False, True), "parties": (False, False, True), "logo": (False, False, False),
}
FULL = frozenset(t for t, (full, _, _) in TYPES.items() if full)          # o roteiro pede grafico de tela cheia
PIL_FULL = frozenset(t for t, (full, pil, _) in TYPES.items() if full and pil)  # tela cheia que o gfx.py desenha
REAL = ("real_photo", "real_photo_parallax")


def kind(s):
    """O que a cena e. Grafico ganha de tudo (e o que a montagem mostra); depois foto real; depois imagem local; senao IA.
    Cena ja convertida (tem gfx_legacy): o grafico vem de ec.full ou do que sobrou em gfx para o gfx.py desenhar; o que o
    convert recusou fica em gfx_recusado e nao conta. Cena ainda nao convertida (caminho antigo): conta o que o gfx.py desenha."""
    if (s.get("ec") or {}).get("full") or s.get("source") == "gfx": return "grafico"
    gfx = [g.get("type") for g in s.get("gfx") or [] if isinstance(g, dict)]
    if any(t in PIL_FULL for t in gfx): return "grafico"
    if "gfx_legacy" not in s and any(t in FULL for t in gfx):  # flow/stack/list/takeaway: o convert ainda vai traduzir
        return "grafico"
    if s.get("source") in REAL: return "foto_real"
    if s.get("source") == "local": return "local"
    return "ia"


def needs_media(s, pdir):
    """Falta o arquivo da midia da cena (grafico ainda nao renderizado, IA ainda nao gerada, foto ainda nao copiada)."""
    f = s.get("file")
    return not (f and (Path(pdir) / f).is_file())
