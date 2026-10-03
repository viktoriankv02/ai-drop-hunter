"""Import a reviewed research note without claiming it is a raw scrape or Ollama output."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace
from ai_analyzer.grounded import historical_context

def import_note(store, path):
    note=json.loads(Path(path).read_text("utf-8"))
    sources={s["url"] for s in note["sources"]}
    if any(x.get("source_url") not in sources for x in note["facts"]+note["tasks"]):
        raise ValueError("Every fact and task must identify a reviewed source")
    pid,_=store.add_project(note["title"],note["project_url"],"CryptoRank",note["summary"])
    body={"url":note["project_url"],"text":note["summary"],"research_note":note,
          "links":[{"url":s["url"],"label":s["title"]} for s in note["sources"]],
          "truncated":True,"characters_available":len(note["summary"])}
    sid,changed=store.save_snapshot(pid,note["project_url"],body,via="reviewed_research_note")
    if not changed and store.rows("SELECT 1 FROM reports WHERE project_id=? AND snapshot_id=?",(pid,sid)):
        return {"project_id":pid,"changed":False}
    report={"status":"partial","facts":note["facts"],"tasks":note["tasks"],
            "provenance":note["provenance"],"unknowns":note["unknowns"],"errors":[],
            "coverage":{"processed_characters":len(note["summary"]),"retained_characters":len(note["summary"]),
                        "available_characters":len(note["summary"]),"complete":False},
            "historical_comparisons":historical_context(note["summary"])}
    store.save_report(pid,sid,report,"codex-reviewed-research-note")
    with store.db() as c:
        c.execute("UPDATE projects SET summary=? WHERE id=?",(note["summary"],pid))
    return {"project_id":pid,"changed":changed}

if __name__=="__main__":
    print(json.dumps(import_note(Workspace(),sys.argv[1]),ensure_ascii=False))
