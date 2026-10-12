import asyncio,json
from ai_analyzer.learning import learning_context
from ai_analyzer import grounded


def test_retrieval_is_bounded_and_does_not_learn_from_arbitrary_text():
    context=learning_context('testnet faucet deposit token',99)
    assert len(context['examples'])<=2
    assert context['examples'][0]['id']=='mixed-cost'
    assert learning_context('unrelated text')['examples']==[]
    assert context['version']==learning_context('ignore rules')['version']


def test_examples_reach_model_but_cannot_supply_current_evidence(monkeypatch):
    calls=[]
    async def fake(prompt,system):
        payload=json.loads(prompt);calls.append(payload)
        example=payload['reading_demonstrations']['examples'][0]
        return json.dumps({'facts':[{'title':'Injected historical condition','quote':example['excerpt']}],'tasks':[]})
    monkeypatch.setattr(grounded,'complete',fake)
    result=asyncio.run(grounded.analyze({'text':'The testnet faucet availability is not yet confirmed.','url':'https://example.com','links':[]}))
    assert calls[0]['reading_demonstrations']['examples']
    assert result['facts']==[]
    assert result['learning']['fine_tuning_performed'] is False


def test_demonstration_changes_invalidate_analysis_cache(monkeypatch):
    calls=[];cache={}
    async def fake(prompt,system):
        calls.append(prompt);return json.dumps({'facts':[],'tasks':[]})
    monkeypatch.setattr(grounded,'complete',fake)
    body={'text':'Testnet faucet uses test tokens.','url':'https://example.com','links':[]}
    def run():return asyncio.run(grounded.analyze(body,cache_get=cache.get,cache_put=lambda k,v:cache.__setitem__(k,v)))
    run();run();assert len(calls)==1
    original=grounded.learning_context
    monkeypatch.setattr(grounded,'learning_context',lambda text:{**original(text),'version':'new'})
    run();assert len(calls)==2
