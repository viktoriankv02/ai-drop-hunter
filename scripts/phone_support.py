"""Local CLI for phone setup. No model, wallet or cloud credentials."""
import hashlib,json,sys,urllib.request,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.paths import ROOT, mobile_database
from core.mobile_access import MobileAccess
access=MobileAccess(mobile_database())
def download():
 target=ROOT/'data/tools/cloudflared.exe';metadata=target.with_suffix('.json')
 if target.exists() and metadata.exists():
  info=json.loads(metadata.read_text())
  if hashlib.sha256(target.read_bytes()).hexdigest()==info.get('sha256'):return str(target)
 request=urllib.request.Request('https://api.github.com/repos/cloudflare/cloudflared/releases/latest',headers={'User-Agent':'Hunter-local-phone-setup'})
 release=json.load(urllib.request.urlopen(request,timeout=30))
 asset=next(a for a in release['assets'] if a['name']=='cloudflared-windows-amd64.exe')
 digest=asset.get('digest','')
 if not re.fullmatch('sha256:[a-f0-9]{64}',digest):raise RuntimeError('Official asset SHA256 is missing; download stopped')
 url=asset['browser_download_url']
 if not url.startswith('https://github.com/cloudflare/cloudflared/releases/download/'):raise RuntimeError('Unexpected download origin')
 data=urllib.request.urlopen(url,timeout=90).read()
 if hashlib.sha256(data).hexdigest()!=digest[7:]:raise RuntimeError('Checksum mismatch; download stopped')
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 metadata.write_text(json.dumps({'version':release['tag_name'],'url':url,'sha256':digest[7:]},indent=2))
 return str(target)
def verify():
 import httpx
 origin=access.status()['origin']
 if not origin:raise RuntimeError('Phone origin is missing')
 with httpx.Client(timeout=8,trust_env=False,follow_redirects=False) as client:
  page=client.get(origin+'/mobile-login')
  if page.status_code!=200 or 'pair-form' not in page.text:raise RuntimeError('Login page not reachable')
  probe=client.get(origin+'/api/projects')
  if probe.status_code!=401:raise RuntimeError('Unauthenticated API access was not rejected')
 print('Verified HTTPS login and anonymous API protection')

if __name__=='__main__':
 if sys.argv[1]=='download':print(download())
 elif sys.argv[1]=='origin':access.set_origin(sys.argv[2])
 elif sys.argv[1]=='verify':verify()
 elif sys.argv[1]=='status':print(json.dumps(access.status()))
 elif sys.argv[1]=='revoke':access.revoke_all()
 elif sys.argv[1]=='disable':access.disable()
