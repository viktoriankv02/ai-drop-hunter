import asyncio
import pytest
from core.workspace import Workspace
from core.cryptorank_cards import import_capture,inventory,public_guide
from discovery.source_quality import clean_material
from discovery.public_search import search_relevance
from discovery.evidence import SourceUnavailable

URL="https://cryptorank.io/ru/drophunting/example-activity1"
TEXT="Example Testnet\n1. Отримайте тестові токени у faucet для тестової мережі.\n2. Перевірте баланс тестового гаманця та умови кампанії.\nВойдите, чтобы увидеть все данные"
def capture():
    return {"source":URL,"text":TEXT,"sections":[{"title":"Example Testnet","text":TEXT.split("\nВойдите")[0],"links":[{"url":"https://example.com/faucet","label":"Faucet"}]}]}

def test_import_is_separate_idempotent_and_preserves_progress(tmp_path):
    w=Workspace(tmp_path/"w.sqlite");w.initialize()
    pid,_=w.add_project("Example",URL,"CryptoRank",prepare=False)
    w.set_status(pid,"tracking")
    first=import_capture(w,capture());second=import_capture(w,capture())
    assert first["snapshot_id"]==second["snapshot_id"] and not second["changed"]
    assert second["steps"]==2 and second["access"]=="partial_login"
    assert w.project(pid)["status"]=="tracking"
    assert not w.rows("SELECT * FROM reports")
    assert inventory(w)[0]["public_read_at"]
    detail=w.detail(pid)
    assert not detail["public_guide"]["complete"]
    assert detail["activity_screening"]["decision"]=="needs_review"

def test_hidden_section_not_in_visible_text_is_rejected():
    data=capture();data["sections"].append({"title":"Hidden","text":"Hidden\n1. Deposit real funds into the trading account."})
    assert len(public_guide(data["text"],data["sections"],URL)["campaigns"])==1

def test_challenge_is_not_saved(tmp_path):
    w=Workspace(tmp_path/"w.sqlite");w.initialize()
    w.add_project("Example",URL,"CryptoRank",prepare=False)
    with pytest.raises(ValueError):
        import_capture(w,{"source":URL,"text":"Трохи зачекайте. Триває перевірка безпеки.","sections":[]})
    assert not w.rows("SELECT * FROM snapshots")

def test_sensitive_instruction_is_labelled():
    text="Beta\n1. Скопіюйте приватний ключ свого гаманця для імпорту."
    result=public_guide(text,[{"title":"Beta","text":text}],URL)
    assert result["campaigns"][0]["steps"][0]["sensitive"]

@pytest.mark.parametrize("title,url,text",[
    ("Titan (Canton)","https://auto.ria.com/uk/car/nissan/titan/","Nissan Titan for sale crypto accepted"),
    ("Yield Fields","https://dictionary.cambridge.org/dictionary/english/yield","Yield meaning"),
    ("Yield Fields","https://example.com","Yield finance crypto protocol"),
    ("Titan (Canton)","https://example.com","Titan cryptocurrency on Ethereum"),
])
def test_irrelevant_search_is_rejected(title,url,text):
    assert not search_relevance(title,url,text)

def test_matching_project_search_is_only_a_lead():
    assert search_relevance("Titan (Canton)","https://example.com/titan","Titan on Canton blockchain testnet")
    assert search_relevance("Yield Fields","https://example.com","Yield Fields testnet faucet guide")

def test_old_polluted_snapshot_is_filtered_before_inference():
    bad={"url":"https://auto.ria.com/uk/car/nissan/titan/","text":"Cars for sale"}
    good={"url":URL,"text":"Real instruction from the project","links":[]}
    result=clean_material("Titan",{"url":URL,"text":"mixed","documents":[bad,good]})
    assert result["documents"]==[good] and result["truncated"]
    assert "Cars" not in result["text"]
    with pytest.raises(SourceUnavailable):clean_material("Titan",bad)


def test_empty_catalog_card_has_explicit_no_tasks_status():
    guide=public_guide("Прогресс 0 / 0 выполнено",[],URL)
    assert guide["access"]=="no_public_tasks" and not guide["campaigns"]


def test_fresh_capture_reaches_agent_without_blocked_http(tmp_path,monkeypatch):
    from discovery.coordinator import Coordinator
    import discovery.coordinator as module
    w=Workspace(tmp_path/"w.sqlite");w.initialize()
    pid,_=w.add_project("Example",URL,"CryptoRank",prepare=False)
    import_capture(w,capture())
    async def forbidden(*args):pytest.fail("Fresh browser capture should not request CryptoRank again")
    monkeypatch.setattr(module,"read_html",forbidden)
    body,via=asyncio.run(Coordinator(w).read_project(w.project(pid)))
    assert via=="browser_public_capture"
    assert TEXT in body["text"] and body["truncated"]


def test_login_overlay_drops_extra_dom_sections_even_if_present_in_payload():
    text=TEXT+"\nHidden section\n1. This step was behind the overlay and must not become a task."
    sections=capture()["sections"]+[{"title":"Hidden section","text":"Hidden section\n1. This step was behind the overlay and must not become a task."}]
    assert len(public_guide(text,sections,URL)["campaigns"])==1

def test_context_keeps_eligibility_and_omits_numbered_steps():
    text="Testnet\nYou must use test tokens for this campaign.\n1. Obtain test tokens from the faucet."
    guide=public_guide(text,[{"title":"Testnet","text":text}],URL)
    context=guide["campaigns"][0]["excerpt"]
    assert "You must use test tokens" in context and "1." not in context

def test_public_capture_api_requires_known_project_and_preserves_review_state(tmp_path):
    from fastapi.testclient import TestClient
    from web_tma.backend.server import create_app
    w=Workspace(tmp_path/"api.sqlite")
    with TestClient(create_app(w,background=False)) as c:
        token=c.get("/api/session").json()["token"]
        headers={"Origin":"http://testserver","X-Hunter-Session":token}
        assert c.post("/api/cryptorank/cards/import",json={"cards":[capture()]}).status_code==403
        assert c.post("/api/cryptorank/cards/import",json={"cards":[capture()]},headers=headers).json()["results"][0].get("error")
        pid,_=w.add_project("Example",URL,"CryptoRank",prepare=False)
        response=c.post("/api/cryptorank/cards/import",json={"cards":[capture()]},headers=headers)
        assert response.status_code==200 and response.json()["results"][0]["steps"]==2
        detail=c.get(f"/api/projects/{pid}").json()
        assert detail["preparation"]["source_steps"]==2
        assert detail["preparation"]["state"]=="public_material"
        assert not detail["public_guide"]["ai_analysis"]
        assert c.get("/api/cryptorank/cards").json()["public_read"]==1
        listing=c.get("/api/projects").json()
        assert listing[0]["public_preview"]
