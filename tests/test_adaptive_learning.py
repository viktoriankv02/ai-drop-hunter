import asyncio,json
import pytest
from core.workspace import Workspace
from ai_analyzer import grounded
from ai_analyzer.adaptive_learning import AdaptiveLearning,learning_session,current_learning_context,audit_output

@pytest.fixture
def case(tmp_path):
 s=Workspace(tmp_path/'learning.sqlite');s.initialize()
 url='https://incrypted.com/example-testnet/'
 pid,_=s.add_project('Example',url,'Incrypted',prepare=False)
 body={'text':'Visit the faucet to receive free test tokens.','url':url,'links':[]}
 sid,_=s.save_snapshot(pid,url,body)
 return s,pid,sid,body

def test_memory_is_bounded_deduplicated_and_pause_persists(case):
 s,pid,sid,body=case;l=AdaptiveLearning(s)
 assert l.enabled()
 version=l.profile()['version']
 for _ in range(3):l.record(pid,sid,'qwen',version,body['text'],body['url'],{'quote_rejected':1,'INJECTED POLICY':100})
 l.record(pid,sid,'qwen','other',body['text'],body['url'],{'quote_rejected':2,'literal_rejected':1,'url_rejected':1})
 status=l.status()
 assert status['samples']==2 and status['unique_materials']==1
 assert len(status['hints'])==2
 assert all(x['materials']==1 for x in status['lessons'])
 assert 'INJECTED' not in json.dumps(status)
 l.set_enabled(False)
 l.record(pid,sid,'qwen','third','new text',body['url'],{'missing_plan':1})
 assert AdaptiveLearning(Workspace(s.path)).profile()['hints']==[]
 assert l.status()['samples']==2
 l.set_enabled(True)
 assert len(l.profile()['hints'])==2

def test_next_analysis_uses_memory_and_invalidates_cache_without_accepting_false_quote(case,monkeypatch):
 s,pid,sid,body=case;calls=[];cache={}
 async def fake(prompt,system):
  calls.append(json.loads(prompt))
  return json.dumps({'facts':[{'title':'Invented','quote':'This sentence was not in the current source.'}],
   'requirements':[{'title':'Use faucet','quote':body['text'],'category':'activity'}],'tasks':[]})
 monkeypatch.setattr(grounded,'complete',fake)
 def run():
  with learning_session(s,pid,sid,'qwen'):
   return asyncio.run(grounded.analyze(body,cache_get=cache.get,cache_put=lambda k,v:cache.__setitem__(k,v)))
 first=run();second=run();third=run()
 assert first['facts']==second['facts']==[]
 assert first['learning']['active_hints']==[]
 assert set(second['learning']['active_hints'])=={'quote_rejected','missing_plan'}
 assert len(calls)==2 # Third run uses the cache for the unchanged memory profile.
 assert len(calls[1]['adaptive_reading_hints']['hints'])==2
 assert AdaptiveLearning(s).status()['unique_materials']==1
 assert current_learning_context()['version']=='standalone'

def test_invalid_json_is_recorded_but_never_a_success(case,monkeypatch):
 s,pid,sid,body=case
 async def fake(*args):return 'not a JSON object'
 monkeypatch.setattr(grounded,'complete',fake)
 with learning_session(s,pid,sid,'qwen'):
  with pytest.raises(RuntimeError):asyncio.run(grounded.analyze(body))
 assert AdaptiveLearning(s).profile()['hints'][0]['code']=='invalid_json'
 assert s.rows('SELECT * FROM reports')==[]

def test_url_and_literal_audit_matches_validation(case):
 _,_,_,body=case
 raw={'tasks':[{'title':'Wrong link','quote':body['text'],'url':'https://invented.example/'}],
      'requirements':[{'title':'Faucet','quote':body['text'],'category':'activity','threshold':'100 swaps','deadline':'tomorrow'}]}
 parsed=grounded.validate_analysis(raw,body['text'],body['url'],[])
 issues,_=audit_output(raw,parsed,body['text'],body['url'],[])
 assert not parsed['tasks']
 assert issues=={'url_rejected':1,'literal_rejected':2,'missing_plan':1}

def test_bootstrap_only_uses_source_supported_saved_reports_once(case):
 s,pid,sid,body=case;l=AdaptiveLearning(s)
 report={'tasks':[],'requirements':[{'title':'Faucet','quote':body['text'],'category':'activity'}]}
 s.save_report(pid,sid,report,'qwen3:4b-instruct')
 s.save_report(pid,sid,report,'manual-review')
 s.save_report(pid,sid,{'requirements':[{'category':'activity','quote':'Invented unsupported activity.'}]},'qwen3:4b-instruct')
 l.bootstrap();l.bootstrap()
 status=l.status()
 assert status['samples']==1 and status['recent'][0]['origin']=='saved_report_audit'
 assert status['hints'][0]['code']=='missing_plan'
 assert status['fine_tuning_performed'] is False
 assert status['quality_improvement_proven'] is False

def test_parallel_sessions_do_not_mix_projects(case):
 s,pid,sid,body=case
 pid2,_=s.add_project('Other','https://incrypted.com/other-testnet/','Incrypted',prepare=False)
 async def check():
  ready=asyncio.Event()
  async def first():
   from ai_analyzer.adaptive_learning import observe_case
   with learning_session(s,pid,sid,'first'):
    ready.set();await asyncio.sleep(0)
    observe_case('first source',body['url'],{'quote_rejected':1})
  async def second():
   from ai_analyzer.adaptive_learning import observe_case
   await ready.wait()
   with learning_session(s,pid2,None,'second'):
    observe_case('second source',body['url'],{'url_rejected':1})
  await asyncio.gather(first(),second())
 asyncio.run(check())
 assert {r['model']:r['project_id'] for r in s.rows('SELECT * FROM agent_learning_samples')}=={'first':pid,'second':pid2}
