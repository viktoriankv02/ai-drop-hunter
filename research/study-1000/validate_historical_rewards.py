"""Validate provenance, unique counts, quoting and report statistics independently."""
import json,csv,hashlib,re
from pathlib import Path
from decimal import Decimal
from collections import Counter
ROOT=Path(__file__).resolve().parent

def run():
 data=json.loads((ROOT/'historical-rewards.json').read_text(encoding='utf-8'));cases=data['projects'];coverage=json.loads((ROOT/'coverage.json').read_text(encoding='utf-8'))
 names=[c['project'].casefold() for c in cases]
 assert len(names)==len(set(names))
 expected=28+sum(len(json.loads(p.read_text(encoding='utf-8-sig'))) for p in ROOT.glob('expansion-curated-*.json'))
 assert coverage['historical_project_dossiers']==len(cases)==expected
 assert data['window']['date_applies_to']=='reward_distribution_event'
 assert coverage['study_1000_completed'] is False
 assert not any(c['fine_tuning_eligible'] for c in cases)
 assert all(c['unknowns'] and c['sources'] for c in cases)
 assert all(s['url'].startswith('https://') for c in cases for s in c['sources'])
 assert not {'hertzflow','integra','overlayer','note systems'} & set(names)
 assert {'somnia','arbitrum','monad','plasma','juno','osmosis','avail','saga'}<=set(names)
 assert 'polygon' not in names and 'cosmos' not in names
 assert next(c for c in cases if c['project']=='Sui')['payout_evidence_level']=='sale_not_reward'
 csvrows=list(csv.DictReader((ROOT/'historical-rewards.csv').open(encoding='utf-8-sig')))
 assert [c['project'] for c in csvrows]==[c['project'] for c in cases]
 audit=json.loads((ROOT/'reward-source-audit.json').read_text(encoding='utf-8'))
 checked=0
 for s in audit:
  if s.get('content_file'):
   body=(ROOT/s['content_file']).read_bytes();assert hashlib.sha256(body).hexdigest()==s['content_sha256'];checked+=1
 for src in json.loads((ROOT/'expansion-source-audit.json').read_text(encoding='utf-8')):
  if src.get('status')=='fetched':
   evidence=json.loads((ROOT/src['content_file']).read_text(encoding='utf-8'))
   assert hashlib.sha256(evidence['text'].encode()).hexdigest()==src['content_sha256'];checked+=1
 assert (ROOT/'REPORT.html').read_text(encoding='utf-8').count('<article ')==len(cases)
 examples=[json.loads(x) for x in (ROOT/'historical-extraction-examples.jsonl').read_text(encoding='utf-8').splitlines() if x]
 for e in examples:
  body=(ROOT/e['content_file']).read_bytes();assert hashlib.sha256(body).hexdigest()==e['content_sha256'];source=json.loads(body)
  assert ' '.join(e['quote'].split()) in ' '.join(source['text'].split())
  assert len(e['quote'].split())<=25
 extra=[json.loads(x) for x in (ROOT/'expansion-extraction-examples.jsonl').read_text(encoding='utf-8').splitlines() if x]
 transfer_examples=[json.loads(x) for x in (ROOT/'agent-transfer-examples.jsonl').read_text(encoding='utf-8').splitlines() if x]
 assert coverage['total_source_checked_extraction_examples']==len(examples)+12+len(extra)+len(transfer_examples)
 for e in extra+transfer_examples:
  doc=json.loads((ROOT/e['content_file']).read_text(encoding='utf-8'))
  assert hashlib.sha256(doc['text'].encode()).hexdigest()==e['content_sha256']
  assert e['quote'] in ' '.join(doc['text'].split()) and len(e['quote'].split())<=25
  assert not e['fine_tuning_ready']
 monad=list(csv.DictReader((ROOT/'monad-airdrop-results.csv').open()))
 amounts=sorted(Decimal(x['amount']) for x in monad)
 assert len(monad)==len({r['claim_address'].casefold() for r in monad})==76021
 assert all(re.fullmatch(r'0x[0-9a-fA-F]{40}',r['claim_address']) for r in monad)
 assert sum(amounts)==3330583396 and amounts[len(amounts)//2]==12000
 expected=json.loads((ROOT/'monad-csv-provenance.json').read_text())
 assert hashlib.sha256((ROOT/'monad-airdrop-results.csv').read_bytes()).hexdigest()==expected['sha256']
 models=json.loads((ROOT/'claim-model-candidates.json').read_text())
 assert len(models)==44 and all(not x['query_executed'] and not x['payout_verified'] for x in models)
 for m in models:assert hashlib.sha256((ROOT/m['local_model']).read_bytes()).hexdigest()==m['sha256']
 ev=json.loads((ROOT/'historical-extraction-result.json').read_text(encoding='utf-8'));assert ev['total']==len(ev['results'])==7
 assert ev['passed']==sum(x['passed'] for x in ev['results'])==5
 assert all('error' not in x for x in ev['results'])
 output={'status':'passed','unique_dossiers':len(cases),'source_files_hash_checked':checked,'new_quotes_checked':len(examples),'expansion_quotes_checked':len(extra),'claim_models_hash_checked':len(models),'monad_rows_recomputed':len(monad),'model_smoke':'5/7; failures retained','study_1000_completed':False,'fine_tuning_performed':False}
 (ROOT/'historical-validation.json').write_text(json.dumps(output,indent=2),encoding='utf-8');print(json.dumps(output))
if __name__=='__main__':
 run()
 import runpy
 runpy.run_path(str(ROOT/'capture_research_experience.py'),run_name='__main__')
