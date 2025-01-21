import type { NewsResponse } from '$lib/types/news/news';
const api_url = import.meta.env.VITE_API_URL;

export async function getTickerNews(ticker: string): Promise<NewsResponse> {
	try {
		const response = await fetch(`${api_url}/news/${ticker}`);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		return await response.json();
	} catch (error) {
		console.error('Error fetching ticker news:', error);
		throw error;
	}
}
