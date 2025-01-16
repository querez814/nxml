import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { fetchTechnicals } from '$lib/types/technicals/technicals';

export const load: PageLoad = async ({ params }) => {
	try {
		const technicalData = await fetchTechnicals(params.ticker, 'daily');
		return {
			technicalData
		};
	} catch (err) {
		throw error(500, 'Failed to load technical data');
	}
};
