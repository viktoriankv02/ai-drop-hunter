"""Evidence-backed participation plans. Suggestions never become reward eligibility."""
import re
VERSION = 'participation-v1'
CATEGORIES = {'eligibility','activity','threshold','deadline','registration','verification','claim','unlock','cost','reward','other'}
NECESSITIES = {'required','optional','unknown'}

def requirement_fields(item):
    quote = item['quote']
    return {
        'category': item.get('category') if item.get('category') in CATEGORIES else 'other',
        'necessity': item.get('necessity') if item.get('necessity') in NECESSITIES else 'unknown',
        'threshold': item.get('threshold') if isinstance(item.get('threshold'),str) and item['threshold'] in quote else None,
        'deadline': item.get('deadline') if isinstance(item.get('deadline'),str) and item['deadline'] in quote else None,
        'evidence_status': 'source_matched_draft',
        'requires_user_review': True,
    }

def participation_plan(report, project_url):
    report = report or {}
    items = list(report.get('requirements', []))
    # Existing reports remain usable; their task statements are not promoted to mandatory rules.
    for task in report.get('tasks', []):
        if task.get('quote') and not any(x.get('quote') == task['quote'] for x in items):
            items.append({**task, **requirement_fields(task)})
    known = {x.get('category') for x in items if x.get('evidence_status') not in {'source_matched_candidate','platform_reference_not_reward_rule'}}
    missing = [('eligibility','Хто має право на участь та які є виключення'),
               ('deadline','Дати активності, snapshot, реєстрації та claim'),
               ('cost','Тестові чи реальні токени, комісії та інші витрати'),
               ('reward','Що саме обіцяно та як визначається розмір винагороди'),
               ('verification','Потрібні перевірки облікового запису або особи'),
               ('unlock','Умови розблокування й отримання всієї винагороди')]
    gaps = [{'category': key, 'title': text} for key,text in missing if key not in known]
    suggestions = []
    current_text = ' '.join(x.get('quote','') for x in items).lower()
    if re.search(r'testnet|тестнет|test token|тестов', current_text):
        suggestions.append({'title':'Перевірити нові функції тестнету та надіслати відтворюваний звіт про помилку',
            'reason':'Корисний внесок у тестування продукту; зарахування до нагороди потрібно підтвердити.', 'url': project_url})
    suggestions.extend([
        {'title':'Перевірити офіційні додаткові квести або програму внесків',
         'reason':'Може існувати окрема бонусна гілка; її наявність і правила ще потрібно знайти.', 'url':project_url},
        {'title':'Перевірити зарахування дій і зберегти докази участі',
         'reason':'Зберегти transaction hash, дату та статус квесту; це допоможе помітити пропущені умови.', 'url':project_url},
    ])
    for item in suggestions:
        item.update(status='proposal_not_reward_requirement',reward_effect='unknown',requires_user_review=True)
    return {'version':VERSION,'requirements':items,'suggestions':suggestions,'missing':gaps,
            'coverage':report.get('coverage',{}),'guaranteed_reward':False,
            'notice':'Пункти звірені з текстом джерела та потребують перегляду. Додаткові пропозиції мають невідомий вплив на винагороду.'}


def extract_source_requirements(body):
    """Transparent candidate extraction; never an assertion of official eligibility."""
    patterns = {
        'deadline': r'\b(snapshot|deadline|before|ends?|until|claim period)\b|дедлайн|до .*20\d\d',
        'eligibility': r'\b(eligible|eligibility|qualify|sybil|excluded|restricted)\b',
        'verification': r'\b(kyc|verify|verification|identity)\b',
        'threshold': r'\b(minimum|at least|threshold)\b',
        'registration': r'\b(register|registration|sign up|join|connect wallet)\b',
        'claim': r'\bclaim\b',
        'unlock': r'\b(vesting|unlock|milestone)\b',
        'cost': r'\b(fee|gas|deposit|test tokens|testnet tokens|faucet)\b',
        'reward': r'\b(reward|airdrop|allocation|distribution|points)\b',
        'activity': r'\b(complete|stake|swap|bridge|quest|task|feedback|mint|testnet)\b',
    }
    items=[];seen=set()
    for paragraph in re.split(r'\n\s*\n|\n',body.get('text','')):
        quote=paragraph.strip()
        if len(quote)<20 or len(quote)>1200 or quote in seen: continue
        category=next((key for key,pat in patterns.items() if re.search(pat,quote,re.I)),None)
        if not category: continue
        seen.add(quote)
        items.append({'title':quote[:160], 'quote':quote,'source_url':body['url'],
            'category':category,'necessity':'unknown','threshold':None,'deadline':None,
            'evidence_status':'source_matched_candidate','requires_user_review':True})
    return items
