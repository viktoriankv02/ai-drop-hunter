from pathlib import Path
from core.workspace import Workspace
from scripts.import_research_note import import_note

def test_note_is_explicit_and_repeat_does_not_reset_completion(tmp_path):
    store=Workspace(tmp_path/"workspace.sqlite")
    store.initialize()
    path=Path(__file__).resolve().parents[1]/"research"/"variational-note.json"
    result=import_note(store,path)
    detail=store.detail(result["project_id"])
    assert detail["snapshots"][0]["via"]=="reviewed_research_note"
    assert detail["report"]["body"]["coverage"]["complete"] is False
    assert len(detail["tasks"])==2
    store.complete_task(detail["tasks"][0]["id"],True)
    assert import_note(store,path)["changed"] is False
    assert store.detail(result["project_id"])["tasks"][0]["status"]=="user_reported"
