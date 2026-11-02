const P = 618, GX = 80, GY = 330, CS = 23, RS = 24, TY = 1010, TX = j => 126 + j * 92;
function drawTester(cx, cy, st, lbl) {
  const col = st === "dead" ? RED : st === "ok" ? GRN : st === "on" ? OR : INK;
  circ(cx, cy, 34, col, null, 0, st === "idle" ? 0.1 : 0.25);
  circ(cx, cy, 34, null, col, 5);
  if (lbl) txt(lbl, cx, cy + 1, 26, INK);
}
function scene(t, b, u) {
  let lit = null, nT = 0, tState = j => "idle", statTxt = "", dim = null, fade = 1, groupsK = 0;
  const poisonOn = (b === 0 && u > 0.5) || b > 0;
  let pulse = false, resOn = 0, digOn = 0, labels = false;
  if (b === 0) statTxt = "TESTERS  ?";
  if (b === 1) {
    statTxt = u < 0.33 ? "POISON KILLS IN 1 HOUR" : u < 0.66 ? "ONE ROUND ONLY" : "MANY BOTTLES PER TESTER";
    circ(540, TY, 60, null, INK, 6);
    const a = -1.5708 + u * 6.283; line(540, TY, 540 + 44 * Math.cos(a), TY + 44 * Math.sin(a), INK, 6);
  }
  if (b === 2) {
    statTxt = u < 0.33 ? "TESTERS  1" : u < 0.66 ? "1 TESTER = 2 GROUPS" : "THE TESTER LIVES";
    nT = u > 0.12 ? 1 : 0;
    if (u > 0.33 && u < 0.66) lit = i => i < 500;
    if (u >= 0.66) dim = i => i < 500;
    tState = j => (u > 0.33 && u < 0.66) ? "on" : (u >= 0.66 ? "ok" : "idle");
  }
  if (b === 3) {
    const q = u < 0.25 ? 0 : u < 0.5 ? 1 : u < 0.75 ? 2 : 3;
    const ts = [2, 3, 10, 10][q], gs = [4, 8, 1024, 1024][q];
    nT = ts; statTxt = "TESTERS  " + ts + "  =  " + gs.toLocaleString("en-US") + " GROUPS";
    groupsK = [2, 3, 10, 10][q];
  }
  if (b >= 4) nT = 10;
  if (b === 4) {
    statTxt = "BOTTLE NUMBERS IN BINARY";
    if (u < 0.78) { const j = Math.min(9, Math.floor(u / 0.78 * 10)); lit = i => bit(i, 9 - j); tState = k => k === j ? "on" : "idle"; }
    else { statTxt = "AFTER 1 HOUR"; tState = k => bit(P, 9 - k) ? "dead" : "ok"; digOn = clamp((u - 0.78) / 0.1); labels = true; dim = i => i !== P; }
  }
  if (b === 5) { statTxt = "RESULT"; tState = k => bit(P, 9 - k) ? "dead" : "ok"; digOn = 1; labels = true; dim = i => i !== P; resOn = clamp(u / 0.5); pulse = true; }
  if (b === 6) {
    statTxt = "10 QUESTIONS  =  1 OF 1,000"; fade = 1 - clamp(u / 0.5);
    tState = k => bit(P, 9 - k) ? "dead" : "ok"; digOn = fade; labels = true; resOn = fade; dim = i => i !== P; pulse = true;
  }
  const dimMul = b === 6 ? clamp(1 - u / 0.4) : 1;
  for (let i = 0; i < 1000; i++) {
    const cx = GX + (i % 40) * CS + CS / 2, cy = GY + Math.floor(i / 40) * RS + RS / 2;
    let a = 0.62, r = 5.5, col = DOT;
    if (groupsK > 0) { const n = Math.min(1 << groupsK, 1000), g = Math.floor(i * n / 1000); if (g % 2 === 1) { col = OR; a = 0.55; } }
    if (lit && lit(i)) { col = OR; a = 0.95; r = 7; }
    if (dim && dim(i)) a = 0.1 * dimMul;
    if (i === P && poisonOn) { col = RED; a = 1; r = pulse ? 12 + 3 * Math.sin(t * 7) : 8; }
    circ(cx, cy, r, col, null, 0, a);
  }
  if (pulse) { const cx = GX + (P % 40) * CS + CS / 2, cy = GY + Math.floor(P / 40) * RS + RS / 2; circ(cx, cy, 30 + 4 * Math.sin(t * 7), null, RED, 4, 0.9); }
  if (nT > 0 && fade > 0) {
    x.globalAlpha = fade;
    for (let j = 0; j < nT; j++) {
      const cx = nT === 1 ? 540 : nT <= 3 ? 540 + (j - (nT - 1) / 2) * 140 : TX(j), st = tState(j);
      drawTester(cx, TY, st, st === "dead" ? "x" : st === "ok" && labels ? "ok" : "");
    }
    x.globalAlpha = 1;
  }
  if (digOn > 0) { x.globalAlpha = digOn; for (let j = 0; j < 10; j++) txt(String(bit(P, 9 - j)), TX(j), 1076, 44, bit(P, 9 - j) ? RED : INK); x.globalAlpha = 1; }
  if (resOn > 0) { x.globalAlpha = resOn; txt("1001101010 = 618", 540, 1122, 46, RED); x.globalAlpha = 1; }
  return statTxt;
}
