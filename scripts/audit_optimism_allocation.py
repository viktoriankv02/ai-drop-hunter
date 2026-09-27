"""Reproduce allocation totals from a local copy of the official CSV, not claims."""
import csv,json,hashlib,argparse
from pathlib import Path
from decimal import Decimal,localcontext

FIELDS=["a_is_voter","b_is_multisig_signer","c_is_gitcoin","d_is_price_out","e_op_user","f_op_repeat","g_overlap_bonus"]
SOURCE="https://raw.githubusercontent.com/ethereum-optimism/op-analytics/main/reference_data/address_lists/op_airdrop1_addresses_detailed_list.csv"

def audit(path,decimals=18):
    if not 0<=decimals<=36: raise ValueError("Invalid decimal scale")
    content=Path(path).read_bytes()
    rows=list(csv.DictReader(content.decode("utf-8").splitlines()))
    if not rows: raise ValueError("Empty allocation")
    addresses=[r["address"].lower() for r in rows]
    if len(set(addresses))!=len(addresses): raise ValueError("Duplicate addresses")
    amounts=[int(r["total_op_eligible_to_claim"]) for r in rows]
    if any(x<0 for x in amounts): raise ValueError("Negative allocation")
    deltas=[a-sum(int(r[k]) for k in FIELDS) for a,r in zip(amounts,rows)]
    with localcontext() as ctx:
        ctx.prec=80
        tokens=str(Decimal(sum(amounts))/Decimal(10**decimals))
    return {"source_url":SOURCE,"sha256":hashlib.sha256(content).hexdigest(),
            "rows":len(rows),"unique_addresses":len(set(addresses)),
            "decimals_applied":decimals,"allocation_sum_raw":str(sum(amounts)),
            "allocation_sum_tokens":tokens,"category_counts":{k:sum(int(r[k])>0 for r in rows) for k in FIELDS},
            "component_difference_rows":sum(d!=0 for d in deltas),
            "maximum_component_difference_raw":str(max(abs(d) for d in deltas)),
            "is_claims_verification":False,
            "note":"Підрахунок алокації у завантаженій версії CSV. Не доказ фактичних виплат. Масштаб одиниць задано параметром decimals; вихідна сума збережена точно."}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("path");p.add_argument("--decimals",type=int,default=18);p.add_argument("--output")
    args=p.parse_args();result=audit(args.path,args.decimals);encoded=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output:Path(args.output).write_text(encoded,encoding="utf-8",newline="\n")
    print(encoded)
