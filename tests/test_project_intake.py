from core.workspace import Workspace
from discovery.coordinator import Coordinator


def test_every_new_project_is_prepared_without_joining_work(tmp_path):
    store=Workspace(tmp_path/'db.sqlite');store.initialize()
    pid,fresh=store.add_project('New protocol','https://example.com/campaign','Manual')
    assert fresh and store.project(pid)['status']=='new'
    assert store.preparation(pid)['state']=='queued'
    assert Coordinator(store).project_research_allowed(store.project(pid))
    again,fresh=store.add_project('New protocol','https://example.com/campaign','Manual')
    assert again==pid and not fresh
    assert len(store.rows("SELECT * FROM jobs WHERE kind='research' AND target_id=?",(pid,)))==1


def test_rejection_stops_waiting_research_and_can_be_reversed(tmp_path):
    store=Workspace(tmp_path/'db.sqlite');store.initialize()
    pid,_=store.add_project('New protocol','https://example.com/campaign','Manual')
    store.set_status(pid,'ignored')
    assert store.prepare_project(pid) is None
    assert store.rows("SELECT state FROM jobs WHERE target_id=?",(pid,))[0]['state']=='cancelled'
    store.set_status(pid,'new')
    assert store.preparation(pid)['state']=='queued'
    assert store.project(pid)['status']=='new'


def test_backfill_is_bounded_and_preserves_existing_decisions(tmp_path):
    store=Workspace(tmp_path/'db.sqlite');store.initialize()
    with store.db() as c:c.execute("UPDATE meta SET value='0' WHERE key='automatic_card_preparation'")
    ids=[store.add_project('Protocol '+str(i),'https://example.com/p'+str(i),'Manual')[0] for i in range(4)]
    store.set_status(ids[0],'ignored');store.set_status(ids[1],'tracking')
    assert len(store.pending_preparation(1))==1
    assert {p['id'] for p in store.pending_preparation()}==set(ids[2:])
    with store.db() as c:c.execute("UPDATE meta SET value='1' WHERE key='automatic_card_preparation'")
    for p in store.pending_preparation():store.prepare_project(p['id'])
    assert store.pending_preparation()==[]
    assert store.project(ids[0])['status']=='ignored'
    assert store.project(ids[1])['status']=='tracking'


def test_intake_does_not_authorize_telegram(tmp_path):
    store=Workspace(tmp_path/'db.sqlite');store.initialize()
    pid,_=store.add_project('Channel post','https://t.me/unapproved/123','Manual')
    assert store.preparation(pid)['state']=='waiting'
    assert not Coordinator(store).project_research_allowed(store.project(pid))
