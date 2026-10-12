"""Local pairing control for the phone gateway. Secrets are hashed; sessions revocable."""
import hashlib,secrets,sqlite3,time,re
from pathlib import Path
from contextlib import contextmanager

COOKIE='__Host-hunter-phone'
class MobileAccess:
 def __init__(self,path):self.path=Path(path)
 @contextmanager
 def db(self):
  self.path.parent.mkdir(parents=True,exist_ok=True)
  c=sqlite3.connect(self.path,timeout=10);c.row_factory=sqlite3.Row
  try:
   c.execute('CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
   c.execute('CREATE TABLE IF NOT EXISTS sessions(hash TEXT PRIMARY KEY,expires REAL NOT NULL)')
   yield c;c.commit()
  finally:c.close()
 @staticmethod
 def digest(value):return hashlib.sha256(value.encode()).hexdigest()
 @staticmethod
 def put(c,k,v):c.execute('INSERT INTO settings VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',(k,str(v)))
 @staticmethod
 def values(c):return {r['key']:r['value'] for r in c.execute('SELECT * FROM settings')}
 def set_origin(self,origin):
  if not re.fullmatch(r'https://[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?(?::[0-9]{1,5})?',origin):raise ValueError('An exact HTTPS origin is required')
  with self.db() as c:
   old=self.values(c).get('origin')
   if old!=origin:
    c.execute('DELETE FROM sessions');c.execute("DELETE FROM settings WHERE key IN ('pair_hash','pair_expires','attempts')")
   self.put(c,'origin',origin)
 def status(self):
  with self.db() as c:
   v=self.values(c);now=time.time()
   c.execute('DELETE FROM sessions WHERE expires<?',(now,))
   return {'origin':v.get('origin'),'paired_devices':c.execute('SELECT count(*) FROM sessions').fetchone()[0],
    'pairing_active':float(v.get('pair_expires','0'))>now and int(v.get('attempts','0'))<8,
    'gateway_ready':float(v.get('heartbeat','0'))>now-90,'temporary':v.get('origin','').endswith(('.trycloudflare.com','.lhr.life','.localhost.run'))}
 def heartbeat(self):
  with self.db() as c:self.put(c,'heartbeat',time.time())
 def pair_code(self):
  code=secrets.token_hex(8).upper()
  with self.db() as c:
   if not self.values(c).get('origin'):raise ValueError('Захищене посилання для телефона ще не запущене')
   self.put(c,'pair_hash',self.digest(code));self.put(c,'pair_expires',time.time()+600);self.put(c,'attempts',0)
  return code
 def redeem(self,code):
  code=code.strip().replace('-','').replace(' ','').upper()
  with self.db() as c:
   c.execute('BEGIN IMMEDIATE');v=self.values(c)
   if float(v.get('pair_expires','0'))<=time.time() or int(v.get('attempts','0'))>=8:return None
   self.put(c,'attempts',int(v.get('attempts','0'))+1)
   if not secrets.compare_digest(self.digest(code),v.get('pair_hash','')):return None
   c.execute("DELETE FROM settings WHERE key IN ('pair_hash','pair_expires','attempts')")
   token=secrets.token_urlsafe(32)
   c.execute('DELETE FROM sessions WHERE expires<?',(time.time(),))
   c.execute('INSERT INTO sessions VALUES (?,?)',(self.digest(token),time.time()+30*86400))
   return token
 def valid(self,token):
  if not token or len(token)>100:return False
  with self.db() as c:return bool(c.execute('SELECT 1 FROM sessions WHERE hash=? AND expires>?',(self.digest(token),time.time())).fetchone())
 def logout(self,token):
  with self.db() as c:c.execute('DELETE FROM sessions WHERE hash=?',(self.digest(token or ''),))
 def revoke_all(self):
  with self.db() as c:
   c.execute('DELETE FROM sessions');c.execute("DELETE FROM settings WHERE key IN ('pair_hash','pair_expires','attempts')")

 def disable(self):
  self.revoke_all()
  with self.db() as c:c.execute("DELETE FROM settings WHERE key='origin'")
