"""Populate every tracked card with source candidates, retaining uncertainty and audit trail."""
import sys,json,asyncio,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace,utcnow
from core.participation import extract_source_requirements,VERSION
from discovery.coordinator import Coordinator
async def main():
    w=Workspace();root=Path('data');audit=[]
    with w.db() as conn:
        backup=sqlite3.connect(root/'participation-before.sqlite');conn.backup(backup);backup.close()
    for p in w.rows("SELECT * FROM projects WHERE status='tracking' ORDER BY id"):
        snapshots=w.rows("SELECT * FROM snapshots WHERE project_id=? AND via!='reviewed_research_note' ORDER BY id DESC LIMIT 1",(p['id'],))
        try:
            if snapshots:
                snapshot=snapshots[0];body=json.loads(snapshot['body_json']);sid=snapshot['id'];fresh=False
            else:
                body,via=await Coordinator(w).read_project(p)
                sid,_=w.save_snapshot(p['id'],p['source_url'],body,via=via);fresh=True
            body.setdefault('url',p['source_url'])
            old=w.rows('SELECT body_json FROM reports WHERE project_id=? ORDER BY id DESC LIMIT 1',(p['id'],))
            report=json.loads(old[0]['body_json']) if old else {'facts':[],'tasks':[],'unknowns':[]}
            requirements=extract_source_requirements(body)
            report.update(requirements=requirements,participation_version=VERSION,status='partial',
                coverage={'processed_characters':len(body.get('text','')),'retained_characters':len(body.get('text','')),'complete':False,'method':'source_candidate_extraction_not_semantic_audit'},
                extraction_method='source_candidate_extraction',errors=[])
            report.setdefault('unknowns',[]).append('Автоматично знайдені уривки потребують агентського й офіційного підтвердження; це не повний аудит умов.')
            Coordinator.attach_provenance(report,body)
            w.save_report(p['id'],sid,report,'source-candidate-extractor-v1')
            row={'id':p['id'],'project':p['title'],'requirements':len(requirements),'fresh_read':fresh,'status':'candidate_draft'}
        except Exception as e:
            w.check_failed(p['id'],str(e)[:600]);row={'id':p['id'],'project':p['title'],'status':'source_unavailable','error':str(e)[:400]}
        audit.append(row);(root/'participation-backfill.json').write_text(json.dumps({'created_at':utcnow(),'projects':audit},ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(row,ensure_ascii=True),flush=True)
asyncio.run(main())
