function mv(n, a, b, c, out) { if (n === 0) return; mv(n - 1, a, c, b, out); out.push([a, c]); mv(n - 1, b, a, c, out); }
function state(n, k) {
  const st = [Array.from({ length: n }, (_, i) => n - i), [], []], m = []; mv(n, 0, 1, 2, m);
  for (let i = 0; i < Math.min(k, m.length); i++) { const [f, t] = m[i]; st[t].push(st[f].pop()); }
  return st;
}
const PX = [220, 540, 860], BASE = 960;
function pegs(st, n) {
  PX.forEach(px => rect(px - 6, BASE - 420, 12, 420, INK, null, 0, 0.8));
  line(100, BASE, 980, BASE, INK, 6);
  const h = Math.min(36, 380 / n);
  st.forEach((s, p) => s.forEach((d, i) => {
    const w = 60 + (d - 1) * (200 / Math.max(1, n - 1));
    rect(PX[p] - w / 2, BASE - (i + 1) * h, w, h - 3, d % 2 ? OR : "#e8dcbc", INK, 3);
  }));
}
function fmt(v) { return v.toLocaleString("en-US"); }
function scene(t, b, u) {
  if (b === 0) { pegs(state(12, 0), 12); return u < 0.5 ? "64 GOLDEN DISKS" : "HOW LONG WILL IT TAKE?"; }
  if (b === 1) { pegs(state(4, 0), 4);
    if (u > 0.33 && u < 0.66) { line(PX[1] - 90, BASE - 200, PX[1] + 90, BASE - 120, RED, 10); txt("NOT ALLOWED", PX[1], BASE - 250, 34, RED); }
    return u < 0.33 ? "ONE DISK AT A TIME" : u < 0.66 ? "NEVER BIG ON SMALL" : "MOVE THE WHOLE STACK"; }
  if (b === 2) { const k = Math.floor(ease(u / 0.9) * 7); pegs(state(3, k), 3); return "3 DISKS  ·  " + k + " / 7 MOVES"; }
  if (b === 3) {
    const rows = [[4, 15], [5, 31], [10, 1023], [20, 1048575]], k = Math.floor(ease(u / 0.85) * 4.99);
    rows.forEach((r, i) => { if (i <= k) {
      txt("n = " + r[0], 260, 470 + i * 130, 50, INK, "center"); txt("→", 440, 470 + i * 130, 50, DOT);
      txt(fmt(r[1]), 700, 470 + i * 130, 56, RED, "center"); } });
    return "EACH DISK DOUBLES THE WORK  +1";
  }
  if (b === 4) {
    txt("2⁶⁴ − 1", 540, 520, 110, INK);
    txt("18,446,744,073,709,551,615", 540, 650, 38, RED); txt("moves", 540, 710, 40, INK);
    if (u > 0.45) { txt("1 move per second", 540, 830, 40, INK); txt("≈ 585 billion years", 540, 910, 56, RED); }
    return "64 DISKS";
  }
  if (b === 5) {
    const w1 = 800 * 13.8 / 585, w2 = 800 * ease(u / 0.7);
    txt("THE UNIVERSE", 540, 500, 34, INK); rect(140, 530, w1, 60, DOT, null, 0, 1); txt("13.8 billion years", 540, 640, 34, INK);
    txt("HANOI, 64 DISKS", 540, 760, 34, INK); rect(140, 790, w2, 60, RED, null, 0, 1); if (u > 0.7) txt("585 billion years", 540, 900, 34, RED);
    return "MORE THAN 40× LONGER";
  }
  const k = Math.floor(ease(u / 0.9) * 11);
  for (let i = 0; i < 11; i++) { if (i > k) continue; const h = Math.max(6, 520 * Math.pow(2, i) / 1024); rect(130 + i * 78, 1010 - h, 60, h, i > 7 ? RED : OR, null, 0, 1); txt(String(i), 160 + i * 78, 1040, 24, INK); }
  return "EXPONENTIAL: SLOW, THEN ALL AT ONCE";
}
