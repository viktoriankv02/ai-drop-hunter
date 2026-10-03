"""Reuse exact product descriptions from saved source text; never infer from names."""
import sys,json,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace

def name_key(s): return re.sub(r"[^a-z0-9]","",s.lower())
w=Workspace();w.initialize();profiles={};count=0
for row in w.rows("SELECT p.id,p.title,s.id sid,s.url,s.body_json FROM projects p JOIN snapshots s ON s.project_id=p.id ORDER BY s.id DESC"):
    key=name_key(row['title'])
    if not key or key in profiles: continue
    body=json.loads(row['body_json']);text=body.get('text','')
    name=re.escape(row['title'].split(' (')[0])
    paragraphs=re.split(r'\n\s*\n',text)
    quote=next((x.strip() for x in paragraphs if 30<len(x.strip())<=700 and re.search(name+r"\s+(?:is|provides|offers|enables|brings|builds|combines|creates|connects)\b",x,re.I)),None)
    if not quote: continue
    source=body.get('url',row['url'])
    profiles[key]={'brief':quote,'quote':quote,'source_url':source}
    try:w.save_overview(row['id'],row['sid'],profiles[key]);count+=1
    except ValueError: profiles.pop(key,None)
for row in w.rows("SELECT id,title FROM projects WHERE status IN ('new','tracking')"):
    profile=profiles.get(name_key(row['title']))
    if not profile or w.rows('SELECT 1 FROM project_overviews WHERE project_id=?',(row['id'],)):continue
    sid,_=w.save_snapshot(row['id'],profile['source_url'],{'url':profile['source_url'],'text':profile['quote'],'truncated':True,'scope':'product_description_only'},via='product_description')
    w.save_overview(row['id'],sid,profile);count+=1
print(json.dumps({'saved_overviews':count,'unique_source_products':len(profiles)}))
