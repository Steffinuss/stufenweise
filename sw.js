/* Stufenweise – Offline-Baustein (Service Worker)
   Die App holt sich immer zuerst die neueste Fassung aus dem Netz. Nur wenn kein Internet da ist,
   kommt die zuletzt gespeicherte Fassung aus dem Zwischenspeicher. Es werden keine Kinderdaten gespeichert:
   Die liegen weiter nur im Browser (localStorage). Lizenz: EUPL-1.2 */
const CACHE = 'stufenweise-v1';
const SHELL = ['./', './index.html', './manifest.webmanifest', './version.json', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => Promise.all(SHELL.map(u => c.add(new Request(u, {cache: 'reload'})).catch(() => null)))));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('stufenweise-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if(req.method !== 'GET' || url.origin !== self.location.origin) return;
  const isPage = req.mode === 'navigate' || /\.(html|json|webmanifest)$/.test(url.pathname) || url.pathname.endsWith('/');
  if(isPage){
    // Netz zuerst, damit Updates sofort ankommen; ohne Netz die gespeicherte Fassung
    e.respondWith(fetch(req).then(res => {
      if(res.ok){ const copy = res.clone(); caches.open(CACHE).then(c => c.put(new Request(url.pathname), copy)).catch(() => {}); }
      return res;
    }).catch(async () => (await caches.match(new Request(url.pathname)))
      || (req.mode === 'navigate' && (await caches.match('./index.html') || await caches.match('./')))
      || Response.error()));
    return;
  }
  // Bilder und Ähnliches: aus dem Zwischenspeicher, sonst aus dem Netz
  e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => {
    if(res.ok){ const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {}); }
    return res;
  })));
});
