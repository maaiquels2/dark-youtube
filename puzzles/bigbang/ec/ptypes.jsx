var comp = app.project.items.addComp("pt", 1200, 400, 1, 3, 30);
comp.layers.addSolid([0, 0, 0], "bg", 1200, 400, 1);
for (var t = 1; t <= 18; t++) {
  var l = comp.layers.addSolid([0, 0, 0], "p" + t, 1200, 400, 1); l.blendingMode = BlendingMode.ADD;
  var e = l.Effects.addProperty("CC Particle World");
  var pt = e.property("Particle").property("Particle Type");
  try { pt.setValue(t); } catch (x) { writeLn("type " + t + " fail"); continue; }
  e.property("Birth Rate").setValue(0.6);
  e.property("Physics").property("Velocity").setValue(0.15);
  e.property("Physics").property("Gravity").setValue(0);
  e.property("Particle").property("Birth Size").setValue(0.25);
  e.property("Particle").property("Death Size").setValue(0.25);
  var c = (t - 1) % 9, r = Math.floor((t - 1) / 9);
  l.property("Transform").property("Position").setValue([65 + c * 130, 100 + r * 200]);
  l.property("Transform").property("Scale").setValue([30, 30]);
  var tx = comp.layers.addText(String(t)); tx.property("Transform").property("Position").setValue([65 + c * 130, 190 + r * 200]);
}
