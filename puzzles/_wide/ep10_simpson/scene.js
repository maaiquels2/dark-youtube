const CA = OR, CB = "#1f5fbf";
function bar(y, label, pa, pb, ta, tb, show) {
  txt(label, 540, y - 70, 44, INK);
  const k = ease(show); const w = 640 * k;
  txt("A", 150, y, 40, CA, "center"); rect(190, y - 30, w * pa, 60, CA, null, 0, 1);
  txt("B", 150, y + 80, 40, CB, "center"); rect(190, y + 50, w * pb, 60, CB, null, 0, 1);
  if (k > 0.98) { txt(ta, 190 + 640 * pa + 20, y, 38, CA, "left"); txt(tb, 190 + 640 * pb + 20, y + 80, 38, CB, "left"); }
}
function stack(y, label, small, large, c, show) {
  const k = ease(show), tot = 350, W = 640;
  txt(label, 120, y, 40, c, "center");
  rect(190, y - 30, W * small / tot * k, 60, c, null, 0, 0.45); rect(190 + W * small / tot * k, y - 30, W * large / tot * k, 60, c, null, 0, 1);
  if (k > 0.98) { txt("small " + small, 190 + W * small / tot / 2, y + 62, 28, INK); txt("large " + large, 190 + W * (small + large / 2) / tot, y + 62, 28, INK); }
}
function scene(t, b, u) {
  if (b === 0) {
    txt("A beats B on small stones", 540, 520, 46, INK); txt("A beats B on large stones", 540, 620, 46, INK);
    if (u > 0.55) txt("but B wins overall?", 540, 780, 64, RED);
    return "SAME DATA, TWO ANSWERS";
  }
  if (b === 1) { bar(520, "SMALL STONES", 0.93, 0.87, "93%", "87%", u / 0.4); if (u > 0.5) bar(840, "LARGE STONES", 0.73, 0.69, "73%", "69%", (u - 0.5) / 0.4); return "CURE RATES BY GROUP"; }
  if (b === 2) {
    bar(470, "ALL PATIENTS", 0.78, 0.826, "78%", "83%", u / 0.5);
    if (u > 0.55) { txt("A: 273 of 350", 300, 800, 40, CA); txt("B: 289 of 350", 780, 800, 40, CB); }
    return "ADD EVERYONE UP";
  }
  if (b === 3) { stack(520, "A", 87, 263, CA, u / 0.4); if (u > 0.4) stack(760, "B", 270, 80, CB, (u - 0.4) / 0.4); return "WHO GOT WHICH CASES"; }
  if (b === 4) {
    stack(520, "A", 87, 263, CA, 1); stack(760, "B", 270, 80, CB, 1);
    txt("A got the hard cases", 540, 950, 54, CA); if (u > 0.5) txt("so its average looks worse", 540, 1030, 44, INK);
    return "THE AVERAGE HID THE GROUPS";
  }
  txt("ask: who is in each group?", 540, 700, 56, RED); txt("the trend can flip when you combine data", 540, 820, 38, INK);
  return "SIMPSON'S PARADOX";
}
