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

// Base trend metrics interface
interface TrendMetrics {
	consistency: number;
	strength: number;
	direction: 'up' | 'down';
}

interface TrendAnalysis {
	consistency: number;
	macd_trend: TrendMetrics;
	aroon_trend: TrendMetrics;
	momentum_trend: TrendMetrics;
	stochastic_trend: TrendMetrics;
}

interface ComponentScores {
	macd: number;
	aroon: number;
	momentum: number;
	stochastic: number;
}

type MarketCondition =
	| 'STRONG_UPTREND'
	| 'STRONG_DOWNTREND'
	| 'MODERATE_UPTREND'
	| 'MODERATE_DOWNTREND'
	| 'CONSOLIDATION';

interface SymbolMomentum {
	symbol: string;
	date: string;
	momentum_score: number;
	market_condition: MarketCondition;
	trend_analysis: TrendAnalysis;
	component_scores: ComponentScores;
	period: string;
}

export interface MarketMomentum {
	[symbol: string]: SymbolMomentum;
}

/* Example of how to fetch and use these types:
async function fetchMarketMomentum(): Promise<MarketMomentum> {
  const response = await fetch('your-api-endpoint/marketmomentum');
  const data = await response.json();
  return data;
}

// Example usage with type safety
async function analyzeMomentum() {
  try {
    const marketData = await fetchMarketMomentum();
    
    // Access data with full type safety
    const spyMomentum = marketData.SPY.momentum_score;
    const qqQCondition = marketData.QQQ.market_condition;
    const diaTrend = marketData.DIA.trend_analysis.consistency;
    
    // TypeScript will ensure all properties exist and are of correct type
  } catch (error) {
    console.error('Failed to fetch market momentum:', error);
  }
}*/
