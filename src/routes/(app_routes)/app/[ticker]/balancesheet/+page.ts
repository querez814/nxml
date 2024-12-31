import { fetchBalanceSheet } from '../../../../../api/balancesheet/balancesheetdata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchBalanceSheet(ticker);
	return { quarters };
}) satisfies PageLoad;
