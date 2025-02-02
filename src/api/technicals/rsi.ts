const api_url = import.meta.env.VITE_API_URL;

export const fetchDailyRSI = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/technicals/rsi/${ticker}`);

	const rawData = await response.json();

	return rawData;
};
