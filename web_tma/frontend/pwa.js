const local=['127.0.0.1','localhost'].includes(location.hostname);
const install=document.querySelector('#pwa-install'),connect=document.querySelector('#phone-connect'),dialog=document.querySelector('#phone-dialog'),content=document.querySelector('#phone-content');
let installEvent;
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installEvent=e;install.hidden=false;});
install.onclick=async()=>{if(installEvent){await installEvent.prompt();await installEvent.userChoice;installEvent=null;install.hidden=true;}};
window.addEventListener('appinstalled',()=>{install.hidden=true;});
if('serviceWorker' in navigator&&window.isSecureContext)navigator.serviceWorker.register('/sw.js').catch(()=>{});
const connection=document.querySelector('#connection-notice');
function connectivity(){connection.hidden=navigator.onLine;connection.textContent='Немає інтернет-зв’язку. Зміни не збережуться, доки підключення не відновиться.';}
window.addEventListener('online',connectivity);window.addEventListener('offline',connectivity);connectivity();
document.querySelector('#phone-close').onclick=()=>dialog.close();
async function request(path,method='GET'){
 const headers={'Content-Type':'application/json'};if(method!=='GET')headers['X-Hunter-Session']=(await (await fetch('/api/session')).json()).token;
 const r=await fetch(path,{method,headers,...(method!=='GET'?{body:'{}'}:{})});const v=await r.json();if(!r.ok)throw Error(v.detail||'Не вдалося виконати дію');return v;
}
if(!local){connect.hidden=true;document.querySelector('#connection-label').textContent='Телефон · спільна база';const logout=document.querySelector('#phone-logout');logout.hidden=false;logout.onclick=async()=>{try{const r=await fetch('/mobile/logout',{method:'POST'});if(!r.ok)throw Error();location.replace('/mobile-login');}catch{connection.hidden=false;connection.textContent='Немає зв’язку: вихід не підтверджений. Спробуй ще раз.';}};}
connect.onclick=async()=>{
 content.replaceChildren();const title=document.createElement('h2');title.textContent='Hunter для Android';content.append(title);dialog.showModal();
 try{
  const s=await request('/api/mobile/status');
  const p=document.createElement('p');p.textContent=s.origin&&s.gateway_ready?'Підключи телефон до тих самих проєктів. ПК і застосунок мають залишатися ввімкненими.':'Захищену адресу ще не підключено. Після її налаштування тут з’явиться QR-код для входу з телефона.';content.append(p);
  if(!s.origin||!s.gateway_ready)return;
  const a=document.createElement('a');a.href=s.origin;a.textContent=s.origin;a.target='_blank';a.rel='noopener noreferrer';content.append(a);
  const steps=document.createElement('p');steps.textContent='1. Створи код. 2. Відскануй QR камерою телефона й відкрий у Chrome. 3. Натисни «Встановити Hunter» або меню ⋮ → «Додати на головний екран».';content.append(steps);
  if(s.temporary||/\.(?:lhr\.life|localhost\.run)$/.test(new URL(s.origin).hostname)){const warning=document.createElement('p');warning.className='muted';warning.textContent='Тестова адреса: після перезапуску доступу вона зміниться. Для постійної встановленої версії потрібна стабільна адреса.';content.append(warning);}
  const create=document.createElement('button');create.textContent='Створити код';create.className='primary';content.append(create);
  const result=document.createElement('div');result.className='phone-pair-result';content.append(result);
  create.onclick=async()=>{create.disabled=true;try{const v=await request('/api/mobile/pair-code','POST');result.replaceChildren();const img=document.createElement('img');img.src=v.qr;img.alt='QR для одноразового входу';img.width=240;img.height=240;const code=document.createElement('p');code.textContent='Код: '+v.code+' · діє 10 хвилин';result.append(img,code);}catch(e){result.textContent=e.message;}finally{create.disabled=false;}};
  const revoke=document.createElement('button');revoke.textContent='Відключити всі телефони ('+s.paired_devices+')';content.append(revoke);revoke.onclick=async()=>{try{await request('/api/mobile/revoke','POST');result.textContent='Телефони відключені. Для нового входу створи код.';}catch(e){result.textContent=e.message;}};
 }catch(e){const p=document.createElement('p');p.textContent=e.message;content.append(p);}
};

if(local&&new URLSearchParams(location.search).get('phone')==='1')connect.click();
