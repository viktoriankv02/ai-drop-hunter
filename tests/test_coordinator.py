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

def test_official_document_fallback_keeps_provenance(tmp_path,monkeypatch):
    from pathlib import Path
    from scripts.import_research_note import import_note
    store=Workspace(tmp_path/"workspace.sqlite");store.initialize()
    note=Path(__file__).resolve().parents[1]/"research"/"variational-note.json"
    pid=import_note(store,note)["project_id"]
    visited=[]
    quote="This official statement is specific evidence about points and participation."
    async def read(url,hosts):
        visited.append(url)
        if "cryptorank.io" in url: raise SourceUnavailable("HTTP 403")
        assert hosts=={"docs.variational.io"}
        return "<main><p>"+quote+(" Current program details."*6)+"</p></main>",url
    monkeypatch.setattr(module,"read_html",read)
    body,via=asyncio.run(Coordinator(store).read_project(store.project(pid)))
    assert via=="official_documents_fallback"
    assert body["truncated"] and len(body["documents"])==2
    assert len(visited)==3
    result={"facts":[{"quote":quote}],"tasks":[]}
    Coordinator.attach_provenance(result,body)
    assert result["provenance"]
    assert "source_url" not in result["facts"][0] # ambiguous quote in both documents

def test_unreviewed_import_cannot_authorize_fallback(tmp_path,monkeypatch):
    store=Workspace(tmp_path/"workspace.sqlite");store.initialize()
    pid,_=store.add_project("Test","https://cryptorank.io/ru/drophunting/test-activity1","CryptoRank")
    store.save_snapshot(pid,store.project(pid)["source_url"],{"research_note":{"sources":[{"access":"official_document","url":"https://evil.example"}]}},via="user_paste")
    visited=[]
    async def read(url,hosts):
        visited.append(url)
        raise SourceUnavailable("HTTP 403")
    monkeypatch.setattr(module,"read_html",read)
    with pytest.raises(SourceUnavailable):
        asyncio.run(Coordinator(store).read_project(store.project(pid)))
    assert len(visited)==1

def test_manual_actions_do_not_become_reward_tasks():
    body={"provenance":"partial","documents":[
        {"url":"https://docs.example/manual","text":"Close part or all of the position.","purpose":"platform_manual"},
        {"url":"https://docs.example/points","text":"Check your reward eligibility here.","purpose":"reward_rules"}]}
    result={"facts":[],"tasks":[
        {"title":"Close position","quote":"Close part or all of the position."},
        {"title":"Check eligibility","quote":"Check your reward eligibility here."}]}
    Coordinator.attach_provenance(result,body)
    assert [t["title"] for t in result["tasks"]]==["Check eligibility"]
    assert [t["title"] for t in result["reference_actions"]]==["Close position"]

def test_chunks_preserve_text_and_do_not_split_words():
    from ai_analyzer.grounded import evidence_chunks,validate_analysis
    text=("Paragraph about eligibility and participation. "*200)
    chunks=evidence_chunks(text)
    assert "".join(chunks)==text
    assert all(len(c)<=2500 for c in chunks)
    assert all(not(c[-1].isalnum() and chunks[i+1][0].isalnum()) for i,c in enumerate(chunks[:-1]))
    result=validate_analysis({"facts":[{"title":"Bad fragment","quote":"lable margin required to open the position."}]},"Available margin required to open the position.","https://example.com",[])
    assert not result["facts"]

def test_paused_source_blocks_saved_analysis(tmp_path,monkeypatch):
    s=Workspace(tmp_path/"db.sqlite");s.initialize()
    pid,_=s.add_project("Example","https://airdrops.io/example/","Airdrops.io")
    sid,_=s.save_snapshot(pid,"https://airdrops.io/example/",{"text":"Saved material"})
    source=next(x for x in s.sources() if x["adapter"]=="airdrops")
    s.source_change(source["id"])
    async def forbidden(*args):pytest.fail("Paused source reached model")
    monkeypatch.setattr(module,"analyze",forbidden)
    with pytest.raises(SourceUnavailable):asyncio.run(Coordinator(s).analyze_snapshot(sid))
