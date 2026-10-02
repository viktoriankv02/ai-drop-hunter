"""Append evidence-linked research observations; never invent missing action history."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
R=Path(__file__).resolve().parent
J=R/'research-experience.jsonl'
now=datetime.now(timezone.utc).isoformat()
existing=[json.loads(l) for l in J.read_text(encoding='utf-8').splitlines() if l] if J.exists() else []
ids={x['id'] for x in existing};new=[]
def emit(kind,action,result,evidence,lesson,status='observation_only',occurred=None):
 payload=dict(kind=kind,action=action,result=result,evidence_files=evidence,lesson=lesson,evidence_status=status)
 ident=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 if ident in ids:return
 ids.add(ident)
 new.append(dict(id=ident,recorded_at=now,observed_at=occurred,history_capture='reconstructed_from_saved_artifact',**payload,training_use='candidate_requires_review',fine_tuning_ready=False))
for p in sorted((R/'archive-evidence').glob('*.json')):
 d=json.loads(p.read_text(encoding='utf-8'))
 emit('source_acquisition',{'operation':'fetch_secondary_directory','url':d['source_url']},{'http_status':d.get('http_status'),'error':d.get('error'),'text_sha256':d.get('text_sha256')},[str(p.relative_to(R))],'Завантажена сторінка є джерелом-кандидатом; HTTP 200 не підтверджує виплату.',occurred=d.get('retrieved_at'))
for filename in ['reward-source-audit.json','expansion-source-audit.json']:
 for d in json.loads((R/filename).read_text(encoding='utf-8')):
  emit('source_acquisition',{'operation':'fetch_or_index_source','url':d['url']},{k:d.get(k) for k in ['status','http_status','error','content_sha256']},[filename]+([d['content_file']] if d.get('content_file') else []),'Невдалий прямий доступ не доводить відсутності факту; індексований уривок і повний текст мають різне покриття.',occurred=d.get('retrieved_at'))
lessons=[
('metadata_copy_error','Ethena / Spark','Під час копіювання шаблону Safe потрапив сторонній additional_reward_years=[2022].','Поле видалено; canonical files перезібрано з власних джерел.',['expansion-curated-10.json'],'Створювати досьє з порожньої схеми, не успадковувати факти іншого емітента.'),
('operating_status','Crescent','Історичний mainnet і claim існували, але це не доводить роботу зараз.','Офіційний sunset vote 15.02.2024; кейс виключений з цілі чинних проєктів.',['expansion-curated-12.json'],'Перевіряти життєвий цикл окремо від минулої роздачі.'),
('source_version_conflict','Evmos','Січнева модель містить 80 млн Rektdrop; квітнева інструкція 100 млн.','Обидві версії збережено, фінальний claimed total=null.',['expansion-curated-12.json'],'Порівнювати однакові категорії, дати та версії перед узгодженням чисел.'),
('date_type_confusion','Shardeum','23–28.10.2025 помилково названо вікном перевірки.','Це дати квесту; verification 02–14.12.2025, planned payout з 17.12.2025.',['expansion-curated-7.json'],'Зберігати окремі поля activity_window, verification_window, payout_start.'),
('source_conflict','Drift','Launch allocation: 100 млн проти 120 млн з бонусом.','Суперечність залишено відкритою; reported_amount=null.',['expansion-curated-1.json'],'Не вибирати число без узгодження версій і визначення бонусної частини.'),
('threshold_conflict','Grass','Документ використовує >500 і 500+.','Оператор позначено неоднозначним.',['expansion-curated-6.json'],'Непідтверджений оператор не перетворювати на навчальну істину.'),
('quantity_semantics','Sanctum','Сума запуску містить airdrop і LFG-компоненти.','Початковий airdrop 88 042 001 CLOUD записано окремо.',['expansion-curated-6.json'],'Класифікувати рух токенів перед підсумовуванням.'),
('time_cutoff','Sonic Labs','Дедлайн burn 15.10.2026 пізніше зрізу 29.09.2026.','Майбутнє спалення не зараховане як виконане.',['expansion-curated-6.json'],'Зберігати as_of та planned/occurred незалежно.'),
('unit_of_count','Flare','36 місячних розподілів.','Один проєкт із багатьма подіями.',['expansion-curated-6.json'],'Не збільшувати число емітентів кількістю сезонів.'),
('model_error','Saga','Модель пропустила MATIC-гілку умови OR.','Помилка збережена у результаті 5/7.',['historical-extraction-result.json'],'Перевіряти повноту всіх гілок, а не лише наявність правильної ETH-гілки.'),
('model_schema_error','Arkham','Сезон повернуто рядком замість числа.','Schema failure збережено окремо від змістової помилки.',['historical-extraction-result.json'],'Валідатор типів доповнює перевірку фактів.'),
('tool_failure','Browser validation','CUA runtime завершився до відкриття звіту.','Стару браузерну перевірку позначено непридатною для поточного звіту.',['report-browser-validation.json'],'Не видавати статичну перевірку HTML за візуальну перевірку.'),
('coverage_error','Study 1000','Архівні сторінки та часткові досьє не дорівнюють завершеній вибірці.','Лічильники кандидатів, досьє й доказів виплати розділено.',['coverage.json'],'Не зараховувати знайдені назви до досліджених емітентів.')]
for kind,project,before,after,evidence,lesson in lessons:
 emit(kind,{'operation':'review_and_correct','project':project,'observed_problem':before},{'resolution':after},evidence,lesson,'reviewed_lesson_not_training_certification')
for filename in ['historical-validation.json','expansion-extraction-validation.json']:
 emit('validation',{'operation':'validate_artifacts'},json.loads((R/filename).read_text(encoding='utf-8')),[filename],'Проходження перевірки цілісності не є перевіркою всіх фактів чи оцінкою моделі.')
# Model outcomes and file-integrity failures are retained, including unsuccessful variants.
for filename in ['agent-learning-evaluation-v1.json','agent-learning-evaluation.json','agent-transfer-evaluation.json']:
 path=R/filename
 if not path.exists():continue
 report=json.loads(path.read_text(encoding='utf-8'))
 for row in report.get('results',[]):
  emit('model_evaluation',{'operation':'local_inference','model':report.get('model'),'lesson_version':report.get('lesson_version'),'project':row['project'],'mode':row['mode']},row,[filename],'Зберігати невдалі відповіді та версію інструкцій; успіх на короткому уривку не доводить загальної надійності.',occurred=report.get('as_of'))
startup=R/'agent-learning-startup-error.json'
if startup.exists():emit('tool_failure',{'operation':'local_model_start'},json.loads(startup.read_text()),[startup.name],'Відокремлювати недоступність сервісу від помилок змісту відповіді.')
allocations=R/'allocation-datasets/provenance.json'
if allocations.exists():
 for row in json.loads(allocations.read_text()):
  emit('dataset_acquisition',{'operation':'download_allocation_dataset','url':row['url']},row,['allocation-datasets/provenance.json',row['file']],'Перевіряти повноту response та base units до підрахунку; allocation list не є claims.')
with J.open('a',encoding='utf-8') as f:
 for row in new:f.write(json.dumps(row,ensure_ascii=False)+'\n')
allrows=existing+new
for row in allrows:
 assert row['fine_tuning_ready'] is False
 for name in row['evidence_files']:assert (R/name).is_file(),name
summary=dict(as_of=now,total_records=len(allrows),added_records=len(new),kinds=dict(Counter(x['kind'] for x in allrows)),all_ids_unique=len({x['id'] for x in allrows})==len(allrows),fine_tuning_performed=False,history_complete=False,limitation='Historical records reconstructed only from saved artifacts; unrecorded searches, intermediate thoughts and actions were not invented.')
(R/'research-experience-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=True))
