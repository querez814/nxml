type CacheEntry<T> = {
	expiresAt: number;
	value: T;
};

const inFlight = new Map<string, Promise<unknown>>();
const shortCache = new Map<string, CacheEntry<unknown>>();

/** In-memory single-flight + short TTL cache for identical concurrent fetches (browser + SSR). */
export async function dedupeRequest<T>(
	key: string,
	producer: () => Promise<T>,
	ttlMs = 3500
): Promise<T> {
	const now = Date.now();
	const cached = shortCache.get(key);
	if (cached && cached.expiresAt > now) {
		return cached.value as T;
	}

	const active = inFlight.get(key);
	if (active) {
		return active as Promise<T>;
	}

	const task = producer()
		.then((value) => {
			shortCache.set(key, { value, expiresAt: Date.now() + ttlMs });
			return value;
		})
		.finally(() => {
			inFlight.delete(key);
		});

	inFlight.set(key, task as Promise<unknown>);
	return task;
}
