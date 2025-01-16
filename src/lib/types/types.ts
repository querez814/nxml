export type PricingFeature = {
	name: string;
	included: boolean;
};
export type Trend = 'bullish' | 'bearish' | 'neutral';
export type Strength = 'weak' | 'moderate' | 'strong';
export type Signal = 'buy' | 'sell' | 'hold';
export type Status = 'oversold' | 'neutral' | 'overbought';
export type TierFrequency = 'mo' | 'yr' | 'once';

//Types for News Curation

export interface ttmDisplay {
	evtosales: number;
	evtogrossprofit: number;
	evtoebitda: number;
	evtonetincome: number;
	revenue_per_share_ttm: number;
	price_to_sales_ratio_ttm: number;
	AnalystTargetPrice: number;
	AnalystRatingStrongBuy: number;
	AnalystRatingBuy: number;
	AnalystRatingHold: number;
	AnalystRatingSell: number;
	AnalystRatingStrongSell: number;
}

export interface MarketSentiment {
	overall: string;
	score: number;
	confidence: string;
}

export interface SentimentDistribution {
	positive: number;
	neutral: number;
	negative: number;
}

export interface Summary {
	totalRelevantArticles: number;
	sentimentTrend: string;
	sentimentDistribution: SentimentDistribution;
	marketSentiment: MarketSentiment;
	keyTopics: string[];
}

export interface Article {
	title: string;
	url: string;
	publishedAt: string;
	source: string;
	summary: string;
	tickerRelevance: number;
	tickerSentiment: number;
	sentimentLabel: string;
	overallSentiment: string;
}

// we export this master type which contains what we need
export interface NewsCuration {
	ticker: string;
	ttm_display: ttmDisplay[];
	summary: Summary;
	top_articles: Article[];
	market_sentiment: MarketSentiment;
	sentiment_distribution: SentimentDistribution;
}

export interface Mover {
	ticker: string;
	price: string;
	changeAmount: string;
	changePercentage: string;
	volume: string;
}
