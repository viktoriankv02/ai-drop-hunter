"""Read-only audit of every existing CryptoRank card and its saved evidence."""
import json,sys
from pathlib import Path
from collections import Counter,defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace,utcnow
from core.cryptorank_cards import inventory
from discovery.source_quality import inspect_documents,VERSION

def audit(store):
    cards=inventory(store);by_id={c["id"]:c for c in cards}
    resources=defaultdict(list)
    for r in store.rows("SELECT * FROM project_resources"):
        if r["project_id"] in by_id:resources[r["project_id"]].append(r)
    rejected=[];snapshots=0
    for s in store.rows("""SELECT s.* FROM snapshots s JOIN projects p ON p.id=s.project_id
                          WHERE p.source_url LIKE 'https://cryptorank.io/%' ORDER BY s.id"""):
        snapshots+=1
        _,issues=inspect_documents(by_id[s["project_id"]]["title"],json.loads(s["body_json"]),resources[s["project_id"]])
        for issue in issues:rejected.append({"project_id":s["project_id"],"snapshot_id":s["id"],**issue})
    counts=Counter(r["project_id"] for r in rejected)
    for card in cards:
        card["suspect_saved_documents"]=counts[card["id"]]
    return {"audited_at":utcnow(),"quality_version":VERSION,"total":len(cards),
            "public_read":sum(bool(c["public_read_at"]) for c in cards),
            "with_overview":sum(c["has_overview"] for c in cards),
            "with_analysis":sum(c["has_analysis"] for c in cards),
            "snapshots_inspected":snapshots,"suspect_documents":len(rejected),
            "cards_with_suspect_history":len(counts),"cards":cards,"rejected":rejected,
            "scope":"Read-only completeness and source relevance audit; not a fresh review of all websites."}

if __name__=="__main__":
    w=Workspace();w.initialize()
    result=audit(w);path=w.path.parent/"cryptorank-card-audit.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in ("cards","rejected")}))
