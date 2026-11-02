const CAR = 57, PICK = 6;
const gx = i => 126 + (i % 10) * 92, gy = i => 370 + Math.floor(i / 10) * 64;
const OTH = []; for (let i = 0; i < 100; i++) if (i !== CAR && i !== PICK) OTH.push(i);
function door(cx, cy, w, h, o) {
  const a = o.alpha == null ? 1 : o.alpha;
  if (o.open) { rect(cx - w / 2, cy - h / 2, w, h, "rgba(60,90,140,0.10)", INK, 2, a * 0.35); return; }
  rect(cx - w / 2, cy - h / 2, w, h, "#e8dcbc", o.pick ? OR : INK, o.pick ? 8 : 3, a);
  if (o.car) circ(cx, cy, Math.min(w, h) * 0.22, RED, null, 0, a);
}
function bars(sp, wp, y, a) {
  txt("STAY", 180, y, 30, INK, "right"); rect(200, y - 22, 700 * sp, 44, DOT, null, 0, a);
  txt(Math.round(sp * 100) + "%", 200 + 700 * sp + 14, y, 30, INK, "left");
  txt("SWITCH", 180, y + 64, 30, INK, "right"); rect(200, y + 42, 700 * wp, 44, GRN, null, 0, a);
  txt(Math.round(wp * 100) + "%", 200 + 700 * wp - 14, y + 64, 30, "#fff", "right");
}
function grid(opened, showCar, pickOn, carPulse) {
  const op = new Set(OTH.slice(0, opened));
  for (let i = 0; i < 100; i++)
    door(gx(i), gy(i), 58, 48, { open: op.has(i), car: showCar && i === CAR, pick: pickOn && i === PICK });
  if (carPulse) circ(gx(CAR), gy(CAR), 40 + 5 * Math.sin(T * 6), null, GRN, 6);
}
let T = 0;
function scene(t, b, u) {
  T = t;
  if (b === 0) {
    grid(u > 0.6 ? Math.floor((u - 0.6) / 0.4 * 98) : 0, false, u > 0.3, false);
    return u < 0.3 ? "100 DOORS  ·  1 CAR" : u < 0.6 ? "YOU PICK DOOR 7" : "THE HOST OPENS 98 DOORS";
  }
  if (b === 1) {
    grid(u > 0.66 ? Math.floor((u - 0.66) / 0.34 * 98) : 0, u < 0.33, u > 0.33, false);
    return u < 0.33 ? "1 CAR  ·  99 GOATS" : u < 0.66 ? "THE HOST KNOWS" : "HE NEVER OPENS THE CAR";
  }
  if (b === 2) {
    const xs = [220, 540, 860];
    for (let i = 0; i < 3; i++) {
      txt(String(i + 1), xs[i], 360, 44, INK);
      door(xs[i], 560, 200, 300, { open: i === 2 && u > 0.25, car: i === 1 && u > 0.85, pick: i === 0 });
    }
    if (u > 0.25) txt("goat", xs[2], 560, 40, INK, "center", "bold");
    if (u > 0.5) bars(1 / 3, 2 / 3, 900, 1);
    return u < 0.25 ? "3 DOORS  ·  YOU PICK ONE" : u < 0.5 ? "THE HOST OPENS A GOAT" : "STAY 1/3  ·  SWITCH 2/3";
  }
  if (b === 3) {
    if (u < 0.5) {
      for (let i = 0; i < 10; i++) door(126 + i * 92, 560, 70, 140, { open: i !== 2 && i !== 6, car: false, pick: i === 2 });
      bars(0.1, 0.9, 860, 1);
      return "10 DOORS  ·  STAY 10%  ·  SWITCH 90%";
    }
    grid(98, false, true, false); bars(0.01, 0.99, 1040, 1);
    return "100 DOORS  ·  STAY 1%  ·  SWITCH 99%";
  }
  if (b === 4) {
    grid(98, false, true, u > 0.6);
    const px = gx(PICK), py = gy(PICK), cx = gx(CAR), cy = gy(CAR);
    txt("YOUR PICK: 1%", px, py + 60, 30, OR, "center");
    if (u > 0.3) txt("THE OTHER DOOR: 99%", cx, cy + 60, 30, GRN, "center");
    return "WHERE DID THE 99% GO?";
  }
  if (b === 5) {
    const n = Math.floor(clamp(u / 0.8) * 100);
    for (let i = 0; i < 100; i++) {
      const cx = gx(i), cy = gy(i), played = i < n, stay = i === 37;
      circ(cx, cy, played ? 20 : 8, played ? (stay ? RED : GRN) : DOT, null, 0, played ? 1 : 0.35);
    }
    const sw = n - (n > 37 ? 1 : 0), st = n > 37 ? 1 : 0;
    txt("STAY WINS " + st, 300, 1060, 34, RED, "center");
    txt("SWITCH WINS " + sw, 740, 1060, 34, GRN, "center");
    return "100 GAMES";
  }
  const f = 1 - clamp(u / 0.5);
  for (let i = 0; i < 100; i++) door(gx(i), gy(i), 58, 48, { open: i !== CAR, car: i === CAR, alpha: i === CAR ? 1 : f });
  circ(gx(CAR), gy(CAR), 40, null, GRN, 6);
  return "A CHOICE IS EVIDENCE";
}
