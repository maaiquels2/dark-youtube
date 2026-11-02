function order(n) { const p = Array.from({ length: n }, (_, i) => i + 1), out = []; let i = 0;
  while (p.length > 1) { i = (i + 1) % p.length; out.push(p.splice(i, 1)[0]); }
  return { out, win: p[0] }; }
function surv(n) { return order(n).win; }
const O41 = order(41), BIN = "101001";
function ring(cx, cy, r, n, gone, win, size) {
  const dead = new Set(gone);
  for (let i = 1; i <= n; i++) {
    const a = -1.5708 + (i - 1) * 6.283 / n, px = cx + r * Math.cos(a), py = cy + r * Math.sin(a);
    const d = dead.has(i), w = win === i;
    circ(px, py, w ? size * 1.5 : size, d ? null : (w ? GRN : INK), d ? INK : null, 2, d ? 0.25 : 1);
    if (!d && size >= 14) txt(String(i), px, py, Math.round(size * 0.9), "#f4ecd8", "center");
  }
}
function bits(str, y, hi, off, lift) {
  for (let i = 0; i < str.length; i++) {
    const px = 540 + (i - (str.length - 1) / 2) * 110 + (off ? off[i] : 0), yy = y - (lift && i === 0 ? lift : 0);
    rect(px - 44, yy - 44, 88, 88, hi === i ? "rgba(224,122,0,0.3)" : null, INK, 5);
    txt(str[i], px, yy, 56, str[i] === "1" ? RED : INK);
  }
}
function scene(t, b, u) {
  if (b === 0) { ring(540, 640, 320, 41, [], 0, 18); return u < 0.5 ? "41 PEOPLE IN A CIRCLE" : "EVERY SECOND ONE OUT"; }
  if (b === 1) {
    const k = Math.floor(ease(u / 0.9) * 40);
    ring(540, 640, 320, 41, O41.out.slice(0, k), k >= 40 ? O41.win : 0, 18);
    return k >= 40 ? "LAST ONE STANDING: 19" : "ELIMINATED: " + k;
  }
  if (b === 2) {
    const ns = [5, 6, 7, 8], cs = [[300, 560], [780, 560], [300, 900], [780, 900]];
    ns.forEach((n, j) => { const r = order(n); const show = u > j * 0.22; if (!show) return;
      ring(cs[j][0], cs[j][1], 120, n, r.out, r.win, 15); txt("n = " + n + "  →  " + r.win, cs[j][0], cs[j][1] + 175, 30, INK); });
    return "SMALL CIRCLES";
  }
  if (b === 3) {
    const arr = []; for (let n = 1; n <= 8; n++) arr.push(surv(n));
    const k = Math.floor(ease(u / 0.8) * 8);
    arr.forEach((v, i) => { const px = 120 + i * 120; if (i < k) { rect(px - 48, 560 - 48, 96, 96, i === 0 || i === 7 || i === 3 ? "rgba(214,40,40,0.15)" : null, INK, 4); txt(String(v), px, 560, 52, INK); txt(String(i + 1), px, 650, 28, DOT); } });
    txt("circle size", 540, 720, 28, DOT);
    return "SURVIVOR FOR SIZE 1 … 8";
  }
  if (b === 4) {
    const k = ease((u - 0.35) / 0.4);
    txt("41  =", 540, 480, 56, INK);
    const off = BIN.split("").map((_, i) => i === 0 ? (BIN.length - 1) * 110 * k : -110 * k);
    bits(BIN, 640, 0, off, 110 * Math.sin(3.1416 * k));
    if (u > 0.8) txt("= 19", 540, 840, 64, GRN);
    return u < 0.35 ? "41 IN BINARY" : u < 0.8 ? "MOVE THE LEADING 1 TO THE END" : "010011 = 19";
  }
  if (b === 5) {
    txt("lap 1 removes half", 540, 440, 36, INK);
    const arrow = ease(u / 0.8);
    bits(BIN, 600, 0, null);
    txt("double the old answer…", 540, 760, 34, OR); if (u > 0.4) txt("…binary shift left", 540, 820, 34, OR);
    if (u > 0.7) txt("leading 1 out, 1 in at the back", 540, 900, 34, RED);
    return "WHY IT WORKS";
  }
  ring(540, 640, 320, 41, O41.out, O41.win, 18);
  return "BINARY WAS HIDING IN THE ANSWER";
}
