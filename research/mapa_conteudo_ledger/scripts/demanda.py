# Mede a procura por temas candidatos do Ledger: 1 search.list (100 un.) por tema, vídeos dos últimos 24 meses
# ordenados por views, + videos.list/channels.list em lote. A chave vem do .env e nunca é impressa.
import json, csv, time, statistics, requests
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[3]; OUT = Path(__file__).resolve().parents[1]
KEY = next(l.split('=', 1)[1].strip().strip('"') for l in open(ROOT / '.env', encoding='utf-8') if l.startswith('YOUTUBE_API_KEY='))
API = 'https://www.googleapis.com/youtube/v3/'
TOPICS = {
 # pilar 1: marcas famosas que caíram
 'Blockbuster': 'what happened to blockbuster', 'Toys R Us': 'toys r us collapse', 'Sears': 'sears collapse', 'Kodak': 'kodak downfall',
 'Nokia': 'nokia downfall', 'BlackBerry': 'blackberry downfall', 'Bed Bath & Beyond': 'bed bath and beyond collapse', 'Red Lobster': 'red lobster bankruptcy',
 'Pan Am': 'pan am collapse', 'RadioShack': 'radioshack collapse', 'Circuit City': 'circuit city collapse', 'JCPenney': 'jcpenney decline',
 'Quibi': 'quibi failure', 'Peloton': 'peloton collapse', '23andMe': '23andme bankruptcy', 'Spirit Airlines': 'spirit airlines bankruptcy',
 'Myspace': 'what happened to myspace', 'Yahoo': 'yahoo downfall',
 # pilar 2: fraudes famosas
 'Enron': 'enron scandal', 'Theranos': 'theranos fraud', 'Madoff': 'bernie madoff ponzi', 'Wirecard': 'wirecard scandal', 'Luckin Coffee': 'luckin coffee fraud',
 'Nikola': 'nikola fraud trevor milton', 'WorldCom': 'worldcom fraud', 'Fyre Festival': 'fyre festival scam', 'Purdue Pharma': 'purdue pharma oxycontin',
 'Archegos': 'archegos collapse', 'Greensill': 'greensill capital collapse', 'Adani': 'adani hindenburg',
 # pilar 3: colapsos de mercado e bancos
 'LTCM': 'long term capital management collapse', 'Bear Stearns': 'bear stearns collapse', 'Black Monday 1987': 'black monday 1987 crash',
 'Terra Luna': 'terra luna collapse', 'Evergrande': 'evergrande collapse', 'Credit Suisse': 'credit suisse collapse', 'Barings': 'barings bank nick leeson',
 'Dot-com': 'dot com bubble crash', 'GameStop': 'gamestop short squeeze', 'Celsius': 'celsius network collapse', 'Mt. Gox': 'mt gox collapse',
 'Silvergate': 'silvergate bank collapse', 'Tulip mania': 'tulip mania bubble', 'Boeing': 'boeing downfall', 'Intel': 'intel downfall',
}
after = '2024-11-05T00:00:00Z'; used = 0; rows = []
now = datetime.now(timezone.utc)
for name, q in TOPICS.items():
    r = requests.get(API + 'search', params=dict(part='id', q=q, type='video', order='viewCount', publishedAfter=after,
                                                  relevanceLanguage='en', videoDuration='medium', maxResults=10, key=KEY)).json(); used += 100
    ids = [i['id']['videoId'] for i in r.get('items', [])]
    if not ids: print(name, 'sem resultado', r.get('error', {}).get('message', '')); continue
    v = requests.get(API + 'videos', params=dict(part='snippet,statistics,contentDetails', id=','.join(ids), key=KEY)).json(); used += 1
    vids = v.get('items', [])
    chs = list({x['snippet']['channelId'] for x in vids})
    c = requests.get(API + 'channels', params=dict(part='statistics', id=','.join(chs), key=KEY)).json(); used += 1
    subs = {x['id']: int(x['statistics'].get('subscriberCount', 0) or 0) for x in c.get('items', [])}
    for x in vids:
        d = (now - datetime.fromisoformat(x['snippet']['publishedAt'].replace('Z', '+00:00'))).days or 1
        views = int(x['statistics'].get('viewCount', 0))
        rows.append(dict(topic=name, videoId=x['id'], title=x['snippet']['title'], channel=x['snippet']['channelTitle'],
                         published=x['snippet']['publishedAt'][:10], views=views, views_day=round(views / d),
                         subs=subs.get(x['snippet']['channelId'], 0), ratio=round(views / max(subs.get(x['snippet']['channelId'], 1), 1), 2)))
    time.sleep(0.2)
with open(OUT / 'demanda_temas.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# resumo por tema
summ = []
for name in TOPICS:
    rs = sorted([r for r in rows if r['topic'] == name], key=lambda r: -r['views'])
    if not rs: continue
    summ.append(dict(topic=name, n=len(rs), top_views=rs[0]['views'], top_title=rs[0]['title'][:70], top_channel=rs[0]['channel'], top_subs=rs[0]['subs'],
                     median_views=int(statistics.median([r['views'] for r in rs])), small_hits=sum(1 for r in rs if r['subs'] < 300000 and r['views'] > 200000),
                     best_small=max([r for r in rs if r['subs'] < 300000] or [dict(views=0, title='', channel='', ratio=0)], key=lambda r: r['views'])))
summ.sort(key=lambda s: -s['median_views'])
json.dump(summ, open(OUT / 'demanda_resumo.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for s in summ:
    b = s['best_small']
    print(f"{s['topic'][:18]:18} mediana {s['median_views']:>10,} | topo {s['top_views']:>11,} | pequenos>200k: {s['small_hits']} | melhor pequeno: {b['views']:,} {b.get('channel','')[:20]} ({b.get('ratio',0)}x)")
print('cota usada ~', used)
