import type { PageServerLoad } from './$types';
import { fetchIncomeStatement } from '../../../../api/incomesheet/incomedata';
import { fetchBalanceSheet } from '../../../../api/balancesheet/balancesheetdata';
import { fetchCashFlow } from '../../../../api/cashflowsheet/cashflowdata';
import { fetchValuation, fetchValuationLayout } from '../../../../api/valuation/valuationdata';
import { fetchNewsRecapTicker } from '$lib/api/newsRecap';
import siteMetadata from '$lib/config/site-metadata';
import { withBackoff } from '$lib/server/fetchWithBackoff';

export const load = (async ({ params, fetch }) => {
	const startedAt = Date.now();
	const ticker = (params.ticker ?? '').trim();
	const api = siteMetadata.urls.app.api;

	/* Critical path only: reduce first-render latency and AV burst pressure. */
	const [incomeQuarters, balanceQuarters, cashQuarters, valuationQuarters, layout] = await Promise.all([
		withBackoff(() => fetchIncomeStatement(ticker), []),
		withBackoff(() => fetchBalanceSheet(ticker), []),
		withBackoff(() => fetchCashFlow(ticker), []),
		withBackoff(() => fetchValuation(ticker), []),
		withBackoff(() => fetchValuationLayout(ticker), null)
	]);

	const valuationSnapshot =
		Array.isArray(valuationQuarters) && valuationQuarters.length > 0 ? valuationQuarters[0] : null;

	const newsRecapPromise = ticker
		? fetchNewsRecapTicker(fetch, api, ticker)
		: Promise.resolve(null);

	return {
		ticker,
		layout,
		valuationSnapshot,
		incomeQuarters,
		/* Deferred on first navigation to keep ticker transitions fast. */
		incomeAnnual: [],
		balanceQuarters,
		balanceAnnual: [],
		cashQuarters,
		cashAnnual: [],
		valuationQuarters,
		streamed: {
			newsRecap: newsRecapPromise
		},
		serverTimingsMs: {
			total: Date.now() - startedAt
		}
	};
}) satisfies PageServerLoad;
