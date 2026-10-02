"""Read only explicitly registered official research sources; preserve errors and content hashes."""
import asyncio,hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from discovery.evidence import read_html,material
ROOT=Path(__file__).resolve().parent
async def run():
 cases=json.loads((ROOT.parent/'historical-cases.json').read_text(encoding='utf-8'))['cases']
 registered={}
 for case in cases:
  for source in case['sources']:
   url=source['url']
   if url.endswith(('.pdf','.csv','.mdx')):continue
   registered.setdefault(url,[]).append(case['project'])
 sem=asyncio.Semaphore(3)
 async def fetch(url,projects):
  key=hashlib.sha256(url.encode()).hexdigest()[:16]
  record={'requested_url':url,'projects':projects,'retrieved_at':datetime.now(timezone.utc).isoformat()}
  async with sem:
   try:
    html,resolved=await read_html(url,{urlsplit(url).hostname})
    body=material(html,resolved)
    record.update(status='fetched',resolved_url=resolved,sha256=hashlib.sha256(html.encode()).hexdigest(),characters=body['characters_available'],truncated=body['truncated'],content_file=f'evidence/{key}.json')
    (ROOT/record['content_file']).write_text(json.dumps(body,ensure_ascii=False,indent=2),encoding='utf-8')
   except Exception as e:record.update(status='unavailable',error=f'{type(e).__name__}: {str(e)[:200]}')
   print(json.dumps({k:v for k,v in record.items() if k in ('projects','status','characters','error')},ensure_ascii=True),flush=True)
  return record
 records=await asyncio.gather(*(fetch(u,p) for u,p in registered.items()))
 previous=json.loads((ROOT/'source-audit.json').read_text(encoding='utf-8')) if (ROOT/'source-audit.json').exists() else []
 refreshed={r['requested_url'] for r in records}
 records=[r for r in previous if r['requested_url'] not in refreshed]+records
 (ROOT/'source-audit.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'attempted':len(records),'fetched':sum(r['status']=='fetched' for r in records)}))
if __name__=='__main__':asyncio.run(run())
