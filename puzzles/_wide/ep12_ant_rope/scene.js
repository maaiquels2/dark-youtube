const RX0 = 100, RX1 = 980, RY = 640;
function rope(frac, lenLabel, ticks) {
  line(RX0, RY, RX1, RY, INK, 10);
  for (let i = 0; i <= ticks; i++) { const px = RX0 + (RX1 - RX0) * i / ticks; line(px, RY - 14, px, RY + 14, INK, 3, 0.6); }
  circ(RX0, RY, 12, INK); circ(RX1, RY, 12, RED);
  const ax = RX0 + (RX1 - RX0) * frac; circ(ax, RY - 36, 18, OR, INK, 3); txt("ant", ax, RY - 80, 30, OR);
  txt(lenLabel, 540, RY + 70, 44, INK);
}
const ROWS = [["1 s", "0.001%"], ["1,000 s", "0.0075%"], ["1 million s", "0.014%"], ["1 billion s", "0.021%"], ["e^100,000 s", "100%"]];
function scene(t, b, u) {
  if (b === 0) { rope(0.02, "1 km", 10); txt("ant: 1 cm/s", 540, 930, 44, OR); txt("rope: +1 km every second", 540, 1010, 44, INK); return "WILL THE ANT EVER ARRIVE?"; }
  if (b === 1) { const L = 1 + Math.floor(u * 4); rope(0.02 + 0.01 * L / 5, L + " km", 10 * L > 40 ? 40 : 10 * L); txt("stretches evenly: the ant rides along", 540, 960, 40, INK); return "THE ROPE STRETCHES"; }
  if (b === 2) { rope(0.02, "end runs away 100,000× faster", 24); txt("it looks impossible", 540, 960, 56, RED); return "SPEED OF THE END VS THE ANT"; }
  if (b === 3) { rope(0.02 + 0.01 * u, "fraction covered keeps growing", 24); txt("1 s → 1/100,000 of the rope", 540, 960, 44, INK); if (u > 0.5) txt("progress is never lost", 540, 1040, 44, GRN); return "TRACK THE FRACTION"; }
  if (b === 4) {
    ROWS.slice(0, 4).forEach((r, i) => { if (u > 0.08 + i * 0.18) { txt(r[0], 280, 470 + i * 110, 52, INK); txt("→", 520, 470 + i * 110, 46, DOT); txt(r[1], 760, 470 + i * 110, 56, RED); } });
    if (u > 0.82) txt("1 + 1/2 + 1/3 + … never stops growing", 540, 960, 40, INK);
    return "FRACTION COVERED OVER TIME";
  }
  rope(u > 0.45 ? 1 : 0.03, u > 0.45 ? "arrived" : "after a very long time", 24);
  txt("e^100,000 seconds", 540, 880, 70, RED); txt("a number with 43,429 digits", 540, 970, 44, INK);
  return "INFINITE IS NOT NEVER";
}
