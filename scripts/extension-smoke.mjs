import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/vikto/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const db=path.resolve('data/extension-smoke-'+Date.now()+'.sqlite');
const child=spawn(path.resolve('.venv/Scripts/python.exe'),['scripts/browser_fixture.py',db],{windowsHide:true,stdio:'ignore'});
let context;
const watchdog=setTimeout(()=>{console.error("Extension test timed out");child.kill();process.exit(1);},60000);
try{
 for(let i=0;i<50;i++){try{if((await fetch('http://127.0.0.1:4319/api/stats')).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
 const extension=path.resolve('browser-extension/cryptorank-reader');
 context=await chromium.launchPersistentContext(path.resolve('data/extension-profile-'+Date.now()),{
 executablePath:'D:/AI/playwright-browsers/chromium-1234/chrome-win64/chrome.exe',headless:true,
 args:['--disable-extensions-except='+extension,'--load-extension='+extension]});
 // Send every local-app request to the isolated fixture, never the user's database.
 await context.route('http://127.0.0.1:4318/**',async route=>{
  const request=route.request();
  const response=await route.fetch({url:request.url().replace(':4318',':4319'),
    headers:{...request.headers(),host:'127.0.0.1:4319',origin:'http://127.0.0.1:4319'}});
  await route.fulfill({response});
 });
 const card='https://cryptorank.io/ru/drophunting/extension-fixture-activity999999';
 await context.route('https://cryptorank.io/**',route=>route.fulfill({contentType:'text/html',body:
  '<html><title>Extension fixture</title><main><h1>Extension fixture</h1><p>'+
  'This is an isolated test of importing public campaign instructions. Read the official conditions before choosing an action. No reward is guaranteed. '.repeat(3)+
  '</p><a href="https://example.com/instructions">Read instructions</a></main></html>'}));
 let worker=context.serviceWorkers()[0]||await context.waitForEvent('serviceworker',{timeout:15000});
 const extensionId=worker.url().split('/')[2];
 const app=await context.newPage();await app.goto('http://127.0.0.1:4318/');
 const popup=await context.newPage();await popup.goto('chrome-extension://'+extensionId+'/popup.html');
 const started=await popup.evaluate(url=>chrome.runtime.sendMessage({type:'catalog-start',urls:[url]}),card);
 assert(started.ok,JSON.stringify(started));
 for(let i=0;i<30;i++){const ready=await worker.evaluate(async()=>{const {catalog}=await chrome.storage.local.get('catalog');return (await chrome.tabs.get(catalog.tabId)).status==='complete';});if(ready)break;await new Promise(r=>setTimeout(r,100));}
 const rendered=context.pages().find(p=>p.url()===card);assert(rendered);await rendered.goto(card);
 await worker.evaluate(()=>catalogTick());
 let state=await worker.evaluate(()=>chrome.storage.local.get('catalog'));
 assert.equal(state.catalog.done,1,JSON.stringify(state));
 await worker.evaluate(()=>catalogTick());
 state=await worker.evaluate(()=>chrome.storage.local.get('catalog'));
 assert.equal(state.catalog.enabled,false);
 const projects=await (await fetch('http://127.0.0.1:4319/api/projects?status=all')).json();
 const imported=projects.find(p=>p.source_url===card);assert(imported);
 const detail=await (await fetch('http://127.0.0.1:4319/api/projects/'+imported.id)).json();
 assert.equal(detail.snapshots.length,1);
 const jobs=await (await fetch('http://127.0.0.1:4319/api/jobs')).json();
 assert.equal(jobs.filter(j=>j.kind==='analyze').length,1);
 // A browser challenge must stop the collector without adding a fake material.
 await context.unroute('https://cryptorank.io/**');
 await context.route('https://cryptorank.io/**',route=>route.fulfill({contentType:'text/html',
  body:'<html><title>Трохи зачекайте…</title><main>Проверка безопасности</main></html>'}));
 const blocked='https://cryptorank.io/ru/drophunting/challenge-fixture-activity999998';
 await popup.evaluate(url=>chrome.runtime.sendMessage({type:'catalog-start',urls:[url]}),blocked);
 for(let i=0;i<30;i++){const ready=await worker.evaluate(async()=>{const {catalog}=await chrome.storage.local.get('catalog');return (await chrome.tabs.get(catalog.tabId)).status==='complete';});if(ready)break;await new Promise(r=>setTimeout(r,100));}
 await worker.evaluate(()=>catalogTick());
 state=await worker.evaluate(()=>chrome.storage.local.get('catalog'));
 assert.equal(state.catalog.enabled,false);
 assert(state.catalog.message.includes('перевірка'));
 console.log(JSON.stringify({passed:true,checks:['actual MV3 worker','catalogue to isolated API','snapshot saved','analysis queued','challenge stops without import'],db}));
}finally{clearTimeout(watchdog);await context?.close();child.kill();}
