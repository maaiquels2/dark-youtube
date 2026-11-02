const P = [1, 2, 0, 4, 5, 6, 3, 8, 9, 7], CY = [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]], CC = [RED, OR, GRN];
const NX = i => 540 + 270 * Math.cos(-1.5708 + i * 0.6283), NY = i => 700 + 270 * Math.sin(-1.5708 + i * 0.6283);
function node(i, col) { circ(NX(i), NY(i), 34, col ? col : "#e8dcbc", INK, 4); txt("" + (i + 1), NX(i), NY(i), 32, col ? "#fff" : INK); }
function arrow(i, col) { const j = P[i], a = Math.atan2(NY(j) - NY(i), NX(j) - NX(i)); line(NX(i) + 36 * Math.cos(a), NY(i) + 36 * Math.sin(a), NX(j) - 40 * Math.cos(a), NY(j) - 40 * Math.sin(a), col || INK, 5); circ(NX(j) - 42 * Math.cos(a), NY(j) - 42 * Math.sin(a), 7, col || INK); }
function grid(n) { for (let k = 0; k < 100; k++) { const c = k % 10, r = Math.floor(k / 10); rect(220 + c * 64, 430 + r * 64, 52, 52, k < n ? "#f3e7c6" : "#e8dcbc", INK, 3); } }
function scene(t, b, u) {
  if (b === 0) { grid(100); txt("each prisoner opens 50 boxes", 540, 1120, 44, INK); return "100 PRISONERS · 100 BOXES"; }
  if (b === 1) { grid(100); txt("50% each", 540, 1120, 56, INK); if (u > 0.5) txt("all 100: 1 in 2^100", 540, 1200, 56, RED); return "AT RANDOM: ESSENTIALLY ZERO"; }
  if (b === 2) {
    for (let i = 0; i < 10; i++) node(i);
    const n = Math.min(3, Math.floor(u * 4)); let c = 0;
    for (let s = 0; s < n; s++) { arrow(c, RED); c = P[c]; }
    node(0, RED); txt("start at your own number", 540, 1060, 44, INK);
    return "FOLLOW THE CHAIN";
  }
  if (b === 3) {
    CY.forEach((cy, k) => cy.forEach(i => arrow(i, CC[k]))); for (let i = 0; i < 10; i++) node(i, CC.find((_, k) => CY[k].includes(i)));
    txt("loops: 3, 4, 3", 540, 1060, 50, INK);
    return "THE NUMBERS FORM LOOPS";
  }
  if (b === 4) {
    txt("everyone lives if", 540, 560, 56, INK); txt("no loop is longer than 50", 540, 650, 56, RED);
    rect(140, 800, 800, 60, "#e8dcbc", INK, 4); rect(140, 800, 800 * 0.31 * Math.min(1, u * 2), 60, GRN);
    if (u > 0.5) txt("≈ 31%", 540, 940, 90, GRN);
    return "THE ODDS";
  }
  txt("0%  →  31%", 540, 700, 100, GRN); txt("same boxes, smarter plan", 540, 840, 44, INK);
  return "STRUCTURE BEATS LUCK";
}
