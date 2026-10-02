from ai_analyzer.grounded import validate_analysis
from core.participation import participation_plan
from discovery.coordinator import Coordinator

def test_requirements_require_exact_evidence_and_quoted_thresholds():
    text='You must register before 30 October and earn 100 points.'
    result=validate_analysis({'requirements':[{'title':'Register','quote':text,'category':'registration','necessity':'required','deadline':'30 October','threshold':'999 points','url':'https://evil.example'},{'title':'Fake','quote':'Claim guaranteed rewards for everyone.'}]},text,'https://example.org',[])
    assert len(result['requirements'])==1
    item=result['requirements'][0]
    assert item['deadline']=='30 October' and item['threshold'] is None
    assert 'url' not in item and item['requires_user_review']

def test_legacy_actions_and_suggestions_never_guarantee_rewards():
    plan=participation_plan({'tasks':[{'title':'Faucet','quote':'Use the testnet faucet for test tokens.','url':'https://example.org'}]},'https://example.org')
    assert plan['requirements'][0]['necessity']=='unknown'
    assert plan['guaranteed_reward'] is False
    assert all(x['reward_effect']=='unknown' for x in plan['suggestions'])
    assert plan['missing']

def test_product_docs_do_not_become_reward_requirements():
    quote='You must connect a wallet to use the product.'
    result={'requirements':[{'title':'Connect','quote':quote,'necessity':'required'}]}
    Coordinator.attach_provenance(result,{'provenance':'Reference docs','documents':[{'url':'https://example.org/docs','text':quote,'purpose':'product_manual'}]})
    assert result['requirements'][0]['necessity']=='unknown'
    assert result['requirements'][0]['source_url']=='https://example.org/docs'
