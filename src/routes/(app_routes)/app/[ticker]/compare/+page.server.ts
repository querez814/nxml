import type { PageServerLoad } from './$types';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	return { ticker };
}) satisfies PageServerLoad;
