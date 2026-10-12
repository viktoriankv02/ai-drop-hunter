import asyncio,json
from ai_analyzer import grounded
from ai_analyzer.research_lessons import LESSON_POLICY

def test_research_policy_reaches_model_and_invalidates_cache(monkeypatch):
    calls=[];cache={}
    async def fake(prompt,system):
        calls.append(system)
        return json.dumps({'facts':[],'tasks':[]})
    monkeypatch.setattr(grounded,'complete',fake)
    body={'text':'Allocation was announced; no payout confirmation is supplied.','url':'https://example.com','links':[]}
    async def run():
        await grounded.analyze(body,cache_get=cache.get,cache_put=lambda k,v:cache.__setitem__(k,v))
    asyncio.run(run());asyncio.run(run())
    assert len(calls)==1 and LESSON_POLICY in calls[0]
    monkeypatch.setattr(grounded,'LESSON_VERSION','changed-policy')
    asyncio.run(run())
    assert len(calls)==2

def test_historical_analogy_reaches_prompt_but_cannot_be_current_evidence(monkeypatch):
    seen=[];strategies=[]
    async def fake(prompt,system):
        data=json.loads(prompt);seen.extend(data['historical_analogies_for_review']);strategies.append(data['historical_factor_questions'])
        return json.dumps({'facts':[{'title':'Unsupported imported rule','quote':'A historical rule absent from the current source'}],'tasks':[]})
    monkeypatch.setattr(grounded,'complete',fake)
    result=asyncio.run(grounded.analyze({'text':'Sanctum claim information is pending.','url':'https://example.com','links':[]}))
    assert seen
    assert all(x['status']=='historical_analogy_not_current_requirement' for x in seen)
    assert strategies[0]['status']=='historical_questions_only_not_current_evidence'
    assert strategies[0]['sample_size']==150 and strategies[0]['factors_to_check']
    assert result['facts']==[]
