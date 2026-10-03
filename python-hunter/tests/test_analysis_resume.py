import asyncio,json
from core.workspace import Workspace
from ai_analyzer import grounded
def test_resume_cache_and_feedback_invalidation(tmp_path,monkeypatch):
    store=Workspace(tmp_path/"workspace.sqlite");store.initialize()
    calls=[]
    text="Read the official guide and verify campaign eligibility."
    async def fake_complete(prompt,system_prompt):
        calls.append(prompt)
        return json.dumps({"facts":[{"title":"Read guide","quote":text}],"tasks":[]})
    monkeypatch.setattr(grounded,"complete",fake_complete)
    body={"text":text,"url":"https://example.com/","links":[]}
    first=asyncio.run(grounded.analyze(body,cache_get=store.cached_analysis,cache_put=store.cache_analysis))
    second=asyncio.run(grounded.analyze(body,cache_get=store.cached_analysis,cache_put=store.cache_analysis))
    assert len(calls)==1 and first["facts"]==second["facts"]
    asyncio.run(grounded.analyze(body,corrections=["New correction"],cache_get=store.cached_analysis,cache_put=store.cache_analysis))
    assert len(calls)==2

def test_model_failure_is_not_a_positive_rating(monkeypatch):
    async def failing(*args): raise RuntimeError("offline")
    monkeypatch.setattr(grounded,"complete",failing)
    import pytest
    with pytest.raises(RuntimeError,match="offline"):
        asyncio.run(grounded.analyze({"text":"Not enough access to verify a reward.","url":"https://example.com","links":[]}))

def test_historical_context_is_marked_as_analogy():
    result=grounded.historical_context("Read the bridge and transaction instructions.")
    assert result
    assert all(x["status"]=="historical_analogy_not_current_requirement" for x in result)
