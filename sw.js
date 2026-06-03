// 🍟 Lotto-Frite-Mayo — Service Worker
// Permet l'installation PWA et le fonctionnement hors-ligne

const CACHE_NAME = 'lotto-frite-mayo-v1';
const FILES = [
  './index.html',
  './stats.json',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png'
];

// Installation : mise en cache des fichiers de base
self.addEventListener('install', evt => {
  evt.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(FILES))
      .then(() => self.skipWaiting())
  );
});

// Activation : suppression des anciens caches
self.addEventListener('activate', evt => {
  evt.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch : réseau d'abord, cache en fallback (pour stats.json toujours frais)
self.addEventListener('fetch', evt => {
  // stats.json : toujours tenter le réseau d'abord
  if (evt.request.url.includes('stats.json')) {
    evt.respondWith(
      fetch(evt.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(evt.request, clone));
          return res;
        })
        .catch(() => caches.match(evt.request))
    );
    return;
  }
  // Autres fichiers : cache d'abord
  evt.respondWith(
    caches.match(evt.request)
      .then(cached => cached || fetch(evt.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(evt.request, clone));
          return res;
        })
      )
  );
});
