const SA = "THTHH", SB = "TTHT";
function strip(s, y, k, hiFrom) {
  for (let i = 0; i < s.length; i++) {
    if (i >= k) continue;
    const px = 540 + (i - (s.length - 1) / 2) * 130, hit = hiFrom >= 0 && i >= hiFrom;
    circ(px, y, 48, s[i] === "H" ? "#e8dcbc" : "#c9c2ad", hit ? RED : INK, hit ? 8 : 4);
    txt(s[i], px, y, 48, hit ? RED : INK);
  }
}
let seed = 12345;
function rb() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return (seed >> 16) & 1; }
function wait(pat) { let prev = -1, n = 0; for (;;) { const f = rb(); n++; if (prev === 1 && f === (pat === "HH" ? 1 : 0)) return n; prev = f; } }
const GT = [], GH = []; for (let i = 0; i < 12; i++) { GT.push(wait("HT")); GH.push(wait("HH")); }
const avg = a => a.reduce((s, v) => s + v, 0) / a.length;
function node(cx, cy, label, hi) { circ(cx, cy, 70, hi ? "rgba(214,40,40,0.15)" : "#e8dcbc", hi ? RED : INK, 5); txt(label, cx, cy, 30, INK); }
function arrow(x1, y1, x2, y2, lab, col, lx, ly) { line(x1, y1, x2, y2, col || INK, 5); txt(lab, lx, ly, 36, col || INK); }
function machine(kind, hiEdge) {
  node(200, 640, "start"); node(540, 640, "H"); node(880, 640, "done");
  arrow(270, 640, 470, 640, "H", INK, 370, 600);
  arrow(610, 640, 810, 640, kind === "HT" ? "T" : "H", INK, 710, 600);
  txt(kind === "HT" ? "T: stay" : "T: stay", 200, 540, 30, INK); txt("↺", 200, 575, 50, INK);
  if (kind === "HT") { txt("H: stay", 540, 540, 30, hiEdge ? GRN : INK); txt("↺", 540, 575, 50, hiEdge ? GRN : INK); }
  else { arrow(540, 730, 250, 730, "T: back to start", hiEdge ? RED : INK, 395, 790); }
}
function scene(t, b, u) {
  if (b === 0) {
    strip(SA, 520, Math.floor(u / 0.45 * 5) + 1, u > 0.45 ? 3 : (u > 0.3 ? 3 : -1));
    if (u > 0.5) strip(SB, 760, Math.floor((u - 0.5) / 0.45 * 4) + 1, u > 0.8 ? 2 : -1);
    return u < 0.5 ? "GAME A: WAIT FOR HH" : "GAME B: WAIT FOR HT";
  }
  if (b === 1) {
    strip(SA, 520, 9, 3); strip(SB, 760, 9, 2);
    txt("A", 100, 520, 44, RED); txt("B", 100, 760, 44, RED);
    return u < 0.33 ? "GAME A: UNTIL HH" : u < 0.66 ? "GAME B: UNTIL HT" : "COUNT THE FLIPS · AVERAGE";
  }
  if (b === 2) {
    const k = ease(u / 0.8);
    txt("HT", 150, 560, 44, INK); rect(220, 530, 100 * 4 * k, 60, GRN, null, 0, 1); if (k > 0.95) txt("4 flips", 220 + 400 + 80, 560, 36, INK);
    txt("HH", 150, 740, 44, INK); rect(220, 710, 100 * 6 * k, 60, RED, null, 0, 1); if (k > 0.95) txt("6 flips", 220 + 600 + 80, 740, 36, INK);
    return "AVERAGE FLIPS: HT 4 · HH 6";
  }
  if (b === 3) { machine("HT", u > 0.45); return "HT: A SECOND HEAD KEEPS YOU AT H"; }
  if (b === 4) { machine("HH", u > 0.45); return "HH: A TAIL SENDS YOU BACK"; }
  if (b === 5) {
    const k = Math.floor(ease(u / 0.8) * 12);
    txt("HT", 300, 440, 40, GRN); txt("HH", 780, 440, 40, RED);
    for (let i = 0; i < k; i++) {
      rect(130, 480 + i * 42, GT[i] * 36, 30, GRN, null, 0, 1); rect(600, 480 + i * 42, GH[i] * 36, 30, RED, null, 0, 1);
    }
    if (k >= 12) { txt("avg " + avg(GT).toFixed(1), 300, 1030, 36, GRN); txt("avg " + avg(GH).toFixed(1), 780, 1030, 36, RED); }
    return "12 SAMPLE GAMES EACH";
  }
  txt("same chance at every spot:  25%", 540, 560, 40, INK);
  txt("HT waits 4", 300, 720, 44, GRN); txt("HH waits 6", 780, 720, 44, RED);
  if (u > 0.4) txt("clumps make you wait", 540, 880, 48, RED);
  return "AVERAGES HIDE PATTERNS";
}
