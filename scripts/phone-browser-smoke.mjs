import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {spawn,execFileSync} from 'node:child_process';import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);const {chromium}=require('C:/Users/vikto/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve('data/phone-test-'+Date.now());fs.mkdirSync(root,{recursive:true});const cert=path.join(root,'cert.pem'),key=path.join(root,'key.pem'),state=path.join(root,'pair.json');
execFileSync('C:/Program Files/Git/usr/bin/openssl.exe',['req','-x509','-newkey','rsa:2048','-nodes','-keyout',key,'-out',cert,'-days','1','-subj','/CN=phone.test','-addext','subjectAltName=DNS:phone.test'],{windowsHide:true,stdio:'ignore'});
const python=path.resolve('.venv/Scripts/python.exe');const backend=spawn(python,['scripts/browser_fixture.py',path.join(root,'fixture.sqlite')],{windowsHide:true,stdio:'ignore'});
let gateway,browser;
try{
 for(let i=0;i<60;i++){try{if((await fetch('http://127.0.0.1:4319/api/stats')).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
 gateway=spawn(python,['scripts/phone_browser_fixture.py',state,cert,key],{windowsHide:true,stdio:'ignore'});
 for(let i=0;i<60&&!fs.existsSync(state);i++)await new Promise(r=>setTimeout(r,200));
 assert(fs.existsSync(state));await new Promise(r=>setTimeout(r,1000));
 browser=await chromium.launch({channel:'msedge',headless:true,args:['--ignore-certificate-errors','--host-resolver-rules=MAP phone.test 127.0.0.1','--no-proxy-server']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,ignoreHTTPSErrors:true});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('https://phone.test:4322/');await page.getByRole('heading',{name:'Hunter на телефоні'}).waitFor();
 assert.equal(await page.evaluate(async()=>(await fetch('/api/projects')).status),401);
 await page.locator('#pair-code').fill(JSON.parse(fs.readFileSync(state)).code);await page.getByRole('button',{name:'Підключити телефон'}).click();
 await page.getByRole('button',{name:'Знайдені проєкти',exact:true}).waitFor();
 await page.getByRole('button',{name:'Знайдені проєкти',exact:true}).click();await page.getByRole('heading',{name:'Browser test project'}).waitFor();
 await page.getByRole('button',{name:'У роботу',exact:true}).click();await page.getByRole('button',{name:'⭐ У роботі',exact:true}).click();await page.getByRole('heading',{name:'Browser test project'}).waitFor();
 const desktop=await (await fetch('http://127.0.0.1:4319/api/projects?status=tracking')).json();assert(desktop.some(p=>p.title==='Browser test project'));
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
 await page.evaluate(()=>navigator.serviceWorker.ready);await page.reload();await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
 const cacheKeys=await page.evaluate(async()=>{const out=[];for(const name of await caches.keys()){for(const r of await (await caches.open(name)).keys())out.push(new URL(r.url).pathname);}return out;});assert(!cacheKeys.some(p=>p.startsWith('/api/')||p==='/'));
 const cdp=await context.newCDPSession(page);await cdp.send('Page.enable');const install=await cdp.send('Page.getInstallabilityErrors');assert(install.installabilityErrors.every(e=>['in-incognito','not-from-secure-origin'].includes(e.errorId)),'Unexpected manifest/icon/installability failure');
 await page.screenshot({path:'data/android-phone-test.png',fullPage:false});
 await context.setOffline(true);await page.goto('https://phone.test:4322/');await page.getByRole('heading',{name:'Немає зв’язку з Hunter'}).waitFor();await page.screenshot({path:'data/android-offline-test.png'});
 await context.setOffline(false);await page.goto('https://phone.test:4322/');await page.getByRole('button',{name:'Вийти на телефоні'}).click();await page.getByRole('heading',{name:'Hunter на телефоні'}).waitFor();assert.equal(await page.evaluate(async()=>(await fetch('/api/projects')).status),401);
 assert.deepEqual(errors,[]);console.log(JSON.stringify({passed:true,checks:['pairing','shared project write','mobile viewport','manifest and icons (real HTTPS installation still pending)','service worker active','no private API cache','offline page','logout'],installabilityErrors:install.installabilityErrors}));
}finally{await browser?.close();gateway?.kill();backend.kill();}
