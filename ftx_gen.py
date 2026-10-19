import json, sys
sys.path.insert(0, ".")
import app
FACTS = """
- Nov 2, 2022: CoinDesk reported Alameda Research's $14.6B balance sheet was heavy with FTT, the token FTX itself created. https://www.coindesk.com/business/2022/11/02/divisions-in-sam-bankman-frieds-crypto-empire-blur-on-his-trading-titan-alamedas-balance-sheet
- Binance announced it would sell its FTT; withdrawals surged. Nov 8, 2022 Binance signed a non-binding letter of intent to acquire FTX, then backed out on Nov 9. https://apnews.com/article/ftx-bankruptcy-binance-timeline-c519d50b9059aa8bff0ce8b6cd26c40e
- Nov 11, 2022: FTX, Alameda, FTX US and about 130 affiliates filed Chapter 11 in Delaware; Bankman-Fried resigned as CEO. https://www.reuters.com/business/ftx-start-us-bankruptcy-proceedings-ceo-exit-2022-11-11/
- Dec 13, 2022: SEC complaint: FTX raised more than $1.8B from equity investors; it alleged undisclosed diversion of customer funds to Alameda, a virtually unlimited line of credit, and exemptions from risk controls. https://www.sec.gov/newsroom/press-releases/2022-219
- Dec 13, 2022: CFTC complaint alleged customer assets were commingled with Alameda and that more than $8 billion in customer deposits were lost. https://www.cftc.gov/PressRoom/PressReleases/8638-22
- Nov 2, 2023: a jury convicted Bankman-Fried on all seven counts (wire fraud and conspiracy) after a one-month trial before Judge Lewis A. Kaplan in Manhattan federal court (SDNY). https://www.reuters.com/technology/sam-bankman-fried-be-sentenced-multi-billion-dollar-ftx-fraud-2024-03-28/
- Mar 28, 2024: sentenced to 25 years in prison, 3 years supervised release, about $11B forfeiture. DOJ: he misappropriated billions of customer funds, defrauded FTX investors of more than $1.7B and Alameda lenders of more than $1.3B; the US Attorney said he stole over $8 billion of customers' money. https://www.justice.gov/usao-sdny/pr/samuel-bankman-fried-sentenced-25-years-prison
- Jan 3, 2025: FTX's Chapter 11 plan took effect; it projected about 98% of creditors would receive roughly 119% of allowed claims, with claims valued at November 2022 prices (when crypto prices were far lower). https://restructuring.ra.kroll.com/ftx/ and https://www.reuters.com/legal/crypto-exchange-ftxs-liquidation-plan-receives-court-approval-2024-10-07/
- Jun 8, 2026: DOJ pardon-attorney records show Bankman-Fried applied for a "pardon after completion of sentence"; Trump had said in January he had no intention of pardoning him. https://www.cnbc.com/2026/06/08/sam-bankman-fried-files-formal-request-for-presidential-pardon-.html
- Jun 12, 2026: the Second Circuit unanimously affirmed the conviction and the forfeiture (No. 24-961). https://apnews.com/article/sam-bankman-fried-ftx-cryptocurrency-appeal-e709df4a152e9b3b52a266dd81eb44cc
- Sep 10, 2026: he petitioned the US Supreme Court (No. 26-349); the government's response deadline was extended to Nov 16, 2026. https://www.supremecourt.gov/docket/docketfiles/html/public/26-349.html
""".strip()
THEME = ("Channel 'The Cracked Ledger'. Angle: how FTX customer deposits ended up funding Alameda Research, and how the collapse unfolded in about ten days in November 2022. "
         "Bankman-Fried is CONVICTED: state what the jury found; attribute regulators' and prosecutors' characterizations ('according to the SEC', 'prosecutors said'); "
         "make no new accusations against anyone; note he maintains his innocence and continues to appeal. "
         "End with the 2026 updates (appeal affirmed, pardon request, Supreme Court petition pending, government response due Nov 16) and a reflective close. "
         "Visual prompts must never show realistic faces of real people: use silhouettes, hands, screens, abstract data, buildings. No logos or brand names in visual prompts.")
p = {"title": "FTX: How $8 Billion Vanished Overnight", "niche": "Business & Finance documentary (fraud, rise and fall)",
     "language": "English", "minutes": 10, "theme": THEME, "facts": FACTS}
r = app.write_script(p)
sc = r["scenes"]
print(len(sc), sum(len(s["narration"].split()) for s in sc))
r.update({"niche": p["niche"], "language": "English", "minutes": 10, "theme": THEME, "facts": FACTS, "channel": "The Cracked Ledger"})
r["title"] = r.get("title") or p["title"]
saved = app.save_project(r)
print(saved["id"])
open("ftx_id.txt", "w").write(saved["id"])
