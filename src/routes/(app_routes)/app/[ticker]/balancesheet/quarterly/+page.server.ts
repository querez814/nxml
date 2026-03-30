import type { PageServerLoad } from './$types';
import { fetchBalanceSheet } from '../../../../../../api/balancesheet/balancesheetdata';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const quarters = await fetchBalanceSheet(ticker);
		return { quarters };
	} catch {
		return { quarters: [] };
	}
}) satisfies PageServerLoad;
