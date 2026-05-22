import type { PageServerLoad } from './$types';
import { fetchIncomeStatement, fetchIncomeStatementAnnual } from '../../../../api/incomesheet/incomedata';
import { fetchBalanceSheet, fetchBalanceSheetAnnual } from '../../../../api/balancesheet/balancesheetdata';
import { fetchCashFlow, fetchCashFlowAnnual } from '../../../../api/cashflowsheet/cashflowdata';
import { fetchValuation, fetchValuationLayout } from '../../../../api/valuation/valuationdata';
import { fetchNewsRecapTicker } from '$lib/api/newsRecap';
import siteMetadata from '$lib/config/site-metadata';
import { withBackoff } from '$lib/server/fetchWithBackoff';

export const load = (async ({ params, fetch }) => {
	const startedAt = Date.now();
	const ticker = (params.ticker ?? '').trim();
	const api = siteMetadata.urls.app.api;

	const [
		incomeQuarters,
		balanceQuarters,
		cashQuarters,
		valuationQuarters,
		layout,
		incomeAnnual,
		balanceAnnual,
		cashAnnual
	] = await Promise.all([
		withBackoff(() => fetchIncomeStatement(ticker), []),
		withBackoff(() => fetchBalanceSheet(ticker), []),
		withBackoff(() => fetchCashFlow(ticker), []),
		withBackoff(() => fetchValuation(ticker), []),
		withBackoff(() => fetchValuationLayout(ticker), null),
		withBackoff(() => fetchIncomeStatementAnnual(ticker), []),
		withBackoff(() => fetchBalanceSheetAnnual(ticker), []),
		withBackoff(() => fetchCashFlowAnnual(ticker), [])
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
		incomeAnnual,
		balanceQuarters,
		balanceAnnual,
		cashQuarters,
		cashAnnual,
		valuationQuarters,
		streamed: {
			newsRecap: newsRecapPromise
		},
		serverTimingsMs: {
			total: Date.now() - startedAt
		}
	};
}) satisfies PageServerLoad;
