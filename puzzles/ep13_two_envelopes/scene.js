function env(cx, cy, label, col, hl) {
  rect(cx - 150, cy - 95, 300, 190, "#f3e7c6", hl || INK, hl ? 8 : 5);
  line(cx - 150, cy - 95, cx, cy + 10, INK, 4, 0.6); line(cx + 150, cy - 95, cx, cy + 10, INK, 4, 0.6);
  txt(label, cx, cy + 55, 52, col || INK);
}
function scene(t, b, u) {
  if (b === 0) { env(300, 640, "$100", RED, RED); env(780, 640, "?", INK); txt("one holds twice the other", 540, 880, 44, INK); return "TWO ENVELOPES"; }
  if (b === 1) { env(300, 640, "$100", RED, RED); env(780, 640, u < 0.5 ? "$50" : "$200", u < 0.5 ? OR : GRN); txt("$50 or $200, 50/50", 540, 880, 48, INK); return "THE OTHER ENVELOPE"; }
  if (b === 2) {
    txt("+$100", 300, 600, 90, GRN); txt("-$50", 780, 600, 90, RED); txt("half the time each", 540, 740, 40, INK);
    if (u > 0.4) txt("average: $125 > $100", 540, 880, 62, OR);
    if (u > 0.75) txt("so switch!", 540, 990, 70, RED);
    return "THE TEMPTING ARGUMENT";
  }
  if (b === 3) { env(300, 640, "switch", INK); env(780, 640, "back?", RED); txt(u < 0.5 ? "works for any amount" : "…it can't be right", 540, 880, 52, u < 0.5 ? INK : RED); return "SOMETHING IS WRONG"; }
  if (b === 4) {
    txt("$10 and $20", 540, 520, 64, INK);
    txt("switch up: +$10", 540, 660, 60, GRN); if (u > 0.3) txt("switch down: -$10", 540, 760, 60, RED);
    if (u > 0.6) txt("average gain: $0", 540, 920, 70, OR);
    return "COUNT THE MONEY";
  }
  txt("50/50 for every amount?", 540, 640, 56, RED); txt("no fair random pick over all numbers", 540, 760, 40, INK);
  if (u > 0.5) txt("switching = staying", 540, 900, 70, GRN);
  return "THE HIDDEN MISTAKE";
}
