const ANG = [8, 62, 131, 187, 243, 301, 337], R = 290, CX = 540, CY = 600;
const PT = ANG.map(a => { const t = (a - 90) * Math.PI / 180; return [CX + R * Math.cos(t), CY + R * Math.sin(t)]; });
const REG = [1, 2, 4, 8, 16, 31, 57];
function ix(i, k, j, l) {
  const [x1, y1] = PT[i], [x2, y2] = PT[k], [x3, y3] = PT[j], [x4, y4] = PT[l];
  const d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4), tt = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d;
  return [x1 + tt * (x2 - x1), y1 + tt * (y2 - y1)];
}
function board(n, showX, al) {
  circ(CX, CY, R, null, INK, 4, 0.5);
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) line(PT[i][0], PT[i][1], PT[j][0], PT[j][1], INK, 3, al == null ? 0.8 : al);
  if (showX) for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) for (let l = k + 1; l < n; l++) { const p = ix(i, k, j, l); circ(p[0], p[1], 8, RED); }
  for (let i = 0; i < n; i++) circ(PT[i][0], PT[i][1], 12, INK);
}
function scene(t, b, u) {
  if (b === 0) {
    circ(CX, CY, R, null, INK, 4, 0.4);
    ["1", "2", "4", "8", "16", "?"].forEach((s, i) => { if (u > 0.08 + i * 0.12) txt(s, 150 + i * 155, CY, i === 5 ? 120 : 92, i === 5 ? RED : INK); });
    return "WHAT COMES NEXT?";
  }
  if (b === 1) { const n = Math.min(5, 2 + Math.floor(u * 4)); board(n, false); return "EVERY PAIR OF POINTS IS JOINED"; }
  if (b === 2) {
    const n = Math.min(5, 1 + Math.floor(u * 5)); board(n, false);
    txt(REG[n - 1] + (REG[n - 1] === 1 ? " region" : " regions"), 540, 1000, 80, RED);
    return n + (n === 1 ? " POINT" : " POINTS");
  }
  if (b === 3) {
    board(6, u > 0.55);
    if (u < 0.55) txt("32 ?", 540, 1000, 100, RED); else txt("31", 540, 1000, 110, RED);
    return "6 POINTS";
  }
  if (b === 4) {
    board(6, true);
    txt("1 + 15 lines + 15 crossings = 31", 540, 975, 44, INK);
    if (u > 0.7) txt("7 points: 57", 540, 1050, 56, RED);
    return "COUNT LINES AND CROSSINGS";
  }
  board(7, true, 0.35);
  txt("5 examples, 100 patterns", 540, 1010, 50, RED);
  return "A PATTERN IS A GUESS";
}
