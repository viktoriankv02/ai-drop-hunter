import time,json
import httpx,pytest
from fastapi.testclient import TestClient
from core.mobile_access import MobileAccess,COOKIE
from core.workspace import Workspace
from web_tma.backend.mobile_gateway import create_gateway
from web_tma.backend.server import create_app

@pytest.fixture
def access(tmp_path):
 a=MobileAccess(tmp_path/'phone.sqlite');a.set_origin('https://phone.example');return a

def test_codes_are_one_time_expiring_and_rate_limited(access):
 code=access.pair_code();assert not access.valid(code)
 with access.db() as c:assert code not in json.dumps(access.values(c))
 token=access.redeem(code);assert token and access.valid(token)
 assert access.redeem(code) is None
 access.revoke_all();assert not access.valid(token)
 code=access.pair_code()
 for _ in range(8):assert access.redeem('WRONG') is None
 assert access.redeem(code) is None
 code=access.pair_code()
 with access.db() as c:access.put(c,'pair_expires',time.time()-1)
 assert access.redeem(code) is None

def test_origin_rotation_revokes_sessions_and_pending_codes(access):
 token=access.redeem(access.pair_code());code=access.pair_code()
 access.set_origin('https://new-phone.example')
 assert not access.valid(token) and access.redeem(code) is None
 with pytest.raises(ValueError):access.set_origin('http://public.example')

def test_gateway_denies_data_before_login_and_checks_origin_and_host(access):
 seen=[]
 def backend(req):seen.append(req);return httpx.Response(200,json={'private':True})
 app=create_gateway(access,transport=httpx.MockTransport(backend))
 with TestClient(app,base_url='https://phone.example') as c:
  assert c.get('/api/projects').status_code==401
  assert c.get('/',follow_redirects=False).status_code==303
  assert c.get('/mobile-login').status_code==200
  assert c.get('/api/projects',headers={'host':'evil.example'}).status_code==403
  code=access.pair_code()
  assert c.post('/mobile/pair',json={'code':code},headers={'origin':'https://evil.example'}).status_code==403
  r=c.post('/mobile/pair',json={'code':code},headers={'origin':'https://phone.example'})
  assert r.status_code==200 and 'Secure' in r.headers['set-cookie'] and 'HttpOnly' in r.headers['set-cookie']
  assert c.get('/api/projects').json()=={'private':True}
  assert c.post('/api/projects/1/status',json={},headers={'origin':'https://evil.example'}).status_code==403
  assert c.get('/api/mobile/status').status_code==403
  assert c.post('/api/mobile/pair-code',json={},headers={'origin':'https://phone.example'}).status_code==403
  assert c.get('/static/%2e%2e/api/mobile/status').status_code==400
  assert c.get('/api/%6dobile/status').status_code==403
  r=c.post('/api/projects/1/status',json={'status':'tracking'},headers={'origin':'https://phone.example','x-hunter-session':'test-token','x-forwarded-host':'evil.example'})
  assert r.status_code==200
  assert seen[-1].url.host=='127.0.0.1' and seen[-1].headers['origin']=='http://127.0.0.1:4318'
  assert 'x-forwarded-host' not in seen[-1].headers
  assert seen[-1].headers['x-hunter-session']=='test-token'
  assert c.post('/mobile/logout',headers={'origin':'https://phone.example'}).status_code==200
  assert c.get('/api/projects').status_code==401

def test_gateway_revocation_and_backend_failure(access):
 def backend(req):raise httpx.ConnectError('offline')
 with TestClient(create_gateway(access,transport=httpx.MockTransport(backend)),base_url='https://phone.example') as c:
  code=access.pair_code();c.post('/mobile/pair',json={'code':code},headers={'origin':'https://phone.example'})
  assert c.get('/api/projects').status_code==503
  access.revoke_all();assert c.get('/api/projects').status_code==401

def test_local_pairing_api_and_installation_assets(tmp_path):
 store=Workspace(tmp_path/'workspace.sqlite');mobile=MobileAccess(tmp_path/'workspace-mobile.sqlite')
 with TestClient(create_app(store,background=False)) as c:
  token=c.get('/api/session').json()['token']
  c.headers.update({'Origin':'http://testserver','X-Hunter-Session':token})
  assert c.get('/api/mobile/status').json()['origin'] is None
  assert c.post('/api/mobile/pair-code').status_code==400
  mobile.set_origin('https://phone.example');mobile.heartbeat()
  result=c.post('/api/mobile/pair-code').json()
  assert result['qr'].startswith('data:image/svg+xml;base64,') and result['expires_in']==600
  phone=mobile.redeem(result['code']);assert mobile.valid(phone)
  assert 'code' not in c.get('/api/mobile/status').json()
  c.post('/api/mobile/revoke');assert not mobile.valid(phone)
  manifest=c.get('/manifest.webmanifest').json()
  assert manifest['display']=='standalone' and manifest['scope']=='/'
  for icon in manifest['icons']:assert c.get(icon['src']).status_code==200
  worker=c.get('/sw.js');assert worker.headers['service-worker-allowed']=='/'
  assert c.get('/offline.html').status_code==200


def test_phone_edits_the_same_project_and_cannot_manage_pairing(tmp_path):
 store=Workspace(tmp_path/'workspace.sqlite');a=MobileAccess(tmp_path/'workspace-mobile.sqlite');a.set_origin('https://phone.example')
 app=create_app(store,background=False)
 with TestClient(app) as desktop:
  desktop.headers.update({'Origin':'http://testserver','X-Hunter-Session':desktop.get('/api/session').json()['token']})
  pid=desktop.post('/api/projects/manual',json={'title':'Shared phone project','source_url':'https://incrypted.com/shared/'}).json()['project_id']
  gateway=create_gateway(a,transport=httpx.ASGITransport(app=app))
  with TestClient(gateway,base_url='https://phone.example') as phone:
   phone.post('/mobile/pair',json={'code':a.pair_code()},headers={'origin':'https://phone.example'})
   token=phone.get('/api/session').json()['token']
   phone.headers.update({'Origin':'https://phone.example','X-Hunter-Session':token})
   assert phone.post(f'/api/projects/{pid}/status',json={'status':'tracking'}).status_code==200
   assert desktop.get(f'/api/projects/{pid}').json()['status']=='tracking'
   for url in ['/api/mobile/pair-code','/static/%2e%2e/api/mobile/pair-code','/api/%6dobile/pair-code']:
    assert phone.post(url,json={}).status_code in (400,403)
   a.revoke_all()
   assert phone.get('/api/projects').status_code==401
