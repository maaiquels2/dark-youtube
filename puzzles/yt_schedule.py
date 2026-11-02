"""Show Your Work Puzzles: agenda um Short por vez no YouTube Studio (Chrome Profile 6, CDP 9335).
Uso: python puzzles/yt_schedule.py <n> [--dry]   (n = 1..6; --dry para antes de confirmar o agendamento)
Confere o canal antes de enviar; para se o Studio nao abrir o canal certo."""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CHANNEL = "UCrgIwaM5dsNRgrKqZkOepRg"
SHOTS = ROOT / "scratch" / "yt"
EPS = {
 1: ("ep01_poisoned_bottles", "1,000 bottles, one poisoned: 10 testers is enough", "Oct 26, 2026",
     "One of these 1,000 bottles is poisoned. How many testers do you need to find it in one hour? Binary has the answer.\n\n#math #puzzle #binary #shorts"),
 2: ("ep02_monty_hall", "100 doors: should you switch?", "Oct 27, 2026",
     "100 doors, one car. You pick one, the host opens 98 empty ones. Stay or switch?\n\n#math #montyhall #probability #shorts"),
 3: ("ep03_birthday_paradox", "How many people before two share a birthday?", "Oct 28, 2026",
     "Why do just 23 people give you a 50% chance of a shared birthday? Count the pairs.\n\n#math #probability #birthdayparadox #shorts"),
 4: ("ep04_josephus", "41 people in a circle: who survives?", "Oct 29, 2026",
     "41 people in a circle, every second one is out. Who survives? A binary shortcut gives the answer.\n\n#math #puzzle #binary #shorts"),
 5: ("ep05_tower_of_hanoi", "64 disks: 585 billion years", "Oct 30, 2026",
     "Move 64 disks one at a time and it takes about 585 billion years.\n\n#math #towerofhanoi #exponential #shorts"),
 6: ("ep06_hh_vs_ht", "HH or HT: which coin pattern waits longer?", "Oct 31, 2026",
     "Same coin, same odds, but waiting for HH takes 6 flips on average and HT only 4.\n\n#math #probability #coinflip #shorts"),
}
EPS2 = {
 1: ("ep07_moser_circle", "1, 2, 4, 8, 16... what's next? (not 32)", "Nov 2, 2026",
     "The pattern 1, 2, 4, 8, 16 breaks at 6. Count the regions of a circle cut by lines and see why.\n\n#math #puzzle #pattern #shorts"),
 2: ("ep08_party_of_six", "6 people at a party: there is always a trio", "Nov 3, 2026",
     "Six people, two colors of lines, and a triangle you cannot avoid.\n\n#math #ramsey #graphtheory #shorts"),
 3: ("ep09_medical_test", "A 99% accurate test says positive: are you sick?", "Nov 4, 2026",
     "A rare disease, an accurate test, and why a positive result means only about 50%.\n\n#math #probability #bayes #shorts"),
 4: ("ep10_simpson", "A beats B twice, but B wins overall", "Nov 5, 2026",
     "Real kidney stone data where the trend flips when you combine the groups (Simpson's paradox).\n\n#math #statistics #simpsonsparadox #shorts"),
 5: ("ep11_hat_prisoners", "100 prisoners, red or blue hats: how many survive?", "Nov 6, 2026",
     "One bit of parity can save 99 of 100 prisoners.\n\n#math #puzzle #logic #shorts"),
 6: ("ep12_ant_rope", "An ant on a stretching rope: does it arrive?", "Nov 7, 2026",
     "Yes, but it takes about e^100,000 seconds. The harmonic series at work.\n\n#math #infinity #harmonicseries #shorts"),
 7: ("ep13_two_envelopes", "Two envelopes, one holds double: should you switch?", "Nov 8, 2026",
     "Two envelopes, one holds twice the other. You open yours: $100. Switch? The math says yes, then says switch back.\n\n#math #probability #paradox #shorts"),
 8: ("ep14_prisoner_boxes", "100 prisoners, 100 boxes: from 0% to 31%", "Nov 9, 2026",
     "100 prisoners, 100 boxes, 50 tries each. Random guessing: about 0%. With the right plan: about 31%.\n\n#math #puzzle #probability #shorts"),
}
TIME = "1:00 PM"
# serie How It Works: (pasta, titulo, data, descricao, hora); video = <pasta>/renders/mounjaro_up.mp4 etc. (<nome>_up.mp4)
HIW = {
 1: ("mounjaro", "How Mounjaro actually works inside your body", "Oct 30, 2026",
     "Mounjaro (tirzepatide) copies two gut hormones, GLP-1 and GIP. Here is what it does in the pancreas, the stomach and the brain, "
     "and what the biggest trial found.\n\nSource: Jastreboff et al., \"Tirzepatide Once Weekly for the Treatment of Obesity\" (SURMOUNT-1), "
     "NEJM 2022. 15 mg vs placebo, 72 weeks.\nNot medical advice. Prescription only: talk to your doctor.\n"
     "Music: \"Echoes of Time v2\" by Kevin MacLeod (incompetech.com), CC BY 4.0.\n\n#howitworks #science #health #mounjaro #shorts", "7:00 PM"),
 2: ("caffeine", "Coffee doesn't give you energy. Here's what it really does", "Oct 31, 2026",
     "Caffeine is shaped almost exactly like adenosine, the molecule that builds sleep pressure all day. It blocks the receptors "
     "without switching them on, so the tiredness signal can't get through. Until it wears off.\n\n"
     "Source: U.S. FDA, \"Spilling the Beans: How Much Caffeine Is Too Much?\" (up to 400 mg a day for most healthy adults).\n"
     "Not medical advice.\nMusic: \"Stay the Course\" by Kevin MacLeod (incompetech.com), CC BY 4.0.\n\n"
     "#howitworks #science #caffeine #coffee #shorts", "7:00 PM"),
 3: ("ibuprofen", "Ibuprofen doesn't fix the pain. It mutes the alarm", "Nov 1, 2026",
     "Injured tissue makes prostaglandins, the body's alarm messengers, through an enzyme called cyclooxygenase (COX). "
     "Ibuprofen blocks that enzyme: less pain, less swelling, lower fever. But the same enzyme family protects your stomach lining.\n\n"
     "Sources: StatPearls, \"Ibuprofen\" (NCBI Bookshelf); U.S. FDA Drug Safety Communication, July 9, 2015 (non-aspirin NSAIDs and "
     "heart attack/stroke risk); MedlinePlus, Ibuprofen.\nNot medical advice. Read the label and ask a pharmacist or doctor.\n"
     "Music: \"Interloper\" by Kevin MacLeod (incompetech.com), CC BY 4.0.\n\n#howitworks #science #health #ibuprofen #shorts", "7:00 PM"),
}


def shot(pg, name):
    SHOTS.mkdir(parents=True, exist_ok=True); pg.screenshot(path=str(SHOTS / f"{name}.png"), timeout=60000)


def fill(pg, sel, text):
    pg.locator(sel).first.click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.keyboard.insert_text(text); time.sleep(1)
    pg.evaluate("() => document.activeElement && document.activeElement.blur()"); time.sleep(0.7)


def main():
    n = int(sys.argv[1]); dry = "--dry" in sys.argv
    global TIME
    if "--hiw" in sys.argv:
        folder, title, date, desc, TIME = HIW[n]
        # o Playwright por CDP nao envia > 50 MB: usar a copia <folder>_yt.mp4 (~5 Mbps) quando existir
        r = ROOT / "puzzles" / folder / "renders"
        video = r / f"{folder}_yt.mp4" if (r / f"{folder}_yt.mp4").is_file() else r / f"{folder}.mp4"
    else:
        folder, title, date, desc = (EPS2 if "--week2" in sys.argv else EPS)[n]
        video = ROOT / "puzzles" / folder / "renders" / f"{folder}_loud.mp4"
    assert video.is_file(), video
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9335"); ctx = b.contexts[0]
        pg = ctx.new_page(); pg.bring_to_front()
        pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}", wait_until="domcontentloaded"); time.sleep(6)
        if CHANNEL not in pg.url or "Show Your Work Puzzles" not in pg.inner_text("body"):
            shot(pg, "wrong-channel"); raise SystemExit(f"canal errado: {pg.url}")
        if "--resume" in sys.argv:
            pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/short", wait_until="domcontentloaded"); time.sleep(8)
            row = pg.locator("ytcp-video-row").filter(has_text=title).first
            row.get_by_text("Edit draft").first.click(); time.sleep(6)
            vid = "resumed"
        else:
            pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud", wait_until="domcontentloaded"); time.sleep(6)
            # caminho direto pelo CDP (mesma maquina): set_input_files copia o arquivo e trava acima de ~50 MB
            pg.locator("input[type=file]").first.wait_for(state="attached")
            cdp = ctx.new_cdp_session(pg); root = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})["root"]["nodeId"]
            node = cdp.send("DOM.querySelector", {"nodeId": root, "selector": "input[type=file]"})["nodeId"]
            cdp.send("DOM.setFileInputFiles", {"nodeId": node, "files": [str(video)]}); time.sleep(12)
            fill(pg, "#title-textarea #textbox", title); fill(pg, "#description-textarea #textbox", desc)
            pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.click(); time.sleep(1)
            pg.locator("#toggle-button").first.click(); time.sleep(2)
            pg.locator("tp-yt-paper-radio-button[name=VIDEO_HAS_ALTERED_CONTENT_YES]").first.click(); time.sleep(1)
            vid = pg.locator("ytcp-video-info a").first.get_attribute("href").rsplit("/", 1)[-1]; shot(pg, f"{n}-01-details")
        for _ in range(3):
            pg.locator("#next-button").click(); time.sleep(3)
        pg.locator("#second-container-expand-button").click(); time.sleep(2)
        pg.locator("#datepicker-trigger").click(); time.sleep(2)
        di = pg.locator("ytcp-date-picker input").filter(visible=True).first; di.fill(date); pg.keyboard.press("Enter"); time.sleep(2)
        ti = pg.locator("#time-of-day-container input").first; ti.click(); ti.fill(TIME); pg.keyboard.press("Enter"); time.sleep(2)
        shot(pg, f"{n}-02-schedule")
        if dry:
            print("DRY:", vid, "(nao confirmado)"); return
        pg.locator("#done-button").click(); time.sleep(8); shot(pg, f"{n}-03-done")
        for sel in ("#close-button", "ytcp-button#close-button"):
            if pg.locator(sel).filter(visible=True).count(): pg.locator(sel).filter(visible=True).first.click(); break
        time.sleep(2); print("agendado:", n, title, date, TIME, vid); pg.close()


main()
