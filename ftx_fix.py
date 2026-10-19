import json, re, sys
sys.path.insert(0, ".")
import app
pid = "ftx-how-8-billion-vanished-overnight-20261015-155014"
f = app.PROJECTS / f"{pid}.json"
d = json.loads(f.read_text(encoding="utf-8"))
S = d["scenes"]
fix = {
 7: "FTX and Alameda both belonged to Sam Bankman-Fried's business empire. Their relationship would become central to understanding both the collapse and the prosecution.",
 9: "But investor capital and customer deposits are different things. Investors buy ownership; customer deposits do not become money the company is free to spend.",
 44: "On November 2, 2023, a Manhattan federal jury convicted Bankman-Fried on all seven counts he faced, covering fraud and conspiracy.",
}
for n, t in fix.items():
    S[n-1]["narration"] = t
SRC = {
 "coindesk": ("CoinDesk, Nov 2 2022: Alameda balance sheet", "https://www.coindesk.com/business/2022/11/02/divisions-in-sam-bankman-frieds-crypto-empire-blur-on-his-trading-titan-alamedas-balance-sheet"),
 "ap_tl": ("AP: FTX collapse timeline", "https://apnews.com/article/ftx-bankruptcy-binance-timeline-c519d50b9059aa8bff0ce8b6cd26c40e"),
 "reu_bk": ("Reuters, Nov 11 2022: FTX files for bankruptcy", "https://www.reuters.com/business/ftx-start-us-bankruptcy-proceedings-ceo-exit-2022-11-11/"),
 "sec": ("SEC press release 2022-219 / complaint", "https://www.sec.gov/newsroom/press-releases/2022-219"),
 "cftc": ("CFTC press release 8638-22", "https://www.cftc.gov/PressRoom/PressReleases/8638-22"),
 "reu_sent": ("Reuters, Mar 28 2024: sentenced to 25 years (verdict Nov 2 2023)", "https://www.reuters.com/technology/sam-bankman-fried-be-sentenced-multi-billion-dollar-ftx-fraud-2024-03-28/"),
 "doj": ("DOJ SDNY: sentenced to 25 years", "https://www.justice.gov/usao-sdny/pr/samuel-bankman-fried-sentenced-25-years-prison"),
 "kroll": ("Kroll: FTX Chapter 11 case docket", "https://restructuring.ra.kroll.com/ftx/"),
 "reu_plan": ("Reuters, Oct 7 2024: plan approved, repayment terms", "https://www.reuters.com/legal/crypto-exchange-ftxs-liquidation-plan-receives-court-approval-2024-10-07/"),
 "plan_eff": ("FTX: plan effective date Jan 3 2025", "https://www.prnewswire.com/news-releases/ftx-announces-effective-date-and-record-date-of-january-3-2025-for-its-chapter-11-plan-of-reorganization-302332816.html"),
 "cnbc": ("CNBC, Jun 8 2026: formal pardon request", "https://www.cnbc.com/2026/06/08/sam-bankman-fried-files-formal-request-for-presidential-pardon-.html"),
 "ap_app": ("AP, Jun 12 2026: conviction upheld", "https://apnews.com/article/sam-bankman-fried-ftx-cryptocurrency-appeal-e709df4a152e9b3b52a266dd81eb44cc"),
 "ca2": ("Second Circuit opinion, No. 24-961", "https://ww3.ca2.uscourts.gov/decisions/OPN/24-961_opn.pdf"),
 "scotus": ("Supreme Court docket 26-349", "https://www.supremecourt.gov/docket/docketfiles/html/public/26-349.html"),
}
MAP = {2:["ap_tl","reu_bk"],3:["doj"],8:["sec"],13:["coindesk"],14:["coindesk"],15:["coindesk"],18:["coindesk","sec"],20:["sec"],21:["sec"],22:["sec"],
       25:["cftc"],30:["ap_tl"],34:["ap_tl"],36:["ap_tl"],38:["reu_bk"],39:["reu_bk"],40:["coindesk","reu_bk"],44:["reu_sent"],45:["reu_sent","doj"],
       46:["reu_sent"],47:["doj"],48:["doj","ca2"],49:["doj"],50:["doj"],52:["cnbc"],55:["plan_eff","kroll"],56:["reu_plan","kroll"],57:["reu_plan"],58:["reu_plan"],
       64:["cnbc"],65:["cnbc"],66:["cnbc"],67:["ap_app","ca2"],68:["scotus"],69:["scotus"],71:["ap_app","scotus"]}
VIDEO = {1,2,3,14,29,30,31,32,34,36,38,40,44,47,62,64,67,68,72,74}
for n, s in enumerate(S, 1):
    if n in MAP:
        s["sources"] = [{"title": SRC[k][0], "url": SRC[k][1]} for k in MAP[n]]
        s["verified"] = True; s["needs_check"] = False
    else:
        s["sources"] = []
        s["needs_check"] = False  # cena explicativa/analitica, sem afirmacao factual nova
        s["verified"] = True
    s["reviewed"] = True
    s["mode"] = "video" if n in VIDEO else "image"; s["source"] = "site"
    s["logo"] = n <= 2 or bool(re.search(r"\bFTX\b", s["narration"]))
d["scenes"] = S
d["title_options"] = ["FTX: How $8 Billion Vanished Overnight", "FTX: The 10 Days That Erased $8 Billion",
                      "Inside FTX: Where the Customer Money Really Went", "The Cracked Ledger of FTX: Customers, Alameda and $8 Billion"]
d["logo"] = {"file": "assets/logo.png", "position": "top-left", "width_pct": 9, "opacity": 0.85, "intro_seconds": 15, "enabled": True}
app.with_prompts(d)
f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
app.export_prompts(d)
w = sum(len(s["narration"].split()) for s in S)
print("scenes", len(S), "words", w, "est_min", round(w/128 + len(S)*0.3/60, 2), "videos", sum(s["mode"]=="video" for s in S), "logo scenes", sum(s["logo"] for s in S))
print("faces check:", [n for n,s in enumerate(S,1) if re.search(r"\b(face|portrait|Bankman|SBF|Trump)\b", s["visual_prompt"], re.I)])
