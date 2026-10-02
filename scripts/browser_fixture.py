from pathlib import Path
import sys,uvicorn,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace
from web_tma.backend.server import create_app
store=Workspace(sys.argv[1]);store.initialize()
pid,_=store.add_project("Browser test project","https://cryptorank.io/ru/drophunting/browser-test-activity1","CryptoRank",
                       "<img src=x onerror=alert(1)> untrusted text")
store.save_snapshot(pid,store.project(pid)["source_url"],{"text":"Testnet faucet provides test tokens for this test campaign.","truncated":False})
store.save_snapshot(pid,store.project(pid)["source_url"],{"text":"Indexed research only.","truncated":True,"research_note":{"provenance":"Indexed copy, not a live check","facts":[],"unknowns":["Faucet availability is unconfirmed <img src=x onerror=alert(1)>"]}},via="reviewed_research_note")
store.save_snapshot(pid,store.project(pid)["source_url"],{"text":"Testnet faucet provides test tokens for this test campaign.","truncated":False})
sid,_=store.save_snapshot(pid,store.project(pid)["source_url"],{"text":"Testnet faucet provides test tokens. You must register before 30 October. Optional: submit useful testnet feedback.","truncated":False})
store.save_report(pid,sid,{"facts":[],"tasks":[],"requirements":[{"title":"Зареєструватися до дедлайну","quote":"You must register before 30 October.","source_url":store.project(pid)["source_url"],"category":"registration","necessity":"required","deadline":"30 October","requires_user_review":True},{"title":"Надіслати відгук про тестнет","quote":"Optional: submit useful testnet feedback.","source_url":store.project(pid)["source_url"],"category":"activity","necessity":"optional"}],"coverage":{"complete":True,"processed_characters":76,"retained_characters":76},"unknowns":[],"status":"draft"},"fixture")
sid,_=store.save_snapshot(pid,store.project(pid)["source_url"],{"text":"Browser test project is a testnet with a faucet providing test tokens. You must register before 30 October.","truncated":False})
store.save_overview(pid,sid,{"brief":"Тестова мережа з faucet для отримання тестових токенів.","quote":"Browser test project is a testnet with a faucet providing test tokens.","source_url":store.project(pid)["source_url"]})
last=store.rows("SELECT * FROM reports WHERE project_id=? ORDER BY id DESC LIMIT 1",(pid,))[0]
r=json.loads(last['body_json']);task={"title":"Зареєструватися до дедлайну","quote":"You must register before 30 October.","url":store.project(pid)['source_url'],"source_url":store.project(pid)['source_url']}
r['tasks']=[task];r['campaigns']=[{"title":"Beta · поточна кампанія","status":"active","period":"До 30 October","network":"Testnet","reward":"Ще не підтверджено","steps":[task]},{"title":"Alpha · завершена фаза","status":"ended","steps":[]}]
store.save_report(pid,last['snapshot_id'],r,'fixture')
app=create_app(store,background=False)
uvicorn.run(app,host="127.0.0.1",port=4319,log_level="warning")
