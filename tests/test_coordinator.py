import asyncio,json
import pytest
from core.workspace import Workspace
from discovery.coordinator import Coordinator
from discovery.evidence import SourceUnavailable
import discovery.coordinator as module

def test_failed_catalog_records_attempt_for_daily_backoff(tmp_path,monkeypatch):
    store=Workspace(tmp_path/"workspace.sqlite");store.initialize()
    async def unavailable(*args): raise SourceUnavailable("HTTP 403")
    monkeypatch.setattr(module,"read_html",unavailable)
    with pytest.raises(SourceUnavailable): asyncio.run(Coordinator(store).discover(1))
    source=store.sources()[0]
    assert source["last_check"] and source["last_status"]=="failed"

def test_channel_permission_does_not_authorize_other_telegram_channels(tmp_path,monkeypatch):
    store=Workspace(tmp_path/"workspace.sqlite");store.initialize()
    store.add_source("Approved","@approvedchannel","telegram")
    pid,_=store.add_project("Unapproved","https://t.me/unapproved/123","legacy")
    async def forbidden(*args):
        pytest.fail("Unapproved channel reached network")
    monkeypatch.setattr(module,"read_html",forbidden)
    with pytest.raises(SourceUnavailable):
        asyncio.run(Coordinator(store).research(pid))
    from core.source_policy import source_allows_url
    source=next(s for s in store.sources() if s["kind"]=="telegram")
    assert source_allows_url(source,"https://t.me/ApprovedChannel/123")
    assert source_allows_url(source,"https://t.me/s/approvedchannel/123")
    assert not source_allows_url(source,"https://t.me/approvedchannel_other/123")
    assert not source_allows_url(source,"https://t.me/approvedchannel/nonnumeric")
    assert not source_allows_url({**source,"enabled":0},"https://t.me/approvedchannel/123")


def test_imported_snapshot_uses_progress_and_cache(tmp_path,monkeypatch):
    store=Workspace(tmp_path/"workspace.sqlite");store.initialize()
    pid,_=store.add_project("Example","https://cryptorank.io/ru/drophunting/example-activity1","CryptoRank")
    sid,_=store.save_snapshot(pid,"https://cryptorank.io/ru/drophunting/example-activity1",{"text":"source","url":"https://example.com","links":[]})
    job=store.enqueue("analyze",sid)
    coordinator=Coordinator(store);coordinator.current_job=job
    async def fake_analyze(body,corrections,on_progress,cache_get,cache_put):
        on_progress(1,2)
        cache_put("fixture",{"facts":[],"tasks":[]})
        assert cache_get("fixture")=={"facts":[],"tasks":[]}
        return {"status":"draft","tasks":[],"coverage":{"complete":True}}
    monkeypatch.setattr(module,"analyze",fake_analyze)
    asyncio.run(coordinator.analyze_snapshot(sid))
    assert "1/2" in store.rows("SELECT phase FROM jobs WHERE id=?",(job,))[0]["phase"]
    assert len(store.rows("SELECT id FROM reports"))==1
