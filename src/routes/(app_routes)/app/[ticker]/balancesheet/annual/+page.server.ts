import type { PageServerLoad } from './$types';
import { fetchBalanceSheetAnnual } from '../../../../../../api/balancesheet/balancesheetdata';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	try {
		const quarters = await fetchBalanceSheetAnnual(ticker);
		return { quarters };
	} catch {
		return { quarters: [] };
	}
}) satisfies PageServerLoad;
