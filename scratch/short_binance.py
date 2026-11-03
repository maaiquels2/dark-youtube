import os, sys
os.environ["SHORT_PID"] = "binance-hack-north-korea-20261102-150000"
sys.path.insert(0, "scratch")
import short_native as sn
CTA = {"tts": "The full story is on The Cracked Ledger.", "logos": ["binance-logo.png"], "vis": {"type": "cta"}}
sn.SHORTS.update({
 # 1) "20 minutos" (Gate 2: nota 8,5) - o roubo, o recorde e a acusacao do FBI, com fato x alegacao
 "binance-1": {"music": "darkest-child.mp3", "source": "TRM Labs · FBI alert (Oct. 31, 2026) · Binance", "segs": [
   {"tts": "Six point three billion dollars left one crypto exchange in about twenty minutes.",
    "logos": ["binance-logo.png"], "vis": {"type": "kinetic", "lines": [["$6.3B", 0.2, "amber"], ["gone in about", 1.9, "mid"], ["20 minutes", 3.2, "mid"]]}},
   {"src": "The blockchain already told", "logos": ["text:TRM Labs", "binance-logo.png"], "logos_y": 1310, "logos_h": 170, "vis": {"type": "rows", "label": "TRM LABS · OCT. 29", "rows": [["$6.36B", "moved out of Binance wallets", "6"], ["10 chains", "blockchains used", "10"], ["~20 min", "for most of it", "20"]]}},
   {"src": "TRM calls it", "logos": ["text:TRM Labs", "binance-logo.png", "bybit-logo.png"], "vis": {"type": "bars", "label": "LARGEST CRYPTO THEFT · PER TRM", "items": [["Binance · Oct. 2026", "$6.3B", 1.0, "#c98a1b", "largest"], ["Bybit · Feb. 2025", "$1.5B", 0.24, "#d63a34", "Bybit"]]}},
   {"src": "On Saturday, October thirty-first", "logos": ["fbi-seal.png", "binance-logo.png"], "vis": {"type": "rows", "label": "FBI ALERT · OCT. 31", "rows": [["North Korea", "responsible, says the FBI", "North"], ["TraderTraitor", "the group it names", "names"]]}},
   {"src": "Now, fact versus claim", "logos": ["fbi-seal.png"], "vis": {"type": "kinetic", "tag": "FACT VS CLAIM", "lines": [["An attribution,", 0.0, "mid"], ["NOT", "not", "amber"], ["a court ruling.", "court", "mid"]]}},
   CTA]},
 # 2) "Quem congela o que" (Gate 2: nota 8) - stablecoin tem empresa; bitcoin nao
 "binance-2": {"music": "stay-the-course.mp3", "source": "Binance · TRM Labs · Tether · Circle · Aave", "segs": [
   {"tts": "Billions in stolen crypto were frozen within hours. The bitcoin could not be.",
    "vis": {"type": "kinetic", "lines": [["Billions", 0.1, "mid"], ["FROZEN", 1.4, "amber"], ["but not the bitcoin", 3.0, "mid"]]}},
   {"src": "Within hours", "logos": ["aave-logo.png", "tether-logo.png", "circle-logo.png"], "vis": {"type": "rows", "label": "WITHIN HOURS", "rows": [["Aave", "froze its markets", "Aave"], ["$2.36B", "stablecoins frozen by Tether and Circle", "2"]]}},
   {"src": "Here is the part", "logos": ["tether-logo.png", "circle-logo.png"], "vis": {"type": "kinetic", "lines": [["A stablecoin has a", 0.0, "mid"], ["COMPANY", "company", "amber"], ["that can freeze it.", "freeze", "mid"]]}},
   {"src": "Bitcoin and ether have", "logos": ["text:TRM Labs"], "vis": {"type": "counter", "label": "OUT OF REACH · PER TRM", "prefix": "$", "value": 2.4, "dec": 1, "suffix": "B", "at": "2", "sub": "of stolen bitcoin and ether that no one can freeze", "sub_at": "freeze"}},
   {"src": "A freeze does not", "logos": ["binance-logo.png"], "vis": {"type": "rows", "label": "A FREEZE IS NOT A REFUND", "rows": [["Not back", "the money does not return to Binance", "back"], ["Harder", "for the thieves to cash out", "harder"]]}},
   CTA]},
 # 3) "Quem paga a conta" - a promessa, o fundo de 1 bi contra a perda de 6,3, a recompra
 "binance-3": {"music": "darkest-child.mp3", "source": "Binance updates (Oct. 30 – Nov. 1, 2026)", "segs": [
   {"tts": "Six point three billion dollars was stolen. Binance says its customers will not pay for it.",
    "logos": ["binance-logo.png"], "logos_y": 1260, "logos_h": 180, "vis": {"type": "kinetic", "lines": [["$6.3B", 0.1, "amber"], ["stolen.", 1.6, "mid"], ["Customers", 2.9, "mid"], ["won't pay.", 3.8, "mid"]]}},
   {"src": "In its first updates", "logos": ["binance-logo.png"], "vis": {"type": "rows", "label": "SET ASIDE · PER BINANCE", "rows": [["$6.34B+", "of its own funds", "6"], ["3 sources", "users' fund, insurance fund, treasury", "three"]]}},
   {"src": "The users' fund held", "logos": ["binance-logo.png"], "vis": {"type": "bars", "label": "USERS' FUND VS THE LOSS", "items": [["Users' fund (SAFU)", "$1B", 0.16, "#c98a1b", "1"], ["The loss", "$6.3B", 1.0, "#d63a34", "loss"]]}},
   {"src": "It says it is buying back", "logos": ["binance-logo.png"], "logos_y": 1310, "logos_h": 170, "vis": {"type": "rows", "label": "BOUGHT BACK · COMPANY MONEY", "rows": [["80%", "as of Oct. 30", "80"], ["90%", "as of Oct. 31", "90"], ["~95%", "as of Nov. 1", "95"]]}},
   {"src": "The remaining five percent", "end_before": "This", "logos": ["binance-logo.png"], "vis": {"type": "rows", "label": "STILL TO BUY · PER BINANCE", "rows": [["5%", "left to buy back", "5"], ["Less liquid", "tokens outside the top 10, slower to buy", "liquid"]]}},
   {"src": "The remaining five percent", "start": "This", "vis": {"type": "kinetic", "lines": [["Rebuilding", 0.0, "mid"], ["balances.", "balances", "mid"], ["NOT", "not", "amber"], ["getting it back.", "getting", "mid"]]}},
   CTA]},
})
if __name__ == "__main__":
    sn.main(sys.argv[1])
