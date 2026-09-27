import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/vikto/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
fs.mkdirSync('data',{recursive:true});
const db=path.resolve('data/browser-smoke-'+Date.now()+'.sqlite');
const child=spawn(path.resolve('.venv/Scripts/python.exe'),['scripts/browser_fixture.py',db],{windowsHide:true,stdio:'ignore'});
let browser;
try{
 let ready=false;
 for(let i=0;i<50;i++){try{const r=await fetch('http://127.0.0.1:4319/api/stats');if(r.ok){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,200));}
 assert(ready,'Fixture did not start');
 browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:960}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:4319/');
 await page.getByRole('button',{name:'Знайдені проєкти',exact:true}).click();
 await page.getByRole('heading',{name:'Browser test project'}).waitFor();
 assert.equal(await page.locator('article img').count(),0,'Untrusted HTML must be escaped');
 await page.getByRole('button',{name:'☆ Цікаво',exact:true}).click();
 await page.getByRole('button',{name:'⭐ У роботі',exact:true}).click();
 await page.getByRole('heading',{name:'Browser test project'}).waitFor();
 await page.getByRole('button',{name:'План і докази',exact:true}).click();
 await page.getByRole('heading',{name:'Висновки за джерелом'}).waitFor();
 await page.getByLabel('Закрити',{exact:true}).click();
 await page.getByRole('button',{name:'Джерела',exact:true}).click();
 await page.getByText('CryptoRank',{exact:true}).waitFor();
 assert.equal(await page.getByText('Crypto Fortochka',{exact:true}).count(),0);
 await page.locator('#source-form [name=name]').fill('My approved channel');
 await page.locator('#source-form [name=url]').fill('@myapprovedchannel');
 await page.locator('#source-form [name=type]').selectOption('telegram');
 await page.locator('#source-form').getByRole('button',{name:'Додати',exact:true}).click();
 await page.getByText('My approved channel',{exact:true}).waitFor();
 const row=page.locator('.source').filter({hasText:'My approved channel'});
 await row.getByRole('button',{name:'На паузу'}).click();
 await page.locator('.source').filter({hasText:'My approved channel'}).getByRole('button',{name:'Увімкнути'}).waitFor();
 page.once('dialog',d=>d.accept());
 await page.locator('.source').filter({hasText:'My approved channel'}).getByRole('button',{name:'Видалити'}).click();
 await page.getByText('My approved channel',{exact:true}).waitFor({state:'detached'});
 await page.getByRole('button',{name:'Історичні кейси',exact:true}).click();
 await page.getByRole('heading',{name:'Arbitrum',exact:true}).waitFor();
 await page.getByText('0 / 500',{exact:true}).waitFor();
 await page.getByRole('button',{name:'Команда агентів',exact:true}).click();
 await page.getByText('У черзі',{exact:true}).waitFor();
 await page.getByRole('button',{name:'Ринок і сценарії',exact:true}).click();
 await page.getByRole('heading',{name:'Ринок · історія та сценарії'}).waitFor();
 await page.route('**/api/market/chart?*',route=>route.fulfill({json:{
 symbol:'BTC/USDT',exchange:'Test fixture',instrument_type:'crypto_spot',current_price:101,
 coverage:{complete:true,stale:false,note:'Fixture',missing_intervals:0},
 chart:Array.from({length:30},(_,i)=>({timestamp:Date.UTC(2026,8,1)+i*60000,time:new Date(Date.UTC(2026,8,1)+i*60000).toISOString(),open:100,high:102,low:99,close:100+i/30,volume:12}))}}));
 await page.getByRole('button',{name:'Показати графік',exact:true}).click();
 await page.locator('#price-chart').waitFor();
 await page.locator('#candle-slider').fill('0');
 assert((await page.locator('#candle-detail').innerText()).includes('100'));
 await page.setViewportSize({width:390,height:844});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile horizontal overflow');
 await page.screenshot({path:'data/browser-smoke-mobile.png',fullPage:true});
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({passed:true,checks:['project selection','source add/pause/delete','escaped external text','historical progress','agent queue','interactive chart','mobile overflow'],db}));
}finally{
 await browser?.close();
 child.kill();
}
