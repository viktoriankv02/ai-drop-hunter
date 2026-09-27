import asyncio,pytest
from discovery.cryptorank_api import parse_map
from discovery.evidence import SourceUnavailable
from core.workspace import Workspace
from discovery.coordinator import Coordinator
import discovery.coordinator as module


def test_map_uses_actual_slug_not_numeric_id():
    result=parse_map({"data":[{"id":1,"slug":"layerzero-activity0","name":"LayerZero"},
        {"id":999,"slug":"layerzero-activity0","name":"LayerZero"},
        {"id":2,"slug":"../../public-api/dashboard","name":"Invalid"}]})
    assert len(result)==1
    assert result[0]["url"].endswith("/layerzero-activity0")
    assert "не перевірені" in result[0]["text"]


def test_map_rejects_invalid_or_empty_data():
    for payload in ({},{"data":{}},{"data":[]}):
        with pytest.raises(SourceUnavailable):parse_map(payload)


def test_api_catalog_is_not_truncated_to_200_and_preserves_user_choice(tmp_path,monkeypatch):
    store=Workspace(tmp_path/"workspace.sqlite");store.initialize()
    monkeypatch.setenv("CRYPTORANK_API_KEY","test-only")
    async def fixture():
        return [{"title":f"Project {i}","url":f"https://cryptorank.io/ru/drophunting/project-activity{i}",
                 "text":"Unverified API catalogue"} for i in range(240)]
    monkeypatch.setattr(module,"fetch_map",fixture)
    result=asyncio.run(Coordinator(store).discover(1))
    assert result["found"]==240 and result["added"]==240 and not result["limited"]
    assert result["route"]=="official_api_map" and not result["tasks_included"]
    assert not store.rows("SELECT id FROM tasks")
    pid=store.rows("SELECT id FROM projects ORDER BY id LIMIT 1")[0]["id"]
    store.set_status(pid,"tracking")
    result=asyncio.run(Coordinator(store).discover(1))
    assert result["added"]==0 and store.project(pid)["status"]=="tracking"
