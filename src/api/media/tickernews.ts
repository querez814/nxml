const api_url = import.meta.env.VITE_API_URL;

export interface Publisher {
	name: string;
	homepage_url: string;
	logo_url: string;
	favicon_url: string;
}

export interface Insight {
	ticker: string;
	sentiment: string;
	sentiment_reasoning: string;
}

export interface MasterResponse {
	id: string;
	publisher: Publisher;
	title: string;
	author: string;
	published_utc: string;
	article_url: string;
	tickers: string[]; // Array of ticker symbols
	image_url: string;
	description: string;
	keywords: string[]; // Array of keyword strings
	insights: Insight[]; // Array of insights
}

export const fetchTickerNews = async (ticker: string): Promise<MasterResponse[]> => {
	const response = await fetch(`${api_url}/current/news/${ticker}`);
	const data = (await response.json()) as MasterResponse[];
	return data;
};
