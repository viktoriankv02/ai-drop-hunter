from pathlib import Path
import sys,uvicorn
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace
from web_tma.backend.server import create_app
store=Workspace(sys.argv[1]);store.initialize()
pid,_=store.add_project("Browser test project","https://cryptorank.io/ru/drophunting/browser-test-activity1","CryptoRank",
                       "<img src=x onerror=alert(1)> untrusted text")
app=create_app(store,background=False)
uvicorn.run(app,host="127.0.0.1",port=4319,log_level="warning")
