"""Show Your Work Puzzles: envia o video longo (6 desafios), com miniatura e capitulos, e agenda (Chrome Profile 6, CDP 9335).
Uso: python puzzles/yt_long.py [--dry]"""
import subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CHANNEL = "UCrgIwaM5dsNRgrKqZkOepRg"
WEEK2 = "--week2" in sys.argv
VIDEO = ROOT / "puzzles" / "long" / ("week2_long.mp4" if WEEK2 else "6_puzzles_long.mp4")
THUMB = ROOT / "puzzles" / "long" / ("thumb_B.png" if WEEK2 else "thumb_A.png")
SEGS = [("long_intro", "Intro: six obvious answers"), ("ep01_poisoned_bottles", "Puzzle 1: 1,000 bottles, one poisoned"),
        ("ep02_monty_hall", "Puzzle 2: 100 doors, switch or stay?"), ("ep03_birthday_paradox", "Puzzle 3: 23 people and a shared birthday"),
        ("ep04_josephus", "Puzzle 4: 41 people in a circle"), ("ep05_tower_of_hanoi", "Puzzle 5: 64 disks, 585 billion years"),
        ("ep06_hh_vs_ht", "Puzzle 6: HH or HT?"), ("long_outro", "Which one fooled you?")]
SEGS2 = [("long_intro2", "Intro: six more traps"), ("ep07_moser_circle", "Puzzle 1: 1, 2, 4, 8, 16, ?"),
         ("ep08_party_of_six", "Puzzle 2: six people at a party"), ("ep09_medical_test", "Puzzle 3: the 99% test"),
         ("ep10_simpson", "Puzzle 4: A beats B twice"), ("ep11_hat_prisoners", "Puzzle 5: 100 prisoners and hats"),
         ("ep12_ant_rope", "Puzzle 6: the ant on the rope"), ("long_outro2", "Which one fooled you?")]
if WEEK2: SEGS = SEGS2
TITLE = "1, 2, 4, 8, 16, 31?! 6 Puzzles That Fool Everyone" if WEEK2 else "6 Puzzles Where Your Gut Is Wrong (Proof Included)"
DATE, TIME = ("Nov 8, 2026" if WEEK2 else "Nov 1, 2026"), "1:00 PM"


def dur(name):
    f = ROOT / "puzzles" / "_wide" / name / "renders" / f"{name}.mp4"
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))


def chapters():
    t, out = 0.0, []
    for name, label in SEGS:
        out.append(f"{int(t // 60)}:{int(t % 60):02d} {label}"); t += dur(name)
    return "\n".join(out)


def description():
    intro = ("Six more puzzles where the obvious answer is wrong, each solved step by step: a pattern that breaks at six, a party that "
             "always hides a triangle, a 99% test that means 50%, a treatment that wins and loses, a line of prisoners with hats, and an ant on a stretching rope."
             if WEEK2 else
             "Six classic puzzles where the obvious answer is wrong, each solved step by step: the poisoned bottles and binary, "
             "the Monty Hall problem with 100 doors, the birthday paradox, the Josephus circle, the Tower of Hanoi and two coin patterns "
             "that should be equal but are not.")
    return (intro + "\n\nChapters:\n" + chapters() +
            "\n\nShort versions of every puzzle live on this channel.\n\n#math #puzzles #probability #binary #logic")


def fill(pg, sel, text):
    pg.locator(sel).first.click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.keyboard.insert_text(text); time.sleep(1)
    pg.evaluate("() => document.activeElement && document.activeElement.blur()"); time.sleep(0.7)


def main():
    dry = "--dry" in sys.argv
    desc = description(); print(desc)
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9335", timeout=30000); ctx = b.contexts[0]
        pg = ctx.new_page(); pg.bring_to_front()
        pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}", wait_until="domcontentloaded"); time.sleep(6)
        if CHANNEL not in pg.url or "Show Your Work Puzzles" not in pg.inner_text("body"): raise SystemExit("canal errado: " + pg.url)
        pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud", wait_until="domcontentloaded"); time.sleep(6)
        pg.locator("input[type=file]").first.set_input_files(str(VIDEO)); time.sleep(20)
        fill(pg, "#title-textarea #textbox", TITLE); fill(pg, "#description-textarea #textbox", desc)
        if pg.locator("input#file-loader").count():
            pg.locator("input#file-loader").first.set_input_files(str(THUMB)); time.sleep(6)
        else:
            print("AVISO: sem campo de miniatura (canal talvez nao verificado); envio sem miniatura propria")
        pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.click(); time.sleep(1)
        pg.locator("#toggle-button").first.click(); time.sleep(2)
        pg.locator("tp-yt-paper-radio-button[name=VIDEO_HAS_ALTERED_CONTENT_YES]").first.click(); time.sleep(1)
        vid = pg.locator("ytcp-video-info a").first.get_attribute("href").rsplit("/", 1)[-1]
        pg.screenshot(path=str(ROOT / "scratch" / "yt" / "long-01-details.png"), timeout=60000)
        for _ in range(3):
            pg.locator("#next-button").click(); time.sleep(3)
        if "--now" in sys.argv:
            pg.locator("tp-yt-paper-radio-button[name=PUBLIC]").first.click(); time.sleep(2)
        else:
            pg.locator("#second-container-expand-button").click(); time.sleep(2)
            pg.locator("#datepicker-trigger").click(); time.sleep(2)
            di = pg.locator("ytcp-date-picker input").filter(visible=True).first; di.fill(DATE); pg.keyboard.press("Enter"); time.sleep(2)
            ti = pg.locator("#time-of-day-container input").first; ti.click(); ti.fill(TIME); pg.keyboard.press("Enter"); time.sleep(2)
        pg.screenshot(path=str(ROOT / "scratch" / "yt" / "long-02-schedule.png"), timeout=60000)
        if dry: print("DRY", vid); return
        pg.locator("#done-button").click(); time.sleep(10)
        pg.screenshot(path=str(ROOT / "scratch" / "yt" / "long-03-done.png"), timeout=60000)
        print("publicado agora:" if "--now" in sys.argv else "agendado:", vid)


main()
