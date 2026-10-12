// Sync commit/rollback decision. No DOM, no Cache API: the storage is injected.
//
// store: {
//   stage(url, response)  write one fetched response into the new (uncommitted) cache
//   commit(meta)          make the new cache the active one and delete the old
//   discard()             throw the new cache away; the old one stays active
// }
// fetchFn(url) must return a fetch-like Response (ok, json(), clone()).

export async function performSync({ fetchFn, store, now = () => new Date() }) {
  try {
    const bundleRes = await get(fetchFn, "cards.json");
    const bundle = await bundleRes.clone().json();
    if (!bundle || !Array.isArray(bundle.cards) || !Array.isArray(bundle.graphs)) {
      throw new Error("cards.json is malformed");
    }
    const shellRes = await get(fetchFn, "shell.json");
    const shell = await shellRes.clone().json();
    if (!Array.isArray(shell)) throw new Error("shell.json is malformed");

    await store.stage("cards.json", bundleRes);
    await store.stage("shell.json", shellRes);
    for (const url of [...shell, ...bundle.graphs]) {
      await store.stage(url, await get(fetchFn, url));
    }
    const meta = { syncedAt: now().toISOString(), count: bundle.cards.length };
    await store.commit(meta);
    return { ok: true, meta };
  } catch (error) {
    await store.discard();
    return { ok: false, error };
  }
}

async function get(fetchFn, url) {
  const res = await fetchFn(url);
  if (!res || !res.ok) throw new Error(`Failed to fetch ${url}`);
  return res;
}
