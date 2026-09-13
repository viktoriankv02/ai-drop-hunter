document.querySelector('#export').onclick=async()=>{
 const status=document.querySelector('#status');try{
 const [tab]=await chrome.tabs.query({active:true,currentWindow:true});
 const url=new URL(tab.url);if(url.origin!=='https://cryptorank.io'||!/^\/(?:[a-z]{2}\/)?drophunting\/[^/]+/.test(url.pathname))throw Error('Відкрий окрему картку проєкту в розділі Drophunting. Панель API та список проєктів не експортуються.');
 const [{result}]=await chrome.scripting.executeScript({target:{tabId:tab.id},func:()=>({name:document.querySelector('h1')?.innerText||document.title,text:String(window.getSelection()).trim()||(document.querySelector('main')||document.body).innerText,source:location.href})});
 if(!result.text||result.text.length<80)throw Error('Недостатньо тексту. Дочекайся завантаження картки.');
 if(result.text.length>16000)throw Error('Сторінка довга. Виділи потрібну інструкцію (до 16 000 символів) і натисни ще раз.');
 const data={format:'ai-drop-hunter-material',version:1,name:result.name.slice(0,120),source:result.source,text:result.text,capturedAt:new Date().toISOString()};
 const blob=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=blob;a.download='cryptorank-material.json';a.click();setTimeout(()=>URL.revokeObjectURL(blob),10000);
 status.textContent='Файл збережено. У AI Drop Hunter → Імпорт CryptoRank вибери цей файл і натисни «Імпортувати матеріал».';
 }catch(e){status.textContent=e.message;}
};