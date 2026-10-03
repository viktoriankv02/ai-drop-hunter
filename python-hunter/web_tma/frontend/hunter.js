const $=s=>document.querySelector(s);
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url=s=>{try{const u=new URL(s);return u.protocol==='https:'?escape(u.href):'#';}catch{return '#';}};
const stamp=s=>s?new Date(s).toLocaleString('uk-UA'):'Ще не перевірено';
const money=x=>Number(x).toLocaleString('uk-UA',{maximumSignificantDigits:8});
let token='',tab='tracking',detailId=null,marketData=null,viewGeneration=0,projectOffset=0,projectQuery='',activityFilter='all';
function notice(text){$('#notice').hidden=false;$('#notice').textContent=text;const b=document.createElement('button');b.textContent='Закрити';b.onclick=()=>$('#notice').hidden=true;$('#notice').append(b);}
async function api(path,method='GET',body){
 const r=await fetch(path,{method,headers:{'Content-Type':'application/json',...(method!=='GET'?{'X-Hunter-Session':token}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});
 let value;try{value=await r.json();}catch{throw Error('Сервер не повернув дані. Перевір запуск застосунку.');}
 if(!r.ok)throw Error(typeof value.detail==='string'?value.detail:'Невірні дані запиту');
 return value;
}
async function action(fn){try{await fn();}catch(e){notice(e.message);}}
async function stats(){const s=await api('/api/stats');$('#stats').textContent=s.total+' карток · '+s.tracking+' у роботі'+(s.migration_issues?' · '+s.migration_issues+' записи імпорту потребують відновлення':'');}
const badge=(s,kind='')=>'<span class="badge '+kind+'">'+escape(s)+'</span>';
function link(h,label='Відкрити джерело ↗'){return '<a href="'+url(h)+'" target="_blank" rel="noopener noreferrer">'+escape(label)+'</a>';}
function overviewView(p,expanded=false){
 const o=p.overview;
 const useful=p.summary&&!p.summary.startsWith('Каталог CryptoRank API.')&&!p.summary.startsWith('Кандидат для дослідження.')?p.summary:null;
 if(o)return '<div class="project-overview"><span class="eyebrow">ЩО ЦЕ ЗА ПРОЄКТ</span><p>'+escape(o.brief)+'</p><small>'+link(o.source_url,'Джерело опису ↗')+' · '+stamp(o.updated_at)+'</small>'+(expanded?'<details><summary>Цитата про продукт</summary><blockquote>'+escape(o.quote)+'</blockquote></details>':'')+'</div>';
 if(useful)return '<div class="project-overview"><span class="eyebrow">ОПИС ІЗ КАРТКИ ДЖЕРЕЛА</span><p>'+escape(useful.slice(0,expanded?700:300))+'</p><small>'+link(p.source_url,'Перевірити опис ↗')+'</small></div>';
 return '<div class="project-overview overview-missing"><strong>Опис продукту ще не знайдено</strong><p>Є лише назва й посилання з каталогу. Агент автоматично готує опис і план участі. Якщо джерело недоступне, картка покаже помилку та відсутні дані.</p></div>';
}
function preparationView(p){
 const v=p.preparation;if(!v)return '';
 const labels={waiting:'Очікує підготовки',queued:'У черзі підготовки',running:'Агент готує картку',draft:'Чернетка зібрана — переглянь план',partial:'Картка потребує доповнення',failed:'Підготовку не завершено'};
 return '<div class="preparation-summary">'+badge(labels[v.state]||v.state,v.state==='failed'?'bad':'warn')+'<small>Кроків у плані: '+v.steps+(v.missing?.length?' · Бракує: '+escape(v.missing.join(', ')):'')+'</small>'+(v.error?'<small>'+escape(v.error)+'</small>':'')+'</div>';
}
function sourceScanView(s){
 const j=s.last_job,r=j?.result;
 if(!j)return '<small>Автоматичний пошук ще не запускався.</small>';
 if(j.state==='queued'||j.state==='running')return '<small>Пошук '+(j.state==='queued'?'у черзі.':'виконується…')+'</small>';
 if(j.error)return '<small class="bad">Останній пошук: '+escape(j.error)+'</small>';
 if(!r)return '<small>Останній пошук завершено без підсумку.</small>';
 return '<div class="source-scan-result"><strong>Перевірено: '+r.found+' · нових: '+r.added+' · уже були: '+r.duplicates+'</strong>'+
  (r.added===0?'<small>Нових записів у каталозі не з’явилося — це не помилка пошуку.</small>':'<small>Нові картки додано до «Знайдених проєктів».</small>')+'</div>';
}
async function load(){
 document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab===tab));
 const generation=++viewGeneration;$('#content').innerHTML='<p class="muted">Завантаження…</p>';stats().catch(()=>{});
 if(tab==='sources')return sources(generation);
 if(tab==='jobs')return jobs(generation);
 if(tab==='history')return history(generation);
 if(tab==='market')return market();
 let ps=await api('/api/projects?status='+tab+'&limit=61&offset='+projectOffset+'&q='+encodeURIComponent(projectQuery)+'&screen='+(tab==='new'?activityFilter:'all'));if(generation!==viewGeneration)return;
 $('#content').innerHTML='<h1>'+(tab==='tracking'?'Твої проєкти у роботі':tab==='ignored'?'Не беремо в роботу':'Знайдені проєкти')+'</h1><p class="muted">CryptoRank → Incrypted. Інші джерела призупинені за твоєю вказівкою. Нові проєкти автоматично проходять підготовку картки: опис → умови → кроки → джерела та невідомі дані. Переглянь план і виріши: «У роботу» або «Не беремо». Поки ти не вибрав, проєкт залишається у знайдених.</p><div class="toolbar"><input id="filter" aria-label="Пошук проєкту" placeholder="Знайти за назвою або джерелом"><select id="activity-filter" aria-label="Тип активності"><option value="test_only">Лише тестові токени</option><option value="needs_review">Потребують перевірки</option><option value="excluded">Виключено за твоїми правилами</option><option value="all">Усі для аудиту</option></select><button id="discover" class="primary">Перевірити каталоги зараз</button><button id="manual">Додати свій проєкт</button></div><p id="screening-counts" class="muted"></p><div id="discovery-summary"></div><div id="cards" class="grid"></div><div class="toolbar"><button id="previous-page">← Попередні</button><span id="page-number"></span><button id="next-page">Наступні →</button></div>';
 const render=q=>{
  $('#cards').innerHTML=ps.slice(0,60).filter(p=>(p.title+' '+p.source_platform).toLowerCase().includes(q.toLowerCase())).map(p=>'<article class="card">'+
   '<div>'+badge(p.source_platform)+badge(p.check_status==='catalog_only'?'Каталог — очікує дослідження':({catalog_only:'Каталог',new:'Ще не перевірено',pending:'Очікує перевірки',failed:'Джерело недоступне',changed:'Джерело оновлено',unchanged:'Перевірено'}[p.check_status]||p.check_status),p.check_status==='failed'?'bad':'')+'</div><h2>'+escape(p.title)+'</h2>'+
   overviewView(p)+preparationView(p)+
   (p.activity_reason?'<small>'+escape(p.activity_reason)+'</small>':'')+
   (p.legacy?'<small>Імпорт Gemini: старі оцінки потребують перевірки.</small>':'')+
   '<small>Перевірка: '+stamp(p.last_checked)+'</small><div class="toolbar"><button data-open="'+p.id+'">План і докази</button>'+
   (p.status!=='tracking'?'<button data-preview="'+p.id+'">Дослідити</button><button class="primary" data-interest="'+p.id+'">У роботу</button><button data-reject="'+p.id+'">Не беремо</button>':'')+'</div></article>').join('')||'<div class="empty">Немає карток за цим фільтром. Непідтверджені картки — у списку «Потребують перевірки».<p><button id="show-unchecked">Показати неперевірені проєкти</button></p></div>';
  if($('#show-unchecked'))$('#show-unchecked').onclick=()=>{activityFilter='needs_review';projectOffset=0;load();};
  document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>action(()=>detail(+b.dataset.open)));
  document.querySelectorAll('[data-preview]').forEach(b=>b.onclick=()=>action(async()=>{await api('/api/projects/'+b.dataset.preview+'/research','POST',{});notice('Агент дослідить опис та умови. Проєкт залишається у знайдених.');}));
  document.querySelectorAll('[data-reject]').forEach(b=>b.onclick=()=>action(async()=>{await api('/api/projects/'+b.dataset.reject+'/status','POST',{status:'ignored'});load();}));
  document.querySelectorAll('[data-interest]').forEach(b=>b.onclick=()=>action(async()=>{await api('/api/projects/'+b.dataset.interest+'/status','POST',{status:'tracking'});notice('Додано до роботи. План і прогрес збережено; агент перевірятиме оновлення.');load();}));
 };
 const controls=()=>{$('#previous-page').disabled=projectOffset===0;$('#next-page').disabled=ps.length<=60;$('#page-number').textContent='Сторінка '+(Math.floor(projectOffset/60)+1);};
 $('#filter').value=projectQuery;$('#activity-filter').value=activityFilter;$('#activity-filter').hidden=tab!=='new';render(projectQuery);controls();
 let searchVersion=0,searchTimer;
 const fetchPage=async()=>{const version=++searchVersion;const rows=await api('/api/projects?status='+tab+'&limit=61&offset='+projectOffset+'&q='+encodeURIComponent(projectQuery)+'&screen='+(tab==='new'?activityFilter:'all'));if(version!==searchVersion||generation!==viewGeneration)return;ps=rows;render(projectQuery);controls();};
 $('#activity-filter').onchange=e=>{activityFilter=e.target.value;projectOffset=0;action(fetchPage);};
 $('#filter').oninput=e=>{projectQuery=e.target.value;projectOffset=0;searchVersion++;clearTimeout(searchTimer);searchTimer=setTimeout(()=>action(fetchPage),300);};
 $('#previous-page').onclick=()=>{projectOffset=Math.max(0,projectOffset-60);action(fetchPage);};
 $('#next-page').onclick=()=>{projectOffset+=60;action(fetchPage);};
 $('#discover').onclick=()=>action(async()=>{const r=await api('/api/discovery/run','POST',{});notice('Поставлено джерел у чергу: '+r.job_ids.length+'. Прогрес — у розділі «Команда агентів».');});
 $('#manual').onclick=()=>{const title=prompt('Назва проєкту');if(!title)return;const source_url=prompt('HTTPS-посилання на проєкт');if(!source_url)return;action(async()=>{await api('/api/projects/manual','POST',{title,source_url});load();});};
 if(tab==='new'){
  const [c,ss]=await Promise.all([api('/api/activity-screening'),api('/api/sources')]);if(generation!==viewGeneration)return;
  $('#screening-counts').textContent='Тестові: '+c.test_only+' · Потребують перевірки: '+c.needs_review+' · Виключено: '+c.excluded+'. Це фільтр за доступними доказами, не гарантія винагороди.';
  $('#discovery-summary').innerHTML='<section class="panel compact"><h2>Останній пошук нових проєктів</h2>'+ss.filter(s=>s.enabled&&s.purpose==='discovery').map(s=>'<div><strong>'+escape(s.name)+'</strong> · '+stamp(s.last_check)+sourceScanView(s)+'</div>').join('')+'<small>Пошук виконується автоматично раз на добу, поки сервер працює. Повторний запуск покаже 0 нових, якщо каталоги не змінилися.</small></section>';
 }
}
function revisionPanel(change){
 if(!change)return '';
 const group=(title,items)=>items.length?'<h3>'+title+'</h3><ul>'+items.map(x=>'<li>'+escape(x)+'</li>').join('')+'</ul>':'';
 return '<section class="panel"><h2>Що змінилося у джерелі</h2><p class="muted">Порівняно перевірки '+stamp(change.previous_at)+' та '+stamp(change.current_at)+'. Зміна тексту ще не підтверджує зміну умов участі.</p>'+
 group('Додано або оновлено',change.added)+group('Було в попередній версії',change.removed)+
 group('Нові посилання',change.added_links)+group('Посилання, яких більше немає в матеріалі',change.removed_links)+
 (!change.added_count&&!change.removed_count&&!change.added_links.length&&!change.removed_links.length?'<p>Змін у збереженому тексті й посиланнях не виявлено.</p>':'')+
 (change.truncated?'<p class="muted">Показано перші 12 фрагментів кожного типу.</p>':'')+
 (change.source_incomplete?'<p class="badge warn">Порівняння часткове: один із матеріалів збережено не повністю.</p>':'')+'</section>';
}

const campaignSelection=new Map();
function campaignGuideView(p){
 const guide=p.guide||{},campaigns=guide.campaigns||[];
 if(!campaigns.length)return '<section class="panel guide-empty"><h2>Інструкція участі</h2><p>Агент ще не знайшов достатньо доказів для послідовного плану. Нижче видно доступні джерела й умови, які потрібно уточнити.</p></section>';
 let selected=campaignSelection.get(p.id)??Math.max(0,campaigns.findIndex(x=>x.status==='active'));
 if(selected>=campaigns.length)selected=0;
 const labels={active:'Активна',ended:'Завершена',upcoming:'Очікується',unknown:'Статус уточнюється'};
 return '<section class="campaign-guide"><div class="plan-heading"><div><p class="eyebrow">ПРАКТИЧНИЙ ПЛАН</p><h2>Інструкція участі</h2></div>'+badge(campaigns.length+' кампанії')+'</div><p class="muted">Обери кампанію й виконуй кроки за порядком. Позначки зберігають твій прогрес; отримання нагороди перевіряється окремо.</p>'+
 (guide.conflicts?.length?'<details class="guide-conflicts"><summary><strong>'+guide.conflicts.length+' розбіжності джерел — уточнити перед дією</strong></summary>'+guide.conflicts.map(c=>'<p><strong>'+escape(c.title)+'</strong><br>'+escape(c.detail)+'</p><div>'+c.sources.map(u=>link(u,'Джерело ↗')).join(' · ')+'</div>').join('')+'</details>':'')+
 '<div class="campaign-layout"><div class="campaign-nav" role="group" aria-label="Кампанії проєкту">'+campaigns.map((c,i)=>'<button class="campaign-choice '+(i===selected?'selected':'')+'" data-campaign-index="'+i+'" aria-pressed="'+(i===selected)+'"><strong>'+escape(c.title)+'</strong><span>'+badge(labels[c.status]||labels.unknown,c.status==='ended'?'':c.status==='active'?'good':'warn')+'</span><small>'+escape(c.period||'Строк уточнюється')+'</small><small>'+c.done+'/'+c.total+' кроків позначено</small></button>').join('')+'</div><div>'+campaigns.map((c,i)=>'<section class="campaign-body panel" data-campaign-panel="'+i+'" '+(i!==selected?'hidden':'')+'><h3>'+escape(c.title)+'</h3><div class="campaign-meta">'+Object.entries({network:'Мережа',period:'Період',reward:'Винагорода',cost:'Витрати',time:'Час'}).map(([key,label])=>'<div><small>'+label+'</small><strong>'+escape(c[key]||'Не підтверджено')+'</strong></div>').join('')+'</div>'+
 (c.description?'<p>'+escape(c.description)+'</p>':'')+(c.notice?'<p class="badge warn">'+escape(c.notice)+'</p>':'')+
 '<div class="campaign-progress"><progress value="'+c.done+'" max="'+Math.max(1,c.total)+'"></progress><span>'+c.done+' / '+c.total+' позначено виконаними</span></div><ol class="campaign-steps">'+c.steps.map(step=>'<li class="'+(step.done?'step-done':'')+'"><div class="step-title">'+(step.task_id?'<input type="checkbox" data-task="'+step.task_id+'" aria-label="Позначити виконаним: '+escape(step.title)+'" '+(step.done?'checked':'')+'>':'')+'<h4>'+escape(step.title)+'</h4></div>'+(step.description?'<p>'+escape(step.description)+'</p>':'')+(step.evidence_state==='source_changed'?'<p class="badge warn">Джерело змінилось — перевір цей крок</p>':'')+'<div>'+link(step.url||step.source_url||p.source_url,'Відкрити інструкцію ↗')+(step.source_url&&step.source_url!==step.url?' · '+link(step.source_url,'Доказ ↗'):'')+'</div><details><summary>На чому ґрунтується крок</summary><blockquote>'+escape(step.quote||'Джерельна цитата ще не збережена; пункт потребує перевірки.')+'</blockquote></details></li>').join('')+'</ol>'+(c.source_url?link(c.source_url,'Джерело кампанії ↗'):'')+'</section>').join('')+'</div></div>'+
 (guide.recommendations?.length?'<div class="guide-recommendations"><h3>Що ще варто перевірити</h3>'+guide.recommendations.map(x=>'<p><strong>'+escape(x.title)+'</strong><br>'+escape(x.reason)+' '+link(x.url,'Перевірити ↗')+'</p>').join('')+'</div>':'')+
 (guide.unknowns?.length?'<details open><summary>Що ще потрібно з’ясувати агенту</summary><ul>'+guide.unknowns.map(x=>'<li>'+escape(x)+'</li>').join('')+'</ul></details>':'')+'</section>';
}
function resourceView(p){
 return '<section class="panel"><h2>Джерела та перевірки агента</h2><p class="muted">Для знайдених проєктів і проєктів у роботі перевірка планується раз на добу, поки локальний сервер працює. Агент читає пов’язані ресурси; якщо даних бракує, шукає додаткові сторінки в інтернеті.</p>'+((p.resources||[]).length?p.resources.map(r=>'<div class="resource-row"><div>'+link(r.url,r.label||r.url)+' '+badge(r.purpose==='reward_rules'?'Правила':r.purpose==='product_manual'?'Офіційна довідка':'Додаткове джерело')+'<small>'+stamp(r.last_checked)+' · '+escape(r.last_status==='read'?'Прочитано':r.last_status==='failed'?'Недоступне':'Очікує перевірки')+'</small>'+(r.last_error?'<p class="muted">'+escape(r.last_error)+'</p>':'')+'</div></div>').join(''):'<p>Додаткові ресурси ще не знайдено. '+link(p.source_url,'Основна сторінка ↗')+'</p>')+'</section>';
}
function participationView(p){
 const plan=p.participation||{requirements:[],suggestions:[],missing:[]};
 const categories={eligibility:'Допуск',activity:'Дія',threshold:'Поріг',deadline:'Строк',registration:'Реєстрація',verification:'Перевірка',claim:'Отримання',unlock:'Розблокування',cost:'Витрати',reward:'Винагорода',other:'Уточнити'};
 const roles={required:['Обов’язково','required'],optional:['Додатково','optional'],unknown:['Уточнити','unknown']};
 const items=plan.requirements||[];
 const required=items.filter(x=>x.necessity==='required').length,optional=items.filter(x=>x.necessity==='optional').length;
 return '<section class="participation panel"><div class="plan-heading"><div><p class="eyebrow">ТВІЙ ПЛАН УЧАСТІ</p><h2>Вимоги та дії</h2></div>'+badge(p.report?.stale?'Потребує оновлення':'За збереженими джерелами',p.report?.stale?'warn':'')+'</div>'+
 '<div class="plan-summary"><div><strong>'+required+'</strong><span>обов’язкових пунктів</span></div><div><strong>'+optional+'</strong><span>додаткових за джерелом</span></div><div><strong>'+(plan.missing||[]).length+'</strong><span>тем ще перевірити</span></div></div>'+
 '<p class="muted">Це покриття відомих умов, а не ймовірність винагороди. Позначки обов’язковості й висновки агента потребують перегляду.</p>'+
 (items.length?'<ol class="requirement-list">'+items.map(x=>{const role=x.evidence_status==='source_matched_candidate'?['Уривок для перевірки','unknown']:(roles[x.necessity]||roles.unknown);return '<li class="requirement '+role[1]+'"><div class="requirement-top"><span class="requirement-role">'+role[0]+'</span><span class="muted">'+escape(categories[x.category]||categories.other)+'</span></div><h3>'+escape(x.title)+'</h3>'+
 ((x.threshold||x.deadline)?'<dl class="requirement-meta">'+(x.threshold?'<div><dt>Поріг</dt><dd>'+escape(x.threshold)+'</dd></div>':'')+(x.deadline?'<div><dt>Строк</dt><dd>'+escape(x.deadline)+'</dd></div>':'')+'</dl>':'')+
 '<div class="requirement-links">'+link(x.source_url||p.source_url,'Джерело вимоги ↗')+(x.url&&x.url!==x.source_url?' · '+link(x.url,'Сторінка дії ↗'):'')+'</div>'+
 (x.evidence_status==='platform_reference_not_reward_rule'?'<p class="badge warn">Довідка продукту; зв’язок із винагородою не підтверджений</p>':'')+
 '<details><summary>Показати цитату-доказ</summary><blockquote>'+escape(x.quote)+'</blockquote></details></li>';}).join('')+'</ol>':'<div class="plan-empty"><strong>Умови ще не витягнуті з джерел</strong><p>Натисни «Перевірити й проаналізувати». Якщо джерело недоступне, додай його текст нижче.</p></div>')+
 '<div class="plan-suggestions"><h3>Можливі додаткові дії</h3><p class="muted">Пропозиції для перевірки. Вплив на винагороду поки невідомий.</p><ol>'+ (plan.suggestions||[]).map(x=>'<li><strong>'+escape(x.title)+'</strong><p>'+escape(x.reason)+'</p>'+link(x.url,'Перевірити на сторінці проєкту ↗')+'</li>').join('')+'</ol></div>'+
 ((plan.missing||[]).length?'<details class="plan-gaps" open><summary>Що агенту ще потрібно з’ясувати</summary><ul>'+plan.missing.map(x=>'<li>'+escape(x.title)+'</li>').join('')+'</ul></details>':'')+'</section>';
}

async function detail(id){
 detailId=id;const p=await api('/api/projects/'+id);
 const r=p.report?.body;
 $('#detail').innerHTML='<h1>'+escape(p.title)+'</h1>'+link(p.source_url)+'<div class="toolbar"><button id="research" class="primary">Перевірити й проаналізувати</button><button id="take">У роботу</button><button id="defer">Залишити у знайдених</button><button id="ignore">Не беремо</button></div>'+
 '<p class="muted">Остання успішна перевірка: '+stamp(p.last_success)+'. Стан: '+escape(p.check_status)+'</p>'+
 (p.activity_screening?'<p class="badge warn">'+escape(p.activity_screening.reason)+'</p>':'')+
 (p.legacy_warning?'<p class="badge warn">Старі оцінки й автоматичні позначки Gemini не підтверджують винагороду або виконання.</p>':'')+
 preparationView(p)+overviewView(p,true)+campaignGuideView(p)+(p.guide?.campaigns?.length?'<details class="panel"><summary>Деталізовані вимоги та джерельні уривки</summary>'+participationView(p)+'</details>':participationView(p))+resourceView(p)+
 '<section class="panel"><h2>Висновки за джерелом</h2>'+
 (r?badge(r.status)+(p.report.stale?badge('Матеріал змінився — висновок застарів','warn'):'')+'<small> Опрацьовано '+r.coverage.processed_characters+' із '+r.coverage.available_characters+' символів.</small>'+
 (r.provenance?'<p class="badge warn">'+escape(r.provenance)+'</p>':'')+
 (r.unknowns?.length?'<ul class="muted">'+r.unknowns.map(x=>'<li>'+escape(x)+'</li>').join('')+'</ul>':'')+
 r.facts.map(f=>'<p>'+escape(f.title)+'</p><blockquote>'+escape(f.quote)+'</blockquote>'+(f.source_url?link(f.source_url,'Джерело висновку ↗'):'')).join(''):
 '<p class="muted">Ще немає доказового аналізу. Запусти агента або додай матеріал відкритої сторінки нижче.</p>')+'</section>'+
 (r?.historical_comparisons?.length?'<section class="panel"><h2>Що підказують історичні кейси</h2><p class="muted">Аналогії для перевірки, не вимоги цього проєкту.</p>'+r.historical_comparisons.map(c=>'<p><strong>'+escape(c.project)+'</strong>: '+escape(c.lesson)+' '+link(c.source_url,'Джерело кейсу ↗')+'</p>').join('')+'</section>':'')+
 (p.reviewed_note && p.report?.model!=='codex-reviewed-research-note'?'<section class="panel"><h2>Дослідницька нотатка</h2><p class="muted">'+escape(p.reviewed_note.provenance)+'</p>'+p.reviewed_note.facts.map(f=>'<p>'+escape(f.title)+' '+link(f.source_url,'Джерело ↗')+'</p>').join('')+(p.reviewed_note.unknowns?.length?'<h3>Що ще не підтверджено</h3><ul>'+p.reviewed_note.unknowns.map(x=>'<li>'+escape(x)+'</li>').join('')+'</ul>':'')+'</section>':'')+
 (r?.reference_actions?.length?'<details><summary>Довідка платформи — не завдання кампанії</summary><p class="muted">Не є рекомендацією торгувати або умовою отримання винагороди.</p>'+r.reference_actions.map(x=>'<p>'+escape(x.title)+' '+link(x.source_url||x.url,'Джерело ↗')+'</p>').join('')+'</details>':'')+
 revisionPanel(p.source_changes)+
 '<section><h2>План дій</h2><p class="muted">Галочка означає твоє повідомлення про виконання. Вона не є перевіркою транзакції.</p>'+
 p.tasks.map(t=>'<div class="task"><input type="checkbox" aria-label="Позначити виконаним: '+escape(t.title)+'" data-task="'+t.id+'" '+(t.status==='user_reported'?'checked':'')+'><div><strong>'+escape(t.title)+'</strong><div>'+badge(t.status==='user_reported'?'Позначено тобою':t.status==='legacy_unverified'?'Старе завдання — перевірити':'Чернетка з джерела',t.status==='user_reported'?'good':'warn')+'</div>'+
 (t.evidence_state==='source_changed'?'<p class="badge warn">Джерело оновилось — перевір актуальність цього кроку. Твою позначку виконання збережено.</p>':'')+
 (t.target_url?link(t.target_url,'Переглянути сторінку дії ↗'):'')+
 (t.evidence_json?'<blockquote>'+escape(JSON.parse(t.evidence_json).quote)+'</blockquote>':'')+'</div></div>').join('')+'</section>'+
 '<details><summary>Додати матеріал відкритої сторінки</summary><p class="muted">Якщо сайт не дозволив автоматичне читання, встав його текст разом із потрібними посиланнями. Це буде позначено як твій імпорт.</p><textarea id="material" aria-label="Матеріал джерела"></textarea><button id="save-material">Зберегти та проаналізувати</button></details>'+
 '<details><summary>Навчити на моєму виправленні</summary><p>Корекція зберігається для наступних аналізів цього проєкту. Ваги Ollama не змінюються.</p><textarea id="feedback" aria-label="Виправлення агента"></textarea><button id="save-feedback">Зберегти виправлення</button></details>'+
 '<details><summary>Історія перевірок і змін ('+p.events.length+')</summary>'+p.events.map(e=>'<p><small>'+stamp(e.created_at)+'</small> '+escape(e.kind)+'</p><pre>'+escape(e.details)+'</pre>').join('')+'</details>';
 if(!$('#project').open)$('#project').showModal();
 document.querySelectorAll('[data-campaign-index]').forEach(button=>button.onclick=()=>{const selected=Number(button.dataset.campaignIndex);campaignSelection.set(id,selected);document.querySelectorAll('[data-campaign-panel]').forEach(panel=>panel.hidden=Number(panel.dataset.campaignPanel)!==selected);document.querySelectorAll('[data-campaign-index]').forEach(b=>{b.classList.toggle('selected',b===button);b.setAttribute('aria-pressed',String(b===button));});});
 $('#research').onclick=()=>action(async()=>{await api('/api/projects/'+id+'/research','POST',{});notice('Дослідження поставлено в чергу. Повторне натискання не створює дубль.');});
 $('#take').hidden=p.status==='tracking';$('#defer').hidden=p.status==='new';
 $('#take').onclick=()=>action(async()=>{await api('/api/projects/'+id+'/status','POST',{status:'tracking'});$('#project').close();tab='tracking';projectOffset=0;projectQuery='';await load();});
 $('#defer').onclick=()=>action(async()=>{await api('/api/projects/'+id+'/status','POST',{status:'new'});$('#project').close();tab='new';projectOffset=0;projectQuery='';await load();});
 $('#ignore').onclick=()=>action(async()=>{await api('/api/projects/'+id+'/status','POST',{status:'ignored'});$('#project').close();load();});
 document.querySelectorAll('[data-task]').forEach(el=>el.onchange=()=>action(async()=>{await api('/api/tasks/'+el.dataset.task+'/completion','POST',{done:el.checked});detail(id);}));
 $('#save-material').onclick=()=>action(async()=>{await api('/api/projects/'+id+'/material','POST',{text:$('#material').value,url:p.source_url});notice('Матеріал збережено. Аналіз поставлено в чергу.');detail(id);});
 $('#save-feedback').onclick=()=>action(async()=>{const r=await api('/api/projects/'+id+'/feedback','POST',{text:$('#feedback').value});notice(r.learning);});
}
async function sources(generation){
 const ss=await api('/api/sources');if(generation!==viewGeneration)return;
 $('#content').innerHTML='<h1>Джерела під твоїм контролем</h1><p>CryptoRank: каталог може надходити через офіційний API. Назва в каталозі ще не підтверджує mainnet, актуальні завдання або винагороду.</p><p class="muted">Telegram порожній, доки ти сам не додаси канали. Увімкнення джерела не означає, що сайт дозволяє автоматичне читання.</p><section class="panel">'+ss.map(s=>'<div class="source"><div><strong>'+escape(s.name)+'</strong> '+badge('Пріоритет '+s.priority)+badge(s.type)+'<div>'+link(s.url)+'</div><small>'+escape(s.last_error||s.last_status||'Не перевірено')+'</small>'+sourceScanView(s)+(s.adapter==='manual'?'<div>'+badge('Адаптер ще не підключений','warn')+'</div>':'')+'</div><div class="toolbar"><button data-toggle="'+s.id+'">'+(s.enabled?'На паузу':'Увімкнути')+'</button><button data-scan="'+s.id+'" '+(!s.enabled||s.adapter==='manual'?'disabled':'')+'>Зібрати</button><button data-delete="'+s.id+'">Видалити</button></div></div>').join('')+'</section>'+
 '<details class="panel"><summary>Як читати CryptoRank зі свого браузера</summary><ol><li>Відкрий chrome://extensions або edge://extensions і ввімкни режим розробника.</li><li>Натисни «Завантажити розпаковане» та вибери папку <code>D:\\\\Projects\\\\ai-hub-hunter-gemini\\\\browser-extension\\\\cryptorank-reader</code>.</li><li>У тому самому браузері відкрий цей застосунок на порту 4318 і сайт CryptoRank Drophunting.</li><li>У розширенні натисни «Зібрати проєкти зі сторінки». Якщо з’явиться перевірка сайту, пройди її самостійно.</li></ol><p>Імпорт працює, поки браузер та застосунок відкриті. Агент аналізує збережені матеріали через Ollama.</p></details>'+
 '<form id="source-form" class="panel form-grid"><label>Назва<input name="name" required maxlength="120"></label><label>URL або @канал<input name="url" required></label><label>Тип<select name="type"><option value="website">Сайт</option><option value="telegram">Telegram</option></select></label><button class="primary">Додати</button></form>';
 document.querySelectorAll('[data-toggle]').forEach(b=>b.onclick=()=>action(async()=>{await api('/api/sources/'+b.dataset.toggle+'/toggle','POST',{});load();}));
 document.querySelectorAll('[data-delete]').forEach(b=>b.onclick=()=>action(async()=>{if(confirm('Видалити джерело зі збору? Знайдені проєкти залишаться.')){await api('/api/sources/'+b.dataset.delete,'DELETE');load();}}));
 document.querySelectorAll('[data-scan]').forEach(b=>b.onclick=()=>action(async()=>{await api('/api/sources/'+b.dataset.scan+'/scan','POST',{});notice('Збір у черзі.');}));
 $('#source-form').onsubmit=e=>{e.preventDefault();action(async()=>{await api('/api/sources','POST',Object.fromEntries(new FormData(e.target)));load();});};
}
function jobResult(j){
 if(j.error)return '<p class="bad">'+escape(j.error)+'</p>';
 if(j.state==='queued')return '<p class="muted">Очікує своєї черги. Локальна модель опрацьовує один матеріал за раз.</p>';
 if(j.state==='running')return '<p>'+escape(j.phase==='reading'?'Читає доступний матеріал джерела…':j.phase)+'</p>';
 let r;try{r=JSON.parse(j.result_json||'null');}catch{return '<p>Результат не вдалося прочитати.</p>';}
 if(!r)return '<p>Завершено без збереженого результату.</p>';
 if(j.kind==='discover')return '<p>Знайдено карток: '+r.found+'. Додано: '+r.added+'. Уже були: '+r.duplicates+'.</p><small>'+escape(r.scope||(!r.history_complete?'Історія переглянута частково.':''))+'</small>';
 if(r.analysis==='unchanged')return '<p>Матеріал не змінився. Використано попередній повний аналіз.</p>';
 const c=r.coverage;
 return '<p>'+(c?.complete?'Опрацьовано весь збережений текст.':'Аналіз частковий; можна продовжити повторним запуском.')+'</p>'+
 (c?'<small>'+c.processed_characters+' із '+c.available_characters+' символів. Кроки потребують твого перегляду.</small>':'');
}
async function jobs(generation){
 const js=await api('/api/jobs');if(generation!==viewGeneration)return;
 const kinds={discover:'Збір проєктів',research:'Дослідження проєкту',analyze:'Аналіз матеріалу'};
 const states={queued:'У черзі',running:'Працює',succeeded:'Завершено',failed:'Не вдалося',cancelled:'Скасовано за твоїм рішенням'};
 $('#content').innerHTML='<h1>Команда агентів</h1><p>Збирач → дослідник Ollama → перевірка цитат → чернетка плану. Одна локальна модель працює послідовно.</p><p class="muted">Нові проєкти автоматично отримують чернетку картки. Щоденний спостерігач оновлює знайдені проєкти й проєкти у роботі, поки сервер увімкнений. Цей журнал не підтверджує виконання зовнішніх дій.</p><div class="toolbar"><button id="refresh-jobs">Оновити стан</button></div><div class="panel scroll"><table><thead><tr><th>Проєкт або джерело</th><th>Стан</th><th>Результат</th><th>Дія</th></tr></thead><tbody>'+js.map(j=>'<tr><td><strong>'+escape(j.target_name||'Запис видалений')+'</strong><br><small>'+escape(kinds[j.kind]||j.kind)+' · #'+j.id+'<br>'+stamp(j.created_at)+'</small></td><td>'+badge(states[j.state]||j.state,j.state==='failed'?'bad':j.state==='succeeded'?'good':'')+'</td><td>'+jobResult(j)+'</td><td>'+(j.project_id?'<button data-job-project="'+j.project_id+'">Відкрити план</button>':'')+(j.state==='failed'||j.state==='succeeded'?'<button data-retry="'+j.id+'">Повторити</button>':'')+'</td></tr>').join('')+'</tbody></table></div>';
 $('#refresh-jobs').onclick=()=>action(load);
 document.querySelectorAll('[data-job-project]').forEach(b=>b.onclick=()=>action(()=>detail(+b.dataset.jobProject)));
 document.querySelectorAll('[data-retry]').forEach(b=>b.onclick=()=>action(async()=>{await api('/api/jobs/'+b.dataset.retry+'/retry','POST',{});await jobs(generation);notice('Роботу поставлено в чергу. Збережені частини аналізу буде використано повторно.');}));
}
function historyEvidence(c){
 const number=v=>typeof v==='number'?v.toLocaleString('uk-UA'):'Немає підтверджених даних';
 const reward=c.reward||{},outcome=c.outcome||{};
 return '<details><summary>Умови, суми та рівень доказів</summary>'+
 (c.criteria?.length?'<h3>Кому й за які дії</h3><ul>'+c.criteria.map(x=>'<li><strong>'+escape(x.cohort)+'</strong>: '+escape(x.requirement)+' '+link(x.source_url,'Доказ ↗')+'</li>').join('')+'</ul>':'<p>Структуровані критерії ще перевіряються.</p>')+
 '<h3>Оголошена алокація</h3><p>'+number(reward.allocated)+' '+escape(reward.token||'')+(reward.scope?' · '+escape(reward.scope):'')+'</p>'+
 (reward.cohorts?.length?'<ul>'+reward.cohorts.map(x=>'<li>'+escape(x.name||x.cohort||'Група')+
 (x.eligible_wallets!=null?' · адрес з правом участі: '+number(x.eligible_wallets):'')+
 (x.per_wallet!=null?' · на адресу: '+number(x.per_wallet):'')+
 (x.allocated!=null?' · алокація групи: '+number(x.allocated):'')+'</li>').join('')+'</ul>':'')+
 (reward.per_wallet_tiers?'<p>Рівні на адресу: '+reward.per_wallet_tiers.map(number).join(' / ')+' '+escape(reward.token)+'</p>':'')+
 '<h3>Фактично отримані винагороди</h3><p>Отримано токенів: '+number(outcome.claimed)+'. Адрес-одержувачів: '+number(outcome.paid_wallets)+'.</p>'+
 (outcome.statement?'<p>'+escape(outcome.statement)+'</p>':'')+
 '<p class="muted">Оголошена алокація не дорівнює отриманим токенам. Кількість адрес не дорівнює кількості людей.</p>'+
 (c.reported_outcome?'<h3>Опублікована оцінка виплат</h3><p>Зріз '+escape(c.reported_outcome.as_of)+': '+number(c.reported_outcome.claimers)+' адрес; '+number(c.reported_outcome.claimed_value_usd)+' USD за цінами під час отримання. Медіана: '+number(c.reported_outcome.median_claim_usd)+' USD.</p><p class="muted">'+escape(c.reported_outcome.note)+'</p>'+link(c.reported_outcome.source_url,'Таблиця дослідження ↗'):'')+
 (c.current_status_note?'<p class="badge warn">'+escape(c.current_status_note)+'</p>':'')+
 (c.allocation_audit?'<h3>Відтворений підрахунок CSV</h3><p>'+number(c.allocation_audit.unique_addresses)+' унікальних адрес; '+escape(c.allocation_audit.tokens)+' OP за масштабу '+c.allocation_audit.decimals_applied+' decimals.</p><p class="muted">Перевірено список алокації, не фактичні claims. '+escape(c.allocation_audit.note)+'</p><small>SHA-256: '+escape(c.allocation_audit.sha256)+'</small>':'')+
 (c.missing_evidence?.length?'<h3>Що не дозволяє вважати кейс завершеним</h3><ul>'+c.missing_evidence.map(x=>'<li>'+escape(x)+'</li>').join('')+'</ul>':'')+'</details>';
}
async function history(generation){
 const h=await api('/api/research/history');if(generation!==viewGeneration)return;
 const label={primary_source_checked_partial:'Першоджерела прочитано',curated_mixed_sources:'Змішані джерела',secondary_directory_screened:'Вторинний скринінг'};
 const top=(h.factor_analysis||[]).slice(0,10);
 $('#content').innerHTML='<h1>150 історичних роздач за останні 2 роки</h1><div class="metrics"><div class="metric">Проаналізовано<strong>'+h.analyzed_projects+' / '+h.target_projects+'</strong></div><div class="metric">Першоджерела прочитано<strong>'+(h.evidence_tiers.primary_source_checked_partial||0)+'</strong></div><div class="metric">Вторинний скринінг<strong>'+(h.evidence_tiers.secondary_directory_screened||0)+'</strong></div></div><p class="muted">Період: '+escape(h.window.from)+' — '+escape(h.window.to)+'. Частота історичного фактора допомагає ставити питання, але не гарантує винагороду й не є правилом нового проєкту.</p><p><a class="button primary" href="'+escape(h.report_url)+'" target="_blank" rel="noopener">Відкрити повний інтерактивний звіт ↗</a></p>'+
 '<section class="panel"><h2>Головні фактори у вибірці</h2><div class="grid">'+top.map(f=>'<div><strong>'+escape(f.factor)+'</strong><br>'+f.projects+' проєктів · '+Math.round(f.share_of_150*100)+'%<br><small>'+escape(f.strategy)+'</small></div>').join('')+'</div></section>'+
 '<div class="grid">'+h.projects.map(c=>'<article class="card"><h2>'+escape(c.project)+'</h2>'+badge(c.event_date||c.event_year)+badge(label[c.evidence_tier]||c.evidence_tier,c.evidence_tier==='secondary_directory_screened'?'warn':'good')+'<p>'+escape(c.description)+'</p><h3>Умови та дії</h3><ul>'+(c.rewarded_actions||[]).slice(0,8).map(x=>'<li>'+escape(x)+'</li>').join('')+'</ul><p><strong>Фактори:</strong> '+escape((c.factors||[]).join(', ')||'не класифіковано')+'</p><p><strong>Результат:</strong> '+escape(c.payout_summary||('Алокація: '+(c.allocation_reported||'невідомо')+'; eligible: '+(c.eligible_reported||'невідомо')+'; claimants: '+(c.claimants_reported||'невідомо')))+'</p><p><strong>Урок для агента:</strong> '+escape(c.agent_lesson)+'</p><details><summary>Прогалини та джерела</summary><p>'+escape((c.unknowns||[]).join(' '))+'</p>'+(c.sources||[]).map(s=>link(s.url,s.title)).join('<br>')+'</details></article>').join('')+'</div>';
}
function market(){
 $('#content').innerHTML='<h1>Ринок · історія та сценарії</h1><p class="muted">Дані Binance / OKX. Історичний діапазон — експериментальна основа, не готова модель торгових сигналів.</p>'+
 '<div class="toolbar"><label>Актив<input id="symbol" value="BTC" placeholder="BTC, ETH або XAAPL"></label><label>Історія<select id="period"><option value="1h">1 година</option><option value="24h" selected>24 години</option><option value="1m">1 місяць</option><option value="1y">1 рік</option><option value="5y">5 років</option></select></label><button id="chart-load" class="primary">Показати графік</button><label>Горизонт<select id="horizon"><option value="1h">1 година</option><option value="24h" selected>24 години</option><option value="7d">1 тиждень</option></select></label><button id="forecast-load">Розрахувати сценарії</button></div>'+
 '<p><small>XAAPL та подібні інструменти — токенізовані акції OKX. Прямі котирування акцій компаній ще не підключені.</small></p><div id="chart-box" class="panel">Введи символ і натисни «Показати графік».</div><div id="forecast-box"></div>';
 $('#chart-load').onclick=()=>action(async()=>{const b=$('#chart-load');b.disabled=true;try{
  const value=await api('/api/market/chart?symbol='+encodeURIComponent($('#symbol').value)+'&period='+$('#period').value);
  if(tab!=='market')return;marketData=value;drawChart(value);
 }finally{b.disabled=false;}});
 $('#forecast-load').onclick=()=>action(async()=>{const b=$('#forecast-load');b.disabled=true;$('#forecast-box').textContent='Отримую історію та перевіряю часову вибірку…';try{
  const f=await api('/api/market/forecast?symbol='+encodeURIComponent($('#symbol').value)+'&horizon='+$('#horizon').value,'POST',{});
  if(tab!=='market')return;
  $('#forecast-box').innerHTML='<section class="panel"><h2>'+escape(f.symbol)+' · сценарій до '+stamp(f.target_at)+'</h2>'+badge('Експериментальний метод','warn')+
   '<div class="metrics">'+[['Нижній історичний рівень',f.scenarios.lower],['Медіанний рівень',f.scenarios.median],['Верхній історичний рівень',f.scenarios.upper]].map(([k,v])=>'<div class="metric">'+k+'<strong>'+money(v)+'</strong></div>').join('')+'</div>'+
   '<p>'+escape(f.summary)+'</p><p>Перевірка на '+f.evaluation.test_samples+' пізніших незалежних періодах. Порівняно з «ціна не зміниться»: '+(f.evaluation.beats_no_change?'менша історична похибка':'перевагу не підтверджено')+'.</p><small>'+escape(f.evaluation.scope)+' Збережено прогноз #'+f.id+'; майбутній результат ще не оцінено.</small></section>';
 }catch(e){if(tab==='market')$('#forecast-box').textContent='Сценарій не розраховано: '+e.message;throw e;}finally{b.disabled=false;}});
}
function drawChart(d){
 const points=d.chart,min=Math.min(...points.map(x=>x.close)),max=Math.max(...points.map(x=>x.close)),span=max-min||max*.01;
 const coords=points.map((p,i)=>(65+i/(points.length-1||1)*880).toFixed(2)+','+(265-(p.close-min)/span*230).toFixed(2)).join(' ');
 $('#chart-box').innerHTML='<h2>'+escape(d.symbol)+' · '+escape(d.exchange)+' · '+money(d.current_price)+'</h2><p>'+badge(d.instrument_type)+(!d.coverage.complete?badge('Неповна історія','warn'):'')+(d.coverage.stale?badge('Дані застарілі','bad'):'')+'</p><svg id="price-chart" class="chart" viewBox="0 0 1000 310" role="img" aria-label="Графік закритих цін '+escape(d.symbol)+'"><text x="8" y="30">'+money(max)+'</text><text x="8" y="270">'+money(min)+'</text><polyline points="'+coords+'"/><line x1="65" y1="275" x2="945" y2="275" stroke="#cdd7e7"/><text x="65" y="300">'+escape(new Date(points[0].timestamp).toLocaleDateString('uk-UA'))+'</text><text x="810" y="300">'+escape(new Date(points.at(-1).timestamp).toLocaleDateString('uk-UA'))+'</text></svg><label>Перегляд свічки<input id="candle-slider" type="range" min="0" max="'+(points.length-1)+'" value="'+(points.length-1)+'" style="width:100%"></label><p id="candle-detail" aria-live="polite"></p><small>'+escape(d.coverage.note)+' Пропусків: '+d.coverage.missing_intervals+'.</small>';
 const show=i=>{const p=points[i];$('#candle-detail').textContent=stamp(p.time)+' · O '+money(p.open)+' · H '+money(p.high)+' · L '+money(p.low)+' · C '+money(p.close)+' · Обсяг '+money(p.volume);};
 $('#candle-slider').oninput=e=>show(+e.target.value);show(points.length-1);
 $('#price-chart').onpointermove=e=>{const rect=e.currentTarget.getBoundingClientRect();const i=Math.round(Math.max(0,Math.min(1,((e.clientX-rect.left)/rect.width*1000-65)/880))*(points.length-1));$('#candle-slider').value=i;show(i);};
}
$('#close-detail').onclick=()=>$('#project').close();
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{tab=b.dataset.tab;projectOffset=0;projectQuery='';document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===b));action(load);});
action(async()=>{token=(await api('/api/session')).token;await load();const pid=new URLSearchParams(location.search).get('project');if(pid && /^[1-9][0-9]*$/.test(pid))await detail(Number(pid));});
setInterval(()=>{if(!document.hidden)stats().catch(()=>{});},10000);

setInterval(()=>{if(!document.hidden && tab==='jobs')jobs(viewGeneration).catch(()=>{});},5000);
