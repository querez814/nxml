import { fetchBalanceSheetRatios } from '../../../../api/balancesheet/balancesheetdata';
import type { PageLoad } from './$types';
export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchBalanceSheetRatios(ticker); // Fetch the first item
	return { quarters };
}) satisfies PageLoad;
