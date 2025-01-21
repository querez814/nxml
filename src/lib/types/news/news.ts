export interface NewsResponse {
	ticker: string;
	news: News[];
	analystcoverage: AnalystCoverage[];
	valuation: Valuation;
}

export interface GeneralNewsResponse {
	news_url: string;
	image_url: string;
	title: string;
	text: string;
	source_name: string;
	date: string;
	topics: string[];
	sentiment: string;
	type: string;
	tickers: string[];
}

export interface News {
	news_url: string;
	image_url: string;
	title: string;
	text: string;
	source_name: string;
	date: string;
	topics: string[];
	sentiment: string;
	type: string;
	tickers: string[];
}

export interface AnalystCoverage {
	Type: string;
	Ticker: string;
	AnalystFirm: string;
	PreviousRating?: string | null;
	CurrentRating: string;
	PreviousPriceTarget?: string | null;
	CurrentPriceTarget?: string | null;
	Date: string;
}

export interface Valuation {
	fiscalDateEnding: string;
	symbol: string;
	evtosales: number;
	evtogrossprofit: number;
	evtoebit: number;
	evtoebitda: number;
	evtonetincome: number;
	revenue_per_share_ttm: number;
	price_to_sales_ratio_ttm: number;
	current_evtosales_ttm: number;
	current_price_to_sales_ratio_ttm: number;
	AnalystTargetPrice: number;
	AnalystRatingStrongBuy: number;
	AnalystRatingBuy: number;
	AnalystRatingHold: number;
	AnalystRatingSell: number;
	AnalystRatingStrongSell: number;
	TrailingPE: number;
	ForwardPE: number;
	Sector: string;
	Industry: string;
}
