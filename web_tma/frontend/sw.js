const CACHE='hunter-shell-v1';
const FILES=['/offline.html','/static/hunter.css','/static/appearance.css','/static/hunter.js','/static/pwa.js','/static/icons/hunter-192.png','/static/icons/hunter-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES))));
self.addEventListener('activate',e=>e.waitUntil((async()=>{for(const k of await caches.keys())if(k.startsWith('hunter-shell-')&&k!==CACHE)await caches.delete(k);await self.clients.claim();})()));
self.addEventListener('fetch',e=>{
 const u=new URL(e.request.url);if(u.origin!==self.location.origin||e.request.method!=='GET')return;
 if(e.request.mode==='navigate'){e.respondWith(fetch(e.request).catch(()=>caches.match('/offline.html')));return;}
 // Never cache API data, sessions, codes, reports, or write requests.
 if(FILES.includes(u.pathname))e.respondWith(fetch(e.request).then(r=>{if(r.ok&&!r.redirected){const copy=r.clone();e.waitUntil(caches.open(CACHE).then(c=>c.put(u.pathname,copy)));}return r;}).catch(()=>caches.match(u.pathname)));
});
