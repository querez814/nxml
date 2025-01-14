import type { CardType } from './types';

export interface MetricsResponse {
	pe_ratio: number;
	market_cap: number;
}

export interface ValuationResponse {}

export interface BalanceSheetResponse {}

export interface IncomeStatementResponse {}

export type CardDataResponse = {
	metrics: MetricsResponse;
	valuation: ValuationResponse;
	balance: BalanceSheetResponse;
	income: IncomeStatementResponse;
};

type Fetchers = {
	[K in CardType]: (ticker: string) => Promise<CardDataResponse[K]>;
};
