/** Small delay between staggered server-side API bursts to reduce 429s from parallel fan-out. */
export const delay = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

function isRetryableError(error: unknown): boolean {
	if (!(error instanceof Error)) return false;
	const message = error.message.toLowerCase();
	return (
		message.includes('429') ||
		message.includes('too many requests') ||
		message.includes('failed to fetch') ||
		message.includes('network') ||
		message.includes('timeout') ||
		message.includes('503') ||
		message.includes('502')
	);
}

/**
 * Retries a loader a few times with exponential backoff (429 / transient failures).
 * Falls back to `fallback` so the page still renders.
 */
export async function withBackoff<T>(fn: () => Promise<T>, fallback: T, retries = 2): Promise<T> {
	for (let attempt = 0; attempt <= retries; attempt++) {
		try {
			return await fn();
		} catch (e) {
			const shouldRetry = attempt < retries && isRetryableError(e);
			if (!shouldRetry) {
				if (import.meta.env.DEV) {
					console.warn('[fetchWithBackoff] giving up after retries', e);
				}
				return fallback;
			}
			const backoff = 240 * Math.pow(2, attempt);
			const jitter = Math.floor(Math.random() * 120);
			await delay(backoff + jitter);
		}
	}
	return fallback;
}
