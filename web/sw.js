// Cache-first from the newest complete "quantquest-*" cache (see js/cachestore.js).
// Falls through to the network when nothing is cached (e.g. before the first Sync).

const PREFIX = "quantquest-";
const META_URL = new URL("__meta.json", self.registration.scope).href;
const ROOT_URL = new URL("./", self.registration.scope).href;

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

async function activeCache() {
  const names = (await caches.keys()).filter((n) => n.startsWith(PREFIX)).sort().reverse();
  for (const name of names) {
    const cache = await caches.open(name);
    if (await cache.match(META_URL)) return cache;
  }
  return null;
}

async function respond(request) {
  const cache = await activeCache();
  if (cache) {
    const hit =
      (await cache.match(request, { ignoreSearch: true })) ||
      (request.mode === "navigate" ? await cache.match(ROOT_URL) : undefined);
    if (hit) return hit;
  }
  return fetch(request);
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET" || new URL(request.url).origin !== self.location.origin) return;
  // Sync fetches with cache: "no-store" and must reach the network, never the cache.
  if (request.cache === "no-store") return;
  event.respondWith(respond(request));
});
