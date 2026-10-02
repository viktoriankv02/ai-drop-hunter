import concurrent.futures,hashlib,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup
ROOT=Path('research/study-1000');out=ROOT/'reward-evidence';out.mkdir(exist_ok=True)
raw='''Monad|https://monad.xyz/blog/the-mon-airdrop-results
Monad|https://monad.xyz/blog/mon-tokenomics-overview
Monad|https://docs.monad.xyz/
Monad|https://dune.com/blog/dune-digest-037
Arkham|https://info.arkm.com/announcements/arkham-exchange-updates-2
Arkham|https://t.me/s/arkhamintelligence?before=89
Plasma|https://www.plasma.org/company/blog/plasma-mainnet-beta-and-xpl
Plasma|https://www.binance.com/en/support/announcement/detail/b00f28d55c924614b1953484c64dd6f9
Plasma|https://www.yieldnetwork.io/blog/plasma-predeposit
Somnia|https://blog.somnia.network/p/say-hi-to-somi
Somnia|https://blog.somnia.network/p/the-somnia-odyssey-a-60-day-adventure
Somnia|https://www.improbable.io/news/improbable-developed-somnia-launches-mainnet-after-record-breaking-testnet-performance
Osmosis|https://osmosis.gitbook.io/o/osmo/genesis-supply
Osmosis|https://osmosis.gitbook.io/o/osmo/airdrop-claim
Osmosis|https://osmosis.gitbook.io/o/osmo/token-distribution
Juno|https://docs.junonetwork.io/
Stride|https://stride.zone/blog/stride-airdrop-details
Stride|https://stride.zone/blog/airdrop-to-sttia-holders
Neutron|https://docs.neutron.org/concepts/tokenomics
Neutron|https://forum.cosmos.network/t/proposal-792-accepted-launch-neutron-on-replicated-security/10230/90
Stargaze|https://paragraph.com/@stargazezone/stars-token-distribution-and-airdrop
Stargaze|https://stargaze.valopers.com/proposals/4
Avail|https://blog.availproject.org/avails-unification-drop/
Avail|https://blog.availproject.org/avail-2024-wrapped/
Saga|https://medium.com/sagaxyz/saga-community-genesis-airdrop-e0f94c1f2220
Polygon|https://staking.polygon.technology/community-drops
Dymension|https://medium.com/@dymension/genesis-rolldrop-the-first-rolldrop-season-219c8b5ea16e
Dymension|https://github.com/dymensionxyz/rolldrop-genesis
Stellar|https://stellar.org/blog/foundation-news/keybase-stellar-lumens-spacedrop
Stellar|https://keybase.io/airdrop
Optimism|https://raw.githubusercontent.com/ethereum-optimism/community-hub/main/pages/op-token/airdrops/airdrop-1.mdx
Arbitrum|https://docs.arbitrum.foundation/airdrop-eligibility-distribution'''
def fetch(line):
 project,url=line.split('|',1);key=hashlib.sha256(url.encode()).hexdigest()[:16];record={'project':project,'url':url,'retrieved_at':datetime.now(timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'HistoricalRewardsResearch/1.0'})
  res=urllib.request.urlopen(req,timeout=25);body=res.read(3000000);soup=BeautifulSoup(body,'html.parser')
  for el in soup.select('script,style,nav,footer,header'):el.decompose()
  main=soup.select_one('article') or soup.select_one('main') or soup
  text=main.get_text('\n',strip=True) if not url.endswith('.mdx') else body.decode()
  links=[{'text':a.get_text(' ',strip=True)[:100],'url':a['href']} for a in main.select('a[href]') if a['href'].startswith('https://')]
  data={'url':url,'resolved_url':res.url,'text':text,'links':links,'retrieved_at':record['retrieved_at']}
  file=out/(key+'.json');file.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
  record.update(status='fetched',resolved_url=res.url,content_file=str(file.relative_to(ROOT)),characters=len(text),raw_sha256=hashlib.sha256(body).hexdigest(),content_sha256=hashlib.sha256(file.read_bytes()).hexdigest())
 except Exception as e:record.update(status='unavailable',error=str(e)[:180])
 return record
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,raw.splitlines()))
(ROOT/'reward-source-audit.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for r in records:print(json.dumps({k:v for k,v in r.items() if k in ('project','status','characters','error')},ensure_ascii=True))
