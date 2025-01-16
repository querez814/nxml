const api_url = import.meta.env.VITE_API_URL;
import type { NewsCuration } from '$lib/types/types';
export const fetchNewsData = async (ticker: string): Promise<NewsCuration> => {
	const response = await fetch(`${api_url}/financials/news/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch news data: ${response.statusText}`);
	}
	return response.json();
};
export const fetchNews = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/news/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch news data: ${response.statusText}`);
	}
	const rawData = await response.json();
	const topArticles = rawData.top_articles;
	return topArticles;
};

export const fetchSentiment = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/news/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch sentiment data: ${response.statusText}`);
	}
	const rawData = await response.json();
	const sentiment = rawData.market_sentiment;
	return sentiment;
};

export const fetchSummary = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/news/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch summary data: ${response.statusText}`);
	}
	const rawData = await response.json();
	const summary = rawData.summary;
	return summary;
};

export const fetchSentimentTrend = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/news/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch sentiment trend data: ${response.statusText}`);
	}
	const rawData = await response.json();
	const sentimentTrend = rawData.summary.sentiment_trend;
	return sentimentTrend;
};

export const fetchLatestPrice = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/news/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch latest price data: ${response.statusText}`);
	}
	const rawData = await response.json();
	const latestPrice = rawData.latest_price;
	return latestPrice;
};

export const fetchSentimentDistribution = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/financials/news/${ticker}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch sentiment distribution data: ${response.statusText}`);
	}
	const rawData = await response.json();
	const sentimentDistribution = rawData.sentiment_distribution;
	return sentimentDistribution;
};
