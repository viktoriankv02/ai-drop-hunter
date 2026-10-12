"""Automatic error memory. Fixed reading hints; no model weights or self-labelled facts."""
import hashlib,json,re
from collections import Counter
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime,timezone

RULES={
 'quote_rejected':('Неточні цитати','Copy a contiguous exact excerpt from the CURRENT source. Do not translate or paraphrase the quote; translate only the title.'),
 'url_rejected':('Посилання поза джерелом','Use only an exact URL supplied in links or source_url. If the action URL is absent, link to the source; never invent a destination.'),
 'literal_rejected':('Непідтверджені пороги або дати','Threshold and deadline must be literal substrings of the same quote. If absent, return null.'),
 'missing_plan':('Дії не перетворені на кроки','For each source-supported activity requirement, also return a task with the same exact quote and an allowed URL. Do not invent extra activities.'),
 'invalid_json':('Невірна структура відповіді','Return one valid JSON object. facts, tasks and requirements must be arrays; use empty arrays when no evidence exists.'),
}
POLICY_VERSION='adaptive-error-memory-v1'
_profile=ContextVar('adaptive_profile',default=None)
_record=ContextVar('adaptive_record',default=None)

def initialize_learning(connection):
 connection.executescript('''CREATE TABLE IF NOT EXISTS agent_learning_samples(
   id TEXT PRIMARY KEY,case_key TEXT NOT NULL,project_id INTEGER REFERENCES projects(id),
   snapshot_id INTEGER REFERENCES snapshots(id),model TEXT NOT NULL,profile_version TEXT NOT NULL,
   origin TEXT NOT NULL,issues_json TEXT NOT NULL,accepted INTEGER NOT NULL,created_at TEXT NOT NULL);
   CREATE INDEX IF NOT EXISTS learning_case ON agent_learning_samples(case_key);''')
 connection.execute("INSERT OR IGNORE INTO meta VALUES ('automatic_learning','1')")

def current_learning_context():
 return _profile.get() or {'enabled':False,'version':'standalone','hints':[],'method':'error_memory_not_weight_training'}

def observe_case(text,source_url,issues,accepted=0):
 recorder=_record.get()
 if recorder:recorder(text,source_url,issues,accepted)

def audit_output(value,parsed,text,source_url,links):
 issues=Counter();allowed={source_url,*[x['url'] for x in links]}
 for field in ('facts','tasks','requirements'):
  for item in value.get(field,[])[:30]:
   if not isinstance(item,dict):continue
   quote=item.get('quote')
   if not isinstance(quote,str) or len(quote.strip())<15 or quote not in text or not re.search(r'(?<!\w)'+re.escape(quote)+r'(?!\w)',text):
    issues['quote_rejected']+=1;continue
   if not isinstance(item.get('title'),str) or not item['title'].strip():continue
   if field=='tasks' and item.get('url') not in allowed:issues['url_rejected']+=1
   if field=='requirements':
    for key in ('threshold','deadline'):
     literal=item.get(key)
     if literal is not None and (not isinstance(literal,str) or literal not in quote):issues['literal_rejected']+=1
 if not parsed.get('tasks') and not any(c.get('steps') for c in parsed.get('campaigns',[])) and any(x.get('category')=='activity' for x in parsed.get('requirements',[])):
  issues['missing_plan']=1
 accepted=sum(len(parsed.get(k,[])) for k in ('facts','tasks','requirements'))
 return dict(issues),accepted

class AdaptiveLearning:
 def __init__(self,store):self.store=store
 def enabled(self):
  return bool(self.store.rows("SELECT 1 FROM meta WHERE key='automatic_learning' AND value='1'"))
 def set_enabled(self,value):
  with self.store.db() as c:c.execute("INSERT INTO meta VALUES ('automatic_learning',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",('1' if value else '0',))
 def counts(self):
  cases={code:set() for code in RULES}
  for row in self.store.rows('SELECT case_key,issues_json FROM agent_learning_samples'):
   for code,count in json.loads(row['issues_json']).items():
    if code in cases and count>0:cases[code].add(row['case_key'])
  return {code:len(keys) for code,keys in cases.items()}
 def profile(self):
  enabled=self.enabled();counts=self.counts() if enabled else {}
  codes=sorted((code for code,n in counts.items() if n),key=lambda code:(-counts[code],code))[:2]
  # Only reviewed fixed hints can be promoted; source text and model prose cannot become policy.
  hints=[{'code':code,'instruction':RULES[code][1]} for code in codes]
  version=hashlib.sha256(json.dumps([POLICY_VERSION,enabled,hints],sort_keys=True).encode()).hexdigest()[:16]
  return {'enabled':enabled,'version':version,'hints':hints,'method':'error_memory_not_weight_training'}
 def record(self,pid,sid,model,version,text,source_url,issues,accepted=0,origin='live_validation'):
  if not self.enabled():return
  clean={code:min(30,count) for code,count in issues.items() if code in RULES and type(count) is int and count>0}
  case=hashlib.sha256((source_url+'\n'+text).encode()).hexdigest()
  identity=hashlib.sha256((case+'|'+model+'|'+version+'|'+origin).encode()).hexdigest()
  accepted=max(0,min(90,accepted)) if type(accepted) is int else 0
  with self.store.db() as c:
   c.execute('INSERT OR IGNORE INTO agent_learning_samples VALUES (?,?,?,?,?,?,?,?,?,?)',
    (identity,case,pid,sid,model,version,origin,json.dumps(clean),accepted,datetime.now(timezone.utc).isoformat()))
 def status(self):
  profile=self.profile();counts=self.counts();active={x['code'] for x in profile['hints']}
  rows=self.store.rows('''SELECT l.*,p.title FROM agent_learning_samples l LEFT JOIN projects p ON p.id=l.project_id
   ORDER BY l.created_at DESC LIMIT 12''')
  total=self.store.rows('SELECT COUNT(*) n,COUNT(DISTINCT case_key) cases FROM agent_learning_samples')[0]
  return {**profile,'fine_tuning_performed':False,'quality_improvement_proven':False,
   'samples':total['n'],'unique_materials':total['cases'],
   'lessons':[{'code':code,'title':RULES[code][0],'materials':n,'active':code in active} for code,n in counts.items() if n],
   'recent':[{'project_id':r['project_id'],'title':r['title'],'created_at':r['created_at'],'origin':r['origin'],
      'issues':[RULES[k][0] for k in json.loads(r['issues_json']) if k in RULES],'accepted':r['accepted']} for r in rows],
   'notice':'Автоматична пам’ять помилок змінює підказки. Це не перенавчання ваг; зниження кількості помилок ще потрібно підтвердити порівняльними перевірками.'}
 def bootstrap(self):
  if not self.enabled() or self.store.rows("SELECT 1 FROM meta WHERE key='adaptive_bootstrap_v1'"):return
  rows=self.store.rows('''SELECT r.*,s.body_json snapshot_json,s.url FROM reports r
    JOIN snapshots s ON s.id=r.snapshot_id JOIN projects p ON p.id=r.project_id
    WHERE r.model LIKE 'qwen%' AND (p.source_url LIKE 'https://cryptorank.io/%' OR p.source_url LIKE 'https://incrypted.com/%')
    ORDER BY r.id DESC LIMIT 100''')
  for row in rows:
   result=json.loads(row['body_json']);body=json.loads(row['snapshot_json']);text=body.get('text','')
   if not isinstance(text,str):continue
   activities=[x for x in result.get('requirements',[]) if x.get('category')=='activity' and x.get('quote') and x['quote'] in text]
   if activities and not result.get('tasks') and not any(x.get('steps') for x in result.get('campaigns',[])):
    self.record(row['project_id'],row['snapshot_id'],row['model'],'historical-audit',text,row['url'],{'missing_plan':1},len(activities),'saved_report_audit')
  with self.store.db() as c:c.execute("INSERT OR IGNORE INTO meta VALUES ('adaptive_bootstrap_v1','1')")

@contextmanager
def learning_session(store,pid,sid,model):
 learner=AdaptiveLearning(store);profile=learner.profile()
 ptoken=_profile.set(profile)
 rtoken=_record.set(lambda text,url,issues,accepted:learner.record(pid,sid,model,profile['version'],text,url,issues,accepted))
 try:yield profile
 finally:_record.reset(rtoken);_profile.reset(ptoken)
