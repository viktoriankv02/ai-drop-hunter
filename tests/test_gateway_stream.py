import asyncio,json
import httpx,pytest
from contextlib import asynccontextmanager
from ai_analyzer import gateway


def stream_test(monkeypatch,parts):
    payloads=[];events=[]
    real=httpx.AsyncClient
    async def respond(request):
        payloads.append(json.loads(request.content))
        return httpx.Response(200,text='\n'.join(json.dumps(p) for p in parts))
    monkeypatch.setattr(gateway.httpx,'AsyncClient',lambda **kw:real(transport=httpx.MockTransport(respond),**kw))
    @asynccontextmanager
    async def slot():yield
    monkeypatch.setattr(gateway,'model_slot',slot)
    async def run():
        with gateway.observe_inference(events.append):return await gateway.complete('Source text','Rules')
    return run,payloads,events


def test_stream_assembles_response_and_only_emits_numeric_metrics(monkeypatch):
    run,payloads,events=stream_test(monkeypatch,[{'response':'{"facts":'}, {'response':'[]}', 'done':True,'done_reason':'stop','eval_count':7,'eval_duration':1000000000,'context':[42]}])
    assert asyncio.run(run())=='{"facts":[]}'
    assert payloads[0]['stream'] is True
    assert [e['stage'] for e in events]==['waiting','reading','generating','done']
    assert events[-1]['eval_count']==7 and 'context' not in events[-1]
    assert all('response' not in e and 'prompt' not in e for e in events)


@pytest.mark.parametrize('parts',[[{'response':'{"facts":[]}'}],[{'response':'{"facts":[]}','done':True,'done_reason':'length'}],[{'error':'private upstream error'}]])
def test_stream_errors_never_return_partial_success(monkeypatch,parts):
    run,_,events=stream_test(monkeypatch,parts)
    with pytest.raises(RuntimeError):asyncio.run(run())
    assert events[-1]['stage']=='failed'
    assert not any(e['stage']=='done' for e in events)
