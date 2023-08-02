const CACH_NAME = 'my-cache-v1';
const urlsToCache = [
	'/static/js/chat.js'
]

self.addEventListener('install', event => {
	event.waitUntil(
		caches.open(CACHE_NAME)
		.then(cache => cache.addAll(urlsToCache))
	);
});

self.addEventListener('activate', event => {
	event.waitUntil(
		caches.keys().then(cacheNames => {
			return Promise.all(
				cacheNames.map(cacheName => {
					if (cacheName !== CACHE_NAME) {
						return caches.delete(cacheName);
					}
				})
			)
		})
	)
})

self.addEventListener('fetch', event => {
	event.respondWith(
		caches.match(event.request)
		.then(response => {
			return response || fetch(event.request);
		})
	);
});

self.addEventListener('push', event => {
	const payload = event.data.json();
	const title = payload.title || 'Default payload title';
	const options = {
		body: payload.body,
		icon: payload.icon
	}

	event.waitUntil(
		self.registration.showNotification(title, options)
	);
});