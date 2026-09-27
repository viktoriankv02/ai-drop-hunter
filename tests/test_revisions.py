from core.revisions import compare_materials
from core.workspace import Workspace


def test_revision_separates_text_and_link_changes():
    old = {"text": "A stable instruction.\nOld deadline: Monday.", "links": [{"url":"https://example.com/old"}]}
    new = {"text": "A   stable instruction.\nNew deadline: Friday.", "links": [{"url":"https://example.com/new"}]}
    change = compare_materials(old,new)
    assert change["added"] == ["New deadline: Friday."]
    assert change["removed"] == ["Old deadline: Monday."]
    assert change["added_links"] == ["https://example.com/new"]
    assert change["removed_links"] == ["https://example.com/old"]
    assert not change["truncated"]


def test_new_snapshot_preserves_completion_and_marks_old_evidence(tmp_path):
    store=Workspace(tmp_path/"workspace.sqlite");store.initialize()
    pid,_=store.add_project("Test","https://airdrops.io/test/","Airdrops.io")
    text="Complete the original official task."
    sid,_=store.save_snapshot(pid,"https://airdrops.io/test/",{"text":text})
    store.save_report(pid,sid,{"tasks":[{"title":"Original task","url":"https://airdrops.io/test/","quote":text}]},"fixture")
    tid=store.detail(pid)["tasks"][0]["id"]
    store.complete_task(tid,True)
    latest,_=store.save_snapshot(pid,"https://airdrops.io/test/",{"text":text+"\nA new task was published."})
    detail=store.detail(pid)
    assert detail["tasks"][0]["status"]=="user_reported"
    assert detail["tasks"][0]["evidence_state"]=="source_changed"
    assert detail["source_changes"]["current_id"]==latest
    assert detail["source_changes"]["added"]==["A new task was published."]
    store.save_report(pid,latest,{"tasks":[{"title":"Original task","url":"https://airdrops.io/test/","quote":text}]},"fixture")
    assert store.detail(pid)["tasks"][0]["evidence_state"]=="current"


def test_revision_bounds_large_changes_and_discloses_partial_source():
    change=compare_materials({"text":"old"}, {"text":"\n".join(str(i) for i in range(100)), "truncated":True})
    assert len(change["added"])==12
    assert change["truncated"] and change["source_incomplete"]
