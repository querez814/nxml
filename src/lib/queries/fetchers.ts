import type { CardType } from './types';

const api_url = import.meta.env.VITE_API_URL;

export const fetchers = {
	metrics: async (ticker: string) => {
		const response = await fetch(`${api_url}/metrics/${ticker}`);
		if (!response.ok) throw new Error('Failed to fetch metrics');
		return response.json();
	},

	valuation: async (ticker: string) => {
		const response = await fetch(`${api_url}/valuation/${ticker}`);
		if (!response.ok) throw new Error('Failed to fetch valuation');
		return response.json();
	}
};
