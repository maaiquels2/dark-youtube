const CARDS = ["1,000 bottles", "100 doors", "23 people", "41 in a circle", "64 disks", "HH or HT?"];
function scene(t, b, u) {
  CARDS.forEach((c, i) => {
    const a = ease((u - (0.12 + i * 0.1)) / 0.08);
    if (a <= 0) return;
    const cx = 220 + (i % 3) * 320, cy = 520 + Math.floor(i / 3) * 190;
    x.globalAlpha = a; rect(cx - 140, cy - 70, 280, 140, "#e8dcbc", INK, 4); x.globalAlpha = 1;
    txt(String(i + 1), cx - 100, cy - 32, 30, RED, "center"); txt(c, cx + 8, cy + 14, 28, INK, "center");
  });
  if (u > 0.78) txt("one pencil. all the work.", 540, 960, 40, RED);
  return "SIX OBVIOUS ANSWERS";
}
