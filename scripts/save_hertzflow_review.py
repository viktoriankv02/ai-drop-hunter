"""Save a source-reviewed result, explicitly separate from model-only output."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace
w=Workspace();pid=1446
body=json.loads(Path('data/hertzflow-article-check.json').read_text(encoding='utf-8'));url=body['url']
paragraphs=body['text'].split('\n\n')
get=lambda prefix:next(p for p in paragraphs if p.startswith(prefix))
q1=get('Вступаем в Discord');q2=get('После получения кода');overview=get('HertzFlow — это')
def step(title,quote):return {'title':title,'quote':quote,'url':url,'source_url':url,'requires_user_review':True}
steps=[step('Отримати інвайт: верифікація access-verify та заявка support-ticket у Discord.',q1),
       step('Ввести інвайт і підключити гаманець на сайті проєкту.',q2),
       step('Запросити тестові токени з крана; тестувати функції лише в тестнеті.',q2)]
report={'status':'partial','overview':{'brief':'HertzFlow — платформа торгівлі з гаманця. У збереженому гайді описане закрите бета-тестування за інвайтами з тестовими токенами.','quote':overview,'source_url':url},
 'facts':[],'tasks':steps,'requirements':[],
 'unknowns':['Стаття від 09.05.2026. Чинність інвайтів і доступність крана сьогодні не перевірені.','Точна винагорода, snapshot, строки claim та мінімальна кількість дій не підтверджені.','Це план тестнету. Торгівля реальними токенами до нього не входить.'],
 'coverage':{'complete':False,'processed_characters':len(body['text']),'retained_characters':len(body['text'])},
 'provenance':'Пряме читання Incrypted 06.10.2026 і ручна перевірка Codex. Не видається за самостійний результат Ollama.',
 'learning':{'fine_tuning_performed':False,'method':'source_reviewed_example'}}
# Retain model output independently, never silently relabel human review as inference.
model_path=Path('data/hertzflow-live-analysis.json')
if model_path.exists():report['model_comparison_available']=True
sid,_=w.save_snapshot(pid,url,{**body,'truncated':True,'provenance':report['provenance']},via='reviewed_article')
w.save_report(pid,sid,report,'codex-source-reviewed')
w.resource_checked(pid,url)
print(json.dumps({'project_id':pid,'snapshot_id':sid,'steps':len(steps),'url':'http://127.0.0.1:4318/?project=1446'}))
