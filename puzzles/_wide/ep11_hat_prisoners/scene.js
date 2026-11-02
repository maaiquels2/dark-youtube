const HAT = [0, 1, 1, 0, 1, 0, 0, 1, 0, 1], BLU = "#1f5fbf";   // 1 = red; index 0 = back of the line
const HX = i => 110 + i * 96, HY = 640;
const REDS_AHEAD = HAT.slice(1).reduce((s, v) => s + v, 0), CODE = REDS_AHEAD % 2;   // 1 = odd
function person(i, st, hide) {
  const x0 = HX(i);
  circ(x0, HY, 30, "#e8dcbc", st === "ok" ? GRN : st === "back" ? OR : INK, 5);
  line(x0, HY + 30, x0, HY + 120, INK, 5);
  if (!hide) { x.fillStyle = HAT[i] ? RED : BLU; x.fillRect(x0 - 26, HY - 62, 52, 28); }
  else { txt("?", x0, HY - 46, 34, INK); }
}
function line10(sts, hideBack) { for (let i = 0; i < 10; i++) person(i, sts[i] || "", false); }
function deduce(p) {          // what prisoner p announces, using the code and the answers already heard
  const seen = HAT.slice(p + 1).reduce((s, v) => s + v, 0), heard = HAT.slice(1, p).reduce((s, v) => s + v, 0);
  const remaining = (CODE - heard % 2 + 2) % 2;
  return { seen, red: ((remaining - seen % 2) + 2) % 2 === 1 };
}
function scene(t, b, u) {
  if (b === 0) { line10({ 0: "back" }); txt("each sees only the hats ahead", 540, 900, 40, INK); return u < 0.5 ? "100 PRISONERS · RED OR BLUE" : "HOW MANY CAN BE SAVED FOR SURE?"; }
  if (b === 1) { line10({ 0: "back" }); txt("1 word each, heard by everyone", 540, 900, 44, INK); return "PLAN FIRST, THEN SPEAK"; }
  if (b === 2) {
    [0, 1].forEach((i, k) => { const x0 = 330 + k * 420; circ(x0, 600, 50, "#e8dcbc", INK, 6); line(x0, 650, x0, 790, INK, 6); x.fillStyle = HAT[i] ? RED : BLU; x.fillRect(x0 - 44, 520, 88, 40); });
    if (u > 0.35) txt("\"" + (HAT[1] ? "red" : "blue") + "\"", 330, 900, 56, HAT[1] ? RED : BLU);
    if (u > 0.7) { txt("my hat is " + (HAT[1] ? "red" : "blue") + "!", 750, 900, 44, GRN); }
    return "2 PRISONERS: 1 SAVED FOR SURE";
  }
  if (b === 3) {
    line10({ 0: "back" });
    txt("reds ahead: " + REDS_AHEAD + (REDS_AHEAD % 2 ? " (odd)" : " (even)"), 540, 900, 44, INK);
    if (u > 0.5) txt("says \"" + (CODE ? "blue" : "red") + "\"  (a code)", 540, 990, 52, OR);
    return "THE BACK PRISONER SAYS PARITY";
  }
  if (b === 4) {
    const p = Math.min(9, 1 + Math.floor(u * 9)), st = { 0: "back" };
    for (let i = 1; i < p; i++) st[i] = "ok"; st[p] = "back";
    line10(st); const d = deduce(p);
    txt("prisoner " + (p + 1) + " sees " + d.seen + " red", 540, 900, 44, INK);
    txt("code + answers heard → mine is " + (d.red ? "red" : "blue"), 540, 980, 38, d.red ? RED : BLU);
    return "EACH ONE UPDATES THE COUNT";
  }
  const st = { 0: "back" }; for (let i = 1; i < 10; i++) st[i] = "ok";
  line10(st); txt("99 saved for sure", 540, 900, 70, GRN); txt("the first: 50 / 50", 540, 1000, 44, OR);
  return "ONE BIT, PASSED DOWN THE LINE";
}
