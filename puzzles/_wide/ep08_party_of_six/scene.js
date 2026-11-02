const BLU = "#1f5fbf";
function ring(n, cx, cy, r) { const o = []; for (let i = 0; i < n; i++) { const a = -1.5708 + i * 6.283 / n; o.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } return o; }
const H = ring(6, 540, 640, 290), PEN = ring(5, 540, 640, 290);
function edge(P, a, b, col, lw, al) { line(P[a][0], P[a][1], P[b][0], P[b][1], col, lw || 6, al == null ? 1 : al); }
function dots(P, hi) { P.forEach((p, i) => circ(p[0], p[1], i === hi ? 24 : 18, INK)); }
function tri(P, a, b, c, col) { x.globalAlpha = 0.22; x.fillStyle = col; x.beginPath(); x.moveTo(P[a][0], P[a][1]); x.lineTo(P[b][0], P[b][1]); x.lineTo(P[c][0], P[c][1]); x.closePath(); x.fill(); x.globalAlpha = 1; }
const COL6 = (i, j) => ((i * 5 + j * 3 + i * j) % 3 === 0) ? RED : BLU;
function scene(t, b, u) {
  if (b === 0) { dots(H, -1); return u < 0.5 ? "6 PEOPLE AT A PARTY" : "ALWAYS 3 WHO KNOW EACH OTHER, OR 3 STRANGERS"; }
  if (b === 1) {
    const n = Math.floor(u * 16);
    let k = 0; for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) { if (k++ < n) edge(H, i, j, COL6(i, j), 5, 0.85); }
    dots(H, -1); txt("blue = know each other", 300, 1050, 34, BLU); txt("red = strangers", 780, 1050, 34, RED);
    return "ONE LINE PER PAIR";
  }
  if (b === 2) {
    for (let i = 0; i < 5; i++) { edge(PEN, i, (i + 1) % 5, BLU, 8); edge(PEN, i, (i + 2) % 5, RED, 6); }
    dots(PEN, -1); txt("ring = blue, star = red", 540, 1050, 40, INK);
    return "5 PEOPLE: NO SINGLE-COLOR TRIANGLE";
  }
  if (b === 3) {
    const cols = [BLU, BLU, BLU, RED, RED];
    cols.forEach((c, k) => { if (u > 0.1 + k * 0.12) edge(H, 0, k + 1, c, 9); });
    dots(H, 0); txt("5 lines, 2 colors: 3 must match", 540, 1050, 42, INK);
    return "ONE PERSON · FIVE LINES";
  }
  if (b === 4) {
    [1, 2, 3].forEach(k => edge(H, 0, k, BLU, 9, 0.5));
    if (u < 0.5) { edge(H, 1, 2, BLU, 9); tri(H, 0, 1, 2, BLU); txt("one blue line = blue triangle", 540, 1050, 40, BLU); }
    else { edge(H, 1, 2, RED, 9); edge(H, 2, 3, RED, 9); edge(H, 1, 3, RED, 9); tri(H, 1, 2, 3, RED); txt("all red = red triangle", 540, 1050, 40, RED); }
    dots(H, 0);
    return u < 0.5 ? "IF ANY LINE IS BLUE" : "IF ALL THREE ARE RED";
  }
  for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) edge(H, i, j, COL6(i, j), 4, 0.35);
  for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) for (let k = j + 1; k < 6; k++)
    if (!window.__mono && COL6(i, j) === COL6(j, k) && COL6(i, j) === COL6(i, k)) window.__mono = [i, j, k];
  const m = window.__mono; if (m) { tri(H, m[0], m[1], m[2], COL6(m[0], m[1])); edge(H, m[0], m[1], COL6(m[0], m[1]), 10); edge(H, m[1], m[2], COL6(m[0], m[1]), 10); edge(H, m[0], m[2], COL6(m[0], m[1]), 10); }
  dots(H, -1); txt("6 is the smallest crowd that guarantees it", 540, 1000, 38, INK);
  return "ORDER INSIDE CHAOS";
}
