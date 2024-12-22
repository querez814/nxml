import { fetchIncomeStatementMargins } from '../../../../api/incomesheet/incomedata';
import type { PageLoad } from './$types';

export const load = (async ({ params }) => {
	const ticker = params.ticker;
	const quarters = await fetchIncomeStatementMargins(ticker); // Fetch the first item
	return { quarters };
}) satisfies PageLoad;
