"""Rebuild presentation of saved public captures, without rereading remote pages."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace
from core.cryptorank_cards import public_guide
w=Workspace();w.initialize();changed=0
for row in w.rows("SELECT g.*,s.body_json snapshot FROM project_public_guides g JOIN snapshots s ON s.id=g.snapshot_id"):
    old=json.loads(row["body_json"]);body=json.loads(row["snapshot"]);text=body["text"];sections=[]
    for i,c in enumerate(old["campaigns"]):
        start=text.find(c["title"])
        if start<0:continue
        next_title=old["campaigns"][i+1]["title"] if i+1<len(old["campaigns"]) else None
        end=text.find(next_title,start+len(c["title"])) if next_title else len(text)
        content=text[start:end if end>=0 else len(text)].split("Войдите, чтобы увидеть все данные")[0].strip()
        sections.append({"title":c["title"],"text":content,"links":c["links"]})
    new=public_guide(text,sections,old["source_url"],old["access"]=="partial_login")
    with w.db() as db:db.execute("UPDATE project_public_guides SET body_json=? WHERE project_id=?",(json.dumps(new,ensure_ascii=False),row["project_id"]))
    changed+=1
print(json.dumps({"guides_refreshed":changed}))
