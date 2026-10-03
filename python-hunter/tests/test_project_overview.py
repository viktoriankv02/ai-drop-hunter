from ai_analyzer.grounded import validate_analysis
from core.workspace import Workspace
import pytest

def test_overview_rejects_fabricated_quote_and_retains_source():
 text='Alpha is a decentralized exchange for test assets.'
 valid=validate_analysis({'overview':{'brief':'Біржа тестових активів','quote':text}},text,'https://example.org',[])
 assert valid['overview']['source_url']=='https://example.org'
 assert 'overview' not in validate_analysis({'overview':{'brief':'Fake','quote':'Guaranteed reward for everyone.'}},text,'https://example.org',[])

def test_overview_cannot_change_project_choice_or_use_another_projects_evidence(tmp_path):
 w=Workspace(tmp_path/'db');w.initialize();pid,_=w.add_project('Alpha','https://cryptorank.io/alpha','CryptoRank')
 text='Alpha is a decentralized exchange for test assets.'
 sid,_=w.save_snapshot(pid,'https://cryptorank.io/alpha',{'text':text})
 w.save_overview(pid,sid,{'brief':'Біржа тестових активів','quote':text,'source_url':'https://cryptorank.io/alpha'})
 assert w.detail(pid)['overview']['brief']=='Біржа тестових активів'
 assert w.project(pid)['status']=='new'
 other,_=w.add_project('Beta','https://cryptorank.io/beta','CryptoRank')
 with pytest.raises(ValueError): w.save_overview(other,sid,{'brief':'Beta','quote':text})
 with pytest.raises(ValueError): w.save_overview(pid,sid,{'brief':'Alpha','quote':text,'source_url':'https://evil.example'})

def test_product_description_does_not_change_activity_screening(tmp_path):
 w=Workspace(tmp_path/'db');w.initialize();pid,_=w.add_project('Alpha','https://cryptorank.io/alpha','CryptoRank')
 w.save_snapshot(pid,'https://cryptorank.io/alpha',{'text':'Testnet faucet provides test tokens for the campaign.','truncated':False})
 before=w.project(pid)
 w.save_snapshot(pid,'https://example.org/docs',{'text':'The product supports mainnet trading.','truncated':True},via='product_description')
 assert w.detail(pid)['activity_screening']['decision']=='test_only'
 assert w.project(pid)['last_checked']==before['last_checked']
