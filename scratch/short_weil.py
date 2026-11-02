import os, sys
os.environ["SHORT_PID"] = "weil-gotshal-wind-down-20261030-190000"
sys.path.insert(0, "scratch")
import short_native as sn
CTA = {"tts": "The full story is on The Cracked Ledger.", "bg": "gm-building.jpg", "logos": ["weil-logo.png"], "vis": {"type": "cta"}}
GM, BOARD, ELEV, DESK, HALL, STREET = "gm-building.jpg", "local-12.jpg", "local-20.jpg", "local-28.jpg", "local-43.jpg", "local-61.jpg"
sn.SHORTS.update({
 "weil-1": {"music": "darkest-child.mp3", "source": "Bloomberg Law · City AM · Reuters", "segs": [
   {"tts": "A law firm with two billion dollars in revenue lost more than thirty partners in one year.", "bg": GM, "logos": ["weil-logo.png"],
    "vis": {"type": "kinetic", "lines": [["2 billion in revenue", 0.0, "mid"], ["30+", 2.6, "amber"], ["partners gone", 4.0, "mid"]]}},
   {"src": "Then came September", "bg": ELEV, "logos": ["cravath-logo.png"],
    "vis": {"type": "person", "photo": "avatar-aiello.jpg", "label": "SEPT. 2026 · CORPORATE CHAIR", "name": "Michael Aiello", "lines": [["~600 lawyers in his group", "600"], ["Left for Cravath", "Cravath"]]}},
   {"src": "He took five other", "bg": HALL, "logos": ["cravath-logo.png"], "dots": 5, "dots_at": "five", "dots_y": 980, "vis": {"type": "rows", "label": "MICHAEL AIELLO", "rows": [["5 partners", "left with him", "five"]]}},
   {"src": "By late October", "bg": DESK, "logos": ["weil-logo.png"], "dots": 7, "dots_at": "seven", "dots_y": 1060, "vis": {"type": "counter", "label": "MANAGEMENT COMMITTEE", "prefix": "", "value": 7, "dec": 0, "suffix": " gone", "at": "seven", "sub": "left or reported leaving since the end of 2024 (Bloomberg Law)", "sub_at": "since"}},
   {"src": "In a partnership", "bg": STREET, "vis": {"type": "kinetic", "lines": [["In a partnership", 0.0, "mid"], ["NO STOCK", "stock", "amber"], ["to fall.", "fall", "mid"]]}},
   CTA]},
 "weil-2": {"music": "stay-the-course.mp3", "source": "Bloomberg Law · The Wall Street Journal · David Lat", "segs": [
   {"tts": "How does a law firm with two billion dollars in revenue fail without owing money?", "bg": BOARD, "logos": ["weil-logo.png"],
    "vis": {"type": "kinetic", "lines": [["$2 billion", 0.0, "mid"], ["NO DEBT", 1.6, "amber"], ["and it failed?", 3.2, "mid"]]}},
   {"src": "A law firm is not like a bank", "end_before": "assets", "bg": HALL, "vis": {"type": "rows", "label": "A LAW FIRM IS DIFFERENT", "rows": [["Not a bank", "no loans or vaults to seize", "bank"], ["Not a retailer", "no stores or stock", "retailer"], ["Almost nothing", "that cannot walk out the door", "owns"]]}, "dots": 5, "dots_at": "walk", "dots_y": 1340},
   {"src": "A law firm is not like a bank", "start": "assets", "bg": ELEV, "faces": ["avatar-wolf.jpg", "avatar-nee.jpg", "avatar-aiello.jpg", "avatar-zalka.jpg", "avatar-machera.jpg"], "logos": ["weil-logo.png"], "vis": {"type": "kinetic", "lines": [["Its assets are", "assets", "mid"], ["PARTNERS", "partners", "amber"], ["and their relationships", "relationships", "mid"]]}},
   {"src": "If enough of them leave", "bg": DESK, "vis": {"type": "rows", "label": "THE SPIRAL", "rows": [["Partners leave", "revenue falls", "falls"], ["Pay drops", "the rest earn less", "earn"], ["Next group", "has a reason to leave", "reason"]]}},
   {"src": "The comparison is Dewey", "bg": STREET, "logos": ["dewey-logo.png"], "vis": {"type": "bars", "label": "DEWEY & LEBOEUF · 2012", "items": [["Assets at filing", "$193M", 0.79, "#c98a1b", "193"], ["Debt at filing", "$245M", 1.0, "#d63a34", "245"]]}},
   {"src": "Weil is a different case", "bg": GM, "logos": ["weil-logo.png"], "vis": {"type": "bars", "label": "WEIL · REVENUE VS DEBT", "items": [["Revenue 2025 (Am Law)", "$2.08B", 1.0, "#c98a1b", "x"], ["Debt (per the WSJ)", "NONE", 0.0, "#d63a34", "debt"]]}},
   CTA]},
 "weil-3": {"music": "darkest-child.mp3", "source": "Bloomberg Law · The Wall Street Journal · Fortune", "segs": [
   {"tts": "When a law firm shuts down, who gets the bill first?", "bg": GM, "logos": ["weil-logo.png"],
    "vis": {"type": "kinetic", "lines": [["A law firm", 0.0, "mid"], ["shuts down.", 0.9, "mid"], ["WHO PAYS?", 2.2, "amber"]]}},
   {"src": "Associates and staff will be paid", "bg": HALL, "logos": ["weil-logo.png"], "vis": {"type": "rows", "label": "STAFF · PER WEIL", "rows": [["90 days", "paid, with benefits", "90"], ["Bonuses", "if they stay", "eligible"]]}},
   {"src": "One of them, Kroger", "bg": STREET, "logos": ["kroger-logo.png"], "vis": {"type": "counter", "label": "KROGER-ALBERTSONS MERGER · FAILED", "prefix": "$", "value": 24.6, "dec": 1, "suffix": "B", "at": "24", "sub": "Delaware trial under way", "sub_at": "Delaware"}},
   {"src": "And Aiello, the partner", "bg": ELEV, "logos": ["kroger-logo.png", "cravath-logo.png"], "vis": {"type": "person", "photo": "avatar-aiello.jpg", "label": "KROGER'S LEAD DEAL LAWYER", "name": "Michael Aiello", "lines": [["Now at Cravath", "Cravath"], ["Testified in the trial", "testified"]]}},
   {"src": "The biggest remaining", "bg": GM, "logos": ["gm-logo.png"], "vis": {"type": "rows", "label": "THE OFFICE · PER THE WSJ", "rows": [["380,000 sq ft", "lease in the GM Building", "380"]]}},
   {"src": "And on October twenty-ninth", "bg": BOARD, "logos": ["palantir-logo.png"], "vis": {"type": "rows", "label": "OCT. 29", "rows": [["Palantir CFO", "invited would-be Weil summer associates to work there", "Palantir"]]}},
   CTA]},
})
sn.main(sys.argv[1])
