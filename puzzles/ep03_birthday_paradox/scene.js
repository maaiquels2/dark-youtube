const pb = n => { let q = 1; for (let i = 0; i < n; i++) q *= (365 - i) / 365; return 1 - q; };
function people(cx, cy, r, n, la, hiOne) {
  const pts = [];
  for (let i = 0; i < n; i++) { const a = -1.5708 + i * 6.283 / n; pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  if (la > 0) for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++)
    if (!hiOne || i === 0) line(pts[i][0], pts[i][1], pts[j][0], pts[j][1], hiOne ? GRN : RED, hiOne ? 4 : 2, la);
  pts.forEach((p, i) => circ(p[0], p[1], n > 30 ? 5 : n > 12 ? 11 : 16, hiOne && i === 0 ? GRN : INK));
}
const CHX = 120, CHW = 840, CHB = 1110, CHH = 330;
function chart(upto, inv) {
  line(CHX, CHB, CHX + CHW, CHB, INK, 3); line(CHX, CHB, CHX, CHB - CHH, INK, 3);
  [0, 23, 50, 70].forEach(n => txt(String(n), CHX + CHW * n / 70, CHB + 28, 26, INK));
  txt("100%", CHX - 10, CHB - CHH, 24, INK, "right"); txt("50%", CHX - 10, CHB - CHH / 2, 24, INK, "right");
  line(CHX, CHB - CHH / 2, CHX + CHW, CHB - CHH / 2, INK, 2, 0.35);
  x.strokeStyle = inv ? OR : RED; x.lineWidth = 7; x.beginPath();
  for (let n = 0; n <= upto + 0.001; n += 0.5) {
    const p = inv ? 1 - pb(n) : pb(n), px = CHX + CHW * n / 70, py = CHB - CHH * p;
    n === 0 ? x.moveTo(px, py) : x.lineTo(px, py);
  }
  x.stroke();
}
function mark(n, upto) {
  if (upto < n) return;
  const p = pb(n), px = CHX + CHW * n / 70, py = CHB - CHH * p;
  circ(px, py, 11, RED); txt((p * 100).toFixed(1) + "%", Math.min(px, 900), py - 34, 28, RED);
}
function scene(t, b, u) {
  if (b === 0) {
    people(540, 640, 300, 1 + Math.floor(ease(u / 0.8) * 22), 0, false);
    return u < 0.5 ? "HOW MANY PEOPLE?" : "23 PEOPLE";
  }
  if (b === 1) {
    for (let i = 0; i < 365; i++) circ(150 + (i % 20) * 42, 400 + Math.floor(i / 20) * 36, 9, DOT, null, 0, 0.55);
    if (u > 0.66) { [86, 241].forEach(i => circ(150 + (i % 20) * 42, 400 + Math.floor(i / 20) * 36, 17, null, RED, 6)); }
    return u < 0.33 ? "NO LEAP YEARS" : u < 0.66 ? "ALL DAYS EQUAL" : "AT LEAST ONE MATCH";
  }
  if (b === 2) {
    const n = u < 0.2 ? 2 : u < 0.4 ? 3 : u < 0.6 ? 10 : 23;
    people(540, 640, 300, n, 0.55, false);
    return n + " PEOPLE  =  " + (n * (n - 1) / 2) + (n === 2 ? " PAIR" : " PAIRS");
  }
  if (b === 3) {
    people(540, 520, 150, 23, 0.25, false);
    const up = 70 * ease(u / 0.9); chart(up, false); [23, 30, 50, 70].forEach(n => mark(n, up));
    return Math.max(1, Math.round(up)) + " PEOPLE  ·  " + (pb(Math.max(1, Math.round(up))) * 100).toFixed(1) + "% MATCH";
  }
  if (b === 4) {
    people(540, 520, 150, 23, 0, false);
    const up = 30 * ease(u / 0.9); chart(Math.max(up, 0.5), true);
    const k = Math.min(23, Math.max(2, Math.floor(up)));
    txt("364/365  ×  363/365  ×  362/365  ×  …", 540, 700, 30, INK);
    if (up >= 23) { circ(CHX + CHW * 23 / 70, CHB - CHH * (1 - pb(23)), 12, OR); txt("below 50% at person 23", 540, 760, 30, OR); }
    return "ALL DIFFERENT AMONG " + Math.max(1, Math.round(up)) + (Math.round(up) <= 1 ? " PERSON: " : " PEOPLE: ") + ((1 - pb(Math.max(1, Math.round(up)))) * 100).toFixed(1) + "%";
  }
  if (b === 5) {
    if (u < 0.5) { people(540, 640, 300, 23, 0.8, true); return "YOU VS THE ROOM  ·  22 PAIRS"; }
    people(540, 640, 300, 23, 0.4, false); return "EVERYONE VS EVERYONE  ·  253 PAIRS";
  }
  people(540, 640, 300, 23, 0.4 * (1 - clamp(u / 0.6)), false);
  txt("COUNT THE PAIRS", 540, 640, 56, INK);
  return "THE ODDS HIDE IN THE CHANCES";
}
