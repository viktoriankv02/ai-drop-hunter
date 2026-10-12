"""Authenticated phone proxy. Bind loopback only; HTTPS terminates at the tunnel."""
import asyncio,os,json
from contextlib import asynccontextmanager
from pathlib import Path
import httpx
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse,RedirectResponse,FileResponse,Response
from core.mobile_access import MobileAccess,COOKIE
from core.paths import ROOT, mobile_database

PUBLIC={'/mobile-login','/manifest.webmanifest','/sw.js','/offline.html'}
def create_gateway(access=None,transport=None,backend='http://127.0.0.1:4318'):
 access=access or MobileAccess(mobile_database())
 @asynccontextmanager
 async def lifespan(app):
  async def heartbeat():
   while True:access.heartbeat();await asyncio.sleep(30)
  task=asyncio.create_task(heartbeat())
  try:yield
  finally:task.cancel();await asyncio.gather(task,return_exceptions=True)
 app=FastAPI(lifespan=lifespan,docs_url=None,redoc_url=None,openapi_url=None)
 @app.middleware('http')
 async def protect(request,call_next):
  origin=access.status()['origin']
  if not origin or request.headers.get('host')!=origin.removeprefix('https://'):
   return JSONResponse({'detail':'Мобільний доступ не налаштований'},status_code=403)
  if request.method not in ('GET','HEAD') and request.headers.get('origin')!=origin:
   return JSONResponse({'detail':'Невідоме походження запиту'},status_code=403)
  path=request.url.path
  if any(part in ('.','..') for part in path.split('/')) or chr(92) in path:
   return JSONResponse({'detail':'Некоректна адреса'},status_code=400)
  if path.startswith('/api/mobile') or path in ('/docs','/redoc','/openapi.json'):
   return JSONResponse({'detail':'Керування підключенням доступне лише на ПК'},status_code=403)
  public=(path in PUBLIC or path.startswith('/static/')) and request.method in ('GET','HEAD')
  pairing=path=='/mobile/pair' and request.method=='POST'
  if not public and not pairing and not access.valid(request.cookies.get(COOKIE)):
   if path.startswith('/api/') or request.method!='GET':return JSONResponse({'detail':'Увійди за одноразовим кодом','login_url':'/mobile-login'},status_code=401)
   return RedirectResponse('/mobile-login',status_code=303)
  response=await call_next(request)
  response.headers['Cache-Control']='no-store'
  response.headers['Referrer-Policy']='no-referrer'
  response.headers['X-Content-Type-Options']='nosniff'
  response.headers['X-Frame-Options']='DENY'
  return response
 @app.get('/mobile-login')
 def login():return FileResponse(ROOT/'web_tma/frontend/mobile-login.html')
 @app.post('/mobile/pair')
 async def pair(request:Request):
  raw=await limited_body(request,1024)
  if raw is None:return JSONResponse({'detail':'Запит завеликий'},status_code=413)
  try:
   data=json.loads(raw);code=data.get('code')
   if not isinstance(code,str) or len(code)>80:raise ValueError()
  except (ValueError,AttributeError):return JSONResponse({'detail':'Некоректний код'},status_code=400)
  token=access.redeem(code)
  if not token:return JSONResponse({'detail':'Код невірний або вже використаний. Створи новий код на ПК або через SSH сервера.'},status_code=401)
  response=JSONResponse({'ok':True})
  response.set_cookie(COOKIE,token,max_age=30*86400,secure=True,httponly=True,samesite='strict',path='/')
  return response
 @app.post('/mobile/logout')
 def logout(request:Request):
  access.logout(request.cookies.get(COOKIE));response=JSONResponse({'ok':True})
  response.delete_cookie(COOKIE,path='/',secure=True,httponly=True,samesite='strict');return response
 @app.api_route('/{path:path}',methods=['GET','HEAD','POST','DELETE','PUT','PATCH','OPTIONS'])
 async def proxy(path:str,request:Request):
  raw=await limited_body(request,300000)
  if raw is None:return JSONResponse({'detail':'Запит завеликий'},status_code=413)
  # Fixed backend. Never forward a URL/Host/Origin supplied by a caller.
  target=backend+'/'+path
  if request.url.query:target+='?'+request.url.query
  headers={'Origin':backend}
  for key in ('content-type','x-hunter-session'):
   if request.headers.get(key):headers[key]=request.headers[key]
  try:
   async with httpx.AsyncClient(transport=transport,trust_env=False,timeout=35,follow_redirects=False) as client:
    result=await client.request(request.method,target,headers=headers,content=raw)
  except httpx.HTTPError:return JSONResponse({'detail':'Сервіс Hunter недоступний. Перевір, чи він запущений.'},status_code=503)
  return Response(result.content,status_code=result.status_code,headers={k:v for k,v in result.headers.items() if k.lower() in ('content-type','service-worker-allowed')})
 return app

async def limited_body(request,limit):
 data=bytearray()
 async for chunk in request.stream():
  data.extend(chunk)
  if len(data)>limit:return None
 return bytes(data)

app=create_gateway()
if __name__=='__main__':
 import uvicorn
 uvicorn.run(app,host='127.0.0.1',port=4320,proxy_headers=False)
