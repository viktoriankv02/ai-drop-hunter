"""Collect historical archive discovery records. They are NOT verified project dossiers."""
import json,urllib.request,urllib.parse,hashlib,re,time
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
DEST=ROOT/'archive-evidence';DEST.mkdir(exist_ok=True)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.text=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
  if tag=='a':
   d=dict(attrs)
   if d.get('href'):self.links.append(d['href'])
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,t):
  if not self.skip and t.strip():self.text.append(t.strip())
def fetch(url):
 slug=url.rstrip('/').split('/')[-1]; f=DEST/(slug+'.json')
 if f.exists():
  old=json.loads(f.read_text(encoding='utf-8'))
  if old.get('http_status')==200:return old
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'HistoricalRewardsResearch/1.0'})
  with urllib.request.urlopen(req,timeout=20) as r:raw=r.read(1500000);status=r.status;final=r.url
  p=Page();p.feed(raw.decode('utf-8',errors='replace'));text='\n'.join(p.text)
  links=sorted(set(urllib.parse.urljoin(final,x) for x in p.links if x.startswith(('http','/'))))
  item={'slug':slug,'source_url':url,'final_url':final,'http_status':status,'retrieved_at':datetime.now(timezone.utc).isoformat(),'source_kind':'secondary_directory','verification_status':'discovery_only','fine_tuning_eligible':False,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'external_links':[x for x in links if urllib.parse.urlparse(x).netloc!=urllib.parse.urlparse(final).netloc]}
 except Exception as e:item={'slug':slug,'source_url':url,'http_status':None,'error':str(e),'verification_status':'unavailable','fine_tuning_eligible':False}
 f.write_text(json.dumps(item,ensure_ascii=False,indent=2),encoding='utf-8');return item
def main():
 urls=list(json.loads((ROOT/'historical-archive-discovery.json').read_text(encoding='utf-8-sig'))['links']);items=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  for future in as_completed([pool.submit(fetch,u) for u in urls]):
   x=future.result();items.append({k:v for k,v in x.items() if k!='text'})
   if len(items)%50==0:print(json.dumps({'fetched':len(items),'total':len(urls)}),flush=True)
 items.sort(key=lambda x:x['slug'])
 out={'as_of':datetime.now(timezone.utc).isoformat(),'status':'unverified_discovery_not_training_data','warning':'Directory dates may refer to announcements or snapshots. Duplicates, sales, failed projects and out-of-window events still require exclusion.','count':len(items),'successful_fetches':sum(x.get('http_status')==200 for x in items),'projects':items}
 (ROOT/'historical-discovery-queue.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in out.items() if k!='projects'}),flush=True)
if __name__=='__main__':main()

