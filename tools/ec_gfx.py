# -*- coding: utf-8 -*-
"""Dark Studio - graficos animados no EffectCraft (CLI headless, github.com/storytold/effectcraft).
Alternativa animada ao gfx.py: a especificacao fica em pj["scenes"][i]["ec"] = {"full": {...}, "overlay": [...]}.
  full    (vira a midia da cena, gfx/ec-NN.mp4): counter | versus | timeline | stamp | person | pair | statement
          | flow (dinheiro entre partes; um fluxo para, outro vira alerta) | relmap (centro + partes ao redor)
          | stack (ordem de pagamento) | list (perguntas/itens no tempo da fala). Tempos (*_at, at, stop, alert) em
          segundos da cena, tirados de audio/words.json: o grafico tem que acompanhar a frase, nao o contrario.
  overlay (ProRes 4444 com alfa, gfx/ecov-NN.mov, sobreposto na montagem): chapter | lower_third | logo | callout | tag | credit | chip
Duracao = narracao da cena + pad + crossfade (mesma conta do montage.py), para o clipe nao ser esticado.
Uso: python tools/ec_gfx.py <project_id> [--only 5,20] [--kind full|overlay] [--preview 1.0,4.6]
"""
import argparse, json, os, shutil, subprocess, sys, textwrap
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import montage  # noqa: E402

CLI = os.environ.get("EFFECTCRAFT_CLI") or str(Path(os.environ.get("LOCALAPPDATA", "")) / "DarkStudio" / "effectcraft" / "effectcraft-cli.exe")
FULL = {"counter", "versus", "timeline", "stamp", "person", "pair", "statement", "flow", "relmap", "stack", "list"}

PRELUDE = r"""
var W = 1920, H = 1080, FPS = 30, DUR = D.dur;
var COL = {bg: [11, 14, 20], cream: [246, 242, 234], muted: [176, 170, 160], amber: [244, 176, 66], red: [214, 58, 52],
           teal: [64, 196, 200], paper: [236, 228, 208], ink: [34, 30, 26]};
function c01(a) { return [a[0] / 255, a[1] / 255, a[2] / 255]; }
var comp = app.project.items.addComp("G", W, H, 1, DUR, FPS);
comp.bgColor = c01(COL.bg);
function tr(l, n) { return l.property("ADBE Transform Group").property(n); }
function fx(l, n) { return l.property("ADBE Effect Parade").addProperty(n); }
function setp(e, n, v) { try { e.property(n).setValue(v); } catch (x) {} }
function anim(p, ks, infl) {
  for (var i = 0; i < ks.length; i++) p.setValueAtTime(ks[i][0], ks[i][1]);
  for (var k = 1; k <= p.numKeys; k++) {
    var v = p.value, n = (v instanceof Array) ? v.length : 1, e = [];
    for (var j = 0; j < n; j++) e.push(new KeyframeEase(0, infl || 78));
    try { p.setTemporalEaseAtKey(k, e, e); } catch (x) {}
  }
}
function fadeIn(l, t, d) { anim(tr(l, "ADBE Opacity"), [[t, 0], [t + (d || 0.45), 100]]); }
function inOut(l, t0, t1, d, op) {  // aparece em t0, some em t1
  d = d || 0.45; op = op == null ? 100 : op;
  var o = tr(l, "ADBE Opacity"); o.setValueAtTime(t0, 0); o.setValueAtTime(t0 + d, op);
  if (t1 < DUR) { o.setValueAtTime(t1, op); o.setValueAtTime(t1 + d, 0); }
}
function rise(l, t, dy) { var p = tr(l, "ADBE Position"), v = p.value; anim(p, [[t, [v[0], v[1] + (dy || 26)]], [t + 0.6, v]]); }
function text(s, o) {
  o = o || {};
  var l = comp.layers.addText(s);
  var td = l.property("ADBE Text Properties").property("ADBE Text Document"), d = td.value;
  d.font = o.font || "Inter"; if (o.style) d.fontStyle = o.style;
  d.fontSize = o.size || 40; d.fillColor = c01(o.color || COL.cream); d.tracking = o.track || 0;
  if (o.lead) d.leading = o.lead;
  d.justification = o.just == "C" ? ParagraphJustification.CENTER_JUSTIFY : (o.just == "R" ? ParagraphJustification.RIGHT_JUSTIFY : ParagraphJustification.LEFT_JUSTIFY);
  td.setValue(d);
  tr(l, "ADBE Position").setValue(o.pos || [W / 2, H / 2]);
  if (o.name) l.name = o.name;
  return l;
}
function tw(l) { try { return l.sourceRectAtTime(DUR - 0.01, false).width; } catch (x) { return 600; } }
function shapeLayer(name) { var l = comp.layers.addShape(); l.name = name || "shape"; tr(l, "ADBE Anchor Point").setValue([0, 0]); return l; }
function rect(w, h, color, o) {
  o = o || {};
  var l = shapeLayer(o.name || "rect");
  var g = l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"), V = g.property("ADBE Vectors Group");
  var r = V.addProperty("ADBE Vector Shape - Rect");
  r.property("ADBE Vector Rect Size").setValue([w, h]);
  if (o.round) r.property("ADBE Vector Rect Roundness").setValue(o.round);
  if (o.left) r.property("ADBE Vector Rect Position").setValue([w / 2, 0]);
  if (o.stroke) { var s = V.addProperty("ADBE Vector Graphic - Stroke"); s.property("ADBE Vector Stroke Color").setValue(c01(o.stroke)); s.property("ADBE Vector Stroke Width").setValue(o.sw || 4); }
  if (!o.nofill) { var f = V.addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(c01(color)); f.property("ADBE Vector Fill Opacity").setValue(o.op == null ? 100 : o.op); }
  tr(l, "ADBE Position").setValue(o.pos || [W / 2, H / 2]);
  return l;
}
function dot(size, color, pos) {
  var l = shapeLayer("dot");
  var g = l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"), V = g.property("ADBE Vectors Group");
  V.addProperty("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size").setValue([size, size]);
  V.addProperty("ADBE Vector Graphic - Fill").property("ADBE Vector Fill Color").setValue(c01(color));
  tr(l, "ADBE Position").setValue(pos); return l;
}
function line(pts, width, color, t0, t1) {  // caminho que se desenha (Trim Paths)
  var l = shapeLayer("line"); tr(l, "ADBE Position").setValue([0, 0]);
  var g = l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"), V = g.property("ADBE Vectors Group");
  var sh = new Shape(); sh.vertices = pts; sh.closed = false;
  V.addProperty("ADBE Vector Shape - Group").property("ADBE Vector Shape").setValue(sh);
  var s = V.addProperty("ADBE Vector Graphic - Stroke"); s.property("ADBE Vector Stroke Color").setValue(c01(color)); s.property("ADBE Vector Stroke Width").setValue(width);
  var tm = V.addProperty("ADBE Vector Filter - Trim");
  anim(tm.property("ADBE Vector Trim End"), [[t0, 0], [t1, 100]], 85);
  return l;
}
function shadow(l, dist, soft, op) { var s = fx(l, "Drop Shadow"); setp(s, "Distance", dist || 10); setp(s, "Softness", soft || 30); setp(s, "Opacity", op || 60); return s; }
function background(tint) {
  var b = comp.layers.addSolid(c01(COL.bg), "BG", W, H, 1);
  var ramp = fx(b, "Gradient Ramp");
  setp(ramp, "Start of Ramp", [W * 0.5, H * 0.42]); setp(ramp, "End of Ramp", [W * 1.05, H * 1.15]);
  setp(ramp, "Start Color", [0.09, 0.105, 0.145]); setp(ramp, "End Color", [0.012, 0.016, 0.026]); setp(ramp, "Ramp Shape", 2);
  var n = comp.layers.addSolid([0, 0, 0], "Smoke", W, H, 1);
  var f = fx(n, "Fractal Noise");
  setp(f, "Contrast", 170); setp(f, "Brightness", -38); setp(f, "Scale", 900); setp(f, "Complexity", 5);
  try { f.property("Evolution").expression = "time * 22"; } catch (x) {}
  var t = fx(n, "Tint"); setp(t, "Map Black To", [0, 0, 0]); setp(t, "Map White To", c01(tint || COL.amber));
  try { n.blendingMode = BlendingMode.SCREEN; } catch (x) {}
  tr(n, "ADBE Opacity").setValue(18);
  try { tr(n, "ADBE Position").expression = "[960 + time * 10, 540 - time * 4]"; } catch (x) {}
}
function source(s) {
  if (!s) return;
  var l = text("SOURCE  ·  " + s, {size: 22, color: COL.muted, track: 60, pos: [96, 985]}); fadeIn(l, 1.2, 0.6);
}
function toBack(l, above) {  // camada criada depois fica por cima: manda o painel para tras do texto
  try { if (above) l.moveAfter(above); else l.moveToEnd(); } catch (x) {}
}
function img(file) { return app.project.importFile(new ImportOptions(new File(file))); }
function fitScale(item, w, h) { return Math.min(w / item.width, h / item.height) * 100; }
function card(n, w, h, pos) {  // cartao de no: logo/foto em papel, ou texto em painel escuro
  var cd, x = pos[0], y = pos[1];
  if (n.file) {
    cd = rect(w, h, COL.paper, {round: 12, pos: pos}); shadow(cd, 14, 50, 70);
    var it = img(n.file), s = fitScale(it, w - 36, h - 36), lg = comp.layers.add(it);
    tr(lg, "ADBE Scale").setValue([s, s]); lg.parent = cd; tr(lg, "ADBE Position").setValue([0, 0]); fadeIn(lg, n.at, 0.4);
    var lb = text(n.label, {style: "Medium", size: 30, color: COL.amber, track: 200, just: "C", pos: [x, y + h / 2 + 54]}); fadeIn(lb, n.at + 0.3); rise(lb, n.at + 0.3);
    if (n.sub) { var sb = text(n.sub, {size: 28, color: COL.muted, just: "C", pos: [x, y + h / 2 + 98], lead: 36}); fadeIn(sb, n.at + 0.5); }
  } else {
    cd = rect(w, h, COL.bg, {round: 12, op: 92, stroke: COL.muted, sw: 2, pos: pos}); shadow(cd, 10, 40, 60);
    var lb2 = text(n.label, {font: "Playfair Display", size: 50, just: "C", pos: [x, y + (n.sub ? -6 : 16)]}); fadeIn(lb2, n.at + 0.2);
    if (n.sub) { var sb2 = text(n.sub, {size: 28, color: COL.muted, just: "C", pos: [x, y + 44], lead: 34}); fadeIn(sb2, n.at + 0.35); }
  }
  anim(tr(cd, "ADBE Position"), [[n.at, [x, y + 40]], [n.at + 0.7, [x, y]]]); fadeIn(cd, n.at, 0.4);
  if (n.alert_at != null) {  // contorno vermelho + aviso quando a narracao chega na consequencia
    var al = rect(w + 16, h + 16, COL.red, {round: 16, nofill: true, stroke: COL.red, sw: 5, pos: pos}); fadeIn(al, n.alert_at, 0.3);
    var g = fx(al, "Glow"); setp(g, "Glow Radius", 30); setp(g, "Luma Threshold", 10);
    if (n.alert_label) { var at = text(n.alert_label, {style: "SemiBold", size: 26, color: COL.red, track: 160, just: "C", pos: [x, y - h / 2 - 26]}); fadeIn(at, n.alert_at + 0.15); rise(at, n.alert_at + 0.15, -14); }
  }
  if (n.dim_at != null) { var o = tr(cd, "ADBE Opacity"); o.setValueAtTime(n.dim_at, 100); o.setValueAtTime(n.dim_at + 0.5, 35); }
  return cd;
}
function flowDots(x0, y0, x1, y1, color, t0, t1) {  // 3 pontos correndo de (x0,y0) para (x1,y1): dinheiro passando
  for (var k = 0; k < 3; k++) {
    var d = dot(13, color, [x0, y0]), g = fx(d, "Glow"); setp(g, "Glow Radius", 24); setp(g, "Luma Threshold", 10);
    try { tr(d, "ADBE Position").expression = "var u = (Math.max(0, time - " + t0 + ") / 1.6 + " + (k / 3) + ") % 1; [" + x0 + " + u * " + (x1 - x0) + ", " + y0 + " + u * " + (y1 - y0) + "]"; } catch (x) {}
    inOut(d, t0, t1, 0.3);
  }
}
function fit(l, maxw) {  // texto mais largo que o espaco encolhe ate caber (rotulo de seta, item de lista)
  var w = tw(l); if (w <= maxw) return l;
  var td = l.property("ADBE Text Properties").property("ADBE Text Document"), d = td.value; d.fontSize = Math.floor(d.fontSize * maxw / w); td.setValue(d); return l;
}
function credit(s) { if (s) { var cr = text(s, {size: 18, color: COL.muted, just: "R", pos: [W - 96, 1000]}); fadeIn(cr, 0.6); } }
"""

B = {}
B["counter"] = r"""
background(D.tint ? COL[D.tint] : null);
var ctl = comp.layers.addNull(); ctl.name = "CTRL";
var sl = fx(ctl, "Slider Control"); sl.property("Slider").setValue(D.value);
// t1: instante em que o numero e falado (tools/words.py). T0 no maximo 1.2 s: fala tardia conta devagar em vez de deixar a tela vazia
var T1 = D.t1 || 2.5, T0 = Math.min(Math.max(0.3, T1 - 2.05), 1.2), OFF = T1 - 2.5;
var fin = D.prefix + D.value.toFixed(D.dec) + D.suffix;
var num = text(fin, {style: "SemiBold", size: D.size || 190, pos: [0, 0], name: "Number"});
var w = tw(num); tr(num, "ADBE Position").setValue([W / 2 - w / 2, 545]);  // cresce para a direita: numero nao "danca"
num.property("ADBE Text Properties").property("ADBE Text Document").expression =
  'var v = thisComp.layer("CTRL").effect("Slider Control")("Slider"); var x = ease(time, ' + T0 + ', ' + T1 + ', 0, v); ' +
  JSON.stringify(D.prefix) + ' + x.toFixed(' + D.dec + ') + ' + JSON.stringify(D.suffix);
var gl = fx(num, "Glow"); setp(gl, "Luma Threshold", 45); setp(gl, "Glow Radius", 36); setp(gl, "Glow Brightness", 55);
setp(gl, "Use Tint Color", true); setp(gl, "Tint Color", c01(COL.amber));
shadow(num, 8, 40, 70);
var sw = fx(num, "CC Light Sweep"); setp(sw, "Width", 60); setp(sw, "Sweep Intensity", 60);
anim(sw.property("Center"), [[2.7 + OFF, [-300, 400]], [3.7 + OFF, [2300, 400]]], 40);
anim(tr(num, "ADBE Scale"), [[T0 - 0.15, [93, 93]], [T1 + 0.3, [100, 100]]]);
fadeIn(num, Math.max(0, T0 - 0.15), 0.5);
line([[W / 2 - 260, 640], [W / 2 + 260, 640]], 3, COL.amber, 2.3 + OFF, 3.0 + OFF);
var lb = text(D.label, {style: "Medium", size: 38, color: COL.amber, track: 260, just: "C", pos: [W / 2, 712]}); fadeIn(lb, 2.6 + OFF); rise(lb, 2.6 + OFF);
if (D.sub) { var sb = text(D.sub, {font: "Playfair Display", size: 52, color: COL.cream, just: "C", pos: [W / 2, 800]}); fadeIn(sb, 3.0 + OFF); rise(sb, 3.0 + OFF); }
source(D.source);
"""
B["versus"] = r"""
background(COL.teal);
var tt = text(D.title, {font: "Playfair Display", size: 76, just: "C", pos: [W / 2, 205]}); fadeIn(tt, 0.2); rise(tt, 0.2);
line([[W / 2, 330], [W / 2, 760]], 2, COL.muted, 0.6, 1.4);
var mx = Math.max(D.items[0].value, D.items[1].value);
for (var i = 0; i < 2; i++) {
  var it = D.items[i], cx = i ? 1400 : 520, col = COL[it.color] || COL.cream, t0 = 0.8 + i * 1.1;
  var lb = text(it.label, {style: "Medium", size: 30, color: col, track: 220, just: "C", pos: [cx, 395]}); fadeIn(lb, t0); rise(lb, t0);
  var ctl = comp.layers.addNull(); ctl.name = "C" + i; fx(ctl, "Slider Control").property("Slider").setValue(it.value);
  var fin = it.prefix + it.value.toFixed(it.dec) + it.suffix;
  var n = text(fin, {style: "SemiBold", size: 128, pos: [0, 0], name: "N" + i}); var w = tw(n);
  tr(n, "ADBE Position").setValue([cx - w / 2, 560]);
  n.property("ADBE Text Properties").property("ADBE Text Document").expression =
    'var v = thisComp.layer("C' + i + '").effect("Slider Control")("Slider"); var x = ease(time, ' + (t0 + 0.2) + ', ' + (t0 + 1.8) + ', 0, v); ' +
    JSON.stringify(it.prefix) + ' + x.toFixed(' + it.dec + ') + ' + JSON.stringify(it.suffix);
  fadeIn(n, t0 + 0.1); shadow(n, 6, 30, 60);
  var bw = 640 * it.value / mx, bar = rect(bw, 20, col, {left: true, pos: [cx - 320, 640], round: 4});
  rect(640, 20, [255, 255, 255], {left: true, pos: [cx - 320, 640], op: 8, round: 4});
  anim(tr(bar, "ADBE Scale"), [[t0 + 0.2, [0, 100]], [t0 + 1.8, [100, 100]]]);
  if (it.note) { var nt = text(it.note, {size: 30, color: COL.muted, just: "C", pos: [cx, 715]}); fadeIn(nt, t0 + 1.4); }
}
if (D.note) { var no = text(D.note, {size: 28, color: COL.muted, just: "C", pos: [W / 2, 870], lead: 38}); fadeIn(no, 3.4); }
source(D.source);
"""
B["timeline"] = r"""
background(COL.amber);
var tt = text(D.title, {font: "Playfair Display", size: 76, just: "C", pos: [W / 2, 200]}); fadeIn(tt, 0.2); rise(tt, 0.2);
var x0 = 190, x1 = 1730, y = 540, N = D.events.length;
line([[x0, y], [x1, y]], 3, COL.muted, 0.5, 1.6);
var step = Math.min(0.85, (DUR - 3.2) / N);
for (var i = 0; i < N; i++) {
  var e = D.events[i], x = N == 1 ? W / 2 : x0 + 70 + i * (x1 - x0 - 140) / (N - 1), t = 1.0 + i * step, hi = (i == D.highlight);
  var col = hi ? COL.red : COL.amber;
  var d = dot(hi ? 34 : 24, col, [x, y]);
  anim(tr(d, "ADBE Scale"), [[t, [0, 0]], [t + 0.22, [135, 135]], [t + 0.45, [100, 100]]], 60);
  if (hi) { var g = fx(d, "Glow"); setp(g, "Glow Radius", 40); setp(g, "Luma Threshold", 10); }
  var dl = text(e.date, {style: "SemiBold", size: 32, color: col, track: 80, just: "C", pos: [x, y - 52]}); fadeIn(dl, t + 0.1); rise(dl, t + 0.1, -18);
  var lb = text(e.label, {size: 28, color: COL.cream, just: "C", pos: [x, y + 72], lead: 36}); fadeIn(lb, t + 0.25); rise(lb, t + 0.25);
}
source(D.source);
"""
B["stamp"] = r"""
background(COL.red);
var cam = comp.layers.addNull(); cam.name = "CAM"; tr(cam, "ADBE Position").setValue([W / 2, H / 2]);
try { tr(cam, "ADBE Position").expression = "var a = (time > 1.12 && time < 1.7) ? 16 * (1 - (time - 1.12) / 0.58) : 0; [960, 540] + [Math.sin(time * 90) * a, Math.cos(time * 73) * a * 0.6]"; } catch (x) {}
var doc = rect(680, 820, COL.paper, {pos: [690, 535]}); doc.parent = cam; shadow(doc, 18, 60, 70);
var tx = fx(doc, "Fractal Noise"); setp(tx, "Contrast", 60); setp(tx, "Brightness", 30); setp(tx, "Scale", 40); setp(tx, "Opacity", 10);
anim(tr(doc, "ADBE Rotate Z"), [[0, -9], [0.8, -4]]);
anim(tr(doc, "ADBE Position"), [[0, [690 - 960, 535 - 540 + 700]], [0.8, [690 - 960, 535 - 540]]]);
for (var i = 0; i < 12; i++) {  // linhas de texto ilegiveis (objeto de cena, nao documento real)
  var wl = (i % 4 == 3) ? 280 : 530 - (i % 3) * 40;
  var ln = rect(wl, 12, [120, 112, 100], {left: true, op: 55}); ln.parent = doc; tr(ln, "ADBE Position").setValue([-280, -300 + i * 52]);
}
var st = comp.layers.addNull(); st.name = "STAMP"; st.parent = cam; tr(st, "ADBE Position").setValue([690 - 960, 545 - 540]);
tr(st, "ADBE Rotate Z").setValue(-10);
var sl = text(D.text, {style: "Bold", size: 132, color: COL.red, track: 120, just: "C", pos: [0, 46]});
var sw2 = tw(sl), box = rect(sw2 + 90, 190, COL.red, {nofill: true, stroke: COL.red, sw: 12, round: 18, pos: [0, 0]});
sl.parent = st; box.parent = st; tr(sl, "ADBE Position").setValue([0, 46]); tr(box, "ADBE Position").setValue([0, 0]);
var tz = fx(sl, "Turbulent Displace"); setp(tz, "Amount", 18); setp(tz, "Size", 6);
var tz2 = fx(box, "Turbulent Displace"); setp(tz2, "Amount", 18); setp(tz2, "Size", 6);
anim(tr(st, "ADBE Scale"), [[1.0, [230, 230]], [1.16, [100, 100]]], 20);
anim(tr(st, "ADBE Opacity"), [[1.0, 0], [1.08, 100]], 20);
var dt = text(D.date, {font: "Playfair Display", size: 72, pos: [1200, 520]}); fadeIn(dt, 1.8); rise(dt, 1.8);
var sb = text(D.sub, {size: 34, color: COL.muted, pos: [1204, 600], lead: 46}); fadeIn(sb, 2.2); rise(sb, 2.2);
source(D.source);
"""
B["person"] = r"""
background(COL.teal);
var it = img(D.photo), s = fitScale(it, 600, 640);
var pw = it.width * s / 100, phh = it.height * s / 100;
var fr = rect(pw + 44, phh + 150, COL.paper, {pos: [600, 520]}); shadow(fr, 20, 60, 75);
var ph = comp.layers.add(it);  // depois da moldura: fica por cima dela
ph.parent = fr; tr(ph, "ADBE Position").setValue([0, -40]); anim(tr(ph, "ADBE Scale"), [[0, [s, s]], [DUR, [s * 1.05, s * 1.05]]], 10);
var m = ph.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"), ms = new Shape();  // recorta o excesso do push-in
ms.vertices = [[it.width * (1 - 100 / 105) / 2, it.height * (1 - 100 / 105) / 2], [it.width * (1 + 100 / 105) / 2, it.height * (1 - 100 / 105) / 2],
               [it.width * (1 + 100 / 105) / 2, it.height * (1 + 100 / 105) / 2], [it.width * (1 - 100 / 105) / 2, it.height * (1 + 100 / 105) / 2]];
ms.closed = true; m.property("ADBE Mask Shape").setValue(ms);
var cap = text(D.name, {font: "Playfair Display", size: 40, color: COL.ink, just: "C", pos: [0, phh / 2 + 30]}); cap.parent = fr; tr(cap, "ADBE Position").setValue([0, phh / 2 + 32]);
anim(tr(fr, "ADBE Position"), [[0, [380, 580]], [0.9, [600, 520]]]);
anim(tr(fr, "ADBE Rotate Z"), [[0, -9], [0.9, -3]]);
fadeIn(fr, 0, 0.4);
var x = 1010;
var lb = text(D.label, {style: "Medium", size: 32, color: COL.amber, track: 240, pos: [x, 330]}); fadeIn(lb, 0.9); rise(lb, 0.9);
var nm = text(D.name, {font: "Playfair Display", size: 104, pos: [x - 4, 450]});
var nw = tw(nm), room = W - 110 - x;  // nome longo encolhe para caber na area segura
if (nw > room) { var ntd = nm.property("ADBE Text Properties").property("ADBE Text Document"), nd = ntd.value; nd.fontSize = Math.floor(104 * room / nw); ntd.setValue(nd); }
fadeIn(nm, 1.1); rise(nm, 1.1);
line([[x, 492], [x + 420, 492]], 3, COL.amber, 1.4, 2.0);
var rl = text(D.role, {size: 36, color: COL.muted, pos: [x, 560], lead: 48}); fadeIn(rl, 1.6); rise(rl, 1.6);
var pts = D.points || [];
for (var i = 0; i < pts.length; i++) {
  var t = 2.4 + i * 0.7, y = 700 + i * 64;
  var b = dot(12, COL.amber, [x + 6, y - 12]); fadeIn(b, t, 0.3);
  var p = text(pts[i], {size: 36, pos: [x + 32, y]}); fadeIn(p, t); rise(p, t, 14);
}
if (D.credit) { var cr = text(D.credit, {size: 18, color: COL.muted, just: "R", pos: [W - 96, 1000]}); fadeIn(cr, 0.6); }
source(D.source);
"""
B["pair"] = r"""
background(COL.teal);
var tt = text(D.title, {font: "Playfair Display", size: 76, just: "C", pos: [W / 2, 200]}); fadeIn(tt, 0.2); rise(tt, 0.2);
for (var i = 0; i < 2; i++) {
  var e = D.items[i], cx = i ? 1380 : 540, t0 = 0.5 + i * 0.5;
  var it = img(e.file), s = fitScale(it, 380, 120);
  var cd = rect(480, 220, COL.paper, {round: 12, pos: [cx, 470]}); shadow(cd, 14, 50, 70);
  var lg = comp.layers.add(it); tr(lg, "ADBE Scale").setValue([s, s]); lg.parent = cd; tr(lg, "ADBE Position").setValue([0, 0]);
  anim(tr(cd, "ADBE Position"), [[t0, [cx, 520]], [t0 + 0.7, [cx, 470]]]); fadeIn(cd, t0, 0.4); fadeIn(lg, t0, 0.4);
  var lb = text(e.label, {style: "Medium", size: 30, color: COL.amber, track: 220, just: "C", pos: [cx, 650]}); fadeIn(lb, t0 + 0.4); rise(lb, t0 + 0.4);
  if (e.note) { var nt = text(e.note, {size: 30, color: COL.muted, just: "C", pos: [cx, 702], lead: 40}); fadeIn(nt, t0 + 0.6); }
}
line([[800, 470], [1120, 470]], 4, COL.amber, 1.5, 2.2);
var pd = dot(16, COL.amber, [800, 470]); var g = fx(pd, "Glow"); setp(g, "Glow Radius", 30); setp(g, "Luma Threshold", 10);
try { tr(pd, "ADBE Position").expression = "var u = Math.max(0, time - 2.2) % 1.4 / 1.4; [800 + u * 320, 470]"; } catch (x) {}
inOut(pd, 2.2, DUR, 0.3);
if (D.link) { var lk = text(D.link, {style: "Medium", size: 24, color: COL.cream, track: 120, just: "C", pos: [960, 438]}); fadeIn(lk, 2.3); }
source(D.source);
"""
B["statement"] = r"""
background(D.tint ? COL[D.tint] : COL.teal);
var lb = text(D.label, {style: "Medium", size: 32, color: COL.amber, track: 260, just: "C", pos: [W / 2, 380]}); fadeIn(lb, 0.3); rise(lb, 0.3);
line([[W / 2 - 200, 420], [W / 2 + 200, 420]], 2, COL.amber, 0.5, 1.1);
var tx = text(D.text, {font: "Playfair Display", size: 76, just: "C", pos: [W / 2, 540], lead: 96}); fadeIn(tx, 0.8); rise(tx, 0.8); shadow(tx, 6, 30, 60);
var tt = tx.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
try {  // palavras surgem em sequencia
  tt.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity").setValue(0);
  var rs = tt.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  anim(rs.property("ADBE Text Percent Start"), [[0.8, 0], [2.8, 100]], 20);
} catch (x) {}
if (D.sub) { var sb = text(D.sub, {size: 32, color: COL.muted, just: "C", pos: [W / 2, 800]}); fadeIn(sb, 3.0); }
source(D.source);
"""
B["flow"] = r"""
background(D.tint ? COL[D.tint] : COL.teal);
if (D.label) { var lb = text(D.label, {style: "Medium", size: 28, color: COL.amber, track: 260, just: "C", pos: [W / 2, 150]}); fadeIn(lb, D.title_at || 0.2); }
if (D.title) { var tt = text(D.title, {font: "Playfair Display", size: 66, just: "C", pos: [W / 2, 232]}); fadeIn(tt, (D.title_at || 0.2) + 0.15); rise(tt, (D.title_at || 0.2) + 0.15); }
var N = D.nodes.length, Y = 540, CW = 380, X = [];
for (var i = 0; i < N; i++) {
  var n = D.nodes[i]; X.push(N == 1 ? W / 2 : 290 + i * (W - 580) / (N - 1));
  card(n, CW, n.h || (n.file ? 230 : 190), [X[i], Y]);
  if (n.bar != null) {  // duracao do compromisso (curto x longo), sem numero inventado
    var by = Y + (n.file ? 115 : 95) + (n.sub && n.file ? 150 : 72), bx = X[i] - 150;
    var bt = rect(300, 14, [255, 255, 255], {left: true, op: 10, round: 4, pos: [bx, by]}); fadeIn(bt, n.at + 0.3, 0.4);
    var bf = rect(300 * n.bar, 14, COL[n.bar_color || "amber"], {left: true, round: 4, pos: [bx, by]});
    anim(tr(bf, "ADBE Scale"), [[n.at + 0.5, [0, 100]], [n.at + 1.6, [100, 100]]]); fadeIn(bf, n.at + 0.5, 0.2);
    var bl = text(n.bar_label, {style: "Medium", size: 24, color: COL.muted, track: 160, just: "C", pos: [X[i], by + 46]}); fadeIn(bl, n.at + 0.9);
  }
}
for (var j = 0; j < D.edges.length; j++) {
  var e = D.edges[j], a = X[e.from], b = X[e.to], dir = b > a ? 1 : -1, y = Y + (e.dy || 0);
  var x0 = a + dir * (CW / 2 + 26), x1 = b - dir * (CW / 2 + 26), mid = (x0 + x1) / 2;
  line([[x0, y], [x1, y]], 3, COL.muted, e.at, e.at + 0.6);
  var el = fit(text(e.label, {style: "Medium", size: 24, color: COL.cream, track: 140, just: "C", pos: [mid, y - 28]}), Math.abs(x1 - x0) - 16); fadeIn(el, e.at + 0.3);
  var end = e.stop != null ? e.stop : (e.alert != null ? e.alert : DUR);
  flowDots(x0, y, x1, y, COL.amber, e.at + 0.6, end);
  if (e.alert != null) flowDots(x0, y, x1, y, COL.red, e.alert, DUR);
  var tag = e.stop != null ? [e.stop, e.stop_label, COL.muted] : (e.alert != null ? [e.alert, e.alert_label, COL.red] : null);
  if (tag && tag[1]) { var sl = fit(text(tag[1], {style: "SemiBold", size: 24, color: tag[2], track: 160, just: "C", pos: [mid, y + 52]}), Math.abs(x1 - x0) - 16); fadeIn(sl, tag[0] + 0.1); rise(sl, tag[0] + 0.1, 14); }
}
if (D.note) { var no = text(D.note, {size: 32, color: COL[D.note_color || "cream"], just: "C", pos: [W / 2, 880], lead: 42}); fadeIn(no, D.note_at || 3); rise(no, D.note_at || 3); }
credit(D.credit); source(D.source);
"""
B["relmap"] = r"""
background(D.tint ? COL[D.tint] : COL.teal);
if (D.title) { var tt = text(D.title, {font: "Playfair Display", size: 60, just: "C", pos: [W / 2, 130]}); fadeIn(tt, 0.2); rise(tt, 0.2); }
var C = [W / 2, 500], N = D.sats.length;  // 2-4 partes; nenhuma bem em cima do centro (o rotulo do cartao bateria nele)
var a0 = D.angle0 != null ? D.angle0 : (N == 2 ? 180 : N == 3 ? -150 : -135);
for (var i = 0; i < N; i++) {
  var s = D.sats[i], ang = (a0 + i * 360 / N) * Math.PI / 180, p = [C[0] + 640 * Math.cos(ang), C[1] + 330 * Math.sin(ang)];
  var sh = s.h ? 210 : (s.sub ? 150 : 120);
  if (Math.abs(Math.cos(ang)) < 0.5 && Math.sin(ang) > 0)  // parte logo abaixo: a linha sai por baixo do rotulo do centro
    line([[p[0], C[1] + 222], [p[0], p[1] - sh / 2 - 12]], 3, COL.muted, s.at, s.at + 0.5);
  else
    line([[C[0] + 0.26 * (p[0] - C[0]), C[1] + 0.40 * (p[1] - C[1])], [C[0] + 0.70 * (p[0] - C[0]), C[1] + 0.62 * (p[1] - C[1])]], 3, COL.muted, s.at, s.at + 0.5);
  card(s, 360, sh, p);  // foto de pessoa precisa de altura
}
card(D.center, 400, 220, C);
credit(D.credit); source(D.source);
"""
B["stack"] = r"""
background(D.tint ? COL[D.tint] : COL.teal);
if (D.label) { var lb = text(D.label, {style: "Medium", size: 28, color: COL.amber, track: 260, just: "C", pos: [W / 2, 160]}); fadeIn(lb, 0.2); }
var tt = text(D.title, {font: "Playfair Display", size: 66, just: "C", pos: [W / 2, 246]}); fadeIn(tt, 0.35); rise(tt, 0.35);
var N = D.tiers.length, y0 = 400, step = Math.min(170, 440 / Math.max(1, N - 1)), BX = 1010, BW = 650;
line([[230, y0 - 20], [230, y0 + (N - 1) * step + 30]], 3, COL.amber, 0.8, 0.8 + 0.5 * N);
for (var i = 0; i < N; i++) {
  var t = D.tiers[i], y = y0 + i * step, ta = 0.9 + i * 0.45, hi = (i == D.highlight);
  var nm = text((i + 1) + ".  " + t.label, {font: "Playfair Display", size: 46, pos: [290, y + 14]}); fadeIn(nm, ta); rise(nm, ta, 14);
  if (t.sub) { var sb = text(t.sub, {size: 24, color: COL.muted, pos: [330, y + 54]}); fadeIn(sb, ta + 0.2); }
  var bg = rect(BW, 44, [255, 255, 255], {left: true, op: 9, round: 6, pos: [BX, y]}); fadeIn(bg, ta, 0.3);
  if (t.fill > 0) {
    var bf = rect(BW * t.fill, 44, COL.amber, {left: true, round: 6, pos: [BX, y]});
    anim(tr(bf, "ADBE Scale"), [[t.at, [0, 100]], [t.at + 1.2, [100, 100]]]); fadeIn(bf, t.at, 0.15);
  }
  if (hi && D.highlight_at != null) {
    var ol = rect(BW + 12, 56, COL.red, {left: true, nofill: true, stroke: COL.red, sw: 4, round: 8, pos: [BX - 6, y]}); fadeIn(ol, D.highlight_at, 0.3);
    var hl = text(D.highlight_label, {style: "SemiBold", size: 26, color: COL.red, track: 140, pos: [BX, y + 62]}); fadeIn(hl, D.highlight_at + 0.15); rise(hl, D.highlight_at + 0.15, 12);
  }
}
if (D.note) { var no = text(D.note, {size: 22, color: COL.muted, track: 60, just: "R", pos: [BX + BW, 330]}); fadeIn(no, 1.0); }
credit(D.credit); source(D.source);
"""
B["list"] = r"""
background(D.tint ? COL[D.tint] : COL.teal);
var lb = text(D.label, {style: "Medium", size: 30, color: COL.amber, track: 260, just: "C", pos: [W / 2, 300]}); fadeIn(lb, D.label_at || 0.3); rise(lb, D.label_at || 0.3);
line([[W / 2 - 220, 340], [W / 2 + 220, 340]], 2, COL.amber, (D.label_at || 0.3) + 0.2, (D.label_at || 0.3) + 0.8);
var N = D.items.length, step = 118, y0 = 520 - (N - 1) * step / 2 + 30, X, MW = 0, TX = [];
for (var i = 0; i < N; i++) {
  var it = D.items[i], y = y0 + i * step;
  var d = dot(16, COL.amber, [0, y - 20]), tx = text(it.text, {font: "Playfair Display", size: 62, pos: [0, y]});
  fit(tx, W - 300 - 42); fadeIn(d, it.at, 0.3); shadow(tx, 5, 25, 55); TX.push([d, tx, y, it.at]); MW = Math.max(MW, tw(tx));
}
X = D.x || (W / 2 - (MW + 42) / 2);
for (var k = 0; k < TX.length; k++) {
  tr(TX[k][0], "ADBE Position").setValue([X, TX[k][2] - 20]); tr(TX[k][1], "ADBE Position").setValue([X + 42, TX[k][2]]);
  fadeIn(TX[k][1], TX[k][3]); rise(TX[k][1], TX[k][3], 18);
}
credit(D.credit); source(D.source);
"""
B["overlay"] = r"""
comp.bgColor = [0, 0, 0];
var END = DUR - 0.75, HASTAG = false;
for (var q = 0; q < D.items.length; q++) if (D.items[q].type == "tag") HASTAG = true;  // destaque desce para nao encostar na etiqueta
for (var k = 0; k < D.items.length; k++) {
  var e = D.items[k], t0 = e.start == null ? 0.4 : e.start, t1 = e.end == null ? END : Math.min(e.end, END);
  if (e.type == "chapter") {
    t0 = e.start == null ? 0.15 : e.start; t1 = e.end == null ? Math.min(3.4, END) : t1;
    var sc = comp.layers.addSolid([0, 0, 0], "scrim", W, H, 1); inOut(sc, t0, t1, 0.5, 45);
    var lb = text("CHAPTER " + e.num, {style: "Medium", size: 30, color: COL.amber, track: 420, just: "C", pos: [W / 2, 452]}); inOut(lb, t0 + 0.1, t1);
    var tt = text(e.title, {font: "Playfair Display", size: 124, just: "C", pos: [W / 2, 590]}); inOut(tt, t0 + 0.25, t1);
    anim(tr(tt, "ADBE Scale"), [[t0 + 0.25, [106, 106]], [t1 + 0.45, [100, 100]]], 30); shadow(tt, 6, 40, 70);
    var l1 = line([[W / 2 - 150, 482], [W / 2 - 520, 482]], 2, COL.amber, t0 + 0.3, t0 + 1.0); inOut(l1, t0 + 0.3, t1, 0.3);
    var l2 = line([[W / 2 + 150, 482], [W / 2 + 520, 482]], 2, COL.amber, t0 + 0.3, t0 + 1.0); inOut(l2, t0 + 0.3, t1, 0.3);
  } else if (e.type == "lower_third") {
    var X = 120, Y = 860;
    var nm = text(e.name, {font: "Playfair Display", size: 62, pos: [X + 44, Y + 4]}), rl = text(e.role, {size: 30, color: COL.amber, track: 40, pos: [X + 46, Y + 52]});
    var pw = Math.max(tw(nm), tw(rl)) + 100;
    var pn = rect(pw, 150, COL.bg, {left: true, op: 86, pos: [X, Y]}); shadow(pn, 6, 40, 60);
    var br = rect(8, 150, COL.amber, {left: true, pos: [X, Y]});
    toBack(pn, nm);
    anim(tr(pn, "ADBE Scale"), [[t0, [0, 100]], [t0 + 0.6, [100, 100]]]); inOut(pn, t0, t1, 0.2);
    anim(tr(br, "ADBE Scale"), [[t0 - 0.1, [100, 0]], [t0 + 0.25, [100, 100]]]); inOut(br, t0 - 0.1, t1, 0.15);
    var a = nm.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
    try {
      a.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity").setValue(0);
      var rs = a.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
      anim(rs.property("ADBE Text Percent Start"), [[t0 + 0.35, 0], [t0 + 1.0, 100]], 20);
    } catch (x) { fadeIn(nm, t0 + 0.35); }
    inOut(nm, t0 + 0.3, t1, 0.05); inOut(rl, t0 + 0.9, t1);
    anim(tr(rl, "ADBE Position"), [[t0 + 0.9, [X + 46, Y + 76]], [t0 + 1.4, [X + 46, Y + 52]]]);
  } else if (e.type == "logo") {
    var it = img(e.file), s = fitScale(it, 330, 96);
    var X = 120 + 230, Y = 900;
    var cd = rect(460, 170, COL.paper, {round: 10, pos: [X, Y]}); shadow(cd, 10, 40, 65);
    var lg = comp.layers.add(it);  // depois do cartao: fica por cima dele
    tr(lg, "ADBE Scale").setValue([s, s]); lg.parent = cd; tr(lg, "ADBE Position").setValue([0, 0]);
    var lb = text(e.label, {style: "Medium", size: 26, color: COL.amber, track: 200, pos: [X - 230, Y - 112]});
    lb.parent = cd; tr(lb, "ADBE Position").setValue([-230, -112]); shadow(lb, 3, 10, 80);
    anim(tr(cd, "ADBE Position"), [[t0, [X, Y + 60]], [t0 + 0.6, [X, Y]]]); inOut(cd, t0, t1, 0.35);
    inOut(lb, t0 + 0.3, t1); inOut(lg, t0, t1, 0.35);
  } else if (e.type == "callout") {
    var X = 110, Y = HASTAG ? 175 : 120;
    var lb = text(e.label, {style: "Medium", size: 28, color: COL.amber, track: 240, pos: [X + 40, Y + 58]});
    var mt = text(e.text, {style: "SemiBold", size: 56, pos: [X + 38, Y + 128]});
    var pw = Math.max(tw(lb), tw(mt)) + 90;
    var pn = rect(pw, 150, COL.bg, {left: true, op: 84, pos: [X, Y + 85]}); shadow(pn, 6, 40, 60); toBack(pn, lb);
    var br = rect(8, 150, COL.red, {left: true, pos: [X, Y + 85]});
    anim(tr(pn, "ADBE Scale"), [[t0, [0, 100]], [t0 + 0.55, [100, 100]]]); inOut(pn, t0, t1, 0.2); inOut(br, t0, t1, 0.15);
    inOut(lb, t0 + 0.35, t1); inOut(mt, t0 + 0.5, t1); rise(mt, t0 + 0.5, 18);
  } else if (e.type == "tag") {
    var tg = text(e.text, {style: "Medium", size: 26, track: 180, pos: [138, 118]});
    var pl = rect(tw(tg) + 78, 48, COL.bg, {left: true, op: 72, round: 24, pos: [92, 109]}); toBack(pl, tg);
    var d = dot(14, COL.red, [116, 109]);
    inOut(pl, t0, t1, 0.3, 72); inOut(d, t0, t1, 0.3); inOut(tg, t0 + 0.1, t1);
    anim(tr(pl, "ADBE Scale"), [[t0, [0, 100]], [t0 + 0.45, [100, 100]]]);
  } else if (e.type == "chip") {  // logo pequeno no canto superior direito: a empresa citada aparece na tela
    for (var j = 0; j < e.files.length; j++) {
      var cx = W - 110 - 105 - j * 230, it = img(e.files[j]), s = fitScale(it, 170, 44);
      var cd = rect(210, 72, COL.paper, {round: 10, op: 94, pos: [cx, 104]}); shadow(cd, 6, 24, 60);
      var lg = comp.layers.add(it); tr(lg, "ADBE Scale").setValue([s, s]); lg.parent = cd; tr(lg, "ADBE Position").setValue([0, 0]);
      anim(tr(cd, "ADBE Position"), [[t0 + j * 0.15, [cx, 70]], [t0 + j * 0.15 + 0.5, [cx, 104]]]);
      inOut(cd, t0 + j * 0.15, t1, 0.35, 94); inOut(lg, t0 + j * 0.15, t1, 0.35);
    }
  } else if (e.type == "credit") {
    var cr = text(e.text, {size: 18, color: COL.cream, just: "R", pos: [W - 108, 1004]});
    var cp = rect(tw(cr) + 28, 30, COL.bg, {op: 80, round: 6, pos: [W - 108 - tw(cr) / 2, 998]}); toBack(cp, cr);
    inOut(cp, 0.3, END, 0.4, 80); inOut(cr, 0.3, END, 0.4, 92);
  }
}
"""

ENC_FULL = ["--bitrate", "20000"]
ENC_OV = ["--format", "prores", "--prores", "4444", "--channels", "rgba"]


def wrap(s, width):
    return "\r".join(textwrap.wrap(s, width)) if s and len(s) > width else (s or "")


def durations(pdir, n):
    c = montage.cfg()
    ff = shutil.which("ffprobe")
    out = []
    for i in range(n):
        r = subprocess.run([ff, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            str(pdir / "audio" / f"scene-{i+1:02d}.mp3")], capture_output=True, text=True)
        d = float(r.stdout.strip() or 4) + c["pad_seconds"]
        out.append(round(d + (c["crossfade_seconds"] if i < n - 1 else 0), 3))
    return out


def prep(spec, wd, pdir):
    """Copia imagens para a pasta do script (o EffectCraft so le arquivos ao lado do projeto) e quebra linhas."""
    spec = json.loads(json.dumps(spec))
    def local(rel):
        src = pdir / rel; dst = wd / src.name
        if not dst.is_file() or dst.stat().st_size != src.stat().st_size or dst.stat().st_mtime < src.stat().st_mtime:
            shutil.copyfile(src, dst)  # recopia se a imagem em entities/ foi trocada (antes ficava a versao velha no render)
        return src.name
    if spec.get("photo"): spec["photo"] = local(spec["photo"])
    for it in spec.get("items") or []:
        if it.get("file"): it["file"] = local(it["file"])
    if spec["type"] == "timeline":
        for e in spec["events"]: e["label"] = wrap(e["label"], 17 if len(spec["events"]) > 4 else 22)
    if spec["type"] == "person": spec["role"] = wrap(spec.get("role", ""), 34)
    if spec["type"] == "versus" and spec.get("note"): spec["note"] = wrap(spec["note"], 80)
    if spec["type"] == "pair":
        for it in spec["items"]: it["note"] = wrap(it.get("note", ""), 30)
    if spec["type"] == "stamp": spec["sub"] = wrap(spec.get("sub", ""), 26)
    if spec["type"] == "statement": spec["text"] = wrap(spec["text"], 34)
    for it in spec.get("items") or []:
        if it.get("files"): it["files"] = [local(f) for f in it["files"]]
    for n in (spec.get("nodes") or []) + (spec.get("sats") or []) + ([spec["center"]] if spec.get("center") else []):
        if n.get("file"): n["file"] = local(n["file"])
        n["sub"] = wrap(n.get("sub", ""), 24)
    if spec["type"] == "flow" and spec.get("note"): spec["note"] = wrap(spec["note"], 70)
    return spec


SYNC = ("callout", "logo", "lower_third", "chip", "tag")


def sync(sc, L, wd):
    """Entradas no instante em que a narracao diz o assunto (audio/words.json). Guarda o tempo original em *_base
    para poder recalcular; "sync": false fixa o tempo escrito no plano."""
    import words as Wd
    n = 0
    for i, s in enumerate(sc):
        ws = (wd.get(str(i + 1)) or {}).get("words") or []; ec = s.get("ec") or {}
        if not ws or not ec: continue
        items = ec.get("overlay") or []; chap = any(e["type"] == "chapter" for e in items)
        for e in items:
            if e["type"] not in SYNC or e.get("sync") is False: continue
            e.setdefault("start_base", e.get("start"))
            txt = " ".join(str(e.get(k) or "") for k in ("text", "label", "name")) + " " + \
                  " ".join(Path(f).stem.rsplit("-", 1)[0].replace("-", " ") for f in [e.get("file")] + list(e.get("files") or []) if f)
            t = Wd.when(ws, txt)
            e["start"] = e["start_base"] if t is None else round(min(max(t - 0.2, 3.6 if chap else 0.3), L[i] - 2.8), 2); n += t is not None
            if t is not None: e.pop("end", None)  # o fim e recalculado abaixo para nao sobrepor o proximo
        for typ in ("lower_third", "callout"):  # mesmo canto: um termina antes do seguinte comecar
            its = sorted((e for e in items if e["type"] == typ), key=lambda e: e.get("start") or 0)
            for a_, b_ in zip(its, its[1:]):
                b_["start"] = round(max(b_.get("start") or 0, (a_.get("start") or 0) + 2.8), 2)
                a_["end"] = round(min(a_.get("end") or 1e9, b_["start"] - 0.3), 2)
        f = ec.get("full")
        if f and f["type"] == "counter":
            t = Wd.when(ws, f"{f['value']:g}")
            if t is not None: f["t1"] = round(min(max(t + 0.35, 1.8), L[i] - 1.5), 2); n += 1  # termina de contar enquanto o numero e dito
    return n


def timing(f, ws, dur):
    """flow/relmap/stack/list: cada "say" (trecho da narracao) vira o instante em que e falado (audio/words.json).
    Quem tem "at" e nao tem "say" fica como esta (plano feito a mao); sem fala achada, ordem fixa."""
    import words as Wd
    hit = [0]
    def at(say, default, after=0.0):
        t = Wd.when(ws, say, after) if (say and ws) else None
        hit[0] += t is not None
        return round(min(max(t - 0.1 if t is not None else default, 0.2), max(0.2, dur - 2.0)), 2)
    def need(x): return "say" in x or "at" not in x
    T = f["type"]
    if T == "flow":
        for k, n in enumerate(f["nodes"]):
            if need(n): n["at"] = at(n.get("say"), 0.3 + 0.5 * k)
            if n.get("alert_say"): n["alert_at"] = at(n["alert_say"], dur * 0.75, n["at"])
        for e in f["edges"]:
            base = max(f["nodes"][e["from"]]["at"], f["nodes"][e["to"]]["at"]) + 0.6
            if need(e): e["at"] = max(at(e.get("say"), base), base)
            for key, d in (("stop", 0.6), ("alert", 0.75)):
                if e.get(key + "_say"): e[key] = max(at(e[key + "_say"], dur * d, e["at"]), e["at"] + 1.0)
        if f.get("note") and ("note_say" in f or "note_at" not in f): f["note_at"] = at(f.get("note_say"), max(3.0, dur * 0.7))
    elif T == "relmap":
        if need(f["center"]): f["center"]["at"] = at(f["center"].get("say"), 0.2)
        for k, n in enumerate(f["sats"]):
            if need(n): n["at"] = max(at(n.get("say"), 0.6 + 0.8 * k), f["center"]["at"])
            if n.get("alert_say"): n["alert_at"] = at(n["alert_say"], dur * 0.75, n["at"])
    elif T == "stack":
        for k, x in enumerate(f["tiers"]):
            if need(x): x["at"] = max(at(x.get("say"), 1.5 + 1.2 * k), 1.0 + 0.45 * k)  # a barra so enche depois do rotulo aparecer
        if f.get("highlight") is not None and ("highlight_say" in f or "highlight_at" not in f):
            f["highlight_at"] = at(f.get("highlight_say"), dur * 0.75)
    elif T == "list":
        prev = 0.0
        for k, x in enumerate(f["items"]):
            if need(x): x["at"] = at(x.get("say"), 1.0 + 1.6 * k, prev)
            prev = x["at"] + 0.3
        f.setdefault("label_at", 0.3)
    return hit[0]


def render_one(job):
    name, spec, wd, out, enc, preview = job
    jsx = wd / f"{name}.jsx"
    jsx.write_text("var D = " + json.dumps(spec, ensure_ascii=False) + ";\n" + PRELUDE + B[spec["type"] if spec["type"] in B else "overlay"],
                   encoding="utf-8")
    proj = wd / f"{name}.ecproj"
    r = subprocess.run([CLI, "script", jsx.name, "--empty", "--save-as", proj.name], cwd=wd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{name}: script falhou: {r.stdout[-600:]} {r.stderr[-600:]}")
    if preview:
        for t in preview:
            subprocess.run([CLI, "render-frame", "--project", proj.name, "--comp", "G", "--time", str(t), "--max-side", "960",
                            "--out", f"{name}_t{t}.png"] + (["--transparent"] if spec["type"] == "overlay" else []), cwd=wd, capture_output=True)
        return name, "preview"
    for _ in range(2):  # o EffectCraft as vezes falha sem motivo e passa na segunda vez (SVB cena 77)
        r = subprocess.run([CLI, "render", "--project", proj.name, "--comp", "G", "--out", str(out)] + enc, cwd=wd, capture_output=True, text=True)
        if not r.returncode and out.is_file(): break
    if r.returncode or not out.is_file():
        raise RuntimeError(f"{name}: render falhou: {r.stdout[-600:]} {r.stderr[-600:]}")
    return name, out.name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("--only", default=""); ap.add_argument("--kind", choices=["full", "overlay"])
    ap.add_argument("--preview", default="",
                    help="tempos (s) separados por virgula: so renderiza quadros PNG para conferir")
    a = ap.parse_args()
    if not Path(CLI).is_file():
        sys.exit(f"effectcraft-cli nao encontrado em {CLI} (defina EFFECTCRAFT_CLI)")
    pfile = ROOT / "projects" / f"{a.project}.json"; pdir = ROOT / "projects" / a.project
    pj = json.loads(pfile.read_text(encoding="utf-8")); sc = pj["scenes"]
    only = {int(x) for x in a.only.split(",") if x.strip()}
    preview = [float(x) for x in a.preview.split(",") if x.strip()]
    L = durations(pdir, len(sc))
    sys.path.insert(0, str(Path(__file__).resolve().parent)); import words as Wd
    wj = Wd.load(pdir)
    if wj: print(f"sincronia com a narracao: {sync(sc, L, wj)} entradas", flush=True)
    gd = pdir / "gfx"; wd = gd / "ec"; wd.mkdir(parents=True, exist_ok=True)
    jobs = []
    for i, s in enumerate(sc):
        ec = s.get("ec") or {}
        if only and i + 1 not in only: continue
        if ec.get("full") and a.kind != "overlay":
            if ec["full"]["type"] in ("flow", "relmap", "stack", "list"):
                timing(ec["full"], ((wj or {}).get(str(i + 1)) or {}).get("words") or [], L[i])
            spec = prep(dict(ec["full"], dur=L[i]), wd, pdir)
            jobs.append((f"full-{i+1:02d}", spec, wd, gd / f"ec-{i+1:02d}.mp4", ENC_FULL, preview))
        if ec.get("overlay") and a.kind != "full":
            spec = prep({"type": "overlay", "items": ec["overlay"], "dur": L[i]}, wd, pdir)
            jobs.append((f"ov-{i+1:02d}", spec, wd, gd / f"ecov-{i+1:02d}.mov", ENC_OV, preview))
    print(f"{len(jobs)} graficos para renderizar", flush=True)
    with ThreadPoolExecutor(3) as ex:
        for name, res in ex.map(render_one, jobs):
            print("ok", name, res, flush=True)
    if preview:
        return
    for i, s in enumerate(sc):  # tela cheia vira a midia da cena (guarda a original para poder voltar)
        f = gd / f"ec-{i+1:02d}.mp4"
        if (s.get("ec") or {}).get("full") and f.is_file():
            s.setdefault("orig_file", s.get("file")); s.update(file=f.relative_to(pdir).as_posix(), source="gfx", status="pronto")
    pfile.write_text(json.dumps(pj, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
