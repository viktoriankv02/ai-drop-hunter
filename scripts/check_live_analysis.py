"""Measure the production analyzer on saved evidence; never overwrites a reviewed card."""
import asyncio,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ai_analyzer.grounded import analyze
async def run():
    body=json.loads(Path('data/hertzflow-article-check.json').read_text(encoding='utf-8'));body['project_title']='HertzFlow'
    started=time.monotonic();events=[]
    def observe(event):
        events.append(event);print(json.dumps(event),flush=True)
    try:
        report=await asyncio.wait_for(analyze(body,on_inference=observe),360)
        result={'checked_on':'2026-10-09','status':'completed','seconds':round(time.monotonic()-started,2),'report':report,'events':events}
    except Exception as error:
        result={'checked_on':'2026-10-09','status':'failed','seconds':round(time.monotonic()-started,2),'error':type(error).__name__+': '+str(error),'events':events}
    Path('data/hertzflow-compact-analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('report','events')}),flush=True)
asyncio.run(run())
