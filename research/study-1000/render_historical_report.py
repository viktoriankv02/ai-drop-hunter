"""Render the evidence-backed historical rewards report. No catalogue padding."""
import json,csv,hashlib,html,re
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
ROOT=Path(__file__).resolve().parent
LABELS={'issuer_reported_claims':'Емітент повідомив про claims','issuer_reported_distribution':'Емітент повідомив про розподіл','published_claim_analysis':'Опублікований аналіз claims','published_distribution_analysis':'Опублікований аналіз розподілу','genesis_distribution_documented':'Документований розподіл genesis','completed_program_reported':'Кампанію позначено завершеною','live_claim_program':'Підтверджено програму claim','allocation_or_rules_only':'Умови/алокація; виплати не доведені','earned_not_claimed':'Зароблене право, не підтверджені claims','sale_not_reward':'Продаж; порівняльний кейс'}
def build():
 data=json.loads((ROOT/'historical-rewards.json').read_text(encoding='utf-8'));cases=data['projects'];models=json.loads((ROOT/'claim-model-candidates.json').read_text(encoding='utf-8'));audit=json.loads((ROOT/'reward-source-audit.json').read_text(encoding='utf-8'))
 evaluation_path=ROOT/'historical-extraction-result.json';ev=json.loads(evaluation_path.read_text(encoding='utf-8')) if evaluation_path.exists() else {'passed':0,'total':0}
 examples=[json.loads(x) for x in (ROOT/'historical-extraction-examples.jsonl').read_text(encoding='utf-8').splitlines() if x]
 oldexamples=[json.loads(x) for x in (ROOT/'source-checked-examples.jsonl').read_text(encoding='utf-8').splitlines() if x]
 levels=Counter(x['payout_evidence_level'] for x in cases);years=Counter(x['reward_year'] for x in cases)
 stats={'as_of':datetime.now(timezone.utc).isoformat(),'schema_version':2,'window':data['window'],'target_unique_reward_projects':1000,'historical_project_dossiers':len(cases),'comparison_sale_cases':levels['sale_not_reward'],'dossiers_with_narrative_payout_or_claim_reports':sum(levels[x] for x in ('issuer_reported_claims','issuer_reported_distribution','published_claim_analysis','published_distribution_analysis','genesis_distribution_documented')),'fully_audited_cases':0,'onchain_claim_models_not_executed':len(models),'new_source_checked_extraction_examples':len(examples),'total_source_checked_extraction_examples':len(examples)+len(oldexamples),'new_direct_source_bodies':sum(s['status']=='fetched' for s in audit),'new_indexed_source_excerpts':sum(s['status']=='web_indexed_excerpt' for s in audit),'new_unusable_or_unavailable_sources':sum(s['status'] not in ('fetched','web_indexed_excerpt') for s in audit),'model_smoke_passed':ev['passed'],'model_smoke_total':ev['total'],'fine_tuning_performed':False,'study_1000_completed':False,'evidence_levels':dict(levels),'reward_years':dict(sorted(years.items()))}
 discovery=json.loads((ROOT/'historical-discovery-queue.json').read_text(encoding='utf-8'))
 expansion=json.loads((ROOT/'expansion-source-audit.json').read_text(encoding='utf-8'))
 extra_examples=[json.loads(x) for x in (ROOT/'expansion-extraction-examples.jsonl').read_text(encoding='utf-8').splitlines() if x]
 transfer_examples=[json.loads(x) for x in (ROOT/'agent-transfer-examples.jsonl').read_text(encoding='utf-8').splitlines() if x]
 learning=json.loads((ROOT/'agent-learning-evaluation.json').read_text(encoding='utf-8'))
 transfer=json.loads((ROOT/'agent-transfer-evaluation.json').read_text(encoding='utf-8'))
 stats['excluded_comparison_cases']=sum('excluded' in c.get('scope_status','') for c in cases)
 stats['current_operation_independently_verified_cases']=sum(c.get('current_operation_check')=='independently_verified' for c in cases)
 stats['agent_learning_scores']=learning['scores']
 stats['agent_transfer_scores']=transfer['scores']
 stats['research_lessons_in_model_prompt']=True
 stats['historical_analogies_in_model_prompt']=True
 stats['expansion_quotes_evaluated_with_subset_targets']=len(extra_examples)
 stats['total_source_checked_extraction_examples']=len(examples)+len(oldexamples)+len(extra_examples)+len(transfer_examples)
 stats.update(discovery_pages=discovery['count'],discovery_pages_fetched=discovery['successful_fetches'],expansion_source_urls=len(expansion),expansion_direct_texts=sum(x['status']=='fetched' for x in expansion))
 (ROOT/'coverage.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
 lines=['# Історичні криптороздачі: умови, виплати та дані для агентів','', 'Оновлено 01.10.2026; історичний зріз зафіксовано на 29.09.2026. Вікно винагород: 29.09.2018–29.09.2026. Ціль — 1000 унікальних проєктів. Дослідження ще не завершене.','',
 '## Результат поточного етапу','',f"Зібрано {len(cases)} поіменних досьє, включно з одним порівняльним кейсом продажу Sui. У {stats['dossiers_with_narrative_payout_or_claim_reports']} є повідомлення про розподіл/claims або документований genesis-розподіл. Це різні рівні доказів; вони не означають повного незалежного аудиту. Повністю перевірених досьє за всіма полями поки 0. 44 SQL-моделі claims збережено як джерела для відтворення, запити не виконані. Ці 44 моделі не додаються до поточного числа досьє як нові перевірені проєкти.",
 f"За новими джерелами збережено {stats['new_direct_source_bodies']} придатних текстів прямих відповідей і {stats['new_indexed_source_excerpts']} індексованих уривків. Для кожного доступного матеріалу є URL, спосіб доступу та хеш. Поточні тестнети із попереднього каталогу вилучено з цільового історичного звіту.",'',
 f"Окремо збережено {stats['discovery_pages']} сторінок-кандидатів архіву, з них {stats['discovery_pages_fetched']} завантажено. Це неперевірена черга: повторні сезони, продажі та події поза вікном не рахуються як нові проєкти. Для розширення досьє перевірено {stats['expansion_source_urls']} URL, збережено {stats['expansion_direct_texts']} текстів прямих відповідей.",'',
 f"Виключено з цілі чинних проєктів: {stats['excluded_comparison_cases']} порівняльні кейси (Sui — продаж; Crescent — офіційне рішення про sunset). Для решти поточну працездатність ще не підтверджено незалежно. Кількість досьє не є кількістю проєктів, що виконали всі критерії користувача.",'',
 '## Виправлена методика','',
 'У період має потрапляти подія винагороди, а не обов’язково перший запуск продукту. Тому ENS із запуском 2017 і роздачею 2021 придатний для історичного дослідження. Дата запуску, snapshot, відкриття claim, escrow, фактичне отримання та розблокування мають окремий зміст.',
 'Одиниця підрахунку — проєкт-емітент винагород. Сезони, переклади, назви токенів і кілька підтримуваних екосистем не створюють додаткові проєкти. Cosmos та Polygon у цьому звіті — також екосистемні напрями; їхні роздачі конкретизовано через Osmosis, Juno, Stride, Neutron, Stargaze, Celestia, Avail і Saga. Міграція MATIC→POL не прирівнюється до винагороди.',
 'Читаємо й історичні кампанії з депозитами/покупками: вони потрібні для вивчення умов і витрат. Це не змінює обмеження поточного пошуку на діяльність із тестовими токенами. Дослідження не виконує фінансових дій.',
 'Відсутність фінальної суми позначено невідомою, а не нулем. Claim-адреса не обов’язково одна людина. Алокація або успішний HTTP 200 не підтверджують виплату. Наявність сайту не доводить безперервну роботу мережі: актуальний uptime ще не перевірений для всіх проєктів.','',
 '## Що показують названі вами проєкти','',
 '| Напрям | Що вивчаємо | Важливе розрізнення |','|---|---|---|',
 '| Optimism | Історична активність, повторні тижні, голосування та внески | Частину OP доправили автоматично; це не самостійні claims усіх адрес. |',
 '| Arbitrum | Бальна система, активні місяці, транзакції/контракти й обсяги | Окремі критерії, штрафи та Sybil-виключення; одна дія не гарантує допуску. |',
 '| Arkham | Ранні користувачі й points; окремо біржові сезони | Понад $20 млн у Season 1 біржі не є сумою початкового airdrop 2023. |',
 '| Monad | Спільнота, розробники, onchain-активність, публічні блага | 70,4% — частка токенів, не відсоток унікальних людей чи гаманців. |',
 '| Plasma | Депозит, перевірка особи, продаж і бонус | Продані токени не є безкоштовною винагородою; резерв не є виконаною виплатою. |',
 '| Somnia | Тестнет, квести, внески, післязапускові завдання | 20% початково; решта за умовами, обов’язковий gas і добровільні платні бонуси. |',
 '| Cosmos | Stake, snapshots, валідатори, governance, міжмережеві когорти | Емітенти мають різні пороги, caps, виключення та способи перерозподілу. |',
 '| Polygon | Історичні Avail та Saga; Planet Mojo у черзі перевірки | Стейкінг, bridge та завершення кампанії потребують власних доказів. |','',
 'Посилання на першоджерела та точні межі висновків наведено в досьє нижче.','',
 '## Перерахунок Monad','',
 'CSV, опублікований проєктом: 76 021 рядок і стільки ж унікальних адрес; сума 3 330 583 396 MON; мінімум 1 500, медіана 12 000, середнє 43 811,36, максимум 12 197 000 MON. Середнє приблизно в 3,65 раза більше медіани: один показник «середня винагорода» погано описує типовий рядок цього списку. Це розрахунок за списком claims/алокацій, без незалежного відтворення всіх переказів і без витрат.',
 '[Офіційні результати](https://monad.xyz/blog/the-mon-airdrop-results) · [опублікований CSV](https://github.com/monad-crypto/airdrop-addresses) · локальні файли monad-allocation-audit.json та monad-csv-provenance.json.',
 'Не обчислюємо «відсоток людей, які отримали»: 289 тис. eligible accounts у зведенні та 76 021 унікальний claiming wallet не є гарантовано однаковими одиницями підрахунку.','',
 '## Поіменні досьє','',
 'У кожному досьє наведено перевірену частину правил, а не повний чекліст повторення історичної кампанії. Умови, опубліковані після snapshot, не можна використовувати як нібито відомі наперед.']
 for c in sorted(cases,key=lambda x:(x['reward_year'],x['project'])):
  lines+=['',f"### {c['project']} — {c['reward_year']}",'',f"**Умови.** {c['rules_summary']}",'',f"**Результат.** {c['payout_summary']}",f"Рівень доказів: {LABELS[c['payout_evidence_level']]}. Блокчейн-перекази повністю не відтворені.",'',f"**Для агента.** {c['agent_lesson']}",'', 'Ще перевірити: '+'; '.join(c['unknowns']), '', 'Джерела: '+ ' · '.join(f"[{i+1}]({s['url']})" for i,s in enumerate(c['sources']))]
 lines+=['','## Що змінювалося у вимогах','',
 'Це якісне порівняння наведених кейсів, а не доведений тренд у вибірці 1000. У поточному наборі немає перевірених подій 2018; завершення FlareDrops представляє 2026 рік; 2019 представлений неповним кейсом Stellar. Розподіл по роках нерівномірний.',
 '- **2020–2021:** історичне використання (Uniswap/1inch), доменна історія (ENS), genesis-роздачі стейкерам та завдання після запуску (Osmosis/Juno). Уже тоді діяли caps, decay та додаткові milestones.',
 '- **2022–2023:** кілька категорій і перетинів умов, часові метрики, governance та перевірки Sybil (Optimism/Arbitrum); Cosmos-програми додали власні правила валідаторів і перерозподілу (Stride).',
 '- **2024–2025:** у відібраних прикладах помітні рольові внески розробників/спільноти, сумісні екосистемні когорти, кілька фаз, умовні розблокування та відокремлення депозитних/продажних механік (Avail/Saga/Monad/Somnia/Plasma). Це не означає, що всі нові програми мають такі вимоги.','',
 '## Пріоритети навчання агентів','',
 '| Пріоритет | Навичка | Еталонні кейси | Що вважати помилкою |','|---|---|---|---|',
 '| P0 | Джерела та статус події | Plasma, Optimism, Monad | Назвати майбутній розподіл уже виконаним. |',
 '| P0 | Логіка AND/OR та пороги | Saga, Arbitrum, Starknet, 1inch | Замінити «>» на «≥», пропустити одну обов’язкову умову. |',
 '| P0 | Облік витрат | Somnia, Plasma, Sui | Назвати gas нульовим, продаж — винагородою, депозит — прибутком. |',
 '| P1 | Snapshot, claim, unlock, версії | Somnia, Stride, Avail, EigenLayer | Пропустити дедлайн або змішати правила фаз. |',
 '| P1 | Когорти та внесок | Monad, Celestia, Jito | Вважати число транзакцій універсальною формулою. |',
 '| P1 | Підрахунок одержувачів і сум | Monad, ENS, Pyth | Змішати токени, адреси, accounts і людей. |',
 '| P2 | Економічний результат | Усі після збору витрат | Рахувати прибуток за ціною ATH або без комісій. |','',
 'Модель має повертати: емітент/сезон; екосистема; категорія учасника; логічний вираз умов; пороги з одиницями; snapshot; claim window; vesting/обмеження; costs; allocated; claimed; delivered; as-of; URL; короткий доказ; невідомі поля. Для прибутку потрібні фактична ціна реалізації та витрати, яких у більшості досьє немає.',
 'Розділяти навчальну й контрольну вибірки за проєктом і часом. Сезони того самого емітента тримати разом. Правила, оприлюднені після snapshot, можна використовувати для навчання читанню документів, але не як вхід у прогноз із минулого. Наявна вибірка успішних/відомих проєктів має selection bias і не оцінює ймовірність майбутньої виплати.','',
 '## Навчання через досвід: що реально підключено','',
 'В агенті працюють дев’ять перевірених правил читання джерел: логіка І/АБО; окремі типи дат; алокація проти виплати; адреси проти людей; масштаб чисел; межі та приблизність; суперечності; історичні аналогії; витрати. Версія правил входить у ключ кешу. Зміна правил не повертає стару відповідь із кешу.',
 'Історичні аналогії тепер передаються моделі до генерації, а не тільки додаються після відповіді. Для них вказані проєкт, джерело і рівень доказів. Цитати у фактах поточної кампанії перевіряються тільки проти її власного тексту; чужа історична цитата не приймається.',
 'Це робота з інструкціями й контекстом агента. Ваги Qwen і ваги асистента не донавчались. Журнал досвіду зберігає помилки й виправлення, але не робить кожен запис правильною навчальною відповіддю.','',
 '## Реальні перевірки моделі','',
 f"Поточне парне порівняння на 13 регресійних уривках: baseline {learning['scores']['baseline']['passed']}/{learning['scores']['baseline']['total']}; уроки + типізовані поля {learning['scores']['lessons_typed']['passed']}/{learning['scores']['lessons_typed']['total']}.",
 'Після зміни інструкцій виправлено Saga (пропущена MATIC-гілка) та Arkham (числовий тип сезону й масштаб мільйонів). Залишився збій Flare: модель повернула null замість тривалості 36 місяців. Перший експеримент збережено у agent-learning-evaluation-v1.json; його помилки не приховані.',
 f"На шести нових уривках чотирьох інших проєктів: baseline {transfer['scores']['baseline']['passed']}/{transfer['scores']['baseline']['total']}; уроки + типи {transfer['scores']['lessons_typed']['passed']}/{transfer['scores']['lessons_typed']['total']}. Обидва варіанти помилились у реченні Spark про повернення невитребуваних SPK у treasury. Покращення узагальнення на цій маленькій перевірці не доведене.",
 'Порядок варіантів чергувався. В інструкції передавали лише назви та типи полів, без еталонних значень. Інструкції й типи змінювались разом, тому окремий внесок кожного не виміряно. Це по одному запуску на уривок, не статистичне підтвердження надійності.',
 f"Збережено {stats['total_source_checked_extraction_examples']} короткий приклад із джерелами. Старий тест 5/7 залишено історичним; нові результати записані окремо. Два нові інтеграційні тести та попередні тести застосунку: разом 63 passed, одна deprecation warning.",'',
 '## Перерахунок первинних списків алокацій','',
 'ParaSwap: 19 999 рядків і стільки ж унікальних адрес. Hop Protocol: 145 329 рядків і стільки ж унікальних адрес; нульових алокацій немає. Збережено вихідні файли, URL та SHA-256. Числа означають рядки опублікованих allocation lists, а не доведених одержувачів виплат.',
 'Перший Hop-файл був обрізаний лімітом 12 МБ. Перевірка виявила це; повний файл 13 435 870 байтів завантажено повторно. Сирі суми збережені як цілі base units; token decimals не припускались. Неповний файл не використаний для підсумкового перерахунку.',
 'Відтворення: audit_allocation_datasets.py. Додатково збережено індекс Rotki з 26 записами; це індекс джерел алокацій, а не 26 нових підтверджених проєктів.','',
 '## Аудит джерел і наступна черга','',
 'Dune Spellbook дає 44 окремі SQL-моделі claims. Збережено SQL, URL і SHA-256; виконання в Dune ще не зроблено. Статичну таблицю airdrop_info не використано для чисел: порядок її числових полів/аліасів вимагає окремої перевірки, а дата Arkham у ній відрізняється від фільтра конкретної моделі claims. Саме тому копіювання зведеного каталогу неприйнятне як перевірка виплат.',
 'Далі перевіряти поіменні джерела і працюючий продукт, фактичний розподіл, full eligibility, залишки, витрати та стан на дату зрізу. Знайдені тільки за моделями: '+', '.join(sorted({x['project_key'] for x in models}))+'.',
 'Публічний індекс airdrops.io вказує на великий архів, але сторінки sitemap у прямому доступі повернули помилки. Метадані каталогу та 1000 торгованих активів CryptoRank залишаються кандидатами, а не підтвердженою вибіркою. Не було запиту на оплату або нового обмеження дозволу користувача; прогалина — у перевірених даних.',
 'Окремі конкретні прогалини: фінальні SOMI-claims; повний первинний бонусний payout Plasma; початкова формула ARKM; genesis-підрахунки Cosmos; історичні події 2018–2019; актуальний стан продуктів, що реорганізувалися.','',
 '## Файли та відтворення','',
 f'- historical-rewards.json / historical-rewards.csv — {len(cases)} досьє з рівнями доказів і джерелами.',
 '- REPORT.html — зручний пошук за проєктом, роком, екосистемою та станом доказів.',
 '- reward-source-audit.json / reward-evidence — матеріали, індексовані уривки й журнал доступу.',
 '- claim-model-candidates.json / dune-models — 44 невиконані SQL-моделі.',
 '- historical-extraction-examples.jsonl / historical-extraction-result.json — новий набір і результат реального запуску.',
 '- monad-airdrop-results.csv / monad-allocation-audit.json — вихідний список та арифметичний аудит.',
 '- coverage.json / historical-validation.json — поточні лічильники та перевірки якості.',
 '', 'Відтворення: python research/study-1000/build_historical_rewards.py; python research/study-1000/render_historical_report.py; python research/study-1000/validate_historical_rewards.py. Повторний inference: python research/study-1000/evaluate_historical_rewards.py. Всі команди виконуються з кореня ai-hub-hunter-gemini.',
 '', '**Статус цілі 1000: не завершено.** Число 1000 є ціллю дослідження, а не поточним розміром перевіреної вибірки.']
 text='\n'.join(lines)+'\n';(ROOT/'REPORT.uk.md').write_text(text,encoding='utf-8')
 # Self-contained HTML: no network resources and no execution of source content.
 esc=html.escape;cards=[]
 for c in sorted(cases,key=lambda x:(-x['reward_year'],x['project'])):
  search=' '.join([c['project'],str(c['reward_year']),*c['ecosystems'],c['rules_summary'],LABELS[c['payout_evidence_level']]]).casefold()
  links=' · '.join(f'<a href="{esc(s["url"],quote=True)}" target="_blank" rel="noopener noreferrer">Джерело {i+1}</a>' for i,s in enumerate(c['sources']))
  cards.append(f'<article data-search="{esc(search,quote=True)}" data-year="{c["reward_year"]}" data-level="{c["payout_evidence_level"]}"><h2>{esc(c["project"])} <small>{c["reward_year"]}</small></h2><div class="tag">{esc(LABELS[c["payout_evidence_level"]])}</div><p><b>Умови.</b> {esc(c["rules_summary"])}</p><p><b>Результат.</b> {esc(c["payout_summary"])}</p><p><b>Для агента.</b> {esc(c["agent_lesson"])}</p><details><summary>Прогалини та джерела</summary><p>{esc("; ".join(c["unknowns"]))}</p><p>{links}</p></details></article>')
 options=''.join(f'<option value="{k}">{esc(LABELS[k])}</option>' for k in sorted(levels))
 page='''<!doctype html><html lang="uk"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Історичні роздачі — звіт</title><style>body{font:16px/1.6 system-ui,sans-serif;color:#172638;background:#f3f5f8;margin:0}main{max-width:1120px;margin:auto;padding:36px 24px}h1{font-size:34px;line-height:1.2}header p{max-width:900px}.metrics{display:flex;gap:16px;flex-wrap:wrap}.metric{padding:16px 24px;background:#fff;border:1px solid #cbd5e1;border-radius:12px}.metric b{display:block;font-size:30px}.filters{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#f3f5f8;padding:16px 0}input,select{font:inherit;padding:10px;border:1px solid #64748b;border-radius:6px}input{flex:1;min-width:200px}article{background:#fff;padding:24px;margin:16px 0;border:1px solid #cbd5e1;border-radius:12px}h2{margin-top:0}small{color:#64748b}.tag{font-size:14px;color:#164e63;background:#ecfeff;display:inline-block;padding:3px 10px;border-radius:20px}a{color:#174da3}summary{cursor:pointer;font-weight:600}article[hidden]{display:none}.notice{padding:14px 18px;border-left:4px solid #b45309;background:#fff7ed}.readmore{white-space:pre-wrap;font-size:14px}@media print{.filters{display:none}body{background:white}article{break-inside:avoid}details{display:block}}</style><main><header><p>AI HUNTER · ОНОВЛЕНО 01.10.2026</p><h1>Історичні роздачі<br>Умови, результати, уроки для агентів</h1><p class="notice">Ціль — 1000 унікальних проєктів за 29.09.2018–29.09.2026. Дослідження не завершене. Нижче — часткові досьє із зазначенням доказів; анонси та завершені кампанії не прирівняні до повного аудиту переказів.</p></header>'''
 page+=f'<div class="metrics"><div class="metric"><b>{len(cases)}</b>досьє, включно з {stats["excluded_comparison_cases"]} виключеними кейсами</div><div class="metric"><b>{len(models)}</b>SQL-моделі, ще не виконані</div><div class="metric"><b>{transfer["scores"]["lessons_typed"]["passed"]}/{transfer["scores"]["lessons_typed"]["total"]}</b>тест на нових уривках</div></div><p>Донавчання ваг не проводилося. <a href="REPORT.uk.md">Докладний текст звіту</a> · <a href="historical-rewards.csv">CSV</a> · <a href="historical-rewards.json">JSON</a> · <a href="CANDIDATES.html">Архівні кандидати: пошук</a> · <a href="RESEARCH-EXPERIENCE.uk.md">Досвід дослідження</a> · <a href="research-experience.jsonl">Журнал JSONL</a></p>'
 page+='<div class="filters"><input id="q" aria-label="Пошук" placeholder="Назва, Cosmos, Polygon, рік, вимога…"><select id="level" aria-label="Рівень доказів"><option value="">Усі рівні доказів</option>'+options+'</select></div><p id="count" aria-live="polite"></p>'+''.join(cards)
 page+='<details><summary>Повний текст звіту для друку</summary><div class="readmore">'+esc(text)+'</div></details><script>const q=document.querySelector("#q"),level=document.querySelector("#level"),cards=[...document.querySelectorAll("article")];function filter(){const text=q.value.toLocaleLowerCase().trim();let n=0;for(const c of cards){const visible=c.dataset.search.includes(text)&&(!level.value||c.dataset.level===level.value);c.hidden=!visible;if(visible)n++;}document.querySelector("#count").textContent=`Показано ${n} із ${cards.length} досьє`;}q.addEventListener("input",filter);level.addEventListener("change",filter);filter();</script></main></html>'
 (ROOT/'REPORT.html').write_text(page,encoding='utf-8')
 print(json.dumps(stats,ensure_ascii=True))
if __name__=='__main__':build()
