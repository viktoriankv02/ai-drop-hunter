"""Fetch source documents for curated expansion; errors stay explicit."""
import json,urllib.request,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from collect_historical_archive import Page
ROOT=Path(__file__).resolve().parent
DEST=ROOT/'expansion-evidence';DEST.mkdir(exist_ok=True)
def fetch(url):
 key=hashlib.sha256(url.encode()).hexdigest()[:18];f=DEST/(key+'.json')
 if f.exists():
  d=json.loads(f.read_text(encoding='utf-8'))
  if d.get('status')=='fetched':return d
 d={'url':url,'retrieved_at':datetime.now(timezone.utc).isoformat(),'content_file':str(f.relative_to(ROOT)),'status':'unavailable'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HistoricalRewardsResearch/1.0'}),timeout=25) as r:
   raw=r.read(4000000);d.update(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type',''))
  if raw.startswith(b'%PDF'):
   pdf=DEST/(key+'.pdf');pdf.write_bytes(raw);d.update(status='binary_saved_not_text_verified',binary_file=str(pdf.relative_to(ROOT)),binary_sha256=hashlib.sha256(raw).hexdigest())
  else:
   t=raw.decode('utf-8',errors='replace');p=Page();p.feed(t);t='\n'.join(p.text) if '<html' in t[:1000].lower() or '<!doctype' in t[:100].lower() else t
   d.update(text=t,characters=len(t),content_sha256=hashlib.sha256(t.encode()).hexdigest(),status='fetched' if len(t)>300 and 'Page Not Found' not in t[:150] else 'insufficient_text')
 except Exception as e:d['error']=str(e)
 f.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');return d
def main():
 rows=[]
 for f in sorted(ROOT.glob('expansion-curated-*.json')):rows.extend(json.loads(f.read_text(encoding='utf-8-sig')))
 urls=sorted({s['url'] for x in rows for s in x['sources']});audit=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  for fu in as_completed([pool.submit(fetch,u) for u in urls]):audit.append({k:v for k,v in fu.result().items() if k!='text'})
 audit.sort(key=lambda x:x['url'])
 (ROOT/'expansion-source-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'sources':len(audit),'fetched':sum(x['status']=='fetched' for x in audit),'unavailable':[x['url'] for x in audit if x['status']!='fetched']}),flush=True)
if __name__=='__main__':
 main()
 import runpy
 runpy.run_path(str(ROOT/'capture_research_experience.py'),run_name='__main__')
