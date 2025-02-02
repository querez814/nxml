import type { PageLoad } from './$types';

export const load = (async ({ params }) => {
	let ticker = params.ticker;
	return { ticker };
}) satisfies PageLoad;
