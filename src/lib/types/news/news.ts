export interface NewsResponse {
	ticker: string;
	count: number;
	news: NewsItem[];
	valuation: ValuationMetrics;
}

export interface NewsItem {
	id: string;
	publisher: {
		name: string;
		homepage_url: string;
		logo_url: string;
		favicon_url: string;
	};
	title: string;
	author: string;
	published_utc: string;
	article_url: string;
	tickers: string[];
	description: string;
	keywords: string[];
	insights: NewsInsight[];
	image_url: string;
}

export interface NewsInsight {
	ticker: string;
	sentiment: 'positive' | 'negative' | 'neutral';
	sentiment_reasoning: string;
}

export interface ValuationMetrics {
	fiscalDateEnding: string;
	symbol: string;
	evtosales: number;
	evtogrossprofit: number;
	evtoebit: number;
	evtoebitda: number;
	evtonetincome: number;
	revenue_per_share_ttm: number;
	price_to_sales_ratio_ttm: number;
	current_evtosales_ttm?: number;
	current_price_to_sales_ratio_ttm?: number;
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
