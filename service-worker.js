// Cache exact page URLs so a newly approved version never reuses an older shell.
const SHELL='portfolio-pages-v20';
self.addEventListener('install',event=>event.waitUntil(self.skipWaiting()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const key of await caches.keys())if((key.startsWith('portfolio-pages-')&&key!==SHELL)||(key.startsWith('portfolio-media-')&&key!=='portfolio-media-v20'))await caches.delete(key);await self.clients.claim()})()));
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET'||event.request.mode!=='navigate'||new URL(event.request.url).origin!==self.location.origin)return;
 event.respondWith((async()=>{
  const cache=await caches.open(SHELL),stored=await cache.match(event.request);
  const refresh=fetch(event.request).then(async response=>{if(response.ok){await cache.put(event.request,response.clone());const keys=await cache.keys();while(keys.length>4)await cache.delete(keys.shift())}return response});
  if(stored){event.waitUntil(refresh.catch(()=>{}));return stored}
  return refresh;
 })());
});
