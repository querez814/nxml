import type { PageServerLoad } from './$types';
import { loadMarketSentimentStream } from '$lib/server/marketSentimentLoad';

export const load = (({ fetch }) => loadMarketSentimentStream(fetch)) satisfies PageServerLoad;
