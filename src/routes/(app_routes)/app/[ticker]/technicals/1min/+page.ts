import { fetchTechnicals } from '$lib/types/technicals/technicals';
import type { PageLoad } from '../../$types';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const interval = '1min';
	const response = await fetchTechnicals(interval, ticker);
	const data = response.data;
	return { data };
}) satisfies PageLoad;
