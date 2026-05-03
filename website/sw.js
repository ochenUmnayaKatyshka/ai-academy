// Service Worker for AI Academy
const CACHE_NAME = 'ai-academy-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/materials.html',
  '/css/style.css',
  '/js/app.js',
  // Add other assets as needed
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});