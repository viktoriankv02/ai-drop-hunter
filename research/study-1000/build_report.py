"""Reproducible evidence inventory; never labels catalogue rows as launched projects."""
import csv, hashlib, json, re, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from core.workspace import Workspace
from core.historical_research import load_history
ROOT=Path(__file__).resolve().parent

def build():
    store=Workspace(); history=load_history()
    projects=[p for p in store.rows('SELECT id,title,source_url,source_platform FROM projects ORDER BY id') if urlsplit(p['source_url']).hostname in ('cryptorank.io','incrypted.com')]
    launch_path=ROOT/'verified-launches.json'
    launches=json.loads(launch_path.read_text(encoding='utf-8')) if launch_path.exists() else []
    source_path=ROOT/'source-audit.json'
    source_audit=json.loads(source_path.read_text(encoding='utf-8')) if source_path.exists() else []
    example_path=ROOT/'source-checked-examples.jsonl'
    examples=[json.loads(x) for x in example_path.read_text(encoding='utf-8').splitlines() if x] if example_path.exists() else []
    rows=[]; names=Counter(re.sub(r'\s+',' ',p['title']).strip().casefold() for p in projects)
    for p in projects:
        snaps=store.rows('SELECT via FROM snapshots WHERE project_id=?',(p['id'],))
        key=re.sub(r'\s+',' ',p['title']).strip().casefold()
        rows.append({**p,'identity_status':'needs_entity_review','same_name_rows':names[key],
            'snapshot_count':len(snaps),'launch_status':'unknown','launch_date':'','launch_evidence_url':'',
            'eligibility_status':'unverified','payout_status':'unknown','training_eligible':False,
            'research_status':'material_available' if snaps else 'catalogue_only'})
    with (ROOT/'candidate-inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    dossiers=[]
    for c in history['cases']:
        dossiers.append({**c,'evidence_review_status':c.get('source_audit_status','prior_local_research_not_reverified_in_this_run'),'training_eligible':False,
                         'exclusion_from_training_reason':'Full case and claim-level source verification pending'})
    (ROOT/'historical-dossiers.json').write_text(json.dumps(dossiers,ensure_ascii=False,indent=2),encoding='utf-8')
    current=[]
    for pid in (1428,1429,1007,1463,1413):
        d=store.detail(pid)
        current.append({'project':d['title'],'source_url':d['source_url'],'screening':d['activity_screening'],
                        'note':d['reviewed_note'],'training_eligible':False,'current_operation_verified':False})
    (ROOT/'recent-campaigns.json').write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf-8')
    metrics={'as_of':datetime.now(timezone.utc).isoformat(),'target_verified_launched_projects':1000,
             'catalogue_rows':len(rows),'normalized_names_not_verified_entities':len(names),
             'rows_with_material':sum(r['snapshot_count']>0 for r in rows),
             'historical_partial_cases':history['partial_cases'],'historical_complete_cases':history['fully_reviewed'],
             'verified_training_examples':0,'source_checked_extraction_examples':len(examples),
             'official_sources_fetched':sum(a['status']=='fetched' for a in source_audit),
             'verified_launches_within_window':sum(a['in_eight_year_window'] for a in launches),'recent_campaigns_reviewed_as_aggregator_notes':len(current)}
    (ROOT/'coverage.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Дослідження 1000 запущених проєктів — аудит і попередній звіт',
      '', 'Зріз: 28.09.2026. Статус: НЕ ЗАВЕРШЕНО. Це не звіт про 1000 перевірених проєктів.', '',
      '## 1. Що фактично є в даних', '',
      f"У дозволених каталогах {len(rows)} записів, {len(names)} нормалізованих назв і {metrics['rows_with_material']} карток зі збереженим матеріалом. Нормалізація назви не доводить унікальність проєкту. Запуск і виплати з цього не випливають.",
      f"Історичні досьє: {history['partial_cases']} часткових, {history['fully_reviewed']} завершених. Перевірених прикладів для навчання: 0. Мета 1000 ще не досягнута.", '',
      '## 2. Визначення та відбір', '',
      'Вікно цільового звіту: 28.09.2018–28.09.2026. Для блокчейну запуск означає production/mainnet; для протоколу — публічний робочий продукт. TGE, testnet, лістинг і запуск продукту зберігаються окремо. Кожній даті потрібне першоджерело. Старий файл історії має зріз на день раніше — його збережено без переписування фактів.',
      'Одиниця підрахунку — проєкт зі сталою ідентичністю; сезони, мови сторінки та ребрендинги не збільшують лічильник. Автоматично однакові назви не об’єднуємо. Вибірка повинна охоплювати роки, категорії, мережі й негативні результати. До верифікації запуску каталог залишається чергою кандидатів.',
      'Вимоги до історичного кейсу: запуск; версія правил; категорія учасника; логіка AND/OR; пороги з одиницями; snapshot; claim/deadline; географія/KYC; критерії виключення; витрати; алокація; отримані виплати; дата зрізу; джерела й невідомі дані. Невідоме не дорівнює нулю.', '',
      '## 3. Історичні досьє: наявні висновки та прогалини', '',
      'Наведені нижче висновки перенесено з попередньої локальної роботи. Для частини досьє офіційні матеріали вже прочитано повторно; конкретні перевірені твердження наведено окремо. Повнота кожного досьє все ще обмежена.', '']
    for c in dossiers:
        lines += [f"### {c['project']}",c['finding'],'',f"Висновок для агента: {c['product_lesson']}",'']
        for r in c.get('criteria',[]):lines.append(f"- {r['cohort']}: {r['requirement']} ([джерело]({r['source_url']})).")
        lines += ['', 'Прогалини: '+ '; '.join(c['missing_evidence'])+'.',
                  'Джерела: '+', '.join(f"[{x['title']}]({x['url']})" for x in c['sources']), '']
    lines += ['## 4. Вимоги в нещодавно перевірених кампаніях', '',
      'Це п’ять відібраних кандидатів, а не репрезентативна вибірка останніх кампаній. Порівняння не дає частот вимог по ринку або ймовірності винагороди. Джерела — індексовані копії агрегаторів.']
    for c in current:
        lines += ['',f"### {c['project']}",f"[Картка джерела]({c['source_url']})"]
        lines += ['- '+f['title'] for f in c['note']['facts']]
        lines += ['Невідоме: '+'; '.join(c['note'].get('unknowns',[]))]
    lines += ['', '## 5. На чому робити акцент зараз', '',
      'Це інженерні пріоритети за виявленими прогалинами, а не статистично доведена стратегія заробітку.',
      '1. Перевірка мережі й активів до формування плану: testnet, faucet, тестовий токен, можливість пройти без купівлі чи депозиту.',
      '2. Календар і версії умов: snapshot, крайній строк, активні дні/тижні/місяці, зміна сезону. Не переносити старі вимоги на новий проєкт.',
      '3. Логічні правила за ролями: усі умови чи альтернативи; користувач, розробник, валідатор, учасник спільноти.',
      '4. Відокремлення points, eligibility, allocation, claim і фактичного прибутку після витрат.',
      '5. Якісні внески і соціальні завдання фіксувати як окремі категорії; не вважати їх гарантією виплати.',
      '6. Відмова від висновку за браку доказів. Не оптимізувати штучний обсяг чи масове створення адрес.', '',
      '## 6. Дані для навчання та оцінювання', '',
      'historical-dossiers.json і recent-campaigns.json — дослідницькі дані; training_eligible=false. До навчального набору включати лише перевірені твердження з URL, датою документа, короткою цитатою, хешем матеріалу й незалежним переглядом. Не перетворювати згенеровані звіти агента на еталон автоматично.',
      'Розділяти train/validation/test за проєктом і часом. Різні сезони, переклади й майже однакові тексти одного проєкту мають залишатися в одному split. Правила, оприлюднені після snapshot, заборонені як вхідні дані для історичного прогнозу.',
      'Оцінювати окремо: точність цитат; precision/recall умов; точність порогів і AND/OR; дедлайни; розпізнавання реальних витрат; правильну відмову; відмінність алокації та виплати. Нуль вигаданих URL/винагород на контрольному наборі — вимога, не поточний результат.',
      'evaluation-spec.json містить синтетичні сценарії перевірки логіки. Це не історичні факти, не виконаний benchmark і не доказ покращення Ollama.', '',
      '## 7. Що заважає завершенню 1000 досьє', '',
      'Потрібні доступні матеріали про запуск, правила та результати для кожного проєкту. Поточний API-каталог дає назви, а не повні завдання. У CryptoRank частина полів вимагає входу; HTTP-доступ раніше повертав 403. За допомогою лише назв ці прогалини не заповнити.',
      'Попереднє обмеження користувача — лише CryptoRank та Incrypted. 28.09.2026 користувач дозволив офіційні документи й відкриті дані про виплати. Дозвіл збережено у research-authorization.json. Інші каталоги автоматичного пошуку залишаються вимкненими.',
      'Критерій готовності: 1000 унікальних підтверджених запусків з досьє, аудитом джерел, видимими невідомими полями та окремим аналізом сучасних кампаній. Відсутність винагороди допускається як задокументований результат, а не вигадана нульова виплата.', '',
      '## 8. Файли та відтворення','',
      '- candidate-inventory.csv — усі кандидати, а не штучно обрізані 1000.',
      '- historical-dossiers.json — 15 часткових досьє.',
      '- recent-campaigns.json — п’ять сучасних кандидатів із застереженнями.',
      '- coverage.json — точні лічильники покриття.',
      '- evaluation-spec.json — синтетичні контрольні сценарії.',
      'Відтворення: .venv/Scripts/python.exe research/study-1000/build_report.py. Скрипт читає робочу базу, але не змінює картки чи статуси.', '']
    lines += ['## 9. Перевірка офіційних джерел після дозволу', '',
      f"Пряме читання: {sum(a['status']=='fetched' for a in source_audit)} документів; невдалі спроби: {sum(a['status']=='unavailable' for a in source_audit)}; окремо індексовані уривки: {sum(a['status']=='indexed_excerpt' for a in source_audit)}.",
      f"Перевірених дат запуску: {len(launches)}; у восьмирічному вікні: {sum(a['in_eight_year_window'] for a in launches)}. Це окремий показник, не кількість завершених досьє.", '',
      '| Проєкт | Запуск | У цільовому вікні | Доказ |', '|---|---|---|---|']
    for x in launches:
        lines.append(f"| {x['project']} | {x['launch_date']} | {'так' if x['in_eight_year_window'] else 'ні — лише історична довідка'} | [офіційне джерело]({x['source_url']}) |")
    lines += ['', '### Суперечність Note Systems',
      'CryptoRank описує конвертацію тестнет-поінтів. Доступна офіційна сторінка прямо заперечує конвертацію й доступний claim. Висновок: не обіцяти токени за тестнет на підставі агрегатора. Офіційна сторінка прочитана через web-інструмент; прямий HTTP повернув 403. Версію на час початкового анонсу не відновлено.',
      '[Офіційні правила](https://note.systems/community/) · [Агрегатор](https://cryptorank.io/drophunting/note-systems-activity1309)', '',
      '### Перевірені уривки для підготовки агентів',
      f"Створено {len(examples)} прикладів вилучення фактів із точним уривком, джерелом, часом читання та хешем. Це один прохід перевірки, не незалежний подвійний аудит. Вони не доводять прогнозної здатності агентів; fine-tuning не запускався.",
      'Файл: source-checked-examples.jsonl. Дев’ять проєктів development, три — test; проєкти між групами не перетинаються. Контрольний набір дуже малий і ще не містить усіх типів помилок.', '']
    for x in examples:
        lines.append(f"- **{x['project']}**: `{json.dumps(x['expected_extraction'],ensure_ascii=False)}` — [джерело]({x['source_url']}).")
    evaluation_path=ROOT/'extraction-smoke-result.json'
    if evaluation_path.exists():
        evaluation=json.loads(evaluation_path.read_text(encoding='utf-8'))
        lines += ['', '## 10. Фактична перевірка локального агента',
          f"Модель {evaluation['model']}: {evaluation['passed']}/{evaluation['total']} точних структурованих відповідей на коротких відкладених уривках. Ваги моделі не змінювалися. Це не оцінка якості на 1000 проєктах.",
          'ENS: правильно вилучено округлені суми claims та кількість адрес. Note Systems: правильно розпізнано відсутність конвертації та claim тестнет-поінтів. Sui: правильно визначено покупку токенів, але на запитання, чи доведено безкоштовний дроп, повернуто null замість очікуваного false. Це помилка виконання схеми; модель не вигадала безкоштовну винагороду.',
          'Потрібно окремо перевіряти тип поля: «винагорода невідома» → null; «чи доведена винагорода» → false за браку доказів. Перед розширенням оцінки переглянути формулювання й еталон незалежно.',
          'Результати: extraction-smoke-result.json. Код запуску: evaluate_extraction.py.']
    feasibility_path=ROOT/'api-feasibility-audit.json'
    if feasibility_path.exists():
        feasibility=json.loads(feasibility_path.read_text(encoding='utf-8'))
        lines += ['', '## 11. Чому масовий каталог не завершує це дослідження',
          f"CryptoRank API повернув {feasibility['map_records']} активів у map і {feasibility['traded_sample_records']} торгованих активів у контрольній вибірці. Ці записи не зараховано до 1000 досліджених проєктів.",
          'У доступній відповіді детального endpoint для Uniswap відсутні дата запуску, офіційні посилання й вимоги винагород. createdAt — не доказ запуску. Автоматичне зарахування цієї тисячі дало б неправильну відповідь на поставлене питання.',
          'Статус запиту: не виконано повністю. Не завершено перевірку 1000 запусків і 1000 досьє. Цей файл містить фактичні результати поточного дослідження; використовувати його як статистичний звіт за вибіркою 1000 заборонено.',
          'Для продовження потрібне поіменне доповнення первинними матеріалами й перевірка тверджень. Прямий доступ обмежений для частини джерел; індексовані копії позначено окремо. Фонове дослідження після завершення відповіді не запущено.']
    (ROOT/'REPORT.uk.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(metrics,ensure_ascii=False))
if __name__=='__main__':
    from render_historical_report import build as render_current_report
    render_current_report()
