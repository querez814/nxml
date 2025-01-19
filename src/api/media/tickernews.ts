import type { NewsResponse } from '$lib/types/news/news';
const api_url = import.meta.env.VITE_API_URL;

export async function getTickerNews(ticker: string): Promise<NewsResponse> {
	try {
		const response = await fetch(`${api_url}/current/news/${ticker}`);
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		return await response.json();
	} catch (error) {
		console.error('Error fetching ticker news:', error);
		throw error;
	}
}

/*
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
	tickers: string[];
	image_url: string;
	description: string;
	keywords: string[];
	insights: Insight[];
	evtosales: number;
	evtogrossprofit: number;
	evtoebitda: number;
	evtonetincome: number;
	price_to_sales_ratio_ttm: number;
}

export const fetchTickerNews = async (ticker: string): Promise<MasterResponse[]> => {
	const response = await fetch(`${api_url}/current/news/${ticker}`);
	const data = (await response.json()) as MasterResponse[];
	return data;
};
*/
