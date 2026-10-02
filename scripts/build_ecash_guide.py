"""Reviewed multi-source eCash example; no keys, downloads or transactions executed."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core.workspace import Workspace
from core.participation import VERSION
from core.campaign_guide import VERSION as GUIDE_VERSION
w=Workspace();w.initialize();pid=w.rows("SELECT id FROM projects WHERE source_url='https://cryptorank.io/ru/drophunting/ecash-drivechains-activity1307'")[0]['id'];p=w.project(pid)
docs=[]
for name in ('join','what-to-expect','download','how-to-claim','coin-splitting','what-is-ecash'):
 d=json.loads(Path('data/ecash-'+name+'.json').read_text(encoding='utf-8'));d['purpose']='reward_rules' if name in ('join','how-to-claim') else 'product_manual';docs.append(d)
 w.add_resource(pid,d['url'],'eCash · '+name,d['purpose'],'reviewed_research');w.resource_checked(pid,d['url'])
body={'url':p['source_url'],'text':'\n\n'.join('Джерело: '+d['url']+'\n'+d['text'] for d in docs),'documents':docs,
      'links':[{'url':d['url'],'label':'Офіційне джерело'} for d in docs]+[l for d in docs for l in d['links']],
      'truncated':True,'provenance':'Перевірено офіційні документи eCash. CryptoRank доступний у вебіндексі та на скриншоті користувача, але пряме читання повертає 403. Досьє містить невирішені розбіжності.'}
body['characters_available']=len(body['text']);sid,_=w.save_snapshot(pid,p['source_url'],body,via='reviewed_multi_source_guide')
url=lambda name:'https://ecash.com/'+name+'/'
def step(title,quote,source,link=None,description=None):
 assert quote in next(d['text'] for d in docs if d['url']==source),quote
 return {'title':title,'quote':quote,'source_url':source,'url':link or source,'description':description,'requires_user_review':True}
beta_steps=[
 step('Перевірити адресу та історичний Beta snapshot','beta (~967,680)',url('how-to-claim'),description='Спершу перевір, чи адреса мала BTC у потрібному snapshot. Участь після історичного знімка сама по собі не створює право на його баланс.'),
 step('Вибрати офіційний реліз для Beta','Check the release notes and selected network before use',url('download'),description='Перейди до офіційних завантажень і звір реліз та мережу. Завантаження й встановлення виконуєш самостійно; застосунок не запускає стороннє ПЗ.'),
 step('Перевірити процедуру роботи з ключами та replay protection','Never paste a seed into this website, a chat, or a claim form.',url('coin-splitting'),description='Не надсилай seed чи приватний ключ цьому застосунку. Інструкція CryptoRank містить імпорт BTC-ключа; до цього кроку потрібна перевірка офіційної процедури coin splitting.'),
 step('Перевірити блоки й транзакції Beta у відповідній мережі','View blocks and transactions on the current rehearsal network.',url('how-to-claim'),'https://beta.ecash.ninja/',description='Зістав мережу в гаманці та оглядачі. Збережи дату, адресу й transaction hash лише для дій, які фактично виконав. Це не підтвердження конвертації pECX.')]
main_steps=[
 step('Перевірити умови mainnet snapshot без купівлі BTC за цією інструкцією','Hold BTC through the snapshot.',url('join'),description='Цей маршрут залежить від реального BTC й тому не входить до режиму «лише тестові токени». Не змішуй його з Beta.'),
 step('Якщо BTC на біржі — перевірити політику підтримки форка','ECX credit depends on exchange policy.',url('join'),description='Сам факт балансу на біржі не підтверджує доступність ECX. Потрібна публічна політика саме твого провайдера.'),
 step('Після запуску перевірити офіційну готовність і coin splitting','Wait for the official wallet and coin-splitting guidance.',url('how-to-claim'),url('coin-splitting'),description='Це майбутній крок після фактичного запуску, а не дія для виконання зараз. Перевіряються незалежність балансів та чинний реліз.')]
campaigns=[
 {'title':'Beta · тестування та перевірка pECX','status':'active','period':'Beta запущено 19.09.2026; CryptoRank вказує активність 21.09–31.10.2026','network':'Betanet · тестова мережа','reward':'pECX — тестовий баланс; конвертація в ECX потребує уточнення','cost':'Розмір витрат не перевірено; eligibility пов’язана з історичним BTC snapshot','time':'CryptoRank оцінює активність у 10 хв; встановлення та синхронізація можуть тривати довше','description':'Перевір eligibility, офіційне ПЗ та Beta-мережу. Наявність тестового балансу не підтверджує майбутню винагороду.','notice':'Snapshot Beta: блок ~967 680. У картці CryptoRank наведено ~963 648 — це розбіжність, а не одне правило.','quote':'The LayerTwoLabs team has working software available today, a full node, wallet, and Beta network.','source_url':url('what-to-expect'),'steps':beta_steps},
 {'title':'Alpha · історична фаза','status':'ended','period':'Запуск 23.08.2026; офіційний довідник: закриття 24.09.2026','network':'Alphanet · архів','reward':'Історичні тестові одиниці; фінальна конвертація не підтверджена','cost':'Не є актуальним маршрутом участі','time':None,'description':'Збережено для історії. Поточне тестування слід перевіряти в Beta. CryptoRank наводить інший кінець вікна активності — 21.09.2026.','quote':'Alpha retires on September 24, 2026; use Beta for current testing.','source_url':url('how-to-claim'),'steps':[]},
 {'title':'Mainnet · майбутній BTC snapshot','status':'upcoming','period':'Орієнтовно 31.10.2026 · блок ~973 728; дата залежить від блоків','network':'Mainnet · ще заплановано','reward':'Заявлено 1:1 ECX за BTC у mainnet snapshot; ринкова вартість не гарантована','cost':'Потрібен реальний BTC; маршрут поза режимом тестових токенів','time':'Очікування запуску; час процедури ще не перевірено','notice':'Не виконуй майбутні кроки як готову інструкцію до запуску.','quote':'mainnet (~973,728, 31st october 2026)','source_url':url('what-to-expect'),'steps':main_steps}]
conflicts=[{'title':'Конвертація pECX → ECX','detail':'CryptoRank описує Beta-курс 0,02. Офіційна join-сторінка наводить 1000 pECX = 10 ECX, а what-to-expect описує Alpha/Beta як практичні одиниці та новий mainnet snapshot. Однозначних узгоджених умов бонусу немає.','sources':[p['source_url'],url('join'),url('what-to-expect')]},
 {'title':'Дати фаз і snapshot','detail':'Запуск мережі, вікно активності агрегатора й дата закриття фази — різні події. Beta: офіційно ~967 680, 19.09; в агрегаторі є згадка ~963 648. Для eligibility потрібне офіційне уточнення.','sources':[p['source_url'],url('what-is-ecash'),url('how-to-claim')]}]
recommendations=[{'title':'Перевірити додаткові програми тестування та внесків','reason':'Офіційний довідник згадує кампанії, конкурси й внески; чинний конкретний набір завдань та його винагорода ще не встановлені.','url':url('how-to-claim')},
 {'title':'Звіряти релізи та готовність потрібної мережі','reason':'Новий реліз може змінити підтримку Beta, доступ до балансу чи replay protection. Це перевірка інструментів, а не спосіб штучно збільшити активність.','url':url('download')}]
report={'status':'partial','facts':[],'tasks':[x for c in campaigns for x in c['steps']],
 'requirements':[],'campaigns':campaigns,'conflicts':conflicts,'recommendations':recommendations,
 'guide_unknowns':['Узгоджений курс та процедура бонусної конвертації pECX.','Чи підтверджує конкретна адреса eligibility для Beta.','Підтримка актуального релізу та точні витрати/час.','Підтверджена сума фінансування: на скриншоті та вебіндексі різні значення.'],
 'guide_version':GUIDE_VERSION,'participation_version':VERSION,'provenance':body['provenance'],'unknowns':[],'errors':[],
 'coverage':{'processed_characters':len(body['text']),'retained_characters':len(body['text']),'available_characters':len(body['text']),'complete':False}}
report['overview']={'brief':'eCash.com (ECX) — окремий Bitcoin-форк для Drivechains за BIP300/301. Це не eCash (XEC). Є тестові Alpha/Beta та запланований mainnet із власним snapshot.','quote':'eCash (ECX) is a Bitcoin hard fork associated with Paul Sztorc and LayerTwo Labs.','source_url':url('what-is-ecash')}
w.save_report(pid,sid,report,'codex-reviewed-multi-source-guide')
Path('research/ecash-participation-guide.json').write_text(json.dumps({'project_id':pid,'report':report},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'project_id':pid,'campaigns':len(campaigns),'steps':len(report['tasks']),'conflicts':len(conflicts)}))
