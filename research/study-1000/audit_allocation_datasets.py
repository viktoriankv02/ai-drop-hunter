"""Recompute published allocation lists; no claim execution is inferred."""
import csv,json,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parent;D=R/'allocation-datasets'
provenance=json.loads((D/'provenance.json').read_text())
results=[]
for name,filename,col in [('ParaSwap','paraswap-users.json','earnings'),('Hop Protocol','hop-finalDistribution.csv','totalTokens')]:
 raw=(D/filename).read_bytes();src=next(x for x in provenance if Path(x.get('file','')).name==filename)
 assert hashlib.sha256(raw).hexdigest()==src['sha256']
 rows=json.loads(raw) if filename.endswith('.json') else list(csv.DictReader(raw.decode().splitlines()))
 assert all(re.fullmatch('0x[0-9a-fA-F]{40}',x['address']) for x in rows)
 amounts=[int(x[col]) for x in rows];addresses=[x['address'].lower() for x in rows]
 assert all(v>=0 for v in amounts)
 results.append(dict(project=name,source_file=str((D/filename).relative_to(R)),sha256=src['sha256'],rows=len(rows),unique_addresses=len(set(addresses)),duplicate_address_rows=len(rows)-len(set(addresses)),positive_allocations=sum(v>0 for v in amounts),zero_allocations=sum(v==0 for v in amounts),amount_column=col,total_base_units=str(sum(amounts)),token_decimals_verified=False,token_total=None,payout_verified=False,meaning='published allocation list, not executed claims'))
(D/'arithmetic-audit.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({'status':'passed','allocations':[{k:r[k] for k in ['project','rows','unique_addresses','zero_allocations','payout_verified']} for r in results]}))
