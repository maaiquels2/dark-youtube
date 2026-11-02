// Teste: explosao do Big Bang no EffectCraft (vertical 1080x1920, 5 s)
var comp = app.project.items.addComp("bang", 1080, 1920, 1, 5, 30);
var bg = comp.layers.addSolid([0, 0, 0], "bg", 1080, 1920, 1);

// nuvem de gas (Fractal Noise colorido, cresce)
var gas = comp.layers.addSolid([0, 0, 0], "gas", 1080, 1920, 1);
var fn = gas.Effects.addProperty("Fractal Noise");
fn.property("Contrast").setValue(160);
fn.property("Brightness").setValue(-30);
fn.property("Evolution").expression = "time*120";
var tint = gas.Effects.addProperty("Tint");
tint.property("Map Black To").setValue([0.02, 0, 0.08]);
tint.property("Map White To").setValue([1, 0.45, 0.1]);
var m = gas.Masks.addProperty("Mask");
var sh = new Shape(); var r = 420;
sh.vertices = [[540 - r, 960], [540, 960 - r], [540 + r, 960], [540, 960 + r]];
sh.inTangents = [[0, r * 0.55], [-r * 0.55, 0], [0, -r * 0.55], [r * 0.55, 0]];
sh.outTangents = [[0, -r * 0.55], [r * 0.55, 0], [0, r * 0.55], [-r * 0.55, 0]];
sh.closed = true;
m.property("Mask Path").setValue(sh);
m.property("Mask Feather").setValue([260, 260]);
gas.blendingMode = BlendingMode.ADD;
var gs = gas.property("Transform").property("Scale");
gs.setValueAtTime(0.0, [5, 5]); gs.setValueAtTime(0.6, [5, 5]); gs.setValueAtTime(4.8, [320, 320]);
var go = gas.property("Transform").property("Opacity");
go.setValueAtTime(0.5, 0); go.setValueAtTime(0.9, 100); go.setValueAtTime(4.8, 70);
var td = gas.Effects.addProperty("Turbulent Displace");
td.property("Amount").setValue(90); td.property("Size").setValue(140);
td.property("Evolution").expression = "time*200";

// particulas (CC Particle World): rajada a partir do centro
var pt = comp.layers.addSolid([0, 0, 0], "particles", 1080, 1920, 1);
var pw = pt.Effects.addProperty("CC Particle World");
pt.blendingMode = BlendingMode.ADD;
pw.property("Birth Rate").setValueAtTime(0.55, 0);
pw.property("Birth Rate").setValueAtTime(0.6, 12);
pw.property("Birth Rate").setValueAtTime(1.4, 1.2);
pw.property("Longevity (sec)").setValue(3.5);
var ph = pw.property("Physics");
var pn = []; for (var i = 1; i <= ph.numProperties; i++) pn.push(ph.property(i).name);
writeLn("Physics: " + pn.join(" | "));
ph.property("Velocity").setValue(1.6);
ph.property("Gravity").setValue(0);

// clarão central
var core = comp.layers.addSolid([1, 0.95, 0.85], "core", 1080, 1920, 1);
var cm = core.Masks.addProperty("Mask");
var s2 = new Shape(); var q = 60;
s2.vertices = [[540 - q, 960], [540, 960 - q], [540 + q, 960], [540, 960 + q]];
s2.inTangents = [[0, q * 0.55], [-q * 0.55, 0], [0, -q * 0.55], [q * 0.55, 0]];
s2.outTangents = [[0, -q * 0.55], [q * 0.55, 0], [0, q * 0.55], [-q * 0.55, 0]];
s2.closed = true;
cm.property("Mask Path").setValue(s2);
cm.property("Mask Feather").setValue([90, 90]);
core.blendingMode = BlendingMode.ADD;
var cs = core.property("Transform").property("Scale");
cs.setValueAtTime(0, [8, 8]); cs.setValueAtTime(0.55, [30, 30]); cs.setValueAtTime(0.7, [900, 900]); cs.setValueAtTime(2.5, [400, 400]);
var co = core.property("Transform").property("Opacity");
co.setValueAtTime(0, 100); co.setValueAtTime(0.7, 100); co.setValueAtTime(1.6, 15); co.setValueAtTime(3.5, 0);

// acabamento: glow + tremida
var adj = comp.layers.addSolid([0, 0, 0], "finish", 1080, 1920, 1);
adj.adjustmentLayer = true;
var gl = adj.Effects.addProperty("Glow");
gl.property("Glow Radius").setValue(120);
gl.property("Glow Intensity").setValue(1.4);
adj.property("Transform").property("Position").expression =
  "var k = time>0.6 && time<1.6 ? (1.6-time)*25 : 0; value + [wiggle(30,k)[0]-value[0], wiggle(30,k)[1]-value[1]]";

writeLn("ok layers=" + comp.numLayers);
