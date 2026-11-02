const GX = 80, GY = 330, CS = 23, RS = 24;
const SICK = new Set(Array.from({ length: 10 }, (_, k) => 37 + k * 97));
const FALSE_POS = new Set(Array.from({ length: 10 }, (_, k) => 11 + k * 99 + (k % 3) * 2));
FALSE_POS.forEach(i => { if (SICK.has(i)) FALSE_POS.delete(i); });
function dotAt(i) { return [GX + (i % 40) * CS + CS / 2, GY + Math.floor(i / 40) * RS + RS / 2]; }
function grid(sickOn, tpOn, fpOn, fade) {
  for (let i = 0; i < 1000; i++) {
    const [cx, cy] = dotAt(i); const s = SICK.has(i), f = FALSE_POS.has(i);
    let col = DOT, a = 0.55, r = 5.5;
    if (s && sickOn) { col = RED; a = 1; r = 8; }
    if (fade && !(s && sickOn) && !(f && fpOn)) a = 0.1;
    circ(cx, cy, r, col, null, 0, a);
    if (s && tpOn) circ(cx, cy, 15, null, RED, 3.5);
    if (f && fpOn) circ(cx, cy, 15, OR, null, 0, 0.9);
  }
}
function scene(t, b, u) {
  if (b === 0) { grid(false, false, false, false); txt("1 in 100 is sick", 540, 1010, 44, INK); return u < 0.5 ? "1,000 PEOPLE" : "POSITIVE TEST. HOW SURE?"; }
  if (b === 1) {
    grid(false, false, false, false);
    txt("sick → positive 99 of 100", 540, 1000, 40, RED); txt("healthy → positive 1 of 100", 540, 1060, 40, OR);
    return "WHAT 99% ACCURATE MEANS";
  }
  if (b === 2) { grid(true, u > 0.4, false, false); txt(u > 0.4 ? "10 sick · 10 positives" : "10 sick", 540, 1040, 52, RED); return "THE SICK"; }
  if (b === 3) { grid(true, true, u > 0.35, false); txt(u > 0.35 ? "990 healthy · 10 false alarms" : "990 healthy", 540, 1040, 46, OR); return "THE HEALTHY"; }
  if (b === 4) {
    grid(true, true, true, u > 0.3);
    txt("20 positives: 10 sick + 10 healthy", 540, 985, 40, INK);
    if (u > 0.55) txt("about 50%", 540, 1055, 80, RED);
    return "WHO TESTS POSITIVE";
  }
  grid(true, true, true, true);
  txt("rare + small error = many false alarms", 540, 1040, 40, INK);
  return "TEST AGAIN, DON'T PANIC";
}
