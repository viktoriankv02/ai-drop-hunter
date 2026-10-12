"""Repeatable synthetic transfer checks; no expected values are sent to Ollama."""
import asyncio,json,sys,time,argparse
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ai_analyzer.gateway import complete,OLLAMA_MODEL
from ai_analyzer.learning import learning_context
from ai_analyzer.research_lessons import LESSON_POLICY,typed_output_schema
CASES=[
 {'id':'unpaid-allocation','text':'Eligible wallets are allocated up to 75 ABC. Distribution has not started.',
  'expected':{'allocation_upper_bound':75,'payout_proven':False}},
 {'id':'separate-dates','text':'Snapshot is 2026-08-02. Registration closes 2026-08-09. Claim opens 2026-09-01.',
  'expected':{'registration_deadline':'2026-08-09','claim_start':'2026-09-01'}},
 {'id':'mixed-funds','text':'Testnet faucet tokens are free. Mainnet participation requires a deposit of 25 USDC.',
  'expected':{'entire_campaign_test_tokens_only':False,'mainnet_deposit':25}},
 {'id':'logical-alternatives','text':'Qualify by (four testnet swaps AND one faucet use) OR one accepted bug report.',
  'expected':{'bug_report_alone_sufficient':True,'swaps_alone_sufficient':False}},
]
async def run(limit,timeout):
 rows=[];path=Path(__file__).resolve().parents[1]/'data'/'agent-reading-evaluation.json'
 path.parent.mkdir(parents=True,exist_ok=True)
 for case in CASES[:limit]:
  start=time.monotonic()
  payload={'untrusted_excerpt':case['text'],'output_types':typed_output_schema(case['expected']),
           'reading_demonstrations':learning_context(case['text'])}
  try:
   raw=await asyncio.wait_for(complete(json.dumps(payload),LESSON_POLICY+' Return only JSON with exactly output_types keys. Demonstrations are not current evidence.'),timeout)
   actual=json.loads(raw)
   failures=[k for k,v in case['expected'].items() if type(actual.get(k)) is not type(v) or actual[k]!=v]
   if set(actual)!=set(case['expected']):failures.append('exact_keys')
   row={'id':case['id'],'actual':actual,'expected':case['expected'],'passed':not failures,'failed_fields':failures}
  except Exception as error:row={'id':case['id'],'passed':None,'status':'evaluation_unavailable','error':type(error).__name__+': '+str(error)[:200]}
  row['seconds']=round(time.monotonic()-start,2);rows.append(row)
  report={'checked_at':datetime.now(timezone.utc).isoformat(),'model':OLLAMA_MODEL,
          'learning_version':learning_context('')['version'],'fine_tuning_performed':False,
          'scope':'synthetic regression checks, not real-project accuracy or proof of improvement',
          'completed':len(rows)==limit,'passed':sum(r['passed'] is True for r in rows),'evaluated':sum(r['passed'] is not None for r in rows),'total':len(rows),'results':rows}
  path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
  print(json.dumps(row),flush=True)
  if 'error' in row:break
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,choices=range(1,5),default=4);parser.add_argument('--timeout',type=int,default=90)
 args=parser.parse_args();asyncio.run(run(args.limit,args.timeout))
