var c = app.project.items.addComp("x", 100, 100, 1, 1, 30);
var l = c.layers.addSolid([0, 0, 0], "s", 100, 100, 1);
var names = ["Transform", "Noise", "Shape Layer"];
var s = c.layers.addShape(); var g = s.property("Contents").addProperty("ADBE Vector Group");
var gc = g.property("Contents"); var a = [];
var el = gc.addProperty("ADBE Vector Shape - Ellipse"); for (var i = 1; i <= el.numProperties; i++) a.push(el.property(i).name);
var st = gc.addProperty("ADBE Vector Graphic - Stroke"); for (var i = 1; i <= st.numProperties; i++) a.push("S:" + st.property(i).name);
var fl = gc.addProperty("ADBE Vector Graphic - Fill"); for (var i = 1; i <= fl.numProperties; i++) a.push("F:" + fl.property(i).name);
writeLn("shape: " + a.join(" | "));
var e0 = l.Effects.addProperty("CC Toner"); writeLn("toner tones=" + e0.property("Tones").value);
var e1 = l.Effects.addProperty("CC Particle World"); var ex = e1.property("Extras"); a = [];
for (var i = 1; i <= ex.numProperties; i++) a.push(ex.property(i).name); writeLn("PW extras: " + a.join(" | "));
names.pop();
for (var k = 0; k < names.length; k++) {
  var e = l.Effects.addProperty(names[k]); var a = [];
  for (var i = 1; i <= e.numProperties; i++) a.push(e.property(i).name);
  writeLn(names[k] + ": " + a.join(" | "));
}
