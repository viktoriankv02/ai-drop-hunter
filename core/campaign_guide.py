"""Campaign guides retain evidence and never treat user completion as eligibility."""
import re
VERSION='campaign-guide-v1'

def validate_campaigns(value,text,source_url,links):
    allowed={source_url,*[x['url'] for x in links]};result=[]
    if not isinstance(value,list):return []
    for item in value[:20]:
        if not isinstance(item,dict):continue
        quote=item.get('quote','');title=item.get('title','')
        if not isinstance(quote,str) or len(quote)<15 or quote not in text or not isinstance(title,str) or not title:continue
        row={'title':title[:160],'quote':quote[:1200],'source_url':source_url,'status':'unknown','steps':[],'requires_user_review':True}
        # Explicit source phrases are displayed; no fabricated ISO dates or reward amounts.
        for field in ('period','reward','network','cost','time'):
            phrase=item.get(field)
            row[field]=phrase if isinstance(phrase,str) and phrase in quote else None
        status=item.get('status')
        if re.search(r'\b(?:not|no|не)\s+(?:yet\s+)?(?:open|live|active|ended|closed|completed)\b',quote,re.I):status='unknown'
        if status in ('active','ended','upcoming') and re.search({'active':r'open|live|active|открыт|відкрит','ended':r'ended|closed|completed|заверш','upcoming':r'planned|upcoming|scheduled|заплан|предваритель'}[status],quote,re.I):row['status']=status
        steps=item.get('steps',[])
        if not isinstance(steps,list):steps=[]
        for step in steps[:30]:
            if not isinstance(step,dict):continue
            proof=step.get('quote','');url=step.get('url')
            if not isinstance(proof,str) or len(proof)<15 or proof not in text or url not in allowed or not isinstance(step.get('title'),str):continue
            row['steps'].append({'title':step['title'][:300],'quote':proof[:1200],'url':url,'source_url':source_url,'requires_user_review':True})
        result.append(row)
    return result

def guide_for_project(report,tasks,project_url=None):
    report=report or {};campaigns=report.get('campaigns') or []
    if not campaigns and tasks:
        campaigns=[{'title':'План участі зі збережених джерел','status':'unknown','steps':[{'title':t['title'],'url':t.get('target_url'),'task_id':t['id'],'quote':__import__('json').loads(t.get('evidence_json') or '{}').get('quote',''),'source_url':__import__('json').loads(t.get('evidence_json') or '{}').get('source_url')} for t in tasks if t['status']!='legacy_unverified']}]
    campaigns=__import__('copy').deepcopy(campaigns)
    for campaign in campaigns:
        for step in campaign.get('steps',[]):
            match=next((t for t in tasks if t['title']==step['title'] and t.get('target_url')==step.get('url')),None)
            if match:
                step.update(task_id=match['id'],done=match['status']=='user_reported',evidence_state=match.get('evidence_state'))
            else:step['done']=False
        campaign['done']=sum(bool(x.get('done')) for x in campaign.get('steps',[]))
        campaign['total']=len(campaign.get('steps',[]))
    recommendations=list(report.get('recommendations',[]))
    for requirement in report.get('requirements',[]):
        if requirement.get('necessity')=='optional' and requirement.get('quote'):
            recommendations.append({'title':requirement['title'],'reason':'Додаткова дія в джерелі; вплив на розмір нагороди потребує окремого підтвердження.','url':requirement.get('url') or requirement.get('source_url') or project_url})
    if not recommendations and project_url:
        from core.participation import participation_plan
        recommendations=participation_plan(report,project_url)['suggestions']
    return {'version':VERSION,'campaigns':campaigns,'conflicts':report.get('conflicts',[]),'recommendations':recommendations,'unknowns':report.get('guide_unknowns',[])}
