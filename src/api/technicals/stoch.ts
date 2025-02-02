const api_url = import.meta.env.VITE_API_URL;

export const fetchDailyStoch = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/technicals/stochastic/${ticker}`);
	const rawData = await response.json();

	return rawData;
};
