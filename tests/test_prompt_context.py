import asyncio,json
from ai_analyzer.prompt_context import useful_links,compact_support
from ai_analyzer.learning import learning_context
from ai_analyzer import grounded


def test_action_links_take_priority_over_share_controls():
    links=[{'url':'https://x.com/intent/tweet?text='+'x'*600,'label':'Share'},
           {'url':'https://example.com/faucet','label':'faucet'},
           {'url':'https://example.com','label':'Website'}]
    assert [x['label'] for x in useful_links(links)]==['faucet','Website']


def test_non_english_source_gets_reading_demonstrations():
    assert learning_context('Тестнет: отримати тестові токени з крана')['examples'][0]['id']=='mixed-cost'
    assert learning_context('Тестнет: запросить тестовые токены в кране')['examples'][0]['id']=='mixed-cost'


def test_compacting_retains_source_and_corrections(monkeypatch):
    seen=[]
    async def fake(prompt,system):
        seen.append(json.loads(prompt));return '{"facts":[],"tasks":[]}'
    monkeypatch.setattr(grounded,'complete',fake)
    text='Testnet faucet source text must remain intact.'
    asyncio.run(grounded.analyze({'text':text,'url':'https://example.com','links':[]},['Keep the snapshot date']))
    assert seen[0]['untrusted_source_text']==text
    assert seen[0]['user_corrections']==['Keep the snapshot date']
    assert len(seen[0]['historical_analogies_for_review'])<=1
    assert len(seen[0]['historical_factor_questions']['factors_to_check'])<=3
