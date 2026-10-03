import asyncio,json
from core.campaign_guide import validate_campaigns
from core.workspace import Workspace
from discovery.coordinator import Coordinator
import discovery.coordinator as module

def test_campaigns_keep_phases_evidence_and_reject_invented_fields():
 text='Beta is live until 31 October. Register your account before participation.'
 campaigns=validate_campaigns([{'title':'Beta','quote':'Beta is live until 31 October.','status':'active','period':'31 October','reward':'1000 tokens','steps':[{'title':'Register','quote':'Register your account before participation.','url':'https://example.org/register'},{'title':'Fake','quote':'Send money for guaranteed rewards.','url':'https://evil.example'}]}],text,'https://example.org',[{'url':'https://example.org/register'}])
 assert len(campaigns)==1 and len(campaigns[0]['steps'])==1
 assert campaigns[0]['status']=='active' and campaigns[0]['period']=='31 October'
 assert campaigns[0]['reward'] is None
 assert validate_campaigns([{'title':'Beta','quote':'Beta is not live yet.','status':'active','steps':{}}],'Beta is not live yet.','https://example.org',[])[0]['status']=='unknown'

def test_resources_work_when_aggregator_is_blocked_and_conflicts_survive(tmp_path,monkeypatch):
 w=Workspace(tmp_path/'db');w.initialize();pid,_=w.add_project('NamedChain','https://cryptorank.io/named-activity1','CryptoRank')
 w.add_resource(pid,'https://example.org/rules','Rules','reward_rules')
 async def reader(url,hosts):
  if 'cryptorank' in url:raise module.SourceUnavailable('HTTP 403')
  return '<main><p>Beta is live. Register your account before participation. Rewards are subject to eligibility and a separate claim period.</p></main>',url
 async def search(title):raise AssertionError('Registered source should be read before search')
 monkeypatch.setattr(module,'read_html',reader);monkeypatch.setattr(module,'search_public_sources',search)
 body,via=asyncio.run(Coordinator(w).read_project(w.project(pid)))
 assert body['documents'][0]['purpose']=='reward_rules' and body['truncated']
 assert w.rows('SELECT last_status FROM project_resources')[0]['last_status']=='read'
 sid,_=w.save_snapshot(pid,w.project(pid)['source_url'],body)
 conflict={'title':'Disagreement','detail':'Review required','sources':['https://example.org/rules']}
 w.save_report(pid,sid,{'conflicts':[conflict],'tasks':[]},'reviewed')
 w.save_report(pid,sid,{'tasks':[],'facts':[]},'model')
 assert w.detail(pid)['guide']['conflicts']==[conflict]

def test_campaign_step_completion_survives_updated_report(tmp_path):
 w=Workspace(tmp_path/'db');w.initialize();pid,_=w.add_project('Beta','https://cryptorank.io/beta','CryptoRank')
 text='Register for Beta and use test tokens.';sid,_=w.save_snapshot(pid,'https://cryptorank.io/beta',{'text':text})
 task={'title':'Register','quote':text,'url':'https://cryptorank.io/beta','source_url':'https://cryptorank.io/beta'}
 report={'tasks':[task],'campaigns':[{'title':'Beta','status':'active','steps':[task]}]}
 w.save_report(pid,sid,report,'fixture');tid=w.detail(pid)['tasks'][0]['id'];w.complete_task(tid,True)
 w.save_report(pid,sid,report,'updated')
 c=w.detail(pid)['guide']['campaigns'][0]
 assert c['done']==1 and c['steps'][0]['task_id']==tid


def test_incomplete_new_analysis_preserves_guide_with_review_notice(tmp_path):
 w=Workspace(tmp_path/'db');w.initialize();pid,_=w.add_project('Beta','https://cryptorank.io/beta','CryptoRank')
 sid,_=w.save_snapshot(pid,'https://cryptorank.io/beta',{'text':'Beta testnet is live for test participants.'})
 w.save_report(pid,sid,{'tasks':[],'campaigns':[{'title':'Beta','status':'active','steps':[]}]},'reviewed')
 w.save_report(pid,sid,{'tasks':[],'campaigns':[]},'incomplete_model')
 guide=w.detail(pid)['guide']['campaigns'][0]
 assert guide['retained_from_previous_review'] and guide['notice']

def test_project_specific_research_scope_does_not_enable_catalog(tmp_path):
 w=Workspace(tmp_path/'db');w.initialize()
 with w.db() as db:db.execute("UPDATE meta SET value='0' WHERE key='automatic_card_preparation'")
 pid,_=w.add_project('Chain','https://other.example/chain','Own')
 c=Coordinator(w);assert not c.project_research_allowed(w.project(pid))
 with w.db() as db:db.execute('INSERT INTO project_research_scope VALUES (?,1)',(pid,))
 assert c.project_research_allowed(w.project(pid))
 assert not any(x['url']=='https://other.example/chain' for x in w.sources())
 tg,_=w.add_project('Channel','https://t.me/s/unapprovedchannel','Telegram')
 with w.db() as db:db.execute('INSERT INTO project_research_scope VALUES (?,1)',(tg,))
 assert not c.project_research_allowed(w.project(tg))


def test_reader_prefers_article_body_over_parent_main_ads():
 from discovery.evidence import material
 html='<main><p>Other project pays fake rewards.</p><article><div class="entry-content"><p>NamedChain is a test network. Its own campaign instructions and eligibility must be checked independently. Use test tokens from its faucet.</p></div></article></main>'
 b=material(html,'https://example.org/chain')
 assert 'NamedChain' in b['text'] and 'Other project' not in b['text']
