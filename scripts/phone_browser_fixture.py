"""Loopback-only HTTPS gateway for browser tests; never opens a tunnel."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import uvicorn
from core.mobile_access import MobileAccess
from web_tma.backend.mobile_gateway import create_gateway
state=Path(sys.argv[1]);access=MobileAccess(state.with_suffix('.sqlite'))
access.set_origin('https://phone.test:4322');state.write_text(json.dumps({'code':access.pair_code()}))
uvicorn.run(create_gateway(access,backend='http://127.0.0.1:4319'),host='127.0.0.1',port=4322,ssl_certfile=sys.argv[2],ssl_keyfile=sys.argv[3],proxy_headers=False,log_level='warning')
