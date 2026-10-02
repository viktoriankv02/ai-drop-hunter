"""Mechanical archive screening. Directory statements are not verified facts."""
import json,re,csv,html,hashlib
from pathlib import Path
from datetime import datetime
R=Path(__file__).resolve().parent
cases=json.loads((R/'historical-rewards.json').read_text(encoding='utf-8'))['projects']
norm=lambda s:re.sub(r'[^a-z0-9]','',s.casefold())
known={norm(x['project']):x['project'] for x in cases}
rows=[]
for p in sorted((R/'archive-evidence').glob('*.json')):
 d=json.loads(p.read_text(encoding='utf-8'));t=d.get('text','');lines=t.splitlines()
 if t:assert hashlib.sha256(t.encode()).hexdigest()==d['text_sha256']
 name=lines[0].split(' | ')[0] if lines else d['slug']
 dates=[x for x in lines[:40] if re.fullmatch(r'[A-Z][a-z]{2} \d{1,2}, \d{4}',x)]
 date=datetime.strptime(dates[0],'%b %d, %Y').date().isoformat() if dates else None
 flag='unknown' if not date else ('inside_window_date_type_unverified' if '2018-09-29'<=date<='2026-09-29' else 'outside_window_catalog_date_only')
 values=lambda label:list(dict.fromkeys(lines[i+1] for i,x in enumerate(lines[:-1]) if x==label))
 links=[u for u in d.get('external_links',[]) if not any(x in u for x in ['coinmarketcap.com','coingecko.com','creativecommons.org','github.com/i-shivamsoni'])]
 row=dict(name=name,slug=d['slug'],catalog_date=date,date_screen=flag,catalog_status=next((x for x in lines[:40] if x in ('Alive','Dead')),'unknown'),catalog_allocation=values('Total Airdrop Amount'),catalog_eligible=values('Number of Eligible Users'),catalog_claimants=values('Number of Claimants'),possible_curated_match=known.get(norm(name)) or known.get(norm(d['slug'])),source_url=d['source_url'],source_file=str(p.relative_to(R)),source_text_sha256=d.get('text_sha256'),outbound_links_to_review=links,verification_status='unverified_secondary_directory',fine_tuning_eligible=False)
 rows.append(row)
out={'as_of':'2026-09-29','unit':'directory_pages_not_unique_verified_issuers','license':'Archive credits Shivam Soni, CC BY 4.0; extracted fields normalized without independent verification.','source':'https://airdroparchive.com/','rows':rows}
(R/'archive-screening.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (R/'archive-screening.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader()
 for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in row.items()})
e=html.escape
page='<!doctype html><html lang="uk"><meta charset="utf-8"><title>Архівні кандидати</title><style>body{font:16px system-ui;margin:32px;color:#172638}table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #ddd;text-align:left}input{padding:12px;width:60%}small{display:block;color:#666}</style><h1>389 архівних сторінок-кандидатів</h1><p>Це автоматично витягнуті твердження вторинного каталогу. Не 389 перевірених проєктів: потрібні першоджерела, перевірка виплат, дати й об’єднання сезонів.</p><p><a href="REPORT.html">Основний звіт</a> · <a href="archive-screening.csv">CSV</a> · <a href="archive-screening.json">JSON</a></p><p>Джерело: <a href="https://airdroparchive.com/">Crypto Airdrop Archive</a>, Shivam Soni, CC BY 4.0. Дані структуровано, точність не підтверджено.</p><input id="q" placeholder="Пошук назви або дати" aria-label="Пошук"><p id="count"></p><table><thead><tr><th>Кандидат</th><th>Дата каталогу</th><th>Статус каталогу</th><th>Заявлені claimants</th><th>Джерела</th></tr></thead><tbody>'
for x in rows:
 page+=f'<tr><td>{e(x["name"])}<small>{e(x["possible_curated_match"] or "Досьє не зіставлено")}</small></td><td>{e(x["catalog_date"] or "Невідомо")}<small>{e(x["date_screen"])}</small></td><td>{e(x["catalog_status"])}</td><td>{e("; ".join(x["catalog_claimants"]) or "Невідомо")}</td><td><a href="{e(x["source_url"],quote=True)}">Каталог</a><small>{len(x["outbound_links_to_review"])} посилань для перевірки в JSON</small></td></tr>'
page+='</tbody></table><script>const rows=[...document.querySelectorAll("tbody tr")],q=document.querySelector("#q");function f(){let n=0;for(const r of rows){r.hidden=!r.textContent.toLowerCase().includes(q.value.toLowerCase());if(!r.hidden)n++}document.querySelector("#count").textContent=`Показано ${n} із ${rows.length}`;}q.addEventListener("input",f);f();</script></html>'
(R/'CANDIDATES.html').write_text(page,encoding='utf-8')
from collections import Counter
print(json.dumps({'pages':len(rows),'date_screen':dict(Counter(x['date_screen'] for x in rows)),'catalog_status':dict(Counter(x['catalog_status'] for x in rows)),'name_matches_only':sum(bool(x['possible_curated_match']) for x in rows),'unique_projects_verified_by_this_script':0}))
