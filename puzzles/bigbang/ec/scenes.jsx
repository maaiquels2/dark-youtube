// Big Bang em 7 cenas (uma por bloco da narracao). WORDS/BLOCKS/DUR/VEND/CHUNKS/IMG vem do build_ec.py.
var W = 1080, H = 1920, CX = 540, CY = 960;
var comp = app.project.items.addComp("bigbang", W, H, 1, DUR, 30);
var B = BLOCKS;

function norm(s) { return s.toLowerCase().replace(/[^a-z0-9]/g, ""); }
function wt(w, after) {
  after = after || 0;
  for (var i = 0; i < WORDS.length; i++) if (WORDS[i].s >= after && norm(WORDS[i].w) == w) return WORDS[i].s;
  throw new Error("palavra nao encontrada: " + w);
}
function K(prop, keys) { for (var i = 0; i < keys.length; i++) prop.setValueAtTime(keys[i][0], keys[i][1]); return prop; }
function tr(l, n) { return l.property("Transform").property(n); }
function P(e, path) {
  var parts = path.split("/"), p = e;
  for (var i = 0; i < parts.length; i++) { p = p.property(parts[i]); if (!p) throw new Error("sem propriedade " + path); }
  return p;
}
function fx(l, name, vals) {
  var e = l.Effects.addProperty(name);
  if (!e) throw new Error("sem efeito " + name);
  for (var k in vals) {
    var v = vals[k], pr = P(e, k);
    if (typeof v == "string" && v.charAt(0) == "=") pr.expression = v.substr(1); else pr.setValue(v);
  }
  return e;
}
function span(l, a, b) { l.inPoint = Math.max(0, a); l.outPoint = Math.min(DUR, b); return l; }
function solid(name, col, a, b) { var l = comp.layers.addSolid(col, name, W, H, 1); return span(l, a, b); }
function fade(l, a, b, fi, fo, peak) {
  if (peak == null) peak = 100;
  K(tr(l, "Opacity"), [[a, 0], [a + fi, peak], [b - fo, peak], [b, 0]]);
}
function circle(l, cx, cy, r, f) {
  var m = l.Masks.addProperty("Mask"), s = new Shape(), k = r * 0.5523;
  s.vertices = [[cx - r, cy], [cx, cy - r], [cx + r, cy], [cx, cy + r]];
  s.inTangents = [[0, k], [-k, 0], [0, -k], [k, 0]];
  s.outTangents = [[0, -k], [k, 0], [0, k], [-k, 0]];
  s.closed = true;
  m.property("Mask Path").setValue(s);
  if (f) m.property("Mask Feather").setValue([f, f]);
  return m;
}
function oval(l, cx, cy, rx, ry, f) {
  var m = l.Masks.addProperty("Mask"), s = new Shape(), kx = rx * 0.5523, ky = ry * 0.5523;
  s.vertices = [[cx - rx, cy], [cx, cy - ry], [cx + rx, cy], [cx, cy + ry]];
  s.inTangents = [[0, ky], [-kx, 0], [0, -ky], [kx, 0]];
  s.outTangents = [[0, -ky], [kx, 0], [0, ky], [-kx, 0]];
  s.closed = true;
  m.property("Mask Path").setValue(s);
  if (f) m.property("Mask Feather").setValue([f, f]);
  return m;
}
function shape(name, a, b, size, fill, stroke, sw) {
  var s = comp.layers.addShape(); s.name = name;
  var gc = s.property("Contents").addProperty("ADBE Vector Group").property("Contents");
  gc.addProperty("ADBE Vector Shape - Ellipse").property("Size").setValue(size);
  if (stroke) { var st = gc.addProperty("ADBE Vector Graphic - Stroke"); st.property("Color").setValue(stroke); st.property("Stroke Width").setValue(sw || 4); }
  if (fill) gc.addProperty("ADBE Vector Graphic - Fill").property("Color").setValue(fill);
  tr(s, "Position").setValue([CX, CY]);
  return span(s, a, b);
}
function text(str, a, b, size, y, col, font, track) {
  var t = comp.layers.addText(str), sd = t.property("Source Text"), d = sd.value;
  d.font = font || "Anton"; d.fontSize = size; d.fillColor = col || [1, 1, 1];
  d.justification = ParagraphJustification.CENTER_JUSTIFY;
  if (track) d.tracking = track;
  d.applyStroke = true; d.strokeColor = [0, 0, 0]; d.strokeWidth = size < 60 ? 2 : Math.max(4, size * 0.07); d.strokeOverFill = false;
  sd.setValue(d);
  tr(t, "Position").setValue([CX, y]);
  return span(t, a, b);
}
function noise(name, a, b, o) {
  var l = solid(name, [0, 0, 0], a, b);
  fx(l, "Fractal Noise", { "Contrast": o.contrast || 120, "Brightness": o.bright || 0, "Complexity": o.cx || 6, "Evolution": "=time*" + (o.evo || 90) });
  fx(l, "Tint", { "Map Black To": o.dark, "Map White To": o.light });
  if (o.disp) fx(l, "Turbulent Displace", { "Amount": o.disp, "Size": 140, "Evolution": "=time*200" });
  if (o.add !== false) l.blendingMode = BlendingMode.ADD;
  return l;
}
// rajada/fluxo de particulas; o = {birth:[[t,v]..], life, vel, type, c1, c2, size, rx, ry, grav}
function particles(name, a, b, o) {
  var l = solid(name, [0, 0, 0], a, b); l.blendingMode = BlendingMode.ADD;
  var e = l.Effects.addProperty("CC Particle World");
  K(P(e, "Birth Rate"), o.birth);
  P(e, "Longevity (sec)").setValue(o.life || 3);
  P(e, "Physics/Velocity").setValue(o.vel == null ? 1 : o.vel);
  P(e, "Physics/Gravity").setValue(o.grav || 0);
  if (o.resist != null) P(e, "Physics/Resistance").setValue(o.resist);
  P(e, "Particle/Particle Type").setValue(o.type || 1);
  P(e, "Particle/Birth Color").setValue(o.c1 || [1, 1, 1]);
  P(e, "Particle/Death Color").setValue(o.c2 || o.c1 || [1, 1, 1]);
  if (o.size) { P(e, "Particle/Birth Size").setValue(o.size[0]); P(e, "Particle/Death Size").setValue(o.size[1]); }
  if (o.rx != null) { P(e, "Producer/Radius X").setValue(o.rx); P(e, "Producer/Radius Y").setValue(o.ry); P(e, "Producer/Radius Z").setValue(o.rz == null ? o.rx : o.rz); }
  if (o.seed != null) P(e, "Extras/Random Seed").setValue(o.seed);
  return l;
}
function grid(name, a, b, cell, col) {
  var l = solid(name, [0, 0, 0], a, b);
  fx(l, "Grid", { "Width": cell, "Border": 2.5, "Color": col || [0.35, 0.6, 1] });
  l.blendingMode = BlendingMode.ADD;
  return l;
}
function flash(t, peak, len, col) {
  var l = solid("flash", col || [1, 1, 1], t - 0.05, t + (len || 0.5));
  K(tr(l, "Opacity"), [[t - 0.05, 0], [t, peak], [t + (len || 0.5), 0]]);
  l.blendingMode = BlendingMode.ADD;
  return l;
}
function photo(file, a, b) {
  var f = app.project.importFile(new ImportOptions(new File(IMG + "/" + file)));
  var l = comp.layers.add(f); span(l, a, b);
  tr(l, "Position").setValue([CX, CY]);
  return l;
}
var HITS = [];  // momentos de tremida da camera

// fundo
solid("bg", [0, 0, 0.012], 0, DUR);

// ---------- 0: o Big Bang (expansao do proprio espaco) ----------
var tB = 0.8, s1 = B[1];
var tSpace = wt("itself") - 0.5;
var g0 = grid("space grid", tSpace - 0.3, s1 + 0.3, 90);
fade(g0, tSpace - 0.3, s1 + 0.3, 0.6, 0.4, 40);
K(tr(g0, "Scale"), [[tSpace - 0.3, [100, 100]], [s1 + 0.3, [260, 260]]]);
var gas0 = noise("gas", tB - 0.1, s1 + 0.3, { contrast: 160, bright: -30, evo: 120, dark: [0.02, 0, 0.08], light: [1, 0.45, 0.1], disp: 90 });
circle(gas0, CX, CY, 420, 260);
K(tr(gas0, "Scale"), [[tB, [5, 5]], [s1, [330, 330]]]);
fade(gas0, tB - 0.1, s1 + 0.3, 0.4, 0.5);
particles("burst", tB - 0.05, s1 + 0.3, { birth: [[tB - 0.05, 0], [tB, 14], [tB + 0.7, 1.5], [s1, 0.6]], life: 3.5, vel: 1.6, type: 1, c1: [1, 0.95, 0.75], c2: [1, 0.35, 0.05] });
var ring0 = shape("shockwave", tB, tB + 1.8, [200, 200], null, [1, 0.85, 0.6], 6);
K(tr(ring0, "Scale"), [[tB, [5, 5]], [tB + 1.8, [900, 900]]]);
K(tr(ring0, "Opacity"), [[tB, 100], [tB + 1.8, 0]]);
var core0 = solid("core", [1, 0.95, 0.85], 0, s1);
circle(core0, CX, CY, 60, 90); core0.blendingMode = BlendingMode.ADD;
K(tr(core0, "Scale"), [[0, [6, 6]], [tB - 0.15, [30, 30]], [tB + 0.1, [900, 900]], [tB + 1.8, [380, 380]]]);
K(tr(core0, "Opacity"), [[0, 100], [tB + 0.1, 100], [tB + 1.2, 18], [s1, 0]]);
HITS.push(tB);

// ---------- 1: 13,8 bilhoes de anos, menor que um atomo, quente e denso ----------
var s2 = B[2], tAtom = wt("smaller", s1) - 0.3, tHot = wt("hot", s1) - 0.3;
var sb1 = solid("time stars", [0, 0, 0], s1, tAtom + 0.6);
fx(sb1, "CC Star Burst", { "Speed": 1.2, "Size": 22 }); sb1.blendingMode = BlendingMode.ADD;
fade(sb1, s1, tAtom + 0.6, 0.5, 0.6, 85);
var y1 = text("13.8 BILLION", wt("thirteen", s1), tAtom, 170, 900, [1, 0.93, 0.8], "Anton", 20);
var y2 = text("YEARS AGO", wt("thirteen", s1), tAtom, 86, 1010, [1, 0.6, 0.25], "Anton", 300);
K(tr(y1, "Scale"), [[wt("thirteen", s1), [80, 80]], [wt("thirteen", s1) + 0.25, [104, 104]], [tAtom, [118, 118]]]);
K(tr(y2, "Scale"), [[wt("thirteen", s1), [80, 80]], [wt("thirteen", s1) + 0.25, [100, 100]], [tAtom, [112, 112]]]);
// atomo: tres orbitas, depois a camera mergulha no nucleo
var orbits = [];
for (var i = 0; i < 3; i++) {
  var o = shape("orbit" + i, tAtom, tHot + 0.5, [760, 250], null, [0.45, 0.8, 1], 5);
  tr(o, "Rotation").setValue(i * 60);
  K(tr(o, "Scale"), [[tAtom, [70, 70]], [tAtom + 0.4, [100, 100]], [tHot - 0.2, [110, 110]], [tHot + 0.5, [2600, 2600]]]);
  K(tr(o, "Opacity"), [[tAtom, 0], [tAtom + 0.3, 100], [tHot, 100], [tHot + 0.5, 0]]);
}
var nuc = shape("nucleus", tAtom, tHot + 0.5, [70, 70], [1, 0.85, 0.6]);
K(tr(nuc, "Scale"), [[tAtom, [0, 0]], [tAtom + 0.4, [100, 100]], [tHot - 0.2, [110, 110]], [tHot + 0.5, [1800, 1800]]]);
var hot = noise("hot dense", tHot, wt("stretched", s2) + 0.6, { contrast: 160, bright: -10, evo: 420, dark: [0.55, 0.06, 0], light: [1, 1, 0.92], disp: 45 });
circle(hot, CX, CY, 330, 120);
K(tr(hot, "Scale"), [[tHot, [10, 10]], [tHot + 0.5, [100, 100]], [s2, [125, 125]], [wt("stretched", s2), [140, 140]], [wt("stretched", s2) + 0.6, [1600, 1600]]]);
K(tr(hot, "Opacity"), [[tHot, 0], [tHot + 0.3, 100], [wt("stretched", s2) + 0.2, 100], [wt("stretched", s2) + 0.6, 0]]);
HITS.push(tHot + 0.4);

// ---------- 2: inflacao ----------
var s3 = B[3], tStr = wt("stretched", s2), tInf = wt("inflation", s2);
var tTr = wt("trillionth", s2);
var num = text("0.000 000 000 000 000 000 000 000 000 000 001", tTr, tStr, 32, 420, [0.75, 0.9, 1], "Inter", 0);
var sec = text("SECONDS", tTr + 0.4, tStr, 64, 510, [0.75, 0.9, 1], "Anton", 400);
fade(num, tTr, tStr, 0.3, 0.2); fade(sec, tTr + 0.4, tStr, 0.3, 0.2);
var g2 = grid("inflation grid", tStr - 0.1, s3 + 0.3, 36, [0.5, 0.75, 1]);
K(tr(g2, "Scale"), [[tStr - 0.1, [40, 40]], [tStr + 0.6, [120, 120]], [tStr + 1.2, [420, 420]], [tStr + 1.8, [1500, 1500]], [tStr + 2.4, [5200, 5200]]]);
K(tr(g2, "Opacity"), [[tStr - 0.1, 0], [tStr + 0.1, 70], [tStr + 2.4, 60], [tStr + 2.6, 0]]);
var g2b = grid("inflation grid 2", tStr + 2.2, s3 + 0.3, 36, [0.5, 0.75, 1]);
K(tr(g2b, "Scale"), [[tStr + 2.2, [30, 30]], [s3 + 0.3, [260, 260]]]);
fade(g2b, tStr + 2.2, s3 + 0.3, 0.4, 0.4, 45);
particles("streaks", tStr - 0.1, s3 + 0.3, { birth: [[tStr - 0.1, 0], [tStr, 9], [s3, 5]], life: 1.2, vel: 4.5, type: 1, c1: [0.85, 0.95, 1], c2: [0.3, 0.5, 1], seed: 7 });
var rb = solid("radial blur", [0, 0, 0], tStr, s3); rb.adjustmentLayer = true;
var rbe = fx(rb, "CC Radial Fast Blur", {});
K(P(rbe, "Amount"), [[tStr, 0], [tStr + 0.3, 70], [s3 - 0.5, 40], [s3, 0]]);
flash(tStr, 85, 0.6);
var inf = text("INFLATION", tInf, s3 + 0.2, 200, 1010, [0.65, 0.88, 1], "Anton", 60);
K(tr(inf, "Scale"), [[tInf, [150, 150]], [tInf + 0.2, [100, 100]], [s3 + 0.2, [92, 92]]]);
fade(inf, tInf, s3 + 0.2, 0.15, 0.3);
HITS.push(tStr);

// ---------- 3: os tres primeiros minutos, hidrogenio e helio ----------
var s4 = B[4], tFuse = wt("fuse", s3), tH = wt("hydrogen", s3), tHe = wt("helium", s3);
var pl3 = noise("plasma", s3 - 0.2, s4 + 0.3, { contrast: 110, bright: -25, evo: 140, dark: [0, 0, 0], light: [0.9, 0.35, 0.12] });
fade(pl3, s3 - 0.2, s4 + 0.3, 0.6, 0.6, 55);
particles("protons", s3, s4 + 0.3, { birth: [[s3, 0.9], [tFuse, 0.4]], life: 6, vel: 0.2, type: 2, c1: [1, 0.35, 0.3], size: [0.06, 0.06], rx: 0.6, ry: 1.0, seed: 3 });
particles("neutrons", s3, s4 + 0.3, { birth: [[s3, 0.9], [tFuse, 0.4]], life: 6, vel: 0.2, type: 2, c1: [0.65, 0.75, 0.9], size: [0.06, 0.06], rx: 0.6, ry: 1.0, seed: 11 });
var clk = text("0:00", s3 + 0.2, s4, 120, 560, [1, 0.9, 0.7], "Inter", 0);
clk.property("Source Text").expression =
  "var s=Math.min(180,Math.max(0,(time-" + (s3 + 0.2) + ")/" + (tFuse - s3 - 0.2) + "*180)); var m=Math.floor(s/60), r=Math.floor(s%60); m+':'+(r<10?'0':'')+r";
var clkL = text("FIRST THREE MINUTES", s3 + 0.2, s4, 44, 440, [1, 0.75, 0.5], "Inter", 300);
fade(clk, s3 + 0.2, s4, 0.3, 0.4); fade(clkL, s3 + 0.2, s4, 0.3, 0.4);
// helio: 2 protons + 2 neutrons colidem
var heX = 760, heY = 1080, from = [[-200, 300], [1280, 500], [-200, 1700], [1280, 1500]], to = [[-36, -33], [36, -33], [-36, 33], [36, 33]];
for (var i = 0; i < 4; i++) {
  var bcol = i % 3 == 0 ? [1, 0.32, 0.28] : [0.7, 0.78, 0.92];
  var bl = shape("he" + i, tFuse - 0.2, s4, [84, 84], bcol);
  K(tr(bl, "Position"), [[tFuse - 0.2, from[i]], [tFuse + 0.5, [heX + to[i][0], heY + to[i][1]]]]);
}
flash(tFuse + 0.5, 50, 0.4, [1, 0.8, 0.5]);
var hb = shape("hydrogen", tH - 0.1, s4, [84, 84], [1, 0.32, 0.28]);
tr(hb, "Position").setValue([320, heY]);
K(tr(hb, "Scale"), [[tH - 0.1, [0, 0]], [tH + 0.15, [130, 130]], [tH + 0.3, [100, 100]]]);
var lH = text("H", tH, s4, 150, 920, [1, 0.55, 0.45], "Anton", 0); tr(lH, "Position").setValue([320, 930]);
var lHe = text("He", tHe, s4, 150, 920, [0.75, 0.85, 1], "Anton", 0); tr(lHe, "Position").setValue([heX, 930]);
K(tr(lH, "Scale"), [[tH, [140, 140]], [tH + 0.15, [100, 100]]]);
K(tr(lHe, "Scale"), [[tHe, [140, 140]], [tHe + 0.15, [100, 100]]]);
HITS.push(tFuse + 0.5);

// ---------- 4: nevoeiro brilhante, a luz se liberta, radiacao cosmica de fundo ----------
var s5 = B[5], tEl = wt("electrons", s4), tL = wt("light", s4), tDet = wt("detect", s4), tC = wt("cosmic", s4);
var fog = noise("fog", s4 - 0.2, tL + 1.4, { contrast: 85, bright: 15, evo: 70, cx: 5, dark: [0.45, 0.12, 0.02], light: [1, 0.72, 0.38], add: false });
K(tr(fog, "Opacity"), [[s4 - 0.2, 0], [s4 + 0.5, 100], [tEl, 100], [tL, 70], [tL + 1.4, 0]]);
var yrs = text("380,000 YEARS", s4 + 0.4, tEl, 150, 980, [1, 0.95, 0.85], "Anton", 30);
fade(yrs, s4 + 0.4, tEl, 0.3, 0.3);
particles("electrons", tEl, tL + 0.6, { birth: [[tEl, 6], [tL, 2]], life: 2, vel: 0.35, type: 3, c1: [0.5, 0.8, 1], size: [0.05, 0.03], rx: 0.7, ry: 1.2, seed: 5 });
particles("free light", tL - 0.1, tDet + 0.5, { birth: [[tL - 0.1, 0], [tL, 7], [tL + 1, 2], [tDet, 0]], life: 1.6, vel: 3.2, type: 1, c1: [1, 0.97, 0.85], c2: [1, 0.75, 0.4], seed: 13 });
var lf = solid("flare", [0, 0, 0], tL - 0.1, tL + 2); lf.blendingMode = BlendingMode.ADD;
var lfe = fx(lf, "Lens Flare", { "Flare Center": [CX, CY] });
K(P(lfe, "Flare Brightness"), [[tL - 0.1, 0], [tL + 0.2, 80], [tL + 2, 0]]);
flash(tL, 25, 0.5, [1, 0.9, 0.7]);
var cmb = noise("cmb", tDet, s5 + 0.3, { contrast: 150, bright: 0, evo: 25, cx: 8, dark: [0, 0, 0], light: [1, 1, 1], add: false });
fx(cmb, "CC Toner", { "Tones": 3, "Highlights": [0.8, 0.08, 0.05], "Brights": [1, 0.55, 0.12], "Midtones": [0.95, 0.92, 0.65], "Darktones": [0.2, 0.6, 1], "Shadows": [0.02, 0.08, 0.45] });
oval(cmb, CX, CY, 490, 260, 4);
K(tr(cmb, "Scale"), [[tDet, [60, 60]], [tDet + 0.6, [100, 100]], [s5 + 0.3, [112, 112]]]);
fade(cmb, tDet, s5 + 0.3, 0.5, 0.4);
var cmbR = shape("cmb ring", tDet, s5 + 0.3, [990, 530], null, [1, 1, 1], 3);
K(tr(cmbR, "Scale"), [[tDet, [60, 60]], [tDet + 0.6, [100, 100]], [s5 + 0.3, [112, 112]]]);
fade(cmbR, tDet, s5 + 0.3, 0.5, 0.4, 60);
var cmbL = text("COSMIC MICROWAVE BACKGROUND", tC, s5 + 0.2, 40, 620, [0.85, 0.92, 1], "Inter", 40);
fade(cmbL, tC, s5 + 0.2, 0.3, 0.3);
HITS.push(tL);

// ---------- 5: gravidade, primeiras estrelas, galaxias nos filamentos ----------
var s6 = B[6], tS = wt("ignited", s5), tG = wt("galaxies", s5);
var clumps = noise("clumps", s5 - 0.2, s6 + 0.3, { contrast: 100, bright: -45, evo: 60, cx: 7, dark: [0, 0, 0.01], light: [0.5, 0.58, 1] });
K(P(clumps.Effects.property("Fractal Noise"), "Contrast"), [[s5, 100], [tS, 420]]);
K(tr(clumps, "Scale"), [[s5, [100, 100]], [s6 + 0.3, [135, 135]]]);
fade(clumps, s5 - 0.2, s6 + 0.3, 0.6, 0.6, 80);
particles("first stars", tS - 0.1, s6 + 0.3, { birth: [[tS - 0.1, 0], [tS, 8], [tS + 1.2, 2], [tS + 1.5, 0]], life: 12, vel: 0.02, type: 3, c1: [1, 0.97, 0.9], c2: [0.75, 0.85, 1], size: [0.05, 0.04], rx: 1.4, ry: 2.2, seed: 21 });
flash(tS, 45, 0.5, [0.85, 0.9, 1]);
var web = photo("06_web.jpg", tG - 0.3, s6 + 0.4); web.blendingMode = BlendingMode.SCREEN;
K(tr(web, "Scale"), [[tG - 0.3, [150, 150]], [s6 + 0.4, [128, 128]]]);
fade(web, tG - 0.3, s6 + 0.4, 0.9, 0.4, 90);

// ---------- 6: as galaxias se afastam; o universo ainda se expande ----------
var tAw = wt("away", s6), tEx = wt("expanding", s6);
var bgs = solid("receding stars", [0, 0, 0], s6 - 0.2, DUR);
fx(bgs, "CC Star Burst", { "Speed": -0.5, "Size": 18 }); bgs.blendingMode = BlendingMode.ADD;
fade(bgs, s6 - 0.2, DUR, 0.6, 0.8, 80);
var g6 = grid("expanding grid", s6, DUR, 120, [0.35, 0.55, 1]);
K(tr(g6, "Scale"), [[s6, [70, 70]], [DUR, [230, 230]]]);
fade(g6, s6, DUR, 0.8, 0.8, 30);
var gal = [];
for (var i = 0; i < 7; i++) {
  var ang = i / 7 * Math.PI * 2 + 0.35, r0 = 230, r1 = 900;
  var gl = photo("07_stars.jpg", s6 - 0.1, DUR); gl.blendingMode = BlendingMode.ADD;
  circle(gl, 432, 768, 210, 150);
  var p0 = [CX + Math.cos(ang) * r0, CY + Math.sin(ang) * r0 * 1.4], p1 = [CX + Math.cos(ang) * r1, CY + Math.sin(ang) * r1 * 1.4];
  K(tr(gl, "Position"), [[s6, p0], [DUR, p1]]);
  K(tr(gl, "Scale"), [[s6, [34, 34]], [DUR, [14, 14]]]);
  tr(gl, "Rotation").setValue(i * 47);
  var tn = fx(gl, "Tint", { "Map Black To": [0, 0, 0], "Map White To": [1, 0.45, 0.3] });
  K(P(tn, "Amount to Tint"), [[tAw, 0], [tAw + 2.5, 85]]);
  fade(gl, s6 - 0.1, DUR, 0.6, 0.8);
}
var us = shape("us", s6, DUR, [26, 26], [0.8, 0.9, 1]);
var usL = text("US", s6 + 0.4, DUR, 40, 1040, [0.8, 0.9, 1], "Inter", 300);
fade(usL, s6 + 0.4, DUR, 0.3, 0.6);
var fin1 = text("STILL", VEND - 0.4, DUR, 120, 860, [1, 1, 1], "Anton", 200);
var fin2 = text("EXPANDING", VEND - 0.2, DUR, 180, 1060, [1, 0.6, 0.35], "Anton", 40);
K(tr(fin1, "Scale"), [[VEND - 0.4, [130, 130]], [VEND - 0.2, [100, 100]], [DUR, [106, 106]]]);
K(tr(fin2, "Scale"), [[VEND - 0.2, [130, 130]], [VEND, [100, 100]], [DUR, [112, 112]]]);
fade(fin1, VEND - 0.4, DUR, 0.15, 0.5); fade(fin2, VEND - 0.2, DUR, 0.15, 0.5);

// cortes entre cenas
for (var i = 2; i <= 6; i++) if (i != 3) flash(B[i], 35, 0.35);

// ---------- acabamento: brilho, tremida, granulacao, vinheta ----------
var fin = solid("finish", [0, 0, 0], 0, DUR); fin.adjustmentLayer = true;
fx(fin, "Glow", { "Glow Threshold": 55, "Glow Radius": 90, "Glow Intensity": 1.1 });
var sh = "var h=" + JSON.stringify(HITS) + ", a=0; for (var i=0;i<h.length;i++){var d=time-h[i]; if(d>0&&d<1.1) a=Math.max(a,(1.1-d)*22);} ";
fx(fin, "Transform", { "Uniform Scale": true, "Scale Height": 104, "Position": "=" + sh + "value + [wiggle(28,a)[0]-value[0], wiggle(31,a)[1]-value[1]]" });
fx(fin, "Noise", { "Amount of Noise": 3 });
var vig = solid("vignette", [0, 0, 0], 0, DUR);
var vm = oval(vig, CX, CY, 760, 1150, 520); vm.inverted = true;
tr(vig, "Opacity").setValue(75);

// ---------- legendas (fora da area dos titulos) ----------
for (var i = 0; i < CHUNKS.length; i++) {
  var c = CHUNKS[i];
  var t = text(c.t, c.s, c.e, 78, 1560, [1, 1, 1], "Anton", 10);
  K(tr(t, "Scale"), [[c.s, [86, 86]], [c.s + 0.08, [100, 100]]]);
}
writeLn("ok layers=" + comp.numLayers);
