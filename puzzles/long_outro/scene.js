const NAMES = ["bottles", "doors", "birthday", "circle", "disks", "coins"];
function scene(t, b, u) {
  NAMES.forEach((c, i) => {
    const cx = 220 + (i % 3) * 320, cy = 520 + Math.floor(i / 3) * 190;
    rect(cx - 140, cy - 70, 280, 140, "#e8dcbc", INK, 4);
    txt(String(i + 1), cx - 100, cy - 32, 30, RED, "center"); txt(c, cx + 8, cy + 14, 30, INK, "center");
  });
  if (u > 0.5) txt("Show Your Work", 540, 960, 54, INK);
  return "WHICH ONE FOOLED YOU?";
}
