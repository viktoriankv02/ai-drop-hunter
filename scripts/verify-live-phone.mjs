import {createRequire} from 'node:module';import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);const {chromium}=require('C:/Users/vikto/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const local='http://127.0.0.1:4318';const session=await (await fetch(local+'/api/session')).json();
const pair=await (await fetch(local+'/api/mobile/pair-code',{method:'POST',headers:{'Content-Type':'application/json','Origin':local,'X-Hunter-Session':session.token},body:'{}'})).json();assert(pair.code&&pair.url);
const context=await chromium.launchPersistentContext('data/phone-live-test-profile',{channel:'msedge',headless:true,viewport:{width:390,height:844},isMobile:true,hasTouch:true});
try{
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pair.url+'/mobile-login');await page.getByRole('heading',{name:'Hunter на телефоні'}).waitFor();
 assert.equal(await page.evaluate(async()=>(await fetch('/api/projects')).status),401);
 await page.goto(pair.url+'/mobile-login#code='+pair.code);await page.getByRole('button',{name:'⭐ У роботі',exact:true}).waitFor();
 assert.equal(await page.evaluate(async()=>(await fetch('/api/projects')).status),200);
 await page.evaluate(()=>navigator.serviceWorker.ready);await page.reload();await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
 const cdp=await context.newCDPSession(page);await cdp.send('Page.enable');const install=await cdp.send('Page.getInstallabilityErrors');assert.deepEqual(install.installabilityErrors,[]);
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
 await page.screenshot({path:'data/android-live-https.png'});
 await page.getByRole('button',{name:'Вийти на телефоні'}).click();await page.getByRole('heading',{name:'Hunter на телефоні'}).waitFor();
 assert.equal(await page.evaluate(async()=>(await fetch('/api/projects')).status),401);assert.deepEqual(errors,[]);
 console.log(JSON.stringify({passed:true,url:pair.url,https:true,login:true,privateApiProtected:true,installabilityErrors:install.installabilityErrors,logout:true}));
}finally{await context.close();}
