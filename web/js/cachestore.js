// Cache Storage side of Sync. A cache is "complete" only once it contains META_KEY, which
// is written last by commit(); the newest complete cache is the active one. sw.js uses
// the same naming rules.

export const PREFIX = "quantquest-";
const META_KEY = "__meta.json";

const keyFor = (url) => new URL(url, document.baseURI).href;
const metaKey = () => keyFor(META_KEY);

async function completeCaches() {
  const names = (await caches.keys()).filter((n) => n.startsWith(PREFIX)).sort().reverse();
  const complete = [];
  for (const name of names) {
    if (await (await caches.open(name)).match(metaKey())) complete.push(name);
  }
  return complete;
}

export async function readActiveMeta() {
  const [name] = await completeCaches();
  if (!name) return null;
  const res = await (await caches.open(name)).match(metaKey());
  return res ? res.json() : null;
}

export function fetchNoStore(url) {
  return fetch(keyFor(url), { cache: "no-store" });
}

export function createStagingStore() {
  const name = `${PREFIX}${Date.now()}`;
  return {
    async stage(url, response) {
      await (await caches.open(name)).put(keyFor(url), response);
    },
    async commit(meta) {
      const cache = await caches.open(name);
      await cache.put(metaKey(), new Response(JSON.stringify(meta), {
        headers: { "Content-Type": "application/json" },
      }));
      for (const other of await caches.keys()) {
        if (other.startsWith(PREFIX) && other !== name) await caches.delete(other);
      }
    },
    async discard() {
      await caches.delete(name);
    },
  };
}
