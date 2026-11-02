var PART_STARTS=[0];
var WORDS=[{"w": "That", "s": 0.25, "e": 0.5}, {"w": "local", "s": 0.5, "e": 0.85}, {"w": "number", "s": 0.85, "e": 1.238}, {"w": "calling", "s": 1.238, "e": 1.65}, {"w": "you?", "s": 1.65, "e": 2.0}, {"w": "It", "s": 2.0, "e": 2.15}, {"w": "might", "s": 2.15, "e": 2.35}, {"w": "not", "s": 2.35, "e": 2.575}, {"w": "be", "s": 2.575, "e": 2.725}, {"w": "local", "s": 2.725, "e": 3.075}, {"w": "at", "s": 3.075, "e": 3.2}, {"w": "all.", "s": 3.2, "e": 4.325}, {"w": "In", "s": 5.025, "e": 5.125}, {"w": "just", "s": 5.125, "e": 5.35}, {"w": "three", "s": 5.35, "e": 5.575}, {"w": "months,", "s": 5.575, "e": 5.975}, {"w": "one", "s": 5.975, "e": 6.175}, {"w": "operation", "s": 6.175, "e": 6.8}, {"w": "made", "s": 6.8, "e": 7.037}, {"w": "ninety-six", "s": 7.037, "e": 7.712}, {"w": "million", "s": 7.712, "e": 8.125}, {"w": "robocalls.", "s": 8.125, "e": 9.4}, {"w": "The", "s": 9.4, "e": 9.55}, {"w": "FCC", "s": 9.55, "e": 10.175}, {"w": "says", "s": 10.175, "e": 10.425}, {"w": "the", "s": 10.425, "e": 10.525}, {"w": "callers", "s": 10.525, "e": 10.962}, {"w": "faked", "s": 10.962, "e": 11.225}, {"w": "their", "s": 11.225, "e": 11.425}, {"w": "numbers,", "s": 11.425, "e": 12.075}, {"w": "so", "s": 12.075, "e": 12.188}, {"w": "they", "s": 12.188, "e": 12.325}, {"w": "looked", "s": 12.325, "e": 12.537}, {"w": "like", "s": 12.537, "e": 12.725}, {"w": "they", "s": 12.725, "e": 12.875}, {"w": "came", "s": 12.875, "e": 13.15}, {"w": "from", "s": 13.15, "e": 13.287}, {"w": "your", "s": 13.287, "e": 13.4}, {"w": "own", "s": 13.4, "e": 13.6}, {"w": "neighborhood.", "s": 13.6, "e": 14.925}, {"w": "The", "s": 15.625, "e": 15.725}, {"w": "trick", "s": 15.725, "e": 16.0}, {"w": "is", "s": 16.0, "e": 16.15}, {"w": "called", "s": 16.15, "e": 16.45}, {"w": "neighbor", "s": 16.45, "e": 16.837}, {"w": "spoofing.", "s": 16.837, "e": 17.7}, {"w": "The", "s": 17.7, "e": 17.837}, {"w": "fake", "s": 17.837, "e": 18.125}, {"w": "number", "s": 18.125, "e": 18.475}, {"w": "copies", "s": 18.475, "e": 18.9}, {"w": "the", "s": 18.9, "e": 19.037}, {"w": "first", "s": 19.037, "e": 19.387}, {"w": "six", "s": 19.387, "e": 19.712}, {"w": "digits", "s": 19.712, "e": 20.037}, {"w": "of", "s": 20.037, "e": 20.112}, {"w": "your", "s": 20.112, "e": 20.225}, {"w": "own.", "s": 20.225, "e": 21.35}, {"w": "Press", "s": 22.05, "e": 22.325}, {"w": "one,", "s": 22.325, "e": 22.65}, {"w": "and", "s": 22.65, "e": 22.762}, {"w": "you", "s": 22.762, "e": 22.875}, {"w": "reach", "s": 22.875, "e": 23.113}, {"w": "a", "s": 23.113, "e": 23.175}, {"w": "call", "s": 23.175, "e": 23.438}, {"w": "center", "s": 23.438, "e": 23.825}, {"w": "selling", "s": 23.825, "e": 24.15}, {"w": "vacation", "s": 24.15, "e": 24.725}, {"w": "packages,", "s": 24.725, "e": 25.575}, {"w": "using", "s": 25.575, "e": 25.9}, {"w": "names", "s": 25.9, "e": 26.238}, {"w": "like", "s": 26.238, "e": 26.45}, {"w": "TripAdvisor,", "s": 26.45, "e": 27.35}, {"w": "Expedia,", "s": 27.35, "e": 28.075}, {"w": "Marriott", "s": 28.075, "e": 28.55}, {"w": "and", "s": 28.55, "e": 28.675}, {"w": "Hilton.", "s": 28.675, "e": 29.613}, {"w": "Those", "s": 29.613, "e": 29.875}, {"w": "companies", "s": 29.875, "e": 30.413}, {"w": "never", "s": 30.413, "e": 30.675}, {"w": "made", "s": 30.675, "e": 30.863}, {"w": "the", "s": 30.863, "e": 30.962}, {"w": "calls.", "s": 30.962, "e": 32.225}, {"w": "And", "s": 32.925, "e": 33.075}, {"w": "here", "s": 33.075, "e": 33.3}, {"w": "is", "s": 33.3, "e": 33.45}, {"w": "the", "s": 33.45, "e": 33.588}, {"w": "twist.", "s": 33.588, "e": 34.225}, {"w": "The", "s": 34.225, "e": 34.35}, {"w": "real", "s": 34.35, "e": 34.663}, {"w": "owners", "s": 34.663, "e": 35.063}, {"w": "of", "s": 35.063, "e": 35.15}, {"w": "those", "s": 35.15, "e": 35.413}, {"w": "faked", "s": 35.413, "e": 35.75}, {"w": "numbers", "s": 35.75, "e": 36.15}, {"w": "started", "s": 36.15, "e": 36.525}, {"w": "getting", "s": 36.525, "e": 36.863}, {"w": "angry", "s": 36.863, "e": 37.225}, {"w": "calls", "s": 37.225, "e": 37.525}, {"w": "back,", "s": 37.525, "e": 38.1}, {"w": "from", "s": 38.1, "e": 38.3}, {"w": "strangers,", "s": 38.3, "e": 39.025}, {"w": "over", "s": 39.025, "e": 39.288}, {"w": "calls", "s": 39.288, "e": 39.675}, {"w": "they", "s": 39.675, "e": 39.825}, {"w": "never", "s": 39.825, "e": 40.125}, {"w": "made.", "s": 40.125, "e": 41.275}, {"w": "So", "s": 42.0, "e": 42.175}, {"w": "remember.", "s": 42.175, "e": 42.75}, {"w": "A", "s": 42.75, "e": 42.85}, {"w": "local", "s": 42.85, "e": 43.175}, {"w": "number", "s": 43.175, "e": 43.462}, {"w": "on", "s": 43.462, "e": 43.562}, {"w": "your", "s": 43.562, "e": 43.675}, {"w": "screen", "s": 43.675, "e": 44.025}, {"w": "proves", "s": 44.025, "e": 44.35}, {"w": "nothing.", "s": 44.35, "e": 44.925}, {"w": "Do", "s": 44.925, "e": 45.038}, {"w": "not", "s": 45.038, "e": 45.225}, {"w": "press", "s": 45.225, "e": 45.525}, {"w": "one.", "s": 45.525, "e": 45.925}, {"w": "Do", "s": 45.925, "e": 46.038}, {"w": "not", "s": 46.038, "e": 46.225}, {"w": "call", "s": 46.225, "e": 46.475}, {"w": "back.", "s": 46.475, "e": 46.85}, {"w": "Hang", "s": 46.85, "e": 47.125}, {"w": "up.", "s": 47.125, "e": 48.15}, {"w": "The", "s": 48.825, "e": 48.9}, {"w": "full", "s": 48.9, "e": 49.125}, {"w": "case,", "s": 49.125, "e": 49.488}, {"w": "the", "s": 49.488, "e": 49.575}, {"w": "record", "s": 49.575, "e": 49.962}, {"w": "fine,", "s": 49.962, "e": 50.337}, {"w": "and", "s": 50.337, "e": 50.438}, {"w": "the", "s": 50.438, "e": 50.525}, {"w": "law", "s": 50.525, "e": 50.75}, {"w": "it", "s": 50.75, "e": 50.913}, {"w": "changed,", "s": 50.913, "e": 51.625}, {"w": "is", "s": 51.625, "e": 51.738}, {"w": "on", "s": 51.738, "e": 51.863}, {"w": "The", "s": 51.863, "e": 51.95}, {"w": "Rule", "s": 51.95, "e": 52.263}, {"w": "Changed.", "s": 52.263, "e": 53.6}];
var BLOCKS=[0.0, 4.775, 15.375, 21.8, 32.675, 41.725, 48.6, 53.9];
var DUR=54.6;
var VEND=53.6;
var CHUNKS=[{"t": "THAT LOCAL NUMBER", "s": 0.25, "e": 1.238}, {"t": "CALLING YOU?", "s": 1.238, "e": 2.0}, {"t": "IT MIGHT NOT", "s": 2.0, "e": 2.575}, {"t": "BE LOCAL AT", "s": 2.575, "e": 3.2}, {"t": "ALL.", "s": 3.2, "e": 4.575}, {"t": "IN JUST THREE", "s": 5.025, "e": 5.575}, {"t": "MONTHS,", "s": 5.575, "e": 5.975}, {"t": "ONE OPERATION MADE", "s": 5.975, "e": 7.037}, {"t": "NINETY-SIX MILLION ROBOCALLS.", "s": 7.037, "e": 9.4}, {"t": "THE FCC SAYS", "s": 9.4, "e": 10.425}, {"t": "THE CALLERS FAKED", "s": 10.425, "e": 11.225}, {"t": "THEIR NUMBERS,", "s": 11.225, "e": 12.075}, {"t": "SO THEY LOOKED", "s": 12.075, "e": 12.537}, {"t": "LIKE THEY CAME", "s": 12.537, "e": 13.15}, {"t": "FROM YOUR OWN", "s": 13.15, "e": 13.6}, {"t": "NEIGHBORHOOD.", "s": 13.6, "e": 15.175}, {"t": "THE TRICK IS", "s": 15.625, "e": 16.15}, {"t": "CALLED NEIGHBOR SPOOFING.", "s": 16.15, "e": 17.7}, {"t": "THE FAKE NUMBER", "s": 17.7, "e": 18.475}, {"t": "COPIES THE FIRST", "s": 18.475, "e": 19.387}, {"t": "SIX DIGITS OF", "s": 19.387, "e": 20.112}, {"t": "YOUR OWN.", "s": 20.112, "e": 21.6}, {"t": "PRESS ONE,", "s": 22.05, "e": 22.65}, {"t": "AND YOU REACH", "s": 22.65, "e": 23.113}, {"t": "A CALL CENTER", "s": 23.113, "e": 23.825}, {"t": "SELLING VACATION PACKAGES,", "s": 23.825, "e": 25.575}, {"t": "USING NAMES LIKE", "s": 25.575, "e": 26.45}, {"t": "TRIPADVISOR,", "s": 26.45, "e": 27.35}, {"t": "EXPEDIA,", "s": 27.35, "e": 28.075}, {"t": "MARRIOTT AND HILTON.", "s": 28.075, "e": 29.613}, {"t": "THOSE COMPANIES NEVER", "s": 29.613, "e": 30.675}, {"t": "MADE THE CALLS.", "s": 30.675, "e": 32.475}, {"t": "AND HERE IS", "s": 32.925, "e": 33.45}, {"t": "THE TWIST.", "s": 33.45, "e": 34.225}, {"t": "THE REAL OWNERS", "s": 34.225, "e": 35.063}, {"t": "OF THOSE FAKED", "s": 35.063, "e": 35.75}, {"t": "NUMBERS STARTED GETTING", "s": 35.75, "e": 36.863}, {"t": "ANGRY CALLS BACK,", "s": 36.863, "e": 38.1}, {"t": "FROM STRANGERS,", "s": 38.1, "e": 39.025}, {"t": "OVER CALLS THEY", "s": 39.025, "e": 39.825}, {"t": "NEVER MADE.", "s": 39.825, "e": 41.525}, {"t": "SO REMEMBER.", "s": 42.0, "e": 42.75}, {"t": "A LOCAL NUMBER", "s": 42.75, "e": 43.462}, {"t": "ON YOUR SCREEN", "s": 43.462, "e": 44.025}, {"t": "PROVES NOTHING.", "s": 44.025, "e": 44.925}, {"t": "DO NOT PRESS", "s": 44.925, "e": 45.525}, {"t": "ONE.", "s": 45.525, "e": 45.925}, {"t": "DO NOT CALL", "s": 45.925, "e": 46.475}, {"t": "BACK.", "s": 46.475, "e": 46.85}, {"t": "HANG UP.", "s": 46.85, "e": 48.4}, {"t": "THE FULL CASE,", "s": 48.825, "e": 49.488}, {"t": "THE RECORD FINE,", "s": 49.488, "e": 50.337}, {"t": "AND THE LAW", "s": 50.337, "e": 50.75}, {"t": "IT CHANGED,", "s": 50.75, "e": 51.625}, {"t": "IS ON THE", "s": 51.625, "e": 51.95}, {"t": "RULE CHANGED.", "s": 51.95, "e": 53.85}];
var IMG="C:/Users/Admin/Documents/Codex/2026-09-10/Dark YouTube/scamlaw/ep01_shorts/s1_local_number/assets/img";
var SPEC={"theme": "rulechanged", "format": "vertical", "comp": "main", "out": "s1_local_number", "music": "library/music/incompetech/interloper.mp3", "music_gain": 0.14, "lufs": -14, "tail": 1.0, "captions": true, "blocks": [{"act": "scam", "scenes": [{"t": "organ_focus", "image": "phone_screen.jpg", "screen": false, "photo": true, "zoom": [100, 108], "illustration": true}, {"t": "impact_title", "at": "start", "fade": [0.15, 0.25], "lines": [{"text": "THAT LOCAL NUMBER?", "size": 104, "y": 860, "color": [1, 0.96, 0.9], "font": "Anton"}]}, {"t": "impact_title", "at": "not", "fade": [0.15, 0.25], "lines": [{"text": "MIGHT BE FAKE", "size": 104, "y": 990, "color": [0.82, 0.25, 0.18], "font": "Anton"}]}]}, {"act": "scam", "scenes": [{"t": "fact_card", "big": "96 MILLION", "size": 150, "at": "months", "image": "stack_phones.jpg", "text": "robocalls in three months, Oct to Dec 2016", "source": "Source: FCC order FCC 18-58", "until": "callers-0.1"}, {"t": "organ_focus", "image": "city_night.jpg", "screen": false, "photo": true, "zoom": [100, 108], "illustration": true, "at": "callers-0.2"}, {"t": "impact_title", "at": "faked", "fade": [0.15, 0.25], "lines": [{"text": "FAKED TO LOOK LOCAL", "size": 96, "y": 900, "color": [1, 0.96, 0.9], "font": "Anton"}]}]}, {"act": "scam", "scenes": [{"t": "fact_card", "big": "SAME 6 DIGITS", "size": 120, "at": "start", "image": "phone_kitchen.jpg", "text": "Neighbor spoofing copies the first six digits of your own number", "source": "Source: FCC order FCC 18-58"}]}, {"act": "scam", "scenes": [{"t": "organ_focus", "image": "callcenter.jpg", "screen": false, "photo": true, "zoom": [100, 108], "illustration": true, "label": {"text": "PRESS 1", "at": 0.3}, "until": "tripadvisor-0.2"}, {"t": "impact_title", "at": "press", "fade": [0.15, 0.25], "lines": [{"text": "PRESS 1", "size": 170, "y": 900, "color": [1, 0.96, 0.9], "font": "Anton"}], "until": "tripadvisor-0.3"}, {"t": "organ_focus", "image": "l_brands.jpg", "screen": false, "photo": true, "zoom": [100, 108], "illustration": false, "label": {"text": "NAMES USED WITHOUT PERMISSION", "at": 0.3}, "at": "tripadvisor-0.3"}]}, {"act": "scam", "scenes": [{"t": "organ_focus", "image": "angry_phone.jpg", "screen": false, "photo": true, "zoom": [100, 108], "illustration": true}, {"t": "impact_title", "at": "twist", "fade": [0.15, 0.25], "lines": [{"text": "THE TWIST", "size": 150, "y": 900, "color": [1, 0.96, 0.9], "font": "Anton"}], "until": "angry-0.2"}, {"t": "impact_title", "at": "angry", "fade": [0.15, 0.25], "lines": [{"text": "ANGRY CALLS BACK", "size": 96, "y": 900, "color": [1, 0.96, 0.9], "font": "Anton"}]}]}, {"act": "rule", "scenes": [{"t": "organ_focus", "image": "hangup.jpg", "screen": false, "photo": true, "zoom": [100, 108], "illustration": true}, {"t": "impact_title", "at": "local", "fade": [0.15, 0.25], "lines": [{"text": "A LOCAL NUMBER", "size": 110, "y": 820, "color": [1, 0.96, 0.9], "font": "Anton"}]}, {"t": "impact_title", "at": "proves", "fade": [0.15, 0.25], "lines": [{"text": "PROVES NOTHING", "size": 110, "y": 950, "color": [0.82, 0.25, 0.18], "font": "Anton"}]}, {"t": "impact_title", "at": "hang", "fade": [0.15, 0.25], "lines": [{"text": "HANG UP.", "size": 130, "y": 1150, "color": [1, 0.96, 0.9], "font": "Anton"}]}]}, {"act": "case", "scenes": [{"t": "web_clip", "image": "fcc_final_2018.png", "site": "FCC.GOV", "date": "MAY 10, 2018", "source": "Source: FCC order FCC 18-58", "marks": [{"box": [395, 443, 1871, 230], "at": "record"}], "until": "is-0.1"}, {"t": "impact_title", "at": "is", "fade": [0.15, 0.25], "lines": [{"text": "FULL CASE", "size": 150, "y": 900, "color": [1, 0.96, 0.9], "font": "Anton"}], "until": "dur"}, {"t": "impact_title", "at": "is+0.15", "fade": [0.15, 0.25], "lines": [{"text": "ON THE RULE CHANGED", "size": 66, "y": 1010, "color": [0.82, 0.25, 0.18], "font": "Anton"}], "until": "dur"}]}]};
var CLIPS={"fcc_final_2018.png": [395, 443, 1871, 230]};
// ec_lib: biblioteca de cenas para o EffectCraft (modelo de objetos do After Effects).
// O build.py injeta antes deste arquivo: WORDS, BLOCKS, DUR, VEND, CHUNKS, IMG, SPEC; e chama buildVideo() no fim.
// Tempos: todo parametro de tempo aceita "palavra", "palavra+0.3", "palavra-0.5", "start", "end", "vend", "dur"
// ou um numero (segundos depois do inicio do bloco). A palavra e procurada a partir do inicio do bloco.
// SPEC.format: "vertical" (padrao, 1080x1920) ou "horizontal" (1920x1080). No vertical todo numero abaixo e o de antes.
var HZ = SPEC.format == "horizontal";
var W = HZ ? 1920 : 1080, H = HZ ? 1080 : 1920, CX = W / 2, CY = H / 2;
var PS = 1080 / W;  // particulas: o efeito mede em larguras da comp; os modelos falam em unidades de 1080 px
var CAP_Y = HZ ? 1012 : 1560, CAP_SIZE = HZ ? 50 : 78;  // legenda (linha de base, tamanho)
var INFO_X = 1360, PANEL_X = 560;  // horizontal: coluna de rotulos/medidores (direita) e centro da imagem (esquerda)
function vh(v, h) { return HZ ? h : v; }  // valor do vertical ou do horizontal
var comp, HITS = [], EVENTS = [], IMPORTS = {};

// ---------------- auxiliares ----------------
function norm(s) { return String(s).toLowerCase().replace(/[^a-z0-9]/g, ""); }
function wt(w, after) {
  after = after || 0;
  for (var i = 0; i < WORDS.length; i++) if (WORDS[i].s >= after && norm(WORDS[i].w) == w) return WORDS[i].s;
  throw new Error("palavra nao encontrada: " + w + " (depois de " + after + "s)");
}
// resolve um tempo do JSON; sc = cena ({s, e} = inicio/fim do bloco)
function T(sc, v, def) {
  if (v == null) v = def;
  if (v == null) return null;
  if (typeof v == "number") return sc.s + v;
  var m = String(v).match(/^([^+\-]+)([+\-][0-9.]+)?$/);
  if (!m) throw new Error("tempo invalido: " + v);
  var k = norm(m[1]), off = m[2] ? parseFloat(m[2]) : 0, base;
  if (k == "start") base = sc.s; else if (k == "end") base = sc.e;
  else if (k == "vend") base = VEND; else if (k == "dur") base = DUR;
  else base = wt(k, sc.s);
  return base + off;
}
function opt(o, k, d) { return o && o[k] != null ? o[k] : d; }
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
function ovalPath(cx, cy, rx, ry) {
  var s = new Shape(), kx = rx * 0.5523, ky = ry * 0.5523;
  s.vertices = [[cx - rx, cy], [cx, cy - ry], [cx + rx, cy], [cx, cy + ry]];
  s.inTangents = [[0, ky], [-kx, 0], [0, -ky], [kx, 0]];
  s.outTangents = [[0, -ky], [kx, 0], [0, ky], [-kx, 0]];
  s.closed = true;
  return s;
}
function oval(l, cx, cy, rx, ry, f) {
  var m = l.Masks.addProperty("Mask");
  m.property("Mask Path").setValue(ovalPath(cx, cy, rx, ry));
  if (f) m.property("Mask Feather").setValue([f, f]);
  return m;
}
function circle(l, cx, cy, r, f) { return oval(l, cx, cy, r, r, f); }
// elipse vetorial (anel se stroke, bola se fill), centrada na tela
function shape(name, a, b, size, fill, stroke, sw) {
  var s = comp.layers.addShape(); s.name = name;
  var gc = s.property("Contents").addProperty("ADBE Vector Group").property("Contents");
  gc.addProperty("ADBE Vector Shape - Ellipse").property("Size").setValue(size);
  if (stroke) { var st = gc.addProperty("ADBE Vector Graphic - Stroke"); st.property("Color").setValue(stroke); st.property("Stroke Width").setValue(sw || 4); }
  if (fill) gc.addProperty("ADBE Vector Graphic - Fill").property("Color").setValue(fill);
  tr(s, "Position").setValue([CX, CY]);
  return span(s, a, b);
}
// texto centralizado; abaixo de 60 px o contorno fica fino (2), senao borra
function text(str, a, b, size, y, col, font, track) {
  var t = comp.layers.addText(str), sd = t.property("Source Text"), d = sd.value;
  d.font = font || "Anton"; d.fontSize = size; d.fillColor = pal(col || [1, 1, 1]);
  d.justification = ParagraphJustification.CENTER_JUSTIFY;
  if (track) d.tracking = track;
  d.applyStroke = true; d.strokeColor = [0, 0, 0]; d.strokeWidth = size < 60 ? 2 : Math.max(4, size * 0.07); d.strokeOverFill = false;
  sd.setValue(d);
  tr(t, "Position").setValue([CX, y]);
  return span(t, a, b);
}
// fumaca/gas animado: o = {contrast, bright, cx, evo, dark, light, disp, add}
function noise(name, a, b, o) {
  var l = solid(name, [0, 0, 0], a, b);
  fx(l, "Fractal Noise", { "Contrast": o.contrast || 120, "Brightness": o.bright || 0, "Complexity": o.cx || 6, "Evolution": "=time*" + (o.evo || 90) });
  fx(l, "Tint", { "Map Black To": o.dark, "Map White To": o.light });
  if (o.disp) fx(l, "Turbulent Displace", { "Amount": o.disp, "Size": 140, "Evolution": "=time*200" });
  if (o.add !== false) l.blendingMode = BlendingMode.ADD;
  return l;
}
// CC Particle World; o = {birth:[[t,v]..], life, vel, type(1 riscos, 2 bolas, 3 estrelas), c1, c2, size:[ini,fim], rx, ry, rz, grav, resist, seed}
function particles(name, a, b, o) {
  var l = solid(name, [0, 0, 0], a, b); l.blendingMode = BlendingMode.ADD;
  var e = l.Effects.addProperty("CC Particle World");
  K(P(e, "Birth Rate"), o.birth);
  P(e, "Longevity (sec)").setValue(o.life || 3);
  P(e, "Physics/Velocity").setValue((o.vel == null ? 1 : o.vel) * PS);
  P(e, "Physics/Gravity").setValue((o.grav || 0) * PS);
  if (o.resist != null) P(e, "Physics/Resistance").setValue(o.resist);
  P(e, "Particle/Particle Type").setValue(o.type || 1);
  P(e, "Particle/Birth Color").setValue(o.c1 || [1, 1, 1]);
  P(e, "Particle/Death Color").setValue(o.c2 || o.c1 || [1, 1, 1]);
  if (o.size) { P(e, "Particle/Birth Size").setValue(o.size[0] * PS); P(e, "Particle/Death Size").setValue(o.size[1] * PS); }
  if (o.rx != null) { P(e, "Producer/Radius X").setValue(o.rx * PS); P(e, "Producer/Radius Y").setValue(o.ry * PS); P(e, "Producer/Radius Z").setValue((o.rz == null ? o.rx : o.rz) * PS); }
  if (o.seed != null) P(e, "Extras/Random Seed").setValue(o.seed);
  // px/py: emissor em unidades de 1080 px a partir do centro: px=(x-CX)/1080, py=(y-CY)/1080; gv = direcao da gravidade
  if (o.px != null) { P(e, "Producer/Position X").setValue(o.px * PS); P(e, "Producer/Position Y").setValue(o.py * PS); }
  if (o.gv) { P(e, "Physics/Gravity Vector/Gravity X").setValue(o.gv[0]); P(e, "Physics/Gravity Vector/Gravity Y").setValue(o.gv[1]); P(e, "Physics/Gravity Vector/Gravity Z").setValue(0); }
  return l;
}
function grid(name, a, b, cell, col) {
  var l = solid(name, [0, 0, 0], a, b);
  fx(l, "Grid", { "Width": cell, "Border": 2.5, "Color": col || [0.35, 0.6, 1] });
  l.blendingMode = BlendingMode.ADD;
  return l;
}
// clarao; somar varios (flare + flash + nevoa) estoura em branco: pico 25-35 nos cortes
function flash(t, peak, len, col) {
  var l = solid("flash", col || [1, 1, 1], t - 0.05, t + (len || 0.5));
  K(tr(l, "Opacity"), [[t - 0.05, 0], [t, peak], [t + (len || 0.5), 0]]);
  l.blendingMode = BlendingMode.ADD;
  return l;
}
function photo(file, a, b) {
  // importa cada arquivo uma vez so (um longo usa a mesma imagem dezenas de vezes)
  var f = (HZ && IMPORTS[file]) || (IMPORTS[file] = app.project.importFile(new ImportOptions(new File(IMG + "/" + file))));
  var l = comp.layers.add(f); span(l, a, b);
  tr(l, "Position").setValue([CX, CY]);
  return l;
}
// efeito sonoro ligado a um evento visual: k = boom | whoosh | rise | thud | chime
function sfx(t, k, g, extra) { var e = { t: t, k: k, g: g }; for (var x in extra) e[x] = extra[x]; EVENTS.push(e); }

// ---------------- modelos de cena ----------------
// Cada modelo recebe sc = {s, e, ...parametros do JSON}. "fim" padrao = fim do bloco + 0.3 (sobreposicao suave).
var TPL = {};

// explosao: nucleo brilhante que estoura, onda de choque, gas e faiscas; grade opcional (espaco que se expande)
TPL.bang = function (sc) {
  var tB = T(sc, sc.at, 0.8), end = T(sc, sc.until, "end+0.3"), tG = T(sc, sc.grid_at, null);
  if (tG != null) {
    var g0 = grid("space grid", tG - 0.3, end, opt(sc, "grid_cell", 90), sc.grid_color);
    fade(g0, tG - 0.3, end, 0.6, 0.4, 40);
    K(tr(g0, "Scale"), [[tG - 0.3, [100, 100]], [end, [260, 260]]]);
  }
  var gas = noise("gas", tB - 0.1, end, { contrast: 160, bright: -30, evo: 120, dark: opt(sc, "gas_dark", [0.02, 0, 0.08]), light: opt(sc, "gas_light", [1, 0.45, 0.1]), disp: 90 });
  circle(gas, CX, CY, 420, 260);
  K(tr(gas, "Scale"), [[tB, [5, 5]], [end - 0.3, [330, 330]]]);
  fade(gas, tB - 0.1, end, 0.4, 0.5);
  particles("burst", tB - 0.05, end, { birth: [[tB - 0.05, 0], [tB, 14], [tB + 0.7, 1.5], [end - 0.3, 0.6]], life: 3.5, vel: 1.6, type: 1, c1: opt(sc, "spark", [1, 0.95, 0.75]), c2: opt(sc, "spark_end", [1, 0.35, 0.05]) });
  var ring = shape("shockwave", tB, tB + 1.8, [200, 200], null, opt(sc, "ring", [1, 0.85, 0.6]), 6);
  K(tr(ring, "Scale"), [[tB, [5, 5]], [tB + 1.8, [900, 900]]]);
  K(tr(ring, "Opacity"), [[tB, 100], [tB + 1.8, 0]]);
  var core = solid("core", opt(sc, "core", [1, 0.95, 0.85]), sc.s, end - 0.3);
  circle(core, CX, CY, 60, 90); core.blendingMode = BlendingMode.ADD;
  K(tr(core, "Scale"), [[sc.s, [6, 6]], [tB - 0.15, [30, 30]], [tB + 0.1, [900, 900]], [tB + 1.8, [380, 380]]]);
  K(tr(core, "Opacity"), [[sc.s, 100], [tB + 0.1, 100], [tB + 1.2, 18], [end - 0.3, 0]]);
  HITS.push(tB);
  sfx(tB - 0.05, "boom", 1.0, { d: 3.0 }); sfx(tB - 0.8, "rise", 0.5, { d: 0.85 });
};

// fundo de estrelas passando (CC Star Burst); speed negativo = afastando
TPL.starfield = function (sc) {
  var a = T(sc, sc.from, "start"), b = T(sc, sc.until, "end+0.3");
  var l = solid("stars", [0, 0, 0], a, b);
  fx(l, "CC Star Burst", { "Speed": opt(sc, "speed", 1.2), "Size": opt(sc, "size", 22) }); l.blendingMode = BlendingMode.ADD;
  var f = opt(sc, "fade", [0.5, 0.6]);
  fade(l, a, b, f[0], f[1], opt(sc, "peak", 85));
};

// titulo de impacto: 1+ linhas que aparecem com "pop" de escala
// lines: [{text, size, y, color, font, track, delay, scale:[inicio, pico, fim]}]; fade: [entrada, saida] ou null (corte seco)
TPL.impact_title = function (sc) {
  var a = T(sc, sc.at, "start"), b = T(sc, sc.until, "end"), pop = opt(sc, "pop", 0.2), f = sc.fade;
  for (var i = 0; i < sc.lines.length; i++) {
    var L = sc.lines[i], la = a + (L.delay || 0);
    var t = text(L.text, la, b, L.size || 150, L.y || CY, L.color || [1, 1, 1], L.font || "Anton", L.track || 0);
    if (L.x != null) tr(t, "Position").setValue([L.x, L.y || CY]);
    // horizontal: linha larga demais encolhe (o pico da escala tambem conta)
    var fit = 1;
    if (HZ) { var tw = t.sourceRectAtTime(la + 0.01, false).width * (L.scale ? Math.max(L.scale[1], L.scale[2]) / 100 : 1); if (tw > W - 160) fit = (W - 160) / tw; }
    if (L.scale) K(tr(t, "Scale"), [[la, [L.scale[0] * fit, L.scale[0] * fit]], [la + pop, [L.scale[1] * fit, L.scale[1] * fit]], [b, [L.scale[2] * fit, L.scale[2] * fit]]]);
    else if (fit < 1) tr(t, "Scale").setValue([fit * 100, fit * 100]);
    if (f) fade(t, la, b, f[0], f[1]);
  }
  if (sc.hit) HITS.push(a);
  if (sc.sfx) sfx(a + (sc.sfx.dt || 0), sc.sfx.k, sc.sfx.g || 0.7, sc.sfx);
};

// objeto (atomo) aparece, camera mergulha no nucleo, que vira uma bola quente que estoura em "until"
TPL.dive_into = function (sc) {
  var a = T(sc, sc.at, "start"), hot = T(sc, sc.hot), u = T(sc, sc.until, "end");
  var oc = opt(sc, "orbit", [0.45, 0.8, 1]), n = opt(sc, "orbits", 3);
  for (var i = 0; i < n; i++) {
    var o = shape("orbit" + i, a, hot + 0.5, [760, 250], null, oc, 5);
    tr(o, "Rotation").setValue(i * 180 / n);
    K(tr(o, "Scale"), [[a, [70, 70]], [a + 0.4, [100, 100]], [hot - 0.2, [110, 110]], [hot + 0.5, [2600, 2600]]]);
    K(tr(o, "Opacity"), [[a, 0], [a + 0.3, 100], [hot, 100], [hot + 0.5, 0]]);
  }
  var nuc = shape("nucleus", a, hot + 0.5, [70, 70], opt(sc, "nucleus", [1, 0.85, 0.6]));
  K(tr(nuc, "Scale"), [[a, [0, 0]], [a + 0.4, [100, 100]], [hot - 0.2, [110, 110]], [hot + 0.5, [1800, 1800]]]);
  var h = noise("hot dense", hot, u + 0.6, { contrast: 160, bright: -10, evo: 420, dark: opt(sc, "hot_dark", [0.55, 0.06, 0]), light: opt(sc, "hot_light", [1, 1, 0.92]), disp: 45 });
  circle(h, CX, CY, 330, 120);
  var ks = [[hot, [10, 10]], [hot + 0.5, [100, 100]]];
  if (sc.e > hot + 0.5 && sc.e < u) ks.push([sc.e, [125, 125]]);
  ks.push([u, [140, 140]], [u + 0.6, [1600, 1600]]);
  K(tr(h, "Scale"), ks);
  K(tr(h, "Opacity"), [[hot, 0], [hot + 0.3, 100], [u + 0.2, 100], [u + 0.6, 0]]);
  HITS.push(hot + 0.4);
  sfx(hot + 0.2, "thud", 0.6);
};

// grade que explode para fora (inflacao/expansao subita) com riscos de luz, desfoque radial e clarao
TPL.grid_expand = function (sc) {
  var t = T(sc, sc.at), end = T(sc, sc.until, "end+0.3"), cell = opt(sc, "cell", 36), col = opt(sc, "color", [0.5, 0.75, 1]);
  var g = grid("burst grid", t - 0.1, end, cell, col);
  K(tr(g, "Scale"), [[t - 0.1, [40, 40]], [t + 0.6, [120, 120]], [t + 1.2, [420, 420]], [t + 1.8, [1500, 1500]], [t + 2.4, [5200, 5200]]]);
  K(tr(g, "Opacity"), [[t - 0.1, 0], [t + 0.1, 70], [t + 2.4, 60], [t + 2.6, 0]]);
  var g2 = grid("settle grid", t + 2.2, end, cell, col);
  K(tr(g2, "Scale"), [[t + 2.2, [30, 30]], [end, [260, 260]]]);
  fade(g2, t + 2.2, end, 0.4, 0.4, 45);
  particles("streaks", t - 0.1, end, { birth: [[t - 0.1, 0], [t, 9], [end - 0.3, 5]], life: 1.2, vel: 4.5, type: 1, c1: opt(sc, "streak", [0.85, 0.95, 1]), c2: opt(sc, "streak_end", [0.3, 0.5, 1]), seed: 7 });
  var rb = solid("radial blur", [0, 0, 0], t, end - 0.3); rb.adjustmentLayer = true;
  K(P(fx(rb, "CC Radial Fast Blur", {}), "Amount"), [[t, 0], [t + 0.3, 70], [end - 0.8, 40], [end - 0.3, 0]]);
  flash(t, opt(sc, "flash", 85), 0.6);
  HITS.push(t);
  sfx(t - 1.0, "rise", 0.9, { d: 1.1 }); sfx(t, "boom", 0.6, { d: 2.2 });
};

// relogio/numero que corre de 0 ate "to" entre "at" e "reach"; format "clock" (m:ss) ou "number" (1,234)
TPL.counter = function (sc) {
  var a = T(sc, sc.at, 0.2), r = T(sc, sc.reach), b = T(sc, sc.until, "end"), to = opt(sc, "to", 180);
  var y = opt(sc, "y", vh(560, 330)), col = opt(sc, "color", [1, 0.9, 0.7]);
  var c = text("0", a, b, opt(sc, "size", 120), y, col, "Inter", 0);
  var v = "var s=Math.min(" + to + ",Math.max(0,(time-" + a + ")/" + (r - a) + "*" + to + ")); ";
  c.property("Source Text").expression = v + (opt(sc, "format", "clock") == "clock"
    ? "var m=Math.floor(s/60), r=Math.floor(s%60); m+':'+(r<10?'0':'')+r"
    : JSON.stringify(opt(sc, "prefix", "")) + "+Math.floor(s).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',')+" + JSON.stringify(opt(sc, "suffix", "")));
  fade(c, a, b, 0.3, 0.4);
  if (sc.label) { var l = text(sc.label, a, b, 44, opt(sc, "label_y", y - 120), opt(sc, "label_color", [1, 0.75, 0.5]), "Inter", 300); fade(l, a, b, 0.3, 0.4); }
};

// particulas que se juntam: 4 bolas colidem em "at" (+0.5), clarao; rotulos opcionais (solo = bola sozinha ao lado)
TPL.collide = function (sc) {
  var t = T(sc, sc.at), b = T(sc, sc.until, "end"), x = opt(sc, "x", vh(760, 1240)), y = opt(sc, "y", vh(1080, 600)), ly = vh(930, y - 150);
  var c1 = opt(sc, "c1", [1, 0.32, 0.28]), c2 = opt(sc, "c2", [0.7, 0.78, 0.92]);
  if (sc.bg !== false) {
    var pl = noise("plasma", sc.s - 0.2, b + 0.3, { contrast: 110, bright: -25, evo: 140, dark: [0, 0, 0], light: opt(sc, "plasma", [0.9, 0.35, 0.12]) });
    fade(pl, sc.s - 0.2, b + 0.3, 0.6, 0.6, 55);
    particles("drift a", sc.s, b + 0.3, { birth: [[sc.s, 0.9], [t, 0.4]], life: 6, vel: 0.2, type: 2, c1: [1, 0.35, 0.3], size: [0.06, 0.06], rx: vh(0.6, 1.0), ry: vh(1.0, 0.6), seed: 3 });
    particles("drift b", sc.s, b + 0.3, { birth: [[sc.s, 0.9], [t, 0.4]], life: 6, vel: 0.2, type: 2, c1: [0.65, 0.75, 0.9], size: [0.06, 0.06], rx: vh(0.6, 1.0), ry: vh(1.0, 0.6), seed: 11 });
  }
  var from = HZ ? [[-200, 150], [W + 200, 300], [-200, H + 150], [W + 200, H - 100]] : [[-200, 300], [1280, 500], [-200, 1700], [1280, 1500]], to = [[-36, -33], [36, -33], [-36, 33], [36, 33]];
  for (var i = 0; i < 4; i++) {
    var bl = shape("ball" + i, t - 0.2, b, [84, 84], i % 3 == 0 ? c1 : c2);
    K(tr(bl, "Position"), [[t - 0.2, from[i]], [t + 0.5, [x + to[i][0], y + to[i][1]]]]);
  }
  flash(t + 0.5, 50, 0.4, [1, 0.8, 0.5]);
  HITS.push(t + 0.5); sfx(t + 0.5, "thud", 0.8);
  if (sc.solo) {
    var so = sc.solo, ts = T(sc, so.at), sx = opt(so, "x", vh(320, 620));
    var hb = shape("solo", ts - 0.1, b, [84, 84], opt(so, "ball", c1));
    tr(hb, "Position").setValue([sx, y]);
    K(tr(hb, "Scale"), [[ts - 0.1, [0, 0]], [ts + 0.15, [130, 130]], [ts + 0.3, [100, 100]]]);
    var lh = text(so.text, ts, b, 150, ly, opt(so, "color", [1, 0.55, 0.45]), "Anton", 0); tr(lh, "Position").setValue([sx, ly]);
    K(tr(lh, "Scale"), [[ts, [140, 140]], [ts + 0.15, [100, 100]]]);
    sfx(ts, "chime", 0.6, { d: 1.5, f: 660 });
  }
  if (sc.label) {
    var gl = sc.label, tl = T(sc, gl.at, t + 0.5 - sc.s);
    var lt = text(gl.text, tl, b, 150, ly, opt(gl, "color", [0.75, 0.85, 1]), "Anton", 0); tr(lt, "Position").setValue([x, ly]);
    K(tr(lt, "Scale"), [[tl, [140, 140]], [tl + 0.15, [100, 100]]]);
    sfx(tl, "chime", 0.6, { d: 1.5, f: 880 });
  }
};

// nevoa brilhante que se dissipa em "at" com clarao e luz que escapa; eletrons opcionais a partir de "electrons"
TPL.fog_clear = function (sc) {
  var t = T(sc, sc.at), lu = T(sc, sc.light_until, sc.at + "+2.5"), te = T(sc, sc.electrons, null);
  var fog = noise("fog", sc.s - 0.2, t + 1.4, { contrast: 85, bright: 15, evo: 70, cx: 5, dark: opt(sc, "dark", [0.45, 0.12, 0.02]), light: opt(sc, "light", [1, 0.72, 0.38]), add: false });
  K(tr(fog, "Opacity"), [[sc.s - 0.2, 0], [sc.s + 0.5, 100], [te != null ? te : t - 1, 100], [t, 70], [t + 1.4, 0]]);
  if (te != null) particles("electrons", te, t + 0.6, { birth: [[te, 6], [t, 2]], life: 2, vel: 0.35, type: 3, c1: [0.5, 0.8, 1], size: [0.05, 0.03], rx: vh(0.7, 1.2), ry: vh(1.2, 0.7), seed: 5 });
  particles("free light", t - 0.1, lu + 0.5, { birth: [[t - 0.1, 0], [t, 7], [t + 1, 2], [lu, 0]], life: 1.6, vel: 3.2, type: 1, c1: [1, 0.97, 0.85], c2: [1, 0.75, 0.4], seed: 13 });
  var lf = solid("flare", [0, 0, 0], t - 0.1, t + 2); lf.blendingMode = BlendingMode.ADD;
  K(P(fx(lf, "Lens Flare", { "Flare Center": [CX, CY] }), "Flare Brightness"), [[t - 0.1, 0], [t + 0.2, 80], [t + 2, 0]]);
  flash(t, 25, 0.5, [1, 0.9, 0.7]);
  HITS.push(t); sfx(t, "chime", 0.9, { d: 3, f: 523 });
};

// mapa oval tipo radiacao cosmica de fundo (CC Toner pentone), com anel e rotulo
TPL.oval_map = function (sc) {
  var t = T(sc, sc.at), b = T(sc, sc.until, "end+0.3"), rx = opt(sc, "rx", vh(490, 620)), ry = opt(sc, "ry", vh(260, 330));
  var m = noise("map", t, b, { contrast: 150, bright: 0, evo: 25, cx: 8, dark: [0, 0, 0], light: [1, 1, 1], add: false });
  var c = opt(sc, "tones", [[0.8, 0.08, 0.05], [1, 0.55, 0.12], [0.95, 0.92, 0.65], [0.2, 0.6, 1], [0.02, 0.08, 0.45]]);
  fx(m, "CC Toner", { "Tones": 3, "Highlights": c[0], "Brights": c[1], "Midtones": c[2], "Darktones": c[3], "Shadows": c[4] });
  oval(m, CX, CY, rx, ry, 4);
  var sk = [[t, [60, 60]], [t + 0.6, [100, 100]], [b, [112, 112]]];
  K(tr(m, "Scale"), sk); fade(m, t, b, 0.5, 0.4);
  var r = shape("map ring", t, b, [rx * 2 + 10, ry * 2 + 10], null, [1, 1, 1], 3);
  K(tr(r, "Scale"), sk); fade(r, t, b, 0.5, 0.4, 60);
  if (sc.label) { var la = T(sc, sc.label_at, sc.at), l = text(sc.label, la, b - 0.1, 40, opt(sc, "label_y", vh(620, CY - ry - 70)), [0.85, 0.92, 1], "Inter", 40); fade(l, la, b - 0.1, 0.3, 0.3); }
  sfx(t, "whoosh", 0.4, { d: 0.7 });
};

// gas que se aglomera, estrelas que acendem em "at" e imagem de textura (ex.: teia cosmica) em "image_at"
TPL.clumps_stars = function (sc) {
  var t = T(sc, sc.at), end = T(sc, sc.until, "end+0.3");
  var cl = noise("clumps", sc.s - 0.2, end, { contrast: 100, bright: -45, evo: 60, cx: 7, dark: [0, 0, 0.01], light: opt(sc, "gas", [0.5, 0.58, 1]) });
  K(P(cl.Effects.property("Fractal Noise"), "Contrast"), [[sc.s, 100], [t, 420]]);
  K(tr(cl, "Scale"), [[sc.s, [100, 100]], [end, [135, 135]]]);
  fade(cl, sc.s - 0.2, end, 0.6, 0.6, 80);
  particles("first stars", t - 0.1, end, { birth: [[t - 0.1, 0], [t, 8], [t + 1.2, 2], [t + 1.5, 0]], life: 12, vel: 0.02, type: 3, c1: [1, 0.97, 0.9], c2: [0.75, 0.85, 1], size: [0.05, 0.04], rx: vh(1.4, 2.2), ry: vh(2.2, 1.4), seed: 21 });
  flash(t, 45, 0.5, [0.85, 0.9, 1]);
  sfx(t, "chime", 0.7, { d: 2.5, f: 1047 });
  if (sc.image) {
    var ia = T(sc, sc.image_at), ib = end + 0.1, im = photo(sc.image, ia, ib); im.blendingMode = BlendingMode.SCREEN;
    var f = HZ ? Math.max(W / im.width, H / im.height) / Math.max(1080 / im.width, 1920 / im.height) : 1;  // textura cobre a tela nos dois formatos
    K(tr(im, "Scale"), [[ia, [150 * f, 150 * f]], [ib, [128 * f, 128 * f]]]);
    fade(im, ia, ib, 0.9, 0.4, 90);
  }
};

// objetos (recortes redondos de uma imagem) se afastando do centro, ficando vermelhos a partir de "redshift_at"
TPL.recede = function (sc) {
  var a = sc.s - 0.1, b = T(sc, sc.until, "dur"), n = opt(sc, "count", 7), crop = opt(sc, "crop", [432, 768, 210, 150]);
  TPL.starfield({ s: sc.s, e: sc.e, from: -0.2, until: sc.until || "dur", speed: -0.5, size: 18, peak: 80, fade: [0.6, 0.8] });
  if (sc.grid !== false) {
    var g = grid("expanding grid", sc.s, b, 120, [0.35, 0.55, 1]);
    K(tr(g, "Scale"), [[sc.s, [70, 70]], [b, [230, 230]]]); fade(g, sc.s, b, 0.8, 0.8, 30);
  }
  var tr0 = T(sc, sc.redshift_at, null);
  for (var i = 0; i < n; i++) {
    var ang = i / n * Math.PI * 2 + 0.35, r0 = 230, r1 = 900, ex = vh(1, 1.4), ey = vh(1.4, 1);  // elipse deitada no horizontal
    var gl = photo(sc.image, a, b); gl.blendingMode = BlendingMode.ADD;
    circle(gl, crop[0], crop[1], crop[2], crop[3]);
    K(tr(gl, "Position"), [[sc.s, [CX + Math.cos(ang) * r0 * ex, CY + Math.sin(ang) * r0 * ey]], [b, [CX + Math.cos(ang) * r1 * ex, CY + Math.sin(ang) * r1 * ey]]]);
    K(tr(gl, "Scale"), [[sc.s, [34, 34]], [b, [14, 14]]]);
    tr(gl, "Rotation").setValue(i * 47);
    if (tr0 != null) K(P(fx(gl, "Tint", { "Map Black To": [0, 0, 0], "Map White To": opt(sc, "tint", [1, 0.45, 0.3]) }), "Amount to Tint"), [[tr0, 0], [tr0 + 2.5, 85]]);
    fade(gl, a, b, 0.6, 0.8);
  }
  if (sc.center_label) {
    shape("center", sc.s, b, [26, 26], [0.8, 0.9, 1]);
    fade(text(sc.center_label, sc.s + 0.4, b, 40, CY + 80, [0.8, 0.9, 1], "Inter", 300), sc.s + 0.4, b, 0.3, 0.6);
  }
};

// ================= corpo humano / medicina / dados =================
// Estilo holograma medico: fundo escuro, ciano/teal com acentos ambar e magenta.
var CYAN = [0.3, 0.9, 1], TEAL = [0.12, 0.72, 0.7], AMBER = [1, 0.7, 0.22], MAGENTA = [1, 0.3, 0.72], WHITE = [1, 1, 1];
var EZ = "function ez(u){u=Math.min(1,Math.max(0,u));return u*u*(3-2*u);} ";  // para expressoes

// ---------------- tema "rulechanged" (SPEC.theme): grafite liso, sem brilho, Anton so em titulo ----------------
// Sem SPEC.theme nada muda. Com ele: pal() troca toda cor pela paleta do canal, camadas somadas (brilhos) ficam desligadas,
// label() em Anton vira Inter-Bold (menos com o.title), e fact_card/bars/lower_third/quote_card tem versao propria.
var RC = SPEC.theme == "rulechanged";
function hx(s) { return [parseInt(s.substr(1, 2), 16) / 255, parseInt(s.substr(3, 2), 16) / 255, parseInt(s.substr(5, 2), 16) / 255]; }
var TH = { bg: hx("#111214"), bg2: hx("#1b1d20"), ink: hx("#ece8e1"), ink2: hx("#c8c3ba"), lbl: hx("#a8a29a"), mute: hx("#86817a"),
  red: hx("#d0402f"), green: hx("#7fb08a"), bar: hx("#b8463b"), dim: hx("#5a5c60"), axis: hx("#3a3c40"), paper: hx("#ece4d0"), doc: hx("#1d1a14"), hl: hx("#f2d24b") };
var ACT_COL = { scam: TH.red, "case": TH.lbl, rule: TH.green };
// cor qualquer -> paleta do canal: escuro vira grafite, neutro vira texto, verde fica verde-salvia, ciano/azul vira rotulo, ambar vira texto secundario, resto vira vermelho
function pal(c) {
  if (!RC || !c || typeof c[0] != "number") return c;
  var mx = Math.max(c[0], c[1], c[2]), mn = Math.min(c[0], c[1], c[2]), m = (c[0] + c[1] + c[2]) / 3;
  if (mx < 0.3) return [m, m, m * 1.05];
  if ((mx - mn) / mx < 0.25) return mx > 0.75 ? TH.ink : [m, m * 0.98, m * 0.95];
  var h = c[0] == mx ? ((c[1] - c[2]) / (mx - mn) * 60 + 360) % 360 : c[1] == mx ? (c[2] - c[0]) / (mx - mn) * 60 + 120 : (c[0] - c[1]) / (mx - mn) * 60 + 240;
  return h >= 70 && h < 170 ? TH.green : h >= 170 && h < 270 ? TH.lbl : h >= 20 && h < 70 ? TH.ink2 : TH.red;
}
// chaves com curva: f = eoExpo (cubic-bezier .16,1,.3,1) ou eioQuart
function KE(prop, t0, d, v0, v1, f) { for (var j = 0; j <= 10; j++) prop.setValueAtTime(t0 + d * j / 10, mixv(v0, v1, f(j / 10))); return prop; }
function eoExpo(u) { return u >= 1 ? 1 : 1 - Math.pow(2, -10 * u); }
function eioQuart(u) { return u < 0.5 ? 8 * u * u * u * u : 1 - Math.pow(-2 * u + 2, 4) / 2; }
// linha de fonte do tema: canto inferior esquerdo (acima da legenda, se houver), Inter caixa-alta, tracking largo
// guardada e desenhada depois da vinheta (no canto ela apagava a fonte para ~#6e6a65)
var SRCQ = [];
function srcLine(str, a, b, x) {  // termina no fim do proprio bloco: a sobra de 0,3 s das cenas nao invade a fonte do bloco seguinte
  for (var i = 0; i < BLOCKS.length; i++) if (BLOCKS[i] > a + 0.01) { b = Math.min(b, BLOCKS[i]); break; }
  if (b > a + 0.3) SRCQ.push([str, a, b, x]);  // cena que mal aparece nao deixa fonte solta
}
function srcLineNow(str, a, b, x) {
  var l = label(String(str).replace(/^source:\s*/i, "Source · ").toUpperCase(), a, b, { y: SPEC.captions !== false ? CAP_Y - vh(110, 74) : H - 70, x: x || 96, just: "left", size: 24, font: "Inter Medium", color: TH.lbl, track: 120, raw: true, maxw: W - (x || 96) - 96 });
  fade(l, a, b, 0.25, 0.15); return l;
}
function ez(u) { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); }
function mixv(a, b, e) { if (typeof a == "number") return a + (b - a) * e; var r = []; for (var i = 0; i < a.length; i++) r.push(a[i] + (b[i] - a[i]) * e); return r; }
// como K, mas com movimento suave (ease in/out) entre as chaves
function KS(prop, keys) {
  var out = [];
  for (var i = 0; i < keys.length; i++) {
    out.push(keys[i]);
    if (i + 1 < keys.length) for (var j = 1; j < 6; j++) out.push([keys[i][0] + (keys[i + 1][0] - keys[i][0]) * j / 6, mixv(keys[i][1], keys[i + 1][1], ez(j / 6))]);
  }
  return K(prop, out);
}
function fadeX(a, b, fi, fo) { return "Math.max(0,Math.min(1,(time-(" + a + "))/" + fi + ",(" + b + "-time)/" + fo + "))"; }
function rnd(i, k) { var x = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); }
// forma vetorial: o = {rect:[w,h], round | ellipse:[w,h] | path:[[x,y]..], closed, tin, tout; fill, fop, stroke, sw, cap (1 reto, 2 redondo), dash:[traco, vao], trim, pos, blur, add}
// path em coordenadas da tela; rect/ellipse centrados em pos. Devolve {l, shape, fill, trim}.
function vec(name, a, b, o) {
  var l = comp.layers.addShape(); l.name = name;
  var gc = l.property("Contents").addProperty("ADBE Vector Group").property("Contents"), r = { l: l }, s;
  if (o.rect) { s = gc.addProperty("ADBE Vector Shape - Rect"); s.property("Size").setValue(o.rect); if (o.round) s.property("Roundness").setValue(o.round); }
  else if (o.ellipse) { s = gc.addProperty("ADBE Vector Shape - Ellipse"); s.property("Size").setValue(o.ellipse); }
  else { s = gc.addProperty("ADBE Vector Shape - Group"); var p = new Shape(); p.vertices = o.path; p.closed = !!o.closed; if (o.tin) { p.inTangents = o.tin; p.outTangents = o.tout; } s.property("Path").setValue(p); }
  r.shape = s;
  if (!o.raw) { o.stroke = pal(o.stroke); o.fill = pal(o.fill); }
  if (o.stroke) {
    var st = gc.addProperty("ADBE Vector Graphic - Stroke"); st.property("Color").setValue(o.stroke); st.property("Stroke Width").setValue(o.sw || 4); st.property("Line Cap").setValue(o.cap || 2);
    if (o.dash) { var ds = st.property("Dashes"); ds.addProperty("ADBE Vector Stroke Dash 1").setValue(o.dash[0]); ds.addProperty("ADBE Vector Stroke Gap 1").setValue(o.dash[1]); }
  }
  if (o.fill) { r.fill = gc.addProperty("ADBE Vector Graphic - Fill"); r.fill.property("Color").setValue(o.fill); if (o.fop != null) r.fill.property("Opacity").setValue(o.fop); }
  if (o.trim) r.trim = gc.addProperty("ADBE Vector Filter - Trim");
  tr(l, "Position").setValue(o.pos || (o.path ? [0, 0] : [CX, CY]));
  if (o.blur) fx(l, "Gaussian Blur", { "Blurriness": o.blur });
  if (o.add) { l.blendingMode = BlendingMode.ADD; if (RC) l.enabled = false; }
  span(l, a, b);
  return r;
}
// rotulo (Inter): o = {y (linha de base), x, just "left"|"right"|"center", size 40, font, color, track, maxw 980}; encolhe para caber em maxw
function label(str, a, b, o) {
  var fn = opt(o, "font", "Inter SemiBold"); if (RC && fn == "Anton" && !o.title) fn = "Inter-Bold";
  var t = text(str, a, b, opt(o, "size", 40), o.y, opt(o, "color", [0.85, 0.97, 1]), fn, opt(o, "track", 60));
  if (RC || o.raw) { var sd0 = t.property("Source Text"), d0 = sd0.value; if (RC) d0.applyStroke = false; if (o.raw) d0.fillColor = o.color; sd0.setValue(d0); }
  var j = opt(o, "just", "center");
  if (j != "center") { var sd = t.property("Source Text"), d = sd.value; d.justification = j == "left" ? ParagraphJustification.LEFT_JUSTIFY : ParagraphJustification.RIGHT_JUSTIFY; sd.setValue(d); }
  tr(t, "Position").setValue([opt(o, "x", CX), o.y]);
  var w = t.sourceRectAtTime(t.inPoint + 0.01, false).width, mw = opt(o, "maxw", W - 100);
  if (w > mw) tr(t, "Scale").setValue([mw / w * 100, mw / w * 100]);
  return t;
}
// null que move/escala um grupo de camadas; filhos mantem as coordenadas da tela (ancora = posicao = c)
function rig(name, a, b, c) { var n = comp.layers.addNull(); n.name = name; span(n, a, b); c = c || [CX, CY]; tr(n, "Anchor Point").setValue(c); tr(n, "Position").setValue(c); return n; }
function adopt(n, ls) { for (var i = 0; i < ls.length; i++) ls[i].parent = n; }
// fundo de holograma: degrade teal radial, grade fraca, poeira
function holoBg(a, b) {
  if (RC) {  // grafite liso com radial muito sutil (#1b1d20 no centro alto -> #111214)
    var g = solid("rc bg", TH.bg, a, b);
    fx(g, "Gradient Ramp", { "Start of Ramp": [CX, H * 0.4], "Start Color": TH.bg2, "End of Ramp": [CX + W * 0.62, H * 0.4], "End Color": TH.bg, "Ramp Shape": 2 });
    return fade(g, a, b, 0.3, 0.3);
  }
  var l = solid("holo bg", [0, 0, 0], a, b);
  fx(l, "Gradient Ramp", { "Start of Ramp": [CX, vh(760, 420)], "Start Color": [0, 0.1, 0.125], "End of Ramp": [CX, vh(1950, 1500)], "End Color": [0, 0.012, 0.02], "Ramp Shape": 2 });
  fade(l, a, b, 0.3, 0.3);
  fade(grid("holo grid", a, b, 72, TEAL), a, b, 0.5, 0.4, 10);
  particles("holo dust", a, b, { birth: [[a, 0.5]], life: 9, vel: 0.03, type: 3, c1: CYAN, c2: TEAL, size: [0.012, 0.006], rx: vh(0.6, 1.0), ry: vh(1.0, 0.6), seed: 17 });
}
// linhas de varredura fixas + faixa de luz que desce
function holoScan(a, b, col, op) {
  if (RC) return;
  var l = solid("scanlines", col, a, b); l.blendingMode = BlendingMode.ADD;
  fx(l, "Venetian Blinds", { "Transition Completion": 82, "Direction": 90, "Width": 7 });
  fade(l, a, b, 0.4, 0.4, op);
  var band = vec("scan band", a, b, { rect: [W + 220, 90], fill: col, blur: 45, add: true }).l;
  tr(band, "Position").expression = "[" + CX + ", -150+((time-(" + a + "))*380)%" + (H + 380) + "]";
  fade(band, a, b, 0.4, 0.4, op * 2);
}
// foto cobrindo a tela; devolve {l, m(x,y) -> ponto na tela a partir de pixels da imagem}
// horizontal: a imagem (retrato) ocupa a altura toda num painel centrado em cx (padrao PANEL_X), com bordas suaves;
// full = cobre a tela inteira (fundo de capitulo). panel = largura do painel (padrao 700).
function cover(file, a, b, k, cx, full, panel) {
  var l = photo(file, a, b), fit = HZ && !full ? H / l.height : Math.max(W / l.width, H / l.height), s = (k || 1) * fit;
  cx = HZ && !full ? (cx == null ? PANEL_X : cx) : CX;
  tr(l, "Scale").setValue([s * 100, s * 100]);
  tr(l, "Position").setValue([cx, CY]);
  var mask = null;
  if (HZ && !full) {  // recorte no painel (coordenadas da imagem), para nao invadir a coluna de rotulos
    var hw = (panel || 700) / 2 / s, ccx = l.width / 2, m = l.Masks.addProperty("Mask"), sh = new Shape();
    sh.vertices = [[ccx - hw, -50], [ccx + hw, -50], [ccx + hw, l.height + 50], [ccx - hw, l.height + 50]]; sh.closed = true;
    mask = { path: sh, f: [60 / s, 0] };
    m.property("Mask Path").setValue(sh); m.property("Mask Feather").setValue(mask.f);
  }
  return { l: l, m: function (x, y) { return [cx + (x - l.width / 2) * s, CY + (y - l.height / 2) * s]; }, s: s, cx: cx, mask: mask };
}
// copia desfocada da foto, somada, com brilho pulsando (holograma)
function holoGlow(file, a, b, s, col, base, amp, im) {
  var g = photo(file, a, b); g.blendingMode = BlendingMode.ADD; tr(g, "Scale").setValue([s * 100, s * 100]);
  if (HZ) { tr(g, "Position").setValue([im.cx, CY]); if (im.mask) { var m = g.Masks.addProperty("Mask"); m.property("Mask Path").setValue(im.mask.path); m.property("Mask Feather").setValue(im.mask.f); } }
  fx(g, "Gaussian Blur", { "Blurriness": 30 }); fx(g, "Tint", { "Map Black To": [0, 0, 0], "Map White To": col });
  tr(g, "Opacity").expression = fadeX(a, b, 0.5, 0.3) + "*(" + base + "+" + amp + "*Math.sin(time*2.4))";
  if (RC) g.enabled = false;
  return g;
}
// titulo pequeno no topo (organ_focus/flow_valve): L = {text, at, y, color}
function topTitle(sc, L, b, C, y, x) {
  var tl = T(sc, L.at, "start+0.3"), yy = opt(L, "y", y), xx = opt(L, "x", x == null ? CX : x);
  var t = label(RC ? String(L.text).toUpperCase() : L.text, tl, b - 0.1, { y: yy, x: xx, size: RC ? 30 : 66, font: RC ? "Inter SemiBold" : "Anton", track: RC ? 200 : 120, color: RC ? TH.lbl : opt(L, "color", mixv(C, WHITE, 0.55)), raw: RC, maxw: HZ && xx != CX ? 2 * Math.min(xx, W - xx) - 80 : W - 100 });
  fade(t, tl, b - 0.1, 0.3, 0.3);
  var ln = vec("title line", tl + 0.1, b - 0.1, { path: [[xx - 110, yy + 30], [xx + 110, yy + 30]], stroke: C, sw: 3, trim: true });
  K(ln.trim.property("End"), [[tl + 0.1, 0], [tl + 0.5, 100]]); fade(ln.l, tl + 0.1, b - 0.1, 0.1, 0.3);
}
// selo "ILLUSTRATION" (cena reconstruida, sem rosto): Inter 600 18, fundo preto 60%, canto superior esquerdo da imagem
function illuTag(x, y, a, b) {
  var t = label("ILLUSTRATION", a, b, { y: y + 23, x: x + 12, just: "left", size: 18, color: RC ? TH.mute : [0.75, 0.75, 0.75], raw: true, track: 200 });
  var w = t.sourceRectAtTime(a + 0.01, false).width, bx = vec("illu box", a, b, { rect: [w + 24, 34], fill: [0, 0, 0], fop: 60, raw: true, pos: [x + (w + 24) / 2, y + 17] }).l;
  bx.moveAfter(t); fade(bx, a, b, 0.4, 0.2); fade(t, a, b, 0.4, 0.2);
}
function enterWhoosh(sc, t) { if (t > (sc.s0 != null ? sc.s0 : sc.s) + 0.3) sfx(t - 0.2, "whoosh", 0.3, { d: 0.6 }); }  // a entrada no inicio do bloco ja tem o whoosh do corte

// mapa do corpo: imagem com leve respiracao; pontos que acendem com linha-guia ate o rotulo; focus = camera mergulha num ponto
// spots: [{x, y (pixels da imagem), at, label, color, side "left"|"right", dy (rotulo acima/abaixo do ponto)}]; focus: {spot, at, zoom 4}
TPL.body_map = function (sc) {
  var a = sc.s - 0.1, b = T(sc, sc.until, "end+0.3"), C = opt(sc, "color", CYAN), kids = [];
  var fo = sc.focus, tf = fo ? T(sc, fo.at) : null, lb = fo ? tf + 0.35 : b;  // rotulos somem quando a camera mergulha
  if (sc.bg !== false) holoBg(a, b);
  var R = rig("body cam", a, b), im = cover(sc.image, a, b, sc.scale, opt(sc, "img_x", CX), false, opt(sc, "panel", 760));
  // photo: true = imagem realista, sem brilho de holograma nem mistura clareadora (estourava a pele)
  fade(im.l, a, b, 0.5, 0.3); kids.push(im.l); if (!sc.photo) kids.push(holoGlow(sc.image, a, b, im.s, C, opt(sc, "glow", 22), 8, im));
  if (sc.screen !== false && !sc.photo) im.l.blendingMode = BlendingMode.SCREEN;  // fundo preto da imagem some e mostra o holograma
  var sp = sc.spots || [];
  for (var i = 0; i < sp.length; i++) {
    var p = sp[i], q = im.m(p.x, p.y), t = T(sc, p.at), c = p.color || C;
    var h = vec("spot glow", t, b, { ellipse: [110, 110], fill: c, blur: 22, add: true, pos: q }).l;
    K(tr(h, "Opacity"), [[t, 0], [t + 0.15, 55], [t + 0.7, 30]]);  // mais que isso + Glow final estoura
    tr(h, "Scale").expression = "var k=1+0.12*Math.sin((time-" + t + ")*5); [100*k,100*k]";
    var rg = vec("spot ring", t, b, { ellipse: [44, 44], stroke: c, sw: 4, pos: q }).l, u = "var u=((time-" + t + ")%1.3)/1.3; ";
    tr(rg, "Scale").expression = u + "[100+220*u,100+220*u]"; tr(rg, "Opacity").expression = u + "100*(1-u)";
    var co = vec("spot", t, b, { ellipse: [24, 24], fill: mixv(c, WHITE, 0.6), stroke: c, sw: 3, pos: q }).l;
    K(tr(co, "Scale"), [[t, [0, 0]], [t + 0.12, [170, 170]], [t + 0.3, [100, 100]]]);
    kids.push(h, rg, co);
    sfx(t, "chime", 0.45, { d: 1.8, f: 660 * Math.pow(1.19, i) });
    if (!p.label) continue;
    var side = p.side || (q[0] < im.cx ? "left" : "right"), dr = side == "left" ? -1 : 1, dy = p.dy || 0, ly = q[1] + dy;
    var ex = q[0] + dr * (Math.abs(dy) + 40), mx = HZ ? (side == "left" ? Math.max(60, ex - 560) : Math.min(W - 60, ex + 560)) : (side == "left" ? 50 : 1030), vl = Math.sqrt((ex - q[0]) * (ex - q[0]) + dy * dy);
    var ln = vec("callout", t + 0.1, lb, { path: [[q[0] + (ex - q[0]) / vl * 16, q[1] + dy / vl * 16], [ex, ly], [mx, ly]], stroke: c, sw: 3, trim: true });
    K(ln.trim.property("End"), [[t + 0.1, 0], [t + 0.5, 100]]); fade(ln.l, t + 0.1, lb, 0.05, 0.3);
    var lt = label(p.label, t + 0.35, lb, { y: ly - 14, x: mx, just: side, size: opt(p, "size", 46), color: mixv(c, WHITE, 0.55), maxw: Math.abs(ex - mx) - 6 });
    fade(lt, t + 0.35, lb, 0.25, 0.3);
    kids.push(ln.l, lt);
  }
  adopt(R, kids);
  var br = "var br=1+0.012*Math.sin((time-(" + a + "))*1.7); ";
  if (fo) {
    var fq = sp[opt(fo, "spot", 0)], fp = im.m(fq.x, fq.y), Z = opt(fo, "zoom", 4) - 1;
    var e = br + EZ + "var e=ez((time-" + tf + ")/" + (b - tf) + "), k=br*(1+" + Z + "*e*e); ";
    tr(R, "Scale").expression = e + "[100*k,100*k]";
    tr(R, "Position").expression = e + "[" + CX + "+(" + (fp[0] - CX) + ")*(1-e-k), " + CY + "+(" + (fp[1] - CY) + ")*(1-e-k)]";
    sfx(tf, "rise", 0.45, { d: b - tf });
  } else tr(R, "Scale").expression = br + "[100*br,100*br]";
};

// orgao em destaque: zoom lento, brilho pulsando, varredura; emit = particulas saindo de um ponto; hold = sinal de bloqueio; label = titulo no topo
// emit: {at, until, color, from:[x,y] (pixels da imagem), dir:[dx,dy] (0,-1 = sobe), type 2|3, rate 4}
// hold: {at, color, x, y (pixels da imagem), text, dir, flow (false = sem fluxo antes do bloqueio)}; label: {text, at}
TPL.organ_focus = function (sc) {
  var a = sc.s - 0.1, b = T(sc, sc.until, "end+0.3"), C = opt(sc, "color", CYAN), z = opt(sc, "zoom", [100, 116]), kids = [];
  if (sc.bg !== false) holoBg(a, b);
  var ix = HZ ? opt(sc, "img_x", PANEL_X) : CX, ifx = ix < CX ? INFO_X : W - INFO_X;  // horizontal: imagem de um lado, titulo do outro
  var R = rig("organ cam", a, b, [ix, CY]), im = cover(sc.image, a, b, sc.scale, ix, false, opt(sc, "panel", 700));
  fade(im.l, a, b, 0.5, 0.3); kids.push(im.l); if (!sc.photo) kids.push(holoGlow(sc.image, a, b, im.s, C, opt(sc, "glow", 30), 16, im));
  if (sc.screen !== false && !sc.photo) im.l.blendingMode = BlendingMode.SCREEN;
  if (!sc.photo) holoScan(a, b, C, 6);
  function flow(nm, q, t0, t1, c, d, rate, type, seed) {
    var n = Math.sqrt(d[0] * d[0] + d[1] * d[1]) || 1;
    return particles(nm, t0 - 0.05, b, { birth: [[t0 - 0.05, 0], [t0, rate], [t1, rate], [t1 + 0.05, 0]], life: 2.4, vel: 0.1, type: type, c1: c, c2: mixv(c, [0, 0, 0], 0.35), size: type == 3 ? [0.06, 0.025] : [0.03, 0.016], rx: 0.02, ry: 0.02, rz: 0.02, grav: 0.35, gv: [d[0] / n, d[1] / n], resist: 0.9, px: (q[0] - CX) / 1080, py: (q[1] - CY) / 1080, seed: seed });
  }
  if (sc.emit) {
    var em = sc.emit, t0 = T(sc, em.at), t1 = T(sc, em.until, "end"), q = im.m(em.from[0], em.from[1]), c = opt(em, "color", AMBER);
    kids.push(flow("emit", q, t0, t1, c, opt(em, "dir", [0, -1]), opt(em, "rate", 4), opt(em, "type", 2), 9));
    var pr = vec("emit ring", t0, t0 + 1.2, { ellipse: [60, 60], stroke: c, sw: 5, pos: q }).l;
    K(tr(pr, "Scale"), [[t0, [50, 50]], [t0 + 1.2, [520, 520]]]); K(tr(pr, "Opacity"), [[t0, 100], [t0 + 1.2, 0]]);
    kids.push(pr); sfx(t0, "chime", 0.5, { d: 2, f: 784 });
  }
  if (sc.hold) {
    var ho = sc.hold, th = T(sc, ho.at), c2 = opt(ho, "color", MAGENTA), hq = ho.x != null ? im.m(ho.x, ho.y) : [ix, CY + vh(200, 150)];
    if (ho.flow !== false) kids.push(flow("blocked flow", hq, a + 0.4, th, c2, opt(ho, "dir", [0, -1]), 2, 2, 4));
    var parts = [vec("hold disk", th, b, { ellipse: [200, 200], fill: [0.03, 0, 0.04], fop: 75, pos: hq }).l,
      vec("hold glow", th, b, { ellipse: [210, 210], fill: c2, blur: 30, add: true, fop: 45, pos: hq }).l,
      vec("hold ring", th, b, { ellipse: [170, 170], stroke: c2, sw: 16, pos: hq }).l,
      vec("hold bar", th, b, { rect: [150, 16], round: 8, fill: c2, pos: hq }).l];
    tr(parts[3], "Rotation").setValue(-45);
    for (var i = 0; i < parts.length; i++) { K(tr(parts[i], "Scale"), [[th, [0, 0]], [th + 0.12, [125, 125]], [th + 0.25, [100, 100]]]); kids.push(parts[i]); }
    if (ho.text) { var ht = label(ho.text, th + 0.1, b, { y: hq[1] + 160 > vh(1440, 900) ? hq[1] - 150 : hq[1] + 160, x: hq[0], size: 48, track: 120, color: mixv(c2, WHITE, 0.45), maxw: 2 * Math.min(hq[0], W - hq[0]) - 60 }); fade(ht, th + 0.1, b, 0.2, 0.3); kids.push(ht); }
    HITS.push(th); sfx(th, "thud", 0.7);
  }
  adopt(R, kids);
  K(tr(R, "Scale"), [[a, [z[0], z[0]]], [b, [z[1], z[1]]]]);
  if (sc.illustration) illuTag(HZ ? ix - opt(sc, "panel", 700) / 2 + 60 : RC ? 84 : 40, !HZ && RC ? 128 : 40, a, b);  // dentro da borda suave da imagem; no Short do tema, abaixo do marcador de ato
  if (sc.label) { if (HZ && ix == CX) topTitle(sc, sc.label, b, C, 130); else if (HZ) topTitle(sc, sc.label, b, C, 360, ifx); else topTitle(sc, sc.label, b, C, 440); }
};

// membrana da celula com receptores em U; ligantes chegam voando e encaixam em "at" (onda de sinal para dentro da celula)
// ligands: [{at*, color, label, receptor (indice), persist}]; receptors: N (padrao = n de ligantes); dissolve_at: os nao-persist viram particulas e somem
TPL.molecule_dock = function (sc) {
  var a = sc.s - 0.1, b = T(sc, sc.until, "end+0.3"), y0 = opt(sc, "y", vh(1080, 700)), bend = opt(sc, "bend", 70), C = opt(sc, "color", TEAL);
  var lig = sc.ligands || [], n = opt(sc, "receptors", lig.length || 2), td = T(sc, sc.dissolve_at, null), np = Math.round((W + 120) / 50);
  if (sc.bg !== false) holoBg(a, b);
  function my(x) { var u = (x - CX) / CX; return y0 + bend * u * u; }
  function off(dy) { var r = []; for (var i = 0; i <= np; i++) { var x = -60 + i * 50; r.push([x, my(x) + dy]); } return r; }
  var mem = [vec("cell inside", a, b, { path: off(0).concat([[W + 60, H + 80], [-60, H + 80]]), closed: true, fill: [0.02, 0.17, 0.19], fop: 60 }).l,
    vec("membrane", a, b, { path: off(0), stroke: mixv(C, [0, 0, 0], 0.55), sw: 112, cap: 1 }).l,
    vec("tails", a, b, { path: off(-20), stroke: mixv(C, [0, 0, 0], 0.3), sw: 5, dash: [14, 11], cap: 1 }).l,
    vec("tails", a, b, { path: off(20), stroke: mixv(C, [0, 0, 0], 0.3), sw: 5, dash: [14, 11], cap: 1 }).l,
    vec("heads", a, b, { path: off(-46), stroke: C, sw: 20, dash: [0.01, 25] }).l,
    vec("heads", a, b, { path: off(46), stroke: C, sw: 20, dash: [0.01, 25] }).l];
  for (var i = 0; i < mem.length; i++) fade(mem[i], a, b, 0.4, 0.3);
  var RC = mixv(C, WHITE, 0.55), dock = [], ang = [];
  for (var r = 0; r < n; r++) {
    var x = W * (r + 1) / (n + 1), g = Math.atan(2 * bend * (x - CX) / (CX * CX)), base = [x, my(x) - 50];
    var U = vec("receptor", a, b, { path: [[-34, -88], [-34, -30], [0, 4], [34, -30], [34, -88]], tin: [[0, 0], [0, 0], [-20, 0], [0, 20], [0, 0]], tout: [[0, 0], [0, 20], [20, 0], [0, 0], [0, 0]], stroke: RC, sw: 16, pos: base }).l;
    var st = vec("receptor stem", a, b, { path: [[0, 4], [0, 80]], stroke: RC, sw: 12, pos: base }).l;
    tr(U, "Rotation").setValue(g * 180 / Math.PI); tr(st, "Rotation").setValue(g * 180 / Math.PI);
    fade(U, a, b, 0.4, 0.3); fade(st, a, b, 0.4, 0.3);
    dock.push([x + Math.sin(g) * 40, base[1] - Math.cos(g) * 40]); ang.push(g * 180 / Math.PI);
  }
  for (var i = 0; i < lig.length; i++) {
    var L = lig[i], t = T(sc, L.at), ri = opt(L, "receptor", i % n), c = L.color || (i % 2 ? MAGENTA : CYAN), dk = dock[ri], sd = dk[0] < CX ? -1 : 1;
    var gone = td != null && !L.persist, le = gone ? td + 0.6 : b, s0 = [dk[0] + sd * 260, vh(330, 150)];
    var lg = vec("ligand", t - 1.3, le, { rect: [58, 92], round: 29, fill: c, stroke: mixv(c, WHITE, 0.6), sw: 4, pos: s0 }).l;
    var hl = vec("ligand glow", t - 1.3, le, { ellipse: [150, 150], fill: c, blur: 26, add: true }).l;
    hl.parent = lg; tr(hl, "Position").setValue([0, 0]);
    KS(tr(lg, "Position"), [[t - 1.3, s0], [t, dk]]); KS(tr(lg, "Rotation"), [[t - 1.3, sd * 70], [t, ang[ri]]]);
    var op = [[t - 1.3, 0], [t - 1.0, 100]];
    if (gone) { op.push([td, 100], [td + 0.5, 0]); K(tr(lg, "Scale"), [[td, [100, 100]], [td + 0.5, [160, 160]]]); }
    K(tr(lg, "Opacity"), op); for (var w = 0; w < op.length; w++) op[w] = [op[w][0], op[w][1] * 0.55]; K(tr(hl, "Opacity"), op);
    if (L.label) {
      var lt = label(L.label, t - 1.3, gone ? td + 0.3 : b, { y: 0, size: 54, font: "Inter-Bold", track: 40, color: mixv(c, WHITE, 0.5) });
      KS(tr(lt, "Position"), [[t - 1.3, [s0[0], s0[1] - 90]], [t, [dk[0], dk[1] - 90]]]); fade(lt, t - 1.3, gone ? td + 0.3 : b, 0.3, 0.3);
    }
    // encaixe: anel no receptor + ondas de sinal para dentro da celula + brilho interno
    var rx = dk[0], ry = my(rx) + 50, ring = vec("dock ring", t, t + 0.8, { ellipse: [90, 90], stroke: mixv(c, WHITE, 0.4), sw: 6, pos: dk }).l;
    K(tr(ring, "Scale"), [[t, [60, 60]], [t + 0.8, [320, 320]]]); K(tr(ring, "Opacity"), [[t, 100], [t + 0.8, 0]]);
    for (var w = 0; w < 3; w++) {
      var tw = t + w * 0.28, wv = vec("signal", tw, tw + 1.4, { ellipse: [160, 160], stroke: c, sw: 8, trim: true, pos: [rx, ry] });
      wv.trim.property("Start").setValue(25); wv.trim.property("End").setValue(75); tr(wv.l, "Rotation").setValue(ang[ri]);
      K(tr(wv.l, "Scale"), [[tw, [30, 30]], [tw + 1.4, [480, 480]]]); K(tr(wv.l, "Opacity"), [[tw, 90], [tw + 1.4, 0]]);
    }
    var ig = vec("inner glow", t, le, { ellipse: [520, 280], fill: c, blur: 60, add: true, pos: [rx, ry + 200] }).l;
    K(tr(ig, "Opacity"), [[t, 0], [t + 0.3, 50], [t + 2, 22], [le - 0.3, 22], [le, 0]]);
    HITS.push(t); sfx(t, "thud", 0.7);
    if (gone) particles("dissolve", td - 0.05, td + 1.4, { birth: [[td - 0.05, 0], [td, 5], [td + 0.3, 0]], life: 1.1, vel: 0.3, type: 3, c1: mixv(c, WHITE, 0.3), c2: c, size: [0.04, 0], rx: 0.03, ry: 0.04, px: (dk[0] - CX) / 1080, py: (dk[1] - CY) / 1080, seed: 30 + i });
  }
  if (td != null) sfx(td, "chime", 0.35, { d: 1.6, f: 1175 });
};

// molecula como corrente de contas: metade c1 + metade c2 se juntam em "at"; tail_at = cauda ondulada; ride_at = viaja num vaso com globulos vermelhos
// labels: {a, b (cada metade), joined (depois de juntar), tail, ride}
TPL.molecule_build = function (sc) {
  var a = sc.s - 0.1, b = T(sc, sc.until, "end+0.3"), tj = T(sc, sc.at), tt = T(sc, sc.tail_at, null), trd = T(sc, sc.ride_at, null);
  var y0 = opt(sc, "y", vh(820, 430)), k = opt(sc, "beads", 5), d = 74, gap = opt(sc, "gap", 190), Lb = sc.labels || {}, kids = [];
  var c1 = opt(sc, "c1", CYAN), c2 = opt(sc, "c2", MAGENTA), tc = opt(sc, "tail_color", [1, 0.84, 0.2]), vy = y0 + 110, vh2 = vh(300, 260);
  if (sc.bg !== false) holoBg(a, b);
  if (trd != null) {  // vaso + globulos (atras da molecula); as particulas nascem 2.5 s antes, invisiveis, para o fluxo ja estar cheio
    var vb = [vec("vessel", trd, b, { rect: [W + 120, vh2 * 2], fill: [0.24, 0.02, 0.05], fop: 65, pos: [CX, vy] }).l,
      vec("vessel wall", trd, b, { path: [[-20, vy - vh2], [W + 20, vy - vh2]], stroke: [0.95, 0.35, 0.42], sw: 6 }).l,
      vec("vessel wall", trd, b, { path: [[-20, vy + vh2], [W + 20, vy + vh2]], stroke: [0.95, 0.35, 0.42], sw: 6 }).l];
    for (var i = 0; i < vb.length; i++) fade(vb[i], trd, b, 0.6, 0.3);
    var rbc = particles("red cells", trd - 2.5, b, { birth: [[trd - 2.5, vh(0.9, 1.5)]], life: vh(4, 6), vel: 0.02, type: 2, c1: [0.9, 0.1, 0.12], c2: [0.6, 0.03, 0.06], size: [0.085, 0.085], rx: 0.01, ry: vh(0.24, 0.21), rz: 0.1, grav: 0.6, gv: [1, 0], resist: 1.2, px: vh(-0.6, -(CX + 100) / 1080), py: (vy - CY) / 1080, seed: 8 });
    K(tr(rbc, "Opacity"), [[trd, 0], [trd + 0.6, 100]]);
    sfx(trd, "whoosh", 0.4, { d: 1.2 });
  }
  var R = rig("molecule", a, b, [CX, y0]);
  for (var h = 0; h < 2; h++) {
    var sg = h ? 1 : -1, col = h ? c2 : c1, off = sg * gap, pts = [];
    for (var j = 0; j < k; j++) pts.push([CX + sg * (d / 2 + j * d), y0 + 16 * Math.sin((j + h * k) * 1.1)]);
    var mv = [[sc.s, [off, 0]], [tj - 0.8, [off, 0]], [tj, [0, 0]]];
    var rod = vec("bond", a, b, { path: pts, stroke: mixv(col, WHITE, 0.3), sw: 8 }).l; KS(tr(rod, "Position"), mv); kids.push(rod);
    var hg = vec("half glow", a, b, { ellipse: [d * k + 60, 130], fill: col, blur: 40, add: true, fop: 30, pos: [CX + sg * d * k / 2, y0] }).l;
    KS(tr(hg, "Position"), [[sc.s, [CX + sg * d * k / 2 + off, y0]], [tj - 0.8, [CX + sg * d * k / 2 + off, y0]], [tj, [CX + sg * d * k / 2, y0]]]); kids.push(hg);
    for (var j = 0; j < k; j++) {
      var bd = vec("bead", a, b, { ellipse: [60, 60], fill: col, stroke: mixv(col, WHITE, 0.55), sw: 4, pos: pts[j] }).l;
      KS(tr(bd, "Position"), [[sc.s, [pts[j][0] + off, pts[j][1]]], [tj - 0.8, [pts[j][0] + off, pts[j][1]]], [tj, pts[j]]]); kids.push(bd);
      fade(bd, a, b, 0.4, 0.3);
    }
    var hl = h ? Lb.b : Lb.a;
    if (hl) {
      var lx = CX + sg * d * k / 2, lt = label(hl, a + 0.3, tj + 0.6, { y: y0 + 120, size: 52, font: "Inter-Bold", track: 60, color: mixv(col, WHITE, 0.45), maxw: 420 });
      KS(tr(lt, "Position"), [[sc.s, [lx + off, y0 + 120]], [tj - 0.8, [lx + off, y0 + 120]], [tj, [lx, y0 + 120]]]); fade(lt, a + 0.3, tj + 0.6, 0.3, 0.3);
    }
  }
  var jr = vec("join ring", tj, tj + 0.9, { ellipse: [80, 80], stroke: WHITE, sw: 6, pos: [CX, y0] }).l;
  K(tr(jr, "Scale"), [[tj, [40, 40]], [tj + 0.9, [500, 500]]]); K(tr(jr, "Opacity"), [[tj, 100], [tj + 0.9, 0]]); kids.push(jr);
  HITS.push(tj); sfx(tj, "thud", 0.8);
  var je = trd != null && Lb.ride ? trd + 0.3 : b - 0.1;  // o rotulo do vaso ocupa o lugar
  if (Lb.joined) { var jl = label(Lb.joined, tj + 0.1, je, { y: y0 - 150, size: 70, font: "Anton", track: 80, color: [0.95, 0.98, 1] }); fade(jl, tj + 0.1, je, 0.25, 0.3); K(tr(jl, "Scale"), [[tj + 0.1, [125, 125]], [tj + 0.3, [100, 100]]]); }
  if (tt != null) {
    var ax = CX - d * 1.5, ay = y0 + 30, tp = [];
    for (var q = 0; q < 36; q++) tp.push([ax + 20 * Math.sin(q * 0.75) + q * 2, ay + q * 8.5]);
    var tl = vec("fatty tail", tt, b, { path: tp, stroke: tc, sw: 11, trim: true });
    K(tl.trim.property("End"), [[tt, 0], [tt + 0.7, 100]]); kids.push(tl.l);
    var tg = vec("tail glow", tt, b, { path: tp, stroke: tc, sw: 34, blur: 18, add: true }).l; K(tr(tg, "Opacity"), [[tt, 0], [tt + 0.7, 45]]); kids.push(tg);
    sfx(tt, "thud", 0.45); sfx(tt + 0.6, "chime", 0.35, { d: 1.5, f: 659 });
    if (Lb.tail) { var ttl = label(Lb.tail, tt + 0.5, trd != null ? trd + 0.3 : b - 0.1, { y: ay + 250, x: ax + 115, just: "left", size: 46, track: 60, color: mixv(tc, WHITE, 0.4), maxw: 480 }); fade(ttl, tt + 0.5, trd != null ? trd + 0.3 : b - 0.1, 0.3, 0.3); kids.push(ttl); }
  }
  adopt(R, kids);
  if (trd != null) {
    var e = EZ + "var e=ez((time-" + trd + ")/0.9); ";
    tr(R, "Scale").expression = e + "[100-28*e,100-28*e]";
    tr(R, "Position").expression = e + "[" + CX + "+e*40*Math.sin((time-" + trd + ")*0.9), " + y0 + "+e*(" + (vy - y0 - 40) + "+12*Math.sin(time*2.3))]";
    if (Lb.ride) { var rl = label(Lb.ride, trd + 0.3, b - 0.1, { y: vy - vh2 - 30, size: 52, font: "Inter-Bold", track: 120, color: [1, 0.75, 0.75] }); fade(rl, trd + 0.3, b - 0.1, 0.3, 0.3); }
  }
};

// tubo com particulas passando; em slow_at a valvula fecha e o fluxo desacelera e afina
// y 960, h 240 (altura do tubo), x 700 (valvula), gap 0.3 (abertura final), speed [520, 110] px/s, count 24, color (tubo), dots (cor), label {text, at}
TPL.flow_valve = function (sc) {
  var a = sc.s - 0.1, b = T(sc, sc.until, "end+0.3"), ts = T(sc, sc.slow_at, "dur+100"), y = opt(sc, "y", vh(960, 600)), h = opt(sc, "h", 240), xv = opt(sc, "x", vh(700, 1250));
  var gp = opt(sc, "gap", 0.3), sp = opt(sc, "speed", [520, 110]), C = opt(sc, "color", CYAN), fc = opt(sc, "dots", [1, 0.66, 0.3]), n = opt(sc, "count", vh(24, 40)), wr = W + 180;
  if (sc.bg !== false) holoBg(a, b);
  var tb = [vec("tube", a, b, { rect: [W + 120, h], fill: [0, 0.22, 0.26], fop: 40, pos: [CX, y] }).l,
    vec("tube wall", a, b, { path: [[-20, y - h / 2], [W + 20, y - h / 2]], stroke: C, sw: 6 }).l,
    vec("tube wall", a, b, { path: [[-20, y + h / 2], [W + 20, y + h / 2]], stroke: C, sw: 6 }).l];
  for (var i = 0; i < tb.length; i++) fade(tb[i], a, b, 0.4, 0.3);
  var dist = "var ts=" + ts + ",r=0.9,v0=" + sp[0] + ",v1=" + sp[1] + ",t=time,d; if(t<ts) d=v0*(t-(" + a + ")); else if(t<ts+r){var q=t-ts; d=v0*(ts-(" + a + "))+v0*q+(v1-v0)*q*q/(2*r);} else d=v0*(ts-(" + a + "))+v0*r+(v1-v0)*r/2+v1*(t-ts-r); ";
  for (var i = 0; i < n; i++) {
    var dd = 24 + 20 * rnd(i, 1), o = (rnd(i, 2) * 2 - 1) * 0.36 * h, x0 = rnd(i, 3) * wr;
    var dt = vec("food", a, b, { ellipse: [dd, dd], fill: mixv(fc, WHITE, 0.35 * rnd(i, 4)), pos: [0, y] }).l;
    tr(dt, "Position").expression = EZ + dist + "var x=((" + x0 + "+d)%" + wr + "+" + wr + ")%" + wr + "-90, g=1-" + (1 - gp) + "*ez((t-ts)/r), f=1-(1-g)*Math.exp(-Math.pow((x-" + xv + ")/120,2)); [x," + y + "+(" + o + ")*f]";
    tr(dt, "Opacity").expression = EZ + fadeX(a, b, 0.4, 0.3) + "*100" + (i % 2 ? "*(1-ez((time-" + ts + "-0.2)/1.2))" : "");
  }
  var pc = mixv(AMBER, WHITE, 0.15), ph = 110, gpx = h * gp;
  for (var s = -1; s <= 1; s += 2) {
    var p0 = [xv, y + s * (h / 2 + ph / 2 - 14)], p1 = [xv, y + s * (gpx / 2 + ph / 2)];
    var pl = vec("valve", a, b, { rect: [80, ph], round: 40, fill: pc, stroke: mixv(pc, WHITE, 0.5), sw: 4, pos: p0 }).l;
    var pg = vec("valve glow", a, b, { ellipse: [150, 170], fill: AMBER, blur: 30, add: true, fop: 35, pos: p0 }).l;
    KS(tr(pl, "Position"), [[ts, p0], [ts + 0.9, p1]]); KS(tr(pg, "Position"), [[ts, p0], [ts + 0.9, p1]]);
    fade(pl, a, b, 0.4, 0.3); fade(pg, a, b, 0.4, 0.3);
  }
  if (sc.slow_at != null) sfx(ts, "thud", 0.6);
  if (sc.label) topTitle(sc, sc.label, b, C, y - h / 2 - vh(150, 120));
};

// medidor (barra arredondada) que vai de "from" a "to" entre "at" e "reach"; cor muda com o nivel; ate 2 lado a lado (meters: [{...}, {...}])
// label*, from 0, to 100, max 100, suffix "", prefix "", decimals 0, colors [baixo, meio, alto], value (false = sem numero); dir "v" | "h"; y (centro; 900 h / 840 v); show (quando aparece)
TPL.meter = function (sc) {
  var ms = sc.meters || [sc], n = Math.min(2, ms.length), hz = opt(sc, "dir", "v") == "h", a0 = T(sc, sc.show, "start"), b = T(sc, sc.until, "end+0.3");
  if (sc.bg !== false) holoBg(a0 - 0.1, b);
  enterWhoosh(sc, a0);
  for (var i = 0; i < n; i++) {
    var M = ms[i], g = function (k, d) { return opt(M, k, opt(sc, k, d)); };
    var at = T(sc, g("at", null), "start+0.4"), rc = T(sc, g("reach", null), at - sc.s + 1.6), from = g("from", 0), to = g("to", 100), mx = g("max", 100);
    var cols = g("colors", [CYAN, AMBER, MAGENTA]), w = hz ? 820 : 150, h = hz ? 96 : vh(600, 460), iw = w - 18, ih = h - 18;
    // horizontal: sem fundo proprio (empilhado sobre uma imagem) vai para a coluna da direita
    var mcx = opt(sc, "x", HZ && sc.bg === false ? INFO_X : CX);
    var yc = opt(sc, "y", HZ ? 560 : hz ? 900 : 840), pos = hz ? [mcx, n == 1 ? yc : yc - 120 + i * 300] : [n == 1 ? mcx : mcx - 210 + i * 420, yc], ls = [];
    var lv = EZ + "var v=" + from + "+(" + (to - from) + ")*ez((time-" + at + ")/" + (rc - at) + "), k=Math.min(1,Math.max(0,v/" + mx + ")); ";
    ls.push(vec("meter track", a0, b, { rect: [w, h], round: Math.min(w, h) / 2, fill: [0.01, 0.06, 0.08], fop: 85, stroke: [0.45, 0.8, 0.85], sw: 4, pos: pos }).l);
    var fl = vec("meter fill", a0, b, { rect: [iw, ih], round: Math.min(iw, ih) / 2, fill: cols[0], pos: pos });
    fl.shape.property("Size").expression = lv + (hz ? "[" + iw + "*k+0.01," + ih + "]" : "[" + iw + "," + ih + "*k+0.01]");
    fl.shape.property("Position").expression = lv + (hz ? "[-" + iw / 2 + "*(1-k),0]" : "[0," + ih / 2 + "*(1-k)]");
    fl.fill.property("Color").expression = lv + "var c=" + JSON.stringify(cols) + ", j=k<0.5?0:1, u=k<0.5?k*2:(k-0.5)*2; [c[j][0]+(c[j+1][0]-c[j][0])*u, c[j][1]+(c[j+1][1]-c[j][1])*u, c[j][2]+(c[j+1][2]-c[j][2])*u, 1]";
    ls.push(fl.l);
    ls.push(vec("ticks", a0, b, hz ? { path: [[pos[0] - iw / 2, pos[1] + h / 2 + 20], [pos[0] + iw / 2, pos[1] + h / 2 + 20]], stroke: [0.45, 0.8, 0.85], sw: 14, cap: 1, dash: [3, iw / 10 - 3] }
      : { path: [[pos[0] + w / 2 + 22, pos[1] - ih / 2], [pos[0] + w / 2 + 22, pos[1] + ih / 2]], stroke: [0.45, 0.8, 0.85], sw: 16, cap: 1, dash: [3, ih / 10 - 3] }).l);
    ls.push(label(g("label", ""), a0, b, hz ? { y: pos[1] - h / 2 - 26, x: pos[0] - w / 2, just: "left", size: 46, track: 160, maxw: w * 0.62 }
      : { y: pos[1] - h / 2 - 40, x: pos[0], size: 46, track: 140, maxw: n == 1 ? 900 : 390 }));
    if (g("value", true) !== false) {
      var vt = label("0", a0, b, hz ? { y: pos[1] - h / 2 - 26, x: pos[0] + w / 2, just: "right", size: 58, font: "Inter-Bold", track: 0, color: [0.93, 0.99, 1] }
        : { y: pos[1] + h / 2 + 100, x: pos[0], size: 80, font: "Inter-Bold", track: 0, color: [0.93, 0.99, 1] });
      vt.property("Source Text").expression = lv + JSON.stringify(g("prefix", "")) + "+v.toFixed(" + g("decimals", 0) + ")+" + JSON.stringify(g("suffix", ""));
      ls.push(vt);
    }
    for (var j = 0; j < ls.length; j++) fade(ls[j], a0, b, 0.4, 0.3);
    sfx(rc, "chime", 0.3, { d: 1.5, f: 988 - i * 247 });
  }
};

// grafico de barras animado (2 a 4): barras crescem e o numero conta junto; down = barras para baixo (perda)
// bars*: [{label, value, color}], at, reach, stagger 0.3, suffix "%", prefix "", decimals 0, max (auto), title, source, show
TPL.bars = function (sc) {
  var bs = sc.bars, n = bs.length, a0 = T(sc, sc.show, "start"), at = T(sc, sc.at, "start+0.5"), rc = T(sc, sc.reach, at - sc.s + 1.6), b = T(sc, sc.until, "end+0.3");
  if (RC) return barsRC(sc, a0, at, b);
  var dn = !!sc.down, stg = opt(sc, "stagger", 0.3), HH = vh(540, 440), base = dn ? vh(660, 300) : vh(1180, 800), mx = opt(sc, "max", 0), dec = opt(sc, "decimals", 0), ls = [];
  var area = vh(800, 1100), x0 = CX - area / 2;  // vertical: 140..940
  for (var i = 0; i < n; i++) mx = Math.max(mx, Math.abs(bs[i].value) * 1.12);
  if (sc.bg !== false) holoBg(a0 - 0.1, b);
  enterWhoosh(sc, a0);
  if (sc.title) ls.push(label(sc.title, a0, b, { y: vh(470, 150), size: 74, font: "Anton", track: 40, color: [0.94, 0.98, 1] }));
  for (var k = 1; k <= 4; k++) { var gy = base + (dn ? 1 : -1) * HH * k / 4; fade(vec("gridline", a0, b, { path: [[x0 - 10, gy], [x0 + area + 10, gy]], stroke: [0.3, 0.7, 0.75], sw: 2, dash: [6, 10], cap: 1 }).l, a0, b, 0.4, 0.3, 40); }
  ls.push(vec("baseline", a0, b, { path: [[x0 - 30, base], [x0 + area + 30, base]], stroke: [0.6, 0.92, 0.95], sw: 4 }).l);
  var bw = Math.min(190, area / n * 0.6), pre = JSON.stringify(opt(sc, "prefix", "")), suf = JSON.stringify(opt(sc, "suffix", "%"));
  for (var i = 0; i < n; i++) {
    var B = bs[i], xc = x0 + area * (i + 0.5) / n, c = B.color || [CYAN, AMBER, MAGENTA, TEAL][i % 4], ai = at + i * stg, hk = HH * Math.abs(B.value) / mx;
    var e = EZ + "var e=ez((time-" + ai + ")/" + (rc - at) + "); ";
    var br = vec("bar", a0, b, { rect: [bw, 10], round: 10, fill: c, stroke: mixv(c, WHITE, 0.5), sw: 3, pos: [xc, base] });
    br.shape.property("Size").expression = e + "[" + bw + "," + hk + "*e+0.01]";
    br.shape.property("Position").expression = e + "[0," + (dn ? "" : "-") + hk / 2 + "*e]";
    ls.push(br.l);
    var vt = label("0", ai, b, { y: base, x: xc, size: 64, font: "Inter-Bold", track: 0, color: mixv(c, WHITE, 0.5) });
    vt.property("Source Text").expression = e + pre + "+(" + Math.abs(B.value) + "*e).toFixed(" + dec + ")+" + suf;
    tr(vt, "Position").expression = e + "[" + xc + "," + base + (dn ? "+" + hk + "*e+72" : "-" + hk + "*e-26") + "]";
    ls.push(vt);
    if (B.label) ls.push(label(B.label, a0, b, { y: dn ? base - 30 : base + 64, x: xc, size: 46, track: 40, maxw: area / n - 16 }));
  }
  if (sc.source) ls.push(label(sc.source, a0, b, { y: vh(1420, 915), size: vh(30, 28), font: "Inter", track: 20, color: [0.6, 0.7, 0.74] }));
  for (var j = 0; j < ls.length; j++) fade(ls[j], a0, b, 0.4, 0.3);
  sfx(at, "rise", 0.25, { d: rc - at }); sfx(rc + (n - 1) * stg, "chime", 0.4, { d: 1.8, f: 1047 });
};

// tema: uma cor por grafico (color, padrao vermelho #b8463b), highlight = indice da barra em cor cheia (as outras cinza);
// cada barra cresce em 0,6 s e o valor aparece pronto quando ela para; sem grade; titulo e fonte como rotulos
function barsRC(sc, a0, at, b) {
  var bs = sc.bars, n = bs.length, stg = opt(sc, "stagger", 0.3), dec = opt(sc, "decimals", 0), c = sc.color ? pal(sc.color) : TH.bar, hi = sc.highlight;
  var x0 = vh(110, 170), x1 = W - x0, top = vh(560, 300), base = vh(1300, H - 265), gap = vh(50, 90), bw = (x1 - x0 - gap * (n - 1)) / n, mx = opt(sc, "max", 0), ls = [];
  for (var i = 0; i < n; i++) mx = Math.max(mx, Math.abs(bs[i].value) / 0.88);
  if (sc.bg !== false) holoBg(a0 - 0.1, b);
  enterWhoosh(sc, a0);
  if (sc.title) ls.push(label(String(sc.title).toUpperCase(), a0, b, { y: top - vh(120, 124), x: x0, just: "left", size: 26, color: TH.lbl, raw: true, track: 200, maxw: x1 - x0 }));
  ls.push(vec("axis", a0, b, { path: [[x0, base], [x1, base]], stroke: TH.axis, raw: true, sw: 2, cap: 1 }).l);
  for (var i = 0; i < n; i++) {
    var B = bs[i], xc = x0 + bw / 2 + i * (bw + gap), ai = at + i * stg, hk = (base - top) * Math.abs(B.value) / mx, col = hi == null || hi == i ? c : TH.dim;
    var br = vec("bar", a0, b, { rect: [bw, 10], fill: col, raw: true, pos: [xc, base] });
    KE(br.shape.property("Size"), ai, 0.6, [bw, 0.01], [bw, hk], eoExpo); KE(br.shape.property("Position"), ai, 0.6, [0, 0], [0, -hk / 2], eoExpo);
    ls.push(br.l);
    var vt = label(opt(sc, "prefix", "") + Math.abs(B.value).toFixed(dec) + opt(sc, "suffix", "%"), a0, b, { y: base - hk - 18, x: xc - bw / 2, just: "left", size: vh(46, 54), font: "Inter-Bold", color: TH.ink, raw: true, track: 0, maxw: bw + gap - 10 });
    K(tr(vt, "Opacity"), [[ai + 0.55, 0], [ai + 0.75, 100], [b - 0.18, 100], [b, 0]]);
    if (B.label) ls.push(label(String(B.label).toUpperCase(), a0, b, { y: base + 50, x: xc - bw / 2, just: "left", size: 24, color: TH.mute, raw: true, track: 200, maxw: bw + gap - 10 }));
  }
  for (var j = 0; j < ls.length; j++) fade(ls[j], a0, b, 0.4, 0.25);
  if (sc.source) srcLine(sc.source, a0 + 0.3, b);
  sfx(at, "rise", 0.2, { d: 0.6 + (n - 1) * stg }); sfx(at + 0.6 + (n - 1) * stg, "chime", 0.3, { d: 1.8, f: 1047 });
}

// cartao de aviso: icone (circulo com "!") + 1-3 linhas; entra suave
// lines*: ["texto", ...] ou [{text, size, font, color}] (1a linha Anton 78, demais Inter 42); at, until, color (ambar), y 900, icon (false = sem)
TPL.end_card = function (sc) {
  var a = T(sc, sc.at, "start+0.2"), b = T(sc, sc.until, "end+0.3"), C = opt(sc, "color", AMBER), y = opt(sc, "y", vh(900, 500)), rows = [], hs = 0, kids = [];
  if (sc.bg !== false) holoBg(sc.s - 0.1, b);
  enterWhoosh(sc, a);
  for (var i = 0; i < sc.lines.length; i++) {
    var o = typeof sc.lines[i] == "string" ? { text: sc.lines[i] } : sc.lines[i];
    rows.push({ text: o.text, size: o.size || (i ? 46 : 80), font: o.font || (i ? "Inter SemiBold" : "Anton"), color: o.color || (i ? [0.82, 0.9, 0.94] : [1, 0.96, 0.9]) });
    hs += rows[i].size * 1.3;
  }
  var ic = sc.icon !== false, ph = 60 + (ic ? 170 : 0) + hs + 40, top = y - ph / 2, R = rig("card", a, b);
  kids.push(vec("card", a, b, { rect: [vh(960, 1160), ph], round: 40, fill: [0.015, 0.05, 0.065], fop: 92, stroke: mixv(C, [0, 0, 0], 0.25), sw: 3, pos: [CX, y] }).l);
  if (ic) {
    var iy = top + 60 + 56, gl = vec("icon glow", a, b, { ellipse: [150, 150], fill: C, blur: 30, add: true, pos: [CX, iy] }).l;
    tr(gl, "Opacity").expression = fadeX(a, b, 0.5, 0.4) + "*(30+12*Math.sin(time*2.5))";
    kids.push(gl, vec("icon", a, b, { ellipse: [112, 112], stroke: C, sw: 8, pos: [CX, iy] }).l, label("!", a, b, { y: iy + 32, size: 86, font: "Anton", track: 0, color: C }));
  }
  var yy = top + 60 + (ic ? 170 : 0);
  for (var i = 0; i < rows.length; i++) { yy += rows[i].size * 1.02; kids.push(label(rows[i].text, a, b, { y: yy, size: rows[i].size, font: rows[i].font, color: rows[i].color, track: i ? 10 : 30, maxw: vh(860, 1060), title: !i })); yy += rows[i].size * 0.28; }
  for (var j = 0; j < kids.length; j++) if (kids[j].name != "icon glow") fade(kids[j], a, b, 0.5, 0.4);
  adopt(R, kids); KS(tr(R, "Position"), [[a, [CX, CY + 50]], [a + 0.6, [CX, CY]]]);
  sfx(a + 0.1, "chime", 0.35, { d: 2.2, f: 523 });
};

// ================= modelos para o video longo (funcionam nos dois formatos) =================
// quebra em linhas pela largura estimada da fonte (o label() ainda encolhe se a estimativa errar)
function wrapText(str, size, maxw, font, maxLines, raw) {
  var cw = size * (font == "Anton" ? 0.5 : 0.58), ws = String(str).split(" "), out = [], cur = "";
  for (var i = 0; i < ws.length; i++) { var t = cur ? cur + " " + ws[i] : ws[i]; if (t.length * cw > maxw && cur) { out.push(cur); cur = ws[i]; } else cur = t; }
  if (cur) out.push(cur);
  while (maxLines && out.length > maxLines) { var last = out.pop(); out[out.length - 1] += " " + last; }
  // equilibra: estreita a largura enquanto o numero de linhas nao muda (evita uma palavra sozinha na ultima linha)
  if (out.length > 1 && !raw) for (var w = maxw * 0.95; w > maxw * 0.4; w *= 0.95) { var r = wrapText(str, size, w, font, 0, true); if (r.length != out.length) break; out = r; }
  return out;
}
// bloco de linhas centrado: devolve as camadas; y = linha de base da 1a linha
function textLines(str, a, b, o) {
  var size = o.size, ls = wrapText(str, size, o.maxw, o.font, o.max || 3), r = [];
  for (var i = 0; i < ls.length; i++) r.push(label(ls[i], a, b, { y: o.y + i * size * (o.lead || 1.12), x: opt(o, "x", CX), just: o.just, size: size, font: o.font, color: o.color, track: opt(o, "track", 0), maxw: o.maxw, title: o.title, raw: o.raw }));
  r.h = ls.length * size * (o.lead || 1.12);
  return r;
}
// entra com foco (desfoque -> nitido), sobe dy px e some no fim
function reveal(l, t, b, dy, blur) {
  var p = tr(l, "Position").value;
  KS(tr(l, "Position"), [[t, [p[0], p[1] + (dy || 0)]], [t + 0.6, p]]);
  fade(l, t, b, 0.45, 0.4);
  if (blur) K(P(fx(l, "Gaussian Blur", {}), "Blurriness"), [[t, blur], [t + 0.6, 0]]);
  return l;
}
// duas linhas que nascem perto do centro e se abrem para os lados (gap = meia distancia do centro, len = comprimento)
function splitLine(y, gap, len, a, b, C) {
  for (var s = -1; s <= 1; s += 2) {
    var ln = vec("split line", a, b, { path: [[CX + s * gap, y], [CX + s * (gap + len), y]], stroke: C, sw: 3, trim: true });
    K(ln.trim.property("End"), [[a, 0], [a + 0.7, 100]]); fade(ln.l, a, b, 0.1, 0.4);
  }
}
function bgOr(sc, a, b) {
  if (sc.image) { var im = cover(sc.image, a, b, opt(sc, "scale", 1), null, true); K(tr(im.l, "Opacity"), [[a, 0], [a + 0.5, opt(sc, "image_opacity", 35)], [b - 0.3, opt(sc, "image_opacity", 35)], [b, 0]]); fx(im.l, "Gaussian Blur", { "Blurriness": 4 }); K(tr(im.l, "Scale"), [[a, [im.s * 100, im.s * 100]], [b, [im.s * 106, im.s * 106]]]); }
  else if (sc.bg !== false) holoBg(a, b);
}

// cartao de capitulo: numero fantasma grande, "CHAPTER 2", linha que se abre e titulo entrando em foco (2-3 s)
// num, title*, kicker ("CHAPTER " + num), sub, at ("start"), until ("end+0.3"), color CYAN, image (fundo escurecido), y
TPL.chapter_card = function (sc) {
  var a = T(sc, sc.at, "start"), b = T(sc, sc.until, "end+0.3"), C = opt(sc, "color", CYAN), y = opt(sc, "y", CY + vh(0, 20)), ls = [];
  var num = sc.num == null ? null : (typeof sc.num == "number" && sc.num < 10 ? "0" : "") + sc.num;
  bgOr(sc, a - 0.1, b);
  if (num) {
    var gs = vh(520, 460), gn = label(num, a, b, { y: y + gs * 0.36, size: gs, font: "Anton", track: 0, color: mixv(C, [0, 0, 0], 0.55) });
    K(tr(gn, "Opacity"), [[a, 0], [a + 0.8, 45], [b - 0.4, 45], [b, 0]]);
    K(tr(gn, "Scale"), [[a, [92, 92]], [b, [104, 104]]]);
  }
  var ky = y - vh(150, 130), kt = label(opt(sc, "kicker", num ? "CHAPTER " + sc.num : ""), a, b, { y: ky, size: vh(38, 34), track: 520, color: mixv(C, WHITE, 0.35) });
  reveal(kt, a + 0.1, b, 18, 0);
  splitLine(ky + 36, 0, vh(180, 220), a + 0.25, b, C);
  var ts = opt(sc, "size", vh(120, 128)), tl = textLines(String(sc.title).toUpperCase(), a, b, { y: ky + 60 + ts * 0.82, size: ts, font: "Anton", maxw: W - vh(120, 360), color: [0.97, 0.99, 1], track: 20, max: 2, lead: 1.05, title: true });
  for (var i = 0; i < tl.length; i++) reveal(tl[i], a + 0.4 + i * 0.12, b, 30, 22);
  if (sc.sub) reveal(label(sc.sub, a, b, { y: ky + 60 + tl.h + vh(40, 30), size: vh(44, 40), color: [0.75, 0.86, 0.9], track: 20 }), a + 0.8, b, 16, 0);
  sfx(a + 0.05, "rise", 0.3, { d: 0.8 }); sfx(a + 0.45, "thud", 0.45); sfx(a + 0.5, "chime", 0.25, { d: 2.2, f: 392 });
};

// rotulo de fonte/dado no canto: barra de destaque + caixa + texto (sem fundo; vai por cima de outra cena)
// text*, sub, at ("start+0.5"), until ("end"), corner "bl" | "br" | "tl" | "tr", color CYAN
TPL.lower_third = function (sc) {
  var a = T(sc, sc.at, "start+0.5"), b = T(sc, sc.until, "end"), C = opt(sc, "color", CYAN), cn = opt(sc, "corner", "bl");
  var lf = cn.charAt(1) == "l", m = vh(60, 80), x0 = lf ? m : W - m, y0 = cn.charAt(0) == "b" ? vh(1390, 870) : vh(240, 120);
  if (RC) {  // tema: fio vertical de 4 px (cor do ato ou color), titulo Inter 600 40, sub Inter 30, sem caixa
    var dr = lf ? 1 : -1, tx = x0 + dr * 22, rc = sc.color ? pal(sc.color) : ACT_COL[sc.act] || TH.lbl, mw = vh(860, 820);
    var t1 = label(sc.text, a, b, { y: y0, x: tx, just: lf ? "left" : "right", size: 40, color: TH.ink, raw: true, track: 0, maxw: mw });
    var t2 = sc.sub ? label(String(sc.sub).replace(/^source:\s*/i, "Source · "), a, b, { y: y0 + 46, x: tx, just: lf ? "left" : "right", size: 30, font: "Inter", color: TH.ink2, raw: true, track: 0, maxw: mw }) : null;
    var hgt = 40 * 1.25 + (t2 ? 46 : 0), cy = y0 - 40 * 0.9 + hgt / 2, R = rig("lower third", a, b, [x0, cy]);
    var bar = vec("lt rule", a, b, { rect: [4, hgt], fill: rc, raw: true, pos: [x0, cy] }).l;
    K(tr(bar, "Scale"), [[a, [100, 0]], [a + 0.25, [100, 100]]]);
    var kids = [bar, t1]; if (t2) kids.push(t2);
    for (var i = 0; i < kids.length; i++) fade(kids[i], a, b, i ? 0.35 : 0.1, 0.2);
    adopt(R, kids); KS(tr(R, "Position"), [[a, [x0 - dr * 30, cy]], [a + 0.4, [x0, cy]]]);
    return;
  }
  var s1 = vh(36, 34), s2 = vh(28, 26), mw = vh(860, 900), dr = lf ? 1 : -1, tx = x0 + dr * 30;
  var t1 = label(sc.text, a, b, { y: y0, x: tx, just: lf ? "left" : "right", size: s1, color: [0.95, 0.99, 1], track: 30, maxw: mw });
  var t2 = sc.sub ? label(sc.sub, a, b, { y: y0 + s2 * 1.45, x: tx, just: lf ? "left" : "right", size: s2, font: "Inter", color: [0.7, 0.82, 0.86], track: 20, maxw: mw }) : null;
  var w = Math.max(t1.sourceRectAtTime(a + 0.01, false).width * tr(t1, "Scale").value[0] / 100, t2 ? t2.sourceRectAtTime(a + 0.01, false).width * tr(t2, "Scale").value[0] / 100 : 0);
  var hgt = s1 * 1.6 + (t2 ? s2 * 1.45 : 0), cy = y0 - s1 * 0.95 + hgt / 2, R = rig("lower third", a, b, [x0, cy]);
  var box = vec("lt box", a, b, { rect: [w + 60, hgt], round: 6, fill: [0.01, 0.045, 0.06], fop: 78, pos: [x0 + dr * (w + 60) / 2, cy] }).l;
  var bar = vec("lt bar", a, b, { rect: [6, hgt], fill: C, pos: [x0, cy] }).l;
  box.moveAfter(t1); bar.moveAfter(t1);  // caixa atras do texto (o texto foi criado antes para medir a largura)
  K(tr(bar, "Scale"), [[a, [100, 0]], [a + 0.25, [100, 100]]]);
  var kids = [box, bar, t1]; if (t2) kids.push(t2);
  for (var i = 0; i < kids.length; i++) fade(kids[i], a, b, i == 1 ? 0.1 : 0.35, 0.3);
  adopt(R, kids); KS(tr(R, "Position"), [[a, [x0 - dr * 40, cy]], [a + 0.45, [x0, cy]]]);
};
TPL.lower_third.overlay = true;  // montado depois do acabamento: fica nitido e a vinheta nao escurece o canto

// cartao de numero grande (respiro entre cenas densas): big (texto) ou to (numero que conta), frase e fonte
// big | to (+ from 0, prefix, suffix, decimals, reach), text, source, at ("start+0.2"), until ("end+0.3"), color AMBER, y
TPL.fact_card = function (sc) {
  var a = T(sc, sc.at, "start+0.2"), b = T(sc, sc.until, "end+0.3"), C = opt(sc, "color", AMBER), y = opt(sc, "y", CY + vh(-60, -40)), bs = opt(sc, "size", vh(230, 220));
  if (RC) return factRC(sc, a, b);
  bgOr(sc, sc.s - 0.1, b);
  enterWhoosh(sc, a);
  var gl = vec("fact glow", a, b, { ellipse: [vh(900, 1100), bs * 1.6], fill: C, blur: 90, add: true, pos: [CX, y - bs * 0.35] }).l;
  K(tr(gl, "Opacity"), [[a, 0], [a + 0.5, 22], [b - 0.3, 22], [b, 0]]);
  var big = label(sc.to != null ? String(sc.to) : sc.big, a, b, { y: y, size: bs, font: "Anton", track: 10, color: mixv(C, WHITE, 0.2) });
  if (sc.to != null) {
    var rc = T(sc, sc.reach, a - sc.s + 1.4);
    big.property("Source Text").expression = EZ + "var v=" + opt(sc, "from", 0) + "+(" + (sc.to - opt(sc, "from", 0)) + ")*ez((time-" + a + ")/" + (rc - a) + "); " + JSON.stringify(opt(sc, "prefix", "")) + "+v.toFixed(" + opt(sc, "decimals", 0) + ").replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',')+" + JSON.stringify(opt(sc, "suffix", ""));
    sfx(rc, "chime", 0.35, { d: 1.8, f: 988 });
  }
  K(tr(big, "Scale"), [[a, [118, 118]], [a + 0.25, [100, 100]]]); fade(big, a, b, 0.25, 0.4);
  var yy = y + vh(110, 95);
  if (sc.text) { var tl = textLines(sc.text, a, b, { y: yy, size: vh(52, 48), font: "Inter SemiBold", maxw: vh(940, 1300), color: [0.9, 0.96, 0.98], max: 3 }); for (var i = 0; i < tl.length; i++) reveal(tl[i], a + 0.35 + i * 0.1, b, 16, 0); yy += tl.h; }
  if (sc.source) {
    var sl = vec("fact rule", a + 0.6, b, { path: [[CX - 60, yy + 6], [CX + 60, yy + 6]], stroke: mixv(C, [0, 0, 0], 0.3), sw: 2 }).l; fade(sl, a + 0.6, b, 0.3, 0.4);
    reveal(label(sc.source, a, b, { y: yy + 56, size: vh(30, 28), font: "Inter", color: [0.62, 0.72, 0.76], track: 20, maxw: vh(940, 1300) }), a + 0.7, b, 10, 0);
  }
  HITS.push(a + 0.05); sfx(a, "thud", 0.6);
};

// tema: numero pronto (Inter 700) sobe de tras de uma mascara em 0,4 s; traco de 520 px corre embaixo; frase e fonte depois.
// Alinhado a esquerda (x 170). color = cor do traco (padrao vermelho; verde para dado da lei). Saida 40% mais curta que a entrada.
function factRC(sc, a, b) {
  var x = opt(sc, "x", vh(110, 170)), bs = opt(sc, "size", vh(150, 170)), y = opt(sc, "y", CY - vh(20, 30)), rc = sc.color ? pal(sc.color) : TH.red;
  bgOr(sc, sc.s - 0.1, b);
  enterWhoosh(sc, a);
  var val = sc.to != null ? opt(sc, "prefix", "") + Number(sc.to).toFixed(opt(sc, "decimals", 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ",") + opt(sc, "suffix", "") : sc.big;
  var n = label(val, a, b, { y: y, x: x, just: "left", size: bs, font: "Inter-Bold", color: TH.ink, raw: true, track: -10, maxw: W - 2 * x });
  var mt = vec("num matte", a, b, { rect: [W, bs * 1.3], fill: [1, 1, 1], raw: true, pos: [CX, y - bs * 0.4] }).l;
  n.setTrackMatte(mt, TrackMatteType.ALPHA);
  KE(tr(n, "Position"), a, 0.4, [x, y + bs * 1.05], [x, y], eoExpo);
  K(tr(n, "Opacity"), [[b - 0.24, 100], [b, 0]]);
  var ry = y + vh(36, 44), ln = vec("fact rule", a + 0.3, b, { path: [[x, ry], [x + 520, ry]], stroke: rc, raw: true, sw: 3, cap: 1, trim: true });
  KE(ln.trim.property("End"), a + 0.3, 0.5, 0, 100, eioQuart); K(tr(ln.l, "Opacity"), [[b - 0.18, 100], [b, 0]]);
  if (sc.text) { var tl = textLines(sc.text, a, b, { y: ry + 64, x: x, just: "left", size: vh(34, 38), font: "Inter", maxw: vh(860, 1100), color: TH.ink2, raw: true, max: 3, lead: 1.3 }); for (var i = 0; i < tl.length; i++) fade(tl[i], a + 0.55, b, 0.25, 0.15); }
  if (sc.source) srcLine(sc.source, a + 0.7, b, HZ ? 96 : x);
  sfx(a, "thud", 0.5);
}

// trecho de documento (pessoa sem foto): folha de papel, cabecalho e corpo em Courier Prime, marca-texto que corre da esquerda
// para a direita em hl_at, trecho final apagado (40%), coluna a direita com o nome. So horizontal. Camera: so zoom centrado lento.
// text*, header ["Federal Communications Commission", "FCC 18-58"], highlight (trecho exato do text), hl_at, hl_dur 0.8, fade (trecho do text
// ate o fim que fica em 40%), kicker, name, role, source, at ("start"), until ("end+0.3"), zoom [100, 106]
TPL.doc_excerpt = function (sc) {
  if (!HZ) throw new Error("doc_excerpt: so no formato horizontal");
  var a = T(sc, sc.at, "start"), b = T(sc, sc.until, "end+0.3"), z = opt(sc, "zoom", [100, 106]), D = TH.doc, kids = [];
  bgOr(sc, sc.s - 0.1, b);
  enterWhoosh(sc, a);
  var px = 230, pw = 1060, pt = 120, pad = 80, fs = 30, cw = fs * 0.6, lh = fs * 1.55, tx = px + pad, cols = Math.floor((pw - 2 * pad) / cw);
  var sh = vec("paper shadow", a, b, { rect: [pw, H], fill: [0, 0, 0], fop: 65, raw: true, blur: 50, pos: [px + pw / 2, pt + H / 2 + 30] }).l;
  var pp = vec("paper", a, b, { rect: [pw, H], fill: TH.paper, raw: true, pos: [px + pw / 2, pt + H / 2] }).l;
  kids.push(sh, pp);
  var hd = sc.header || [], hy = pt + 70 + 18;
  if (hd[0]) kids.push(label(hd[0], a, b, { y: hy, x: tx, just: "left", size: 24, font: "Courier Prime Bold", color: D, raw: true, track: 0, maxw: (pw - 2 * pad) * (hd[1] ? 0.7 : 1) }));
  if (hd[1]) kids.push(label(hd[1], a, b, { y: hy, x: px + pw - pad, just: "right", size: 24, font: "Courier Prime Bold", color: D, raw: true, track: 0, maxw: (pw - 2 * pad) * 0.28 }));
  if (hd.length) { var hr = vec("header rule", a, b, { path: [[tx, hy + 16], [px + pw - pad, hy + 16]], stroke: D, raw: true, sw: 2, cap: 1 }).l; kids.push(hr); }
  // quebra por caracteres (fonte mono: cada caractere tem 0,6 em), guardando onde cada linha comeca no texto
  var str = String(sc.text).replace(/\s+/g, " "), ws = str.split(" "), lines = [], cur = "", st = 0, pos = 0;
  for (var i = 0; i < ws.length; i++) { if (cur && (cur + " " + ws[i]).length > cols) { lines.push([st, cur]); st = pos; cur = ws[i]; } else cur = cur ? cur + " " + ws[i] : ws[i]; pos += ws[i].length + 1; }
  if (cur) lines.push([st, cur]);
  function find(k) { if (!sc[k]) return -1; var j = str.indexOf(sc[k].replace(/\s+/g, " ")); if (j < 0) throw new Error("doc_excerpt: " + k + " nao esta no text: " + sc[k]); return j; }
  var hs = find("highlight"), he = hs < 0 ? -1 : hs + sc.highlight.replace(/\s+/g, " ").length, fs0 = find("fade"), y0 = (hd.length ? hy + 16 + 34 : pt + 70) + fs * 0.8;
  if (hs >= 0) {  // marca-texto antes do texto (fica atras); corre linha a linha
    var th = T(sc, sc.hl_at, "start+1.0"), hd2 = opt(sc, "hl_dur", 0.8), tot = he - hs, done = 0;
    for (var i = 0; i < lines.length; i++) {
      var s0 = Math.max(lines[i][0], hs), e0 = Math.min(lines[i][0] + lines[i][1].length, he);
      if (e0 <= s0) continue;
      var w = (e0 - s0) * cw + 8, t0 = th + hd2 * done / tot, t1 = th + hd2 * (done + e0 - s0) / tot; done += e0 - s0;
      var mk = vec("highlight", a, b, { rect: [w, fs * 1.2], fill: TH.hl, raw: true, pos: [tx + (s0 - lines[i][0]) * cw - 4 + w / 2, y0 + i * lh - fs * 0.32] });
      K(mk.shape.property("Size"), [[t0, [0.01, fs * 1.2]], [t1, [w, fs * 1.2]]]); K(mk.shape.property("Position"), [[t0, [-w / 2, 0]], [t1, [0, 0]]]);
      kids.push(mk.l);
    }
    sfx(th, "whoosh", 0.15, { d: hd2 });
  }
  for (var i = 0; i < lines.length; i++) {
    var ls = lines[i][0], L = lines[i][1], cut = fs0 < 0 ? L.length : Math.max(0, Math.min(L.length, fs0 - ls)), y = y0 + i * lh;
    if (cut > 0) kids.push(label(L.substr(0, cut), a, b, { y: y, x: tx, just: "left", size: fs, font: "Courier Prime", color: D, raw: true, track: 0, maxw: 9999 }));
    if (cut < L.length) { var fl = label(L.substr(cut), a, b, { y: y, x: tx + cut * cw, just: "left", size: fs, font: "Courier Prime", color: D, raw: true, track: 0, maxw: 9999 }); fl.name = "faded"; kids.push(fl); }
  }
  var R = rig("doc cam", a, b);
  for (var i = 0; i < kids.length; i++) fade(kids[i], a, b, 0.4, 0.25, kids[i].name == "faded" ? 40 : kids[i].name == "header rule" ? 33 : 100);
  adopt(R, kids);
  KS(tr(R, "Position"), [[a, [CX, CY + 24]], [a + 0.5, [CX, CY]]]);
  K(tr(R, "Scale"), [[a, [z[0], z[0]]], [b, [z[1], z[1]]]]);
  // coluna do nome (fora da camera)
  var nx = 1330, nw = 480, ny = 400;
  if (sc.kicker) { fade(label(String(sc.kicker).toUpperCase(), a, b, { y: ny, x: nx, just: "left", size: 26, color: TH.lbl, raw: true, track: 200, maxw: nw }), a + 0.3, b, 0.3, 0.2); ny += 36; }
  if (sc.name) { var nl = textLines(String(sc.name).toUpperCase(), a, b, { y: ny + 62, x: nx, just: "left", size: 72, font: "Anton", title: true, color: TH.ink, raw: true, maxw: nw, max: 3, lead: 1.0, track: 10 }); for (var i = 0; i < nl.length; i++) reveal(nl[i], a + 0.4 + i * 0.08, b, 16, 0); ny += 62 + nl.h; }
  if (sc.role) { var rl = textLines(sc.role, a, b, { y: ny + 20, x: nx, just: "left", size: 28, font: "Inter", color: TH.ink2, raw: true, maxw: nw, max: 3, lead: 1.35 }); for (var i = 0; i < rl.length; i++) reveal(rl[i], a + 0.6, b, 10, 0); }
  if (sc.source) srcLine(sc.source, a + 0.7, b, nx);
};

// print real de pagina (noticia, ordem, registro) num cartao claro sobre o fundo; sem moldura de navegador, so zoom centrado
// image* (assets/clips/ ou assets/img/), crop [x,y,w,h] (px da imagem), site, date, marks [{box:[x,y,w,h] px da imagem, at, color}] (ate 3),
// source, at ("start"), until ("end+0.3"), zoom [100, 108]
TPL.web_clip = function (sc) {
  var a = T(sc, sc.at, "start"), b = T(sc, sc.until, "end+0.3"), z = opt(sc, "zoom", [100, 108]), kids = [];
  if (sc.bg !== false) holoBg(sc.s - 0.1, b);
  enterWhoosh(sc, a);
  var file = String(sc.image); if (file.indexOf("/") < 0 && !new File(IMG + "/" + file).exists) file = "../clips/" + file;
  var im = photo(file, a, b), iw = im.source.width, ih = im.source.height, hb = CLIPS[sc.image];
  // sem crop: so a manchete (caixa do .json do print), recorte justo; a folga vem de uma margem branca desenhada,
  // nunca de mais pagina (pegaria menu, etiqueta ou propaganda colados no titulo)
  var auto = !sc.crop && hb, c = sc.crop || (hb ? [Math.max(0, hb[0] - 6), Math.max(0, hb[1] - 4), Math.min(iw - hb[0] + 6, hb[2] + 12), Math.min(ih - hb[1] + 4, hb[3] + 8)] : [0, 0, iw, ih]);
  // moldura (paper): no tema, papel #ece4d0; fora dele, branco. paper: false = sem moldura no crop / branca no automatico; "#rrggbb" ou [r,g,b] troca a cor
  var frame = auto || (sc.paper != null && sc.paper !== false), pc = sc.paper && sc.paper !== true ? (typeof sc.paper == "string" ? hx(sc.paper) : sc.paper) : RC && sc.paper !== false ? TH.paper : [1, 1, 1];
  var px = frame ? vh(32, 56) : 0, py = frame ? vh(28, 40) : 0;  // no Short a margem e menor: a manchete ganha largura
  var top = HZ ? 215 : 330, bot = HZ ? (SPEC.captions !== false ? CAP_Y - 175 : H - 150) : 1500;  // folga para a linha de fonte mesmo com o zoom de 108
  var k = Math.min(((HZ ? 1500 : 960) - 2 * px) / c[2], (bot - top - 2 * py) / c[3]), cw = c[2] * k, ch = c[3] * k, cy = (top + bot) / 2, l0 = CX - cw / 2, t0 = cy - ch / 2;
  tr(im, "Anchor Point").setValue([c[0] + c[2] / 2, c[1] + c[3] / 2]); tr(im, "Position").setValue([CX, cy]); tr(im, "Scale").setValue([k * 100, k * 100]);
  var sh = vec("clip shadow", a, b, { rect: [cw + 2 * px, ch + 2 * py], round: 8, fill: [0, 0, 0], fop: 60, raw: true, blur: 40, pos: [CX, cy + 18] }).l;
  sh.moveAfter(im);
  kids.push(sh);
  if (frame) { var pp = vec("clip paper", a, b, { rect: [cw + 2 * px, ch + 2 * py], round: 8, fill: pc, raw: true, pos: [CX, cy] }).l; pp.moveAfter(im); kids.push(pp); }
  var mt = vec("clip matte", a, b, { rect: [cw, ch], round: frame ? 0 : 8, fill: [1, 1, 1], raw: true, pos: [CX, cy] }).l;
  im.setTrackMatte(mt, TrackMatteType.ALPHA);
  kids.push(im, mt);
  var ms = sc.marks || []; if (ms.length > 3) throw new Error("web_clip: no maximo 3 marks");
  for (var i = 0; i < ms.length; i++) {  // marca-texto (multiplicar) que corre da esquerda para a direita em 0,5 s
    var bx = ms[i].box; if (bx[0] < c[0] - 2 || bx[1] < c[1] - 2 || bx[0] + bx[2] > c[0] + c[2] + 2 || bx[1] + bx[3] > c[1] + c[3] + 2) continue;  // marca fora do recorte
    var w = bx[2] * k, h = bx[3] * k, x = l0 + (bx[0] - c[0]) * k, y = t0 + (bx[1] - c[1]) * k, tm = T(sc, ms[i].at, "start+1.0");
    var mk = vec("clip mark", a, b, { rect: [w, h], fill: ms[i].color || TH.hl, raw: true, pos: [x + w / 2, y + h / 2] });
    mk.l.blendingMode = BlendingMode.MULTIPLY; tr(mk.l, "Opacity").setValue(45);
    KE(mk.shape.property("Size"), tm, 0.5, [0.01, h], [w, h], eioQuart); KE(mk.shape.property("Position"), tm, 0.5, [-w / 2, 0], [0, 0], eioQuart);
    kids.push(mk.l); sfx(tm, "whoosh", 0.12, { d: 0.5 });
  }
  var hd = [sc.site, sc.date].join(" · ").replace(/^ · | · $/g, "").toUpperCase();
  if (hd) kids.push(label(hd, a, b, { y: t0 - py - 30, x: l0 - px, just: "left", size: 20, font: "Inter SemiBold", color: TH.lbl, raw: true, track: 160, maxw: cw + 2 * px }));
  for (var i = 0; i < kids.length; i++) if (kids[i] != mt) fade(kids[i], a, b, 0.3, 0.3, kids[i] == sh ? 60 : kids[i].name == "clip mark" ? 45 : 100);
  var R = rig("clip cam", a, b, [CX, cy]); adopt(R, kids);
  KE(tr(R, "Position"), a, 0.5, [CX, cy + 30], [CX, cy], eoExpo);
  K(tr(R, "Scale"), [[a, [z[0], z[0]]], [b, [z[1], z[1]]]]);
  if (sc.source) srcLine(sc.source, a + 0.7, b);
};

// video pronto (ex.: clipe do HyperFrames) como cena, sem audio. file* (assets/img ou assets/clips), from 0 (segundo do clipe no inicio),
// at ("start"), until ("end+0.3"), fit "cover"|"contain", hold (true: congela o ultimo quadro se a cena passar do clipe), fade [0.15, 0.15], source, bg
TPL.clip = function (sc) {
  var a = T(sc, sc.at, "start"), b = T(sc, sc.until, "end+0.3"), from = opt(sc, "from", 0), fd = opt(sc, "fade", [0.15, 0.15]), fit = opt(sc, "fit", "cover");
  if (fit == "contain" && sc.bg !== false) holoBg(sc.s - 0.1, b);
  enterWhoosh(sc, a);
  var file = String(sc.file); if (file.indexOf("/") < 0 && !new File(IMG + "/" + file).exists) file = "../clips/" + file;
  var l = photo(file, a, b), src = l.source, k = (fit == "contain" ? Math.min : Math.max)(W / src.width, H / src.height), end = src.duration - 1 / 30;
  try { l.audioEnabled = false; } catch (e) {}
  l.startTime = a - from; span(l, a, b);
  if (b > a + end - from && opt(sc, "hold", true)) {  // cena mais longa que o clipe: segue normal e para no ultimo quadro
    l.timeRemapEnabled = true; var tp = l.property("Time Remap");
    while (tp.numKeys) tp.removeKey(1);
    K(tp, [[a, from], [a + end - from, end], [b, end]]); span(l, a, b);
  }
  tr(l, "Scale").setValue([k * 100, k * 100]);
  fade(l, a, b, fd[0], fd[1]);
  if (sc.source) srcLine(sc.source, a + 0.3, b);
};

// mapa dos EUA (fronteiras do US Census, library/maps/us-states.json; geometria em assets/us_states.json, gerada pelo build.py).
// Estados nao citados ficam grafite #2a2c30; os citados acendem em 0,4 s (ease-out-expo) na cor do tom, sem brilho.
// states* [{code "CA", at, tone "scam"|"rule"|"neutral", value, label, dx, dy}] (value/label: numero N1 em Inter Bold e rotulo;
// dx/dy afastam o rotulo do centro do estado e ligam com um fio), title, source, at ("start"), until ("end+0.3"), zoom [100, 100], step 0.25, bg
TPL.us_map = function (sc) {
  var a = T(sc, sc.at, "start"), b = T(sc, sc.until, "end+0.3"), M = USMAP, z = opt(sc, "zoom", [100, 100]), st = sc.states || [], kids = [];
  var TONE = { scam: TH.red, rule: TH.green, neutral: TH.dim };
  if (sc.bg !== false) holoBg(sc.s - 0.1, b);
  enterWhoosh(sc, a);
  var x0 = vh(70, 230), x1 = W - x0, top = vh(560, 210), bot = vh(1200, SPEC.captions !== false ? CAP_Y - 150 : H - 110);
  var k = Math.min((x1 - x0) / M.w, (bot - top) / M.h), ox = CX - M.w * k / 2, oy = (top + bot) / 2 - M.h * k / 2;
  function pt(p) { return [ox + p[0] * k, oy + p[1] * k]; }
  function states(name, codes, fill, t0, t1) {  // uma camada com varios estados: um contorno por anel, preenchimento e fio comuns
    var l = comp.layers.addShape(); l.name = name;
    var gc = l.property("Contents").addProperty("ADBE Vector Group").property("Contents");
    for (var i = 0; i < codes.length; i++) {
      var S = M.s[codes[i]]; if (!S) throw new Error("us_map: estado desconhecido " + codes[i] + " (use a sigla, ex.: CA)");
      for (var r = 0; r < S.p.length; r++) {
        var vs = []; for (var j = 0; j < S.p[r].length; j++) vs.push(pt(S.p[r][j]));
        var sh = new Shape(); sh.vertices = vs; sh.closed = true; gc.addProperty("ADBE Vector Shape - Group").property("Path").setValue(sh);
      }
    }
    var so = gc.addProperty("ADBE Vector Graphic - Stroke"); so.property("Color").setValue(TH.bg); so.property("Stroke Width").setValue(1.5);
    gc.addProperty("ADBE Vector Graphic - Fill").property("Color").setValue(fill);
    tr(l, "Position").setValue([0, 0]); span(l, t0, t1); return l;
  }
  var all = []; for (var c in M.s) all.push(c);
  var base = states("map states", all, hx("#2a2c30"), a, b); fade(base, a, b, 0.4, 0.25); kids.push(base);
  for (var i = 0; i < st.length; i++) {
    var S = st[i], t = T(sc, S.at, a - sc.s + 0.6 + i * opt(sc, "step", 0.25)), col = TONE[S.tone || "neutral"];
    if (!col) throw new Error("us_map: tone deve ser scam, rule ou neutral (veio " + S.tone + ")");
    var l = states("map " + S.code, [S.code], col, t, b);
    KE(tr(l, "Opacity"), t, 0.4, 0, 100, eoExpo); K(tr(l, "Opacity"), [[b - 0.25, 100], [b, 0]]); kids.push(l);
    sfx(t, "whoosh", 0.12, { d: 0.5 });
    if (S.value == null && !S.label) continue;
    var c0 = pt(M.s[S.code].c), dx = opt(S, "dx", 0), dy = opt(S, "dy", 0), q = [Math.max(x0 + 60, Math.min(x1 - 60, c0[0] + dx)), c0[1] + dy], tv = t + 0.2;  // rotulo nunca sai pela borda
    if (dx || dy) {  // fio do centro do estado ate o rotulo
      var ln = vec("map leader", tv, b, { path: [c0, [q[0], q[1] + 14]], stroke: TH.lbl, raw: true, sw: 1.5, cap: 1, trim: true });
      KE(ln.trim.property("End"), tv, 0.3, 0, 100, eoExpo); fade(ln.l, tv, b, 0.01, 0.25); kids.push(ln.l);
      var dt = vec("map dot", tv, b, { ellipse: [8, 8], fill: TH.ink, raw: true, pos: c0 }).l; fade(dt, tv, b, 0.2, 0.25); kids.push(dt);
      q[1] -= S.value != null ? 6 : -20;
    }
    var vy = q[1], vs = vh(64, 52);
    if (S.value != null) {  // N1: o numero pronto sobe 0,4 s de tras de uma mascara
      var n = label(String(S.value), tv, b, { y: vy, x: q[0], size: vs, font: "Inter-Bold", color: TH.ink, raw: true, track: -10 });
      var mt = vec("map value matte", tv, b, { rect: [600, vs * 1.3], fill: [1, 1, 1], raw: true, pos: [q[0], vy - vs * 0.4] }).l;
      n.setTrackMatte(mt, TrackMatteType.ALPHA);
      KE(tr(n, "Position"), tv, 0.4, [q[0], vy + vs * 1.05], [q[0], vy], eoExpo); K(tr(n, "Opacity"), [[b - 0.24, 100], [b, 0]]);
      kids.push(n, mt);
    }
    if (S.label) { var lb = label(String(S.label).toUpperCase(), tv, b, { y: vy + (S.value != null ? vh(40, 32) : 0), x: q[0], size: vh(26, 20), color: TH.ink2, raw: true, track: 160, maxw: vh(700, 320) }); fade(lb, tv + 0.15, b, 0.25, 0.2); kids.push(lb); }
  }
  if (sc.title) { var ti = label(String(sc.title).toUpperCase(), a, b, { y: vh(top - 90, 170), x: vh(60, 170), just: "left", size: 26, color: TH.lbl, raw: true, track: 200, maxw: W - 2 * vh(60, 170) }); fade(ti, a, b, 0.4, 0.25); kids.push(ti); }
  var R = rig("map cam", a, b, [CX, (top + bot) / 2]); adopt(R, kids);
  K(tr(R, "Scale"), [[a, [z[0], z[0]]], [b, [z[1], z[1]]]]);
  if (sc.source) srcLine(sc.source, a + 0.5, b);
};

// cartao de citacao: aspas grandes, frase (ate 4 linhas), autor e fonte
// quote*, by, source, at ("start+0.2"), until ("end+0.3"), color CYAN, size (da frase)
TPL.quote_card = function (sc) {
  var a = T(sc, sc.at, "start+0.2"), b = T(sc, sc.until, "end+0.3"), C = opt(sc, "color", CYAN), qs = opt(sc, "size", vh(58, 56));
  bgOr(sc, sc.s - 0.1, b);
  enterWhoosh(sc, a);
  var ls = wrapText(sc.quote, qs, vh(900, 1300), "Inter SemiBold", 4), hh = ls.length * qs * 1.25, ms = vh(240, 220);
  var y1 = CY - hh / 2 + qs * 0.75 + vh(20, 10);  // linha de base da 1a linha; as aspas ficam logo acima
  if (RC) ms = vh(200, 180);
  var qm = label("“", a, b, { y: y1 - qs * 0.75 - 30 + 0.43 * ms, size: ms, font: RC ? "Inter-Bold" : "Anton", track: 0, color: RC ? TH.lbl : C, raw: RC }); fade(qm, a, b, 0.4, 0.4, 85);
  // header: cabecalho do registro (ex.: transcricao da audiencia) em Courier Prime acima das aspas
  if (sc.header) reveal(label(sc.header, a, b, { y: y1 - qs * 0.75 - 30 - ms * 0.45, size: vh(26, 26), font: "Courier Prime Bold", color: RC ? TH.ink2 : [0.8, 0.86, 0.9], raw: RC, track: 20, maxw: vh(940, 1400) }), a + 0.1, b, 10, 0);
  K(tr(qm, "Scale"), [[a, [70, 70]], [a + 0.3, [100, 100]]]);
  for (var i = 0; i < ls.length; i++) reveal(label(ls[i], a, b, { y: y1 + i * qs * 1.25, size: qs, color: [0.95, 0.98, 1], track: 0, maxw: vh(960, 1400) }), a + 0.25 + i * 0.12, b, 16, 12);
  var yy = y1 + hh + qs * 0.1;
  if (sc.by) { reveal(label("— " + sc.by, a, b, { y: yy, size: vh(38, 36), color: mixv(C, WHITE, 0.4), track: 40 }), a + 0.7, b, 10, 0); yy += vh(56, 52); }
  if (sc.source) reveal(label(sc.source, a, b, { y: yy, size: vh(28, 26), font: "Inter", color: [0.62, 0.72, 0.76], track: 20 }), a + 0.8, b, 10, 0);
  sfx(a + 0.1, "chime", 0.3, { d: 2.2, f: 523 });
};

// linha do tempo com 3-6 marcos que acendem em sequencia (horizontal no 16:9, vertical no 9:16)
// items*: [{date, label, at}], title, at (1o marco, "start+0.5"), step 0.8 (s entre marcos sem "at"), color CYAN, until
TPL.timeline = function (sc) {
  var it = sc.items, n = it.length, a0 = sc.s, b = T(sc, sc.until, "end+0.3"), C = opt(sc, "color", CYAN), t0 = T(sc, sc.at, "start+0.5"), st = opt(sc, "step", 0.8);
  if (sc.bg !== false) holoBg(a0 - 0.1, b);
  if (sc.title) fade(label(sc.title, a0, b, { y: vh(330, 160), size: 74, font: "Anton", track: 40, color: [0.94, 0.98, 1] }), a0, b, 0.4, 0.3);
  // eixo: horizontal x 160..W-160 em y 560; vertical y 470..1400 em x 190
  var p0 = HZ ? [160, 560] : [190, 470], p1 = HZ ? [W - 160, 560] : [190, 1400], ts = [];
  function at(u) { return [p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u]; }
  for (var i = 0; i < n; i++) ts.push(it[i].at != null ? T(sc, it[i].at) : t0 + i * st);
  fade(vec("axis dim", a0, b, { path: [p0, p1], stroke: mixv(C, [0, 0, 0], 0.7), sw: 4 }).l, a0, b, 0.4, 0.3);
  var ax = vec("axis", a0, b, { path: [p0, p1], stroke: C, sw: 5, trim: true }), ke = [[a0, 0]];
  for (var i = 0; i < n; i++) ke.push([ts[i], (i + 0.5) / n * 100]);
  ke.push([ts[n - 1] + 0.6, 100]); K(ax.trim.property("End"), ke); fade(ax.l, a0, b, 0.2, 0.3);
  var cw = HZ ? (p1[0] - p0[0]) / n - 30 : W - 300;
  for (var i = 0; i < n; i++) {
    var I = it[i], t = ts[i], q = at((i + 0.5) / n), c = I.color || C;
    var gw = vec("tl glow", t, b, { ellipse: [90, 90], fill: c, blur: 20, add: true, pos: q }).l; K(tr(gw, "Opacity"), [[t, 0], [t + 0.15, 60], [t + 0.8, 28]]); fade(gw, t, b, 0.01, 0.3, 28);
    var dt = vec("tl dot", t, b, { ellipse: [30, 30], fill: mixv(c, WHITE, 0.6), stroke: c, sw: 4, pos: q }).l;
    K(tr(dt, "Scale"), [[t, [0, 0]], [t + 0.12, [160, 160]], [t + 0.3, [100, 100]]]); fade(dt, t, b, 0.01, 0.3);
    var rg = vec("tl ring", t, t + 0.9, { ellipse: [44, 44], stroke: c, sw: 3, pos: q }).l; K(tr(rg, "Scale"), [[t, [60, 60]], [t + 0.9, [320, 320]]]); K(tr(rg, "Opacity"), [[t, 90], [t + 0.9, 0]]);
    if (HZ) {
      if (I.date) reveal(label(I.date, t, b, { y: q[1] - 46, x: q[0], size: 66, font: "Anton", track: 20, color: mixv(c, WHITE, 0.5), maxw: cw }), t + 0.05, b, 14, 0);
      if (I.label) { var tl = textLines(I.label, t, b, { y: q[1] + 78, x: q[0], size: 34, font: "Inter SemiBold", maxw: cw, color: [0.85, 0.95, 0.98], max: 3, track: 10 }); for (var j = 0; j < tl.length; j++) reveal(tl[j], t + 0.15, b, 12, 0); }
    } else {
      if (I.date) reveal(label(I.date, t, b, { y: q[1] + 6, x: q[0] + 50, just: "left", size: 66, font: "Anton", track: 20, color: mixv(c, WHITE, 0.5), maxw: cw }), t + 0.05, b, 14, 0);
      if (I.label) { var tl = textLines(I.label, t, b, { y: q[1] + 56, x: q[0] + 50, just: "left", size: 38, font: "Inter SemiBold", maxw: cw, color: [0.85, 0.95, 0.98], max: 2, track: 10 }); for (var j = 0; j < tl.length; j++) reveal(tl[j], t + 0.15, b, 12, 0); }
    }
    sfx(t, "chime", 0.35, { d: 1.6, f: 523 * Math.pow(1.122, i) });
  }
};

// abertura do canal (ate 5 s): nome do canal pequeno, linhas que se abrem, titulo do video entrando em foco, faixa de luz
// title*, kicker (ex.: nome do canal; texto, sem logo), sub, at ("start"), until (padrao: fim do bloco, no maximo 5 s), color CYAN, image
TPL.intro = function (sc) {
  var a = T(sc, sc.at, "start"), b = Math.min(T(sc, sc.until, "end+0.3"), a + 5), C = opt(sc, "color", CYAN);
  bgOr(sc, a - 0.1, b + 0.2);
  holoScan(a - 0.1, b + 0.2, C, 4);
  var ts = opt(sc, "size", vh(112, 120)), tl0 = wrapText(String(sc.title).toUpperCase(), ts, W - vh(140, 300), "Anton", 3);
  var hh = tl0.length * ts * 1.05, y = CY - hh / 2 + ts * 0.8;
  var ky = y - ts - vh(40, 30), kw = 0;
  if (sc.kicker) { var kl = label(sc.kicker, a, b, { y: ky, size: vh(36, 34), track: 600, color: mixv(C, WHITE, 0.35), maxw: vh(700, 900) }); kw = kl.sourceRectAtTime(a + 0.01, false).width * tr(kl, "Scale").value[0] / 100; reveal(kl, a + 0.15, b, 14, 0); }
  splitLine(ky - 12, kw / 2 + 30, vh(200, 300), a + 0.3, b, C);
  var tl = textLines(String(sc.title).toUpperCase(), a, b, { y: y, size: ts, font: "Anton", maxw: W - vh(140, 300), color: [0.97, 0.99, 1], track: 20, max: 3, lead: 1.05, title: true });
  for (var i = 0; i < tl.length; i++) { reveal(tl[i], a + 0.45 + i * 0.15, b, 26, 26); var sv = tr(tl[i], "Scale").value[0]; K(tr(tl[i], "Scale"), [[a + 0.45, [sv * 1.08, sv * 1.08]], [b, [sv, sv]]]); }
  if (sc.sub) reveal(label(sc.sub, a, b, { y: y + hh + vh(30, 20), size: vh(42, 40), color: [0.75, 0.86, 0.9], track: 30 }), a + 1.0, b, 14, 0);
  var sw = vec("light sweep", a + 0.9, a + 2.5, { rect: [140, H * 1.6], fill: mixv(C, WHITE, 0.6), blur: 70, add: true, pos: [-200, CY] }).l;
  tr(sw, "Rotation").setValue(18); KS(tr(sw, "Position"), [[a + 0.9, [-200, CY]], [a + 2.5, [W + 200, CY]]]); K(tr(sw, "Opacity"), [[a + 0.9, 0], [a + 1.3, 30], [a + 2.1, 30], [a + 2.5, 0]]);
  sfx(a, "rise", 0.35, { d: 1.1 }); sfx(a + 0.55, "boom", 0.4, { d: 2.2 }); HITS.push(a + 0.55);
};

// fechamento: chamada para inscricao (botao em texto, sem logo) e quadro "proximo video" (serve de area para a tela final do YouTube)
// next* (titulo do proximo video), next_label ("NEXT VIDEO"), cta ("SUBSCRIBE"), line (frase acima do botao), at ("start+0.2"), until ("dur"), color CYAN, button [r,g,b]
TPL.outro = function (sc) {
  var a = T(sc, sc.at, "start+0.2"), b = T(sc, sc.until, "dur"), C = opt(sc, "color", CYAN), bc = opt(sc, "button", [0.86, 0.13, 0.17]);
  bgOr(sc, sc.s - 0.1, b);
  enterWhoosh(sc, a);
  var cx = vh(CX, 560), cy = vh(640, 520), fx0 = vh(CX, 1340), fy = vh(1180, 500), fw = vh(880, 720), fh = fw * 9 / 16;
  if (sc.line) { var tl = textLines(sc.line, a, b, { y: cy - vh(150, 140), x: cx, size: vh(50, 46), font: "Inter SemiBold", maxw: vh(940, 760), color: [0.92, 0.97, 1], max: 2 }); for (var i = 0; i < tl.length; i++) reveal(tl[i], a + 0.1 + i * 0.1, b, 14, 0); }
  var R = rig("cta", a, b, [cx, cy]), cta = opt(sc, "cta", "SUBSCRIBE"), bw = Math.max(380, cta.length * 40 + 120);
  var pill = vec("cta pill", a + 0.3, b, { rect: [bw, 110], round: 55, fill: bc, stroke: mixv(bc, WHITE, 0.4), sw: 3, pos: [cx, cy] }).l;
  var pg = vec("cta glow", a + 0.3, b, { rect: [bw + 40, 150], round: 75, fill: bc, blur: 40, add: true, fop: 35, pos: [cx, cy] }).l;
  var pt = label(cta, a + 0.3, b, { y: cy + 22, x: cx, size: 62, font: "Anton", track: 80, color: WHITE, maxw: bw - 40, title: true });
  adopt(R, [pg, pill, pt]); for (var i = 0; i < 3; i++) fade([pg, pill, pt][i], a + 0.3, b, 0.2, 0.4);
  tr(R, "Scale").expression = EZ + "var e=ez((time-" + (a + 0.3) + ")/0.35), p=1+0.03*Math.sin((time-" + a + ")*3.2); var k=(0.6+0.4*e)*p*100; [k,k]";
  sfx(a + 0.35, "chime", 0.4, { d: 2, f: 659 });
  var tf = a + 0.7, nl = label(opt(sc, "next_label", "NEXT VIDEO"), tf, b, { y: fy - fh / 2 - 26, x: fx0, size: vh(36, 32), track: 420, color: mixv(C, WHITE, 0.35) });
  reveal(nl, tf, b, 12, 0);
  var fr = vec("next frame", tf, b, { rect: [fw, fh], round: 18, fill: [0.01, 0.05, 0.065], fop: 85, stroke: C, sw: 4, pos: [fx0, fy] }).l;
  K(tr(fr, "Scale"), [[tf, [94, 94]], [tf + 0.4, [100, 100]]]); fade(fr, tf, b, 0.35, 0.4);
  var fg = vec("next glow", tf, b, { rect: [fw + 30, fh + 30], round: 24, stroke: C, sw: 10, blur: 22, add: true, pos: [fx0, fy] }).l; fade(fg, tf, b, 0.5, 0.4, 45);
  if (sc.next) { var nt = textLines(String(sc.next).toUpperCase(), tf, b, { y: fy - fh * 0.12, x: fx0, size: vh(64, 58), font: "Anton", maxw: fw - 80, color: [0.97, 0.99, 1], max: 3, track: 20, lead: 1.08, title: true }); for (var i = 0; i < nt.length; i++) reveal(nt[i], tf + 0.25 + i * 0.1, b, 16, 10); }
  sfx(tf, "whoosh", 0.3, { d: 0.7 });
};

// ---------------- montagem ----------------
// horizontal/vertical: {"horizontal": {...}} num modelo troca parametros so naquele formato
function forFormat(p) {
  var o = {}, k, ov = p[HZ ? "horizontal" : "vertical"];
  for (k in p) if (k != "horizontal" && k != "vertical") o[k] = p[k];
  if (ov) for (k in ov) o[k] = ov[k];
  return o;
}
// coordenada de tela fora do quadro = quase sempre um valor do outro formato copiado
function checkXY(p, bi) {
  function bad(v, lim, k) { if (typeof v == "number" && (v < -200 || v > lim + 200)) throw new Error("bloco " + bi + " (" + p.t + "): " + k + "=" + v + " fora da tela " + W + "x" + H + "; use \"" + (HZ ? "horizontal" : "vertical") + "\": {...}"); }
  bad(p.y, H, "y"); bad(p.x, W, "x"); bad(p.label_y, H, "label_y");
  if (p.lines) for (var i = 0; i < p.lines.length; i++) { bad(p.lines[i].y, H, "lines.y"); bad(p.lines[i].x, W, "lines.x"); }
}
// marcador de ato do tema (THE SCAM · THE CASE · THE RULE) no canto superior esquerdo; o ato atual com bolinha, os outros a 55%
function actMark(act, a, b, x) {
  var nm = ["scam", "case", "rule"], xx = x, y = 70 + 15;
  for (var i = 0; i < 3; i++) {
    var on = nm[i] == act;
    if (on) { fade(vec("act dot", a, b, { ellipse: [12, 12], fill: ACT_COL[act], raw: true, pos: [xx + 6, y - 7] }).l, a, b, 0.3, 0.2); xx += 22; }
    var t = label("THE " + nm[i].toUpperCase(), a, b, { y: y, x: xx, just: "left", size: 20, color: on ? TH.ink : TH.mute, raw: true, track: 220, maxw: 9999 });
    fade(t, a, b, 0.3, 0.2, on ? 100 : 55);
    xx += t.sourceRectAtTime(a + 0.01, false).width + 28;
  }
}
function buildVideo() {
  var fin = SPEC.finish || {};
  comp = app.project.items.addComp(SPEC.comp || "main", W, H, 1, DUR, 30);
  solid("bg", opt(SPEC, "bg", RC ? TH.bg : [0, 0, 0.012]), 0, DUR);
  var cutFlash = [], over = [], main = comp, acts = [], late = [];
  var BGNAMES = { "rc bg": 1, "holo bg": 1, "holo grid": 1, "holo dust": 1, "scanlines": 1, "scan band": 1 };
  // horizontal: cada parte (capitulo) numa pre-composicao propria. O custo de criar camada cresce com o numero de camadas
  // da comp (70 blocos numa comp so: ~6,5 min de montagem; em partes: ~1 min). PART_STARTS vem do build.py.
  var starts = HZ && typeof PART_STARTS != "undefined" ? PART_STARTS : [];
  for (var bi = 0; bi < SPEC.blocks.length; bi++) {
    var blk = SPEC.blocks[bi], s = BLOCKS[bi], e = BLOCKS[bi + 1];
    for (var pi = 0; pi < starts.length; pi++) if (starts[pi] == bi) {
      comp = app.project.items.addComp("part " + (pi + 1), W, H, 1, DUR, 30);
      var pl = main.layers.add(comp); pl.inPoint = Math.max(0, s - 1); pl.outPoint = DUR;
    }
    var cut = bi == 0 ? "none" : (blk.cut || (RC ? "whoosh" : "both"));  // tema: corte sem clarao
    // ato do bloco ("act" no bloco ou em alguma cena); com foto a esquerda o marcador vai para a coluna da direita
    var act = blk.act, ax = 96;
    for (var j = 0; j < blk.scenes.length; j++) { var q = blk.scenes[j]; if (!act && q.act) act = q.act; if (HZ && q.t == "organ_focus" && opt(q, "img_x", PANEL_X) < CX) ax = Math.round(W * 0.48); }
    if (act) { if (!ACT_COL[act]) throw new Error("bloco " + bi + ": act deve ser scam, case ou rule (veio " + act + ")"); var la = acts[acts.length - 1]; if (la && la.act == act && la.x == ax && la.e == s) la.e = e; else acts.push({ act: act, x: ax, s: s, e: e }); }
    if (cut == "both" || cut == "flash") cutFlash.push(s);
    if (cut == "both" || cut == "whoosh") sfx(s - 0.35, "whoosh", 0.45, { d: 0.8 });
    var n0 = comp.numLayers;
    for (var j = 0; j < blk.scenes.length; j++) {
      var p = forFormat(blk.scenes[j]), f = TPL[p.t];
      if (!f) throw new Error("modelo desconhecido: " + p.t + " (bloco " + bi + ")");
      checkXY(p, bi);
      var sc = { s: s, e: e, act: act }; for (var k in p) sc[k] = p[k];
      // cena que entra depois de outra no mesmo bloco: fundo e partes fixas comecam no proprio at (nao cobrem a cena de antes)
      var ak = p.show != null ? "show" : "at";  // show = quando a cena aparece (meter); at = quando o conteudo anima
      if (j > 0 && p[ak] != null) { var ta = T(sc, p[ak]); if (ta - 0.1 > s) { sc.s0 = s; sc.s = ta - 0.1; sc[ak] = 0.1; } }
      if (f.overlay) over.push([f, sc]); else f(sc);
    }
    // regra dos Shorts: o primeiro elemento do bloco entra nos primeiros 0,3 s (fundo liso do tema, null e sobra do bloco anterior nao contam; foto que entra 0,1 s antes conta; camada nova = indice 1)
    var first = e;
    for (var li = 1; li <= comp.numLayers - n0; li++) { var L = comp.layer(li); if (L.enabled && !L.nullLayer && !BGNAMES[L.name.replace(/ \d+$/, "")] && L.inPoint > s - 0.15 && L.inPoint < first) first = L.inPoint; }
    if (first > s + 0.3) late.push(bi + (first < e ? " (+" + (first - s).toFixed(1) + "s)" : " (so sobreposicao)"));
  }
  if (late.length) writeLn("AVISO 0,3 s: bloco sem elemento nos primeiros 0,3 s: " + late.join(", "));
  comp = main;
  for (var i = 0; i < cutFlash.length; i++) flash(cutFlash[i], 35, 0.35);
  // acabamento: brilho, tremida nos impactos, granulacao, vinheta
  var fl = solid("finish", [0, 0, 0], 0, DUR); fl.adjustmentLayer = true;
  if (!RC) fx(fl, "Glow", { "Glow Threshold": 55, "Glow Radius": 90, "Glow Intensity": opt(fin, "glow", 1.1) });
  var sh = "var h=" + JSON.stringify(HITS) + ", a=0; for (var i=0;i<h.length;i++){var d=time-h[i]; if(d>0&&d<1.1) a=Math.max(a,(1.1-d)*" + opt(fin, "shake", 22) + ");} ";
  fx(fl, "Transform", { "Uniform Scale": true, "Scale Height": 104, "Position": "=" + sh + "value + [wiggle(28,a)[0]-value[0], wiggle(31,a)[1]-value[1]]" });
  fx(fl, "Noise", { "Amount of Noise": opt(fin, "grain", 3) });
  var vig = solid("vignette", [0, 0, 0], 0, DUR);
  oval(vig, CX, CY, vh(760, 1150), vh(1150, 760), 520).inverted = true;
  tr(vig, "Opacity").setValue(opt(fin, "vignette", 75));
  for (var i = 0; i < over.length; i++) over[i][0](over[i][1]);
  SRCQ.sort(function (p, q) { return p[1] - q[1]; });  // duas fontes no mesmo canto: a anterior sai quando a seguinte entra
  for (var i = 0; i < SRCQ.length; i++) { if (i + 1 < SRCQ.length) SRCQ[i][2] = Math.min(SRCQ[i][2], SRCQ[i + 1][1]); srcLineNow(SRCQ[i][0], SRCQ[i][1], SRCQ[i][2], SRCQ[i][3]); }
  for (var i = 0; i < acts.length; i++) actMark(acts[i].act, acts[i].s, acts[i].e == null ? DUR : acts[i].e, acts[i].x);
  // legendas (vertical y 1560, fora da area dos titulos; horizontal: 1 linha menor perto da base)
  if (SPEC.captions !== false && starts.length) { comp = app.project.items.addComp("captions", W, H, 1, DUR, 30); main.layers.add(comp); }
  if (SPEC.captions !== false) for (var i = 0; i < CHUNKS.length; i++) {
    var c = CHUNKS[i], t = text(c.t, c.s, c.e, CAP_SIZE, CAP_Y, [1, 1, 1], RC ? "Inter-Bold" : "Anton", RC ? 0 : 10);
    var cf = 1;
    if (HZ || RC) { var cw = t.sourceRectAtTime(c.s + 0.01, false).width, mw = W - vh(120, 300); if (cw > mw) cf = mw / cw; }  // nunca quebra nem passa da largura (no tema a Inter Bold e mais larga que a Anton)
    K(tr(t, "Scale"), [[c.s, [86 * cf, 86 * cf]], [c.s + 0.08, [100 * cf, 100 * cf]]]);
  }
  writeLn("EVENTS=" + JSON.stringify(EVENTS));
  comp = main;
  writeLn("ok layers=" + comp.numLayers + " parts=" + starts.length + " format=" + (HZ ? "horizontal" : "vertical") + " " + W + "x" + H);
}

buildVideo();
