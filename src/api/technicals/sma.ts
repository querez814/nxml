const api_url = import.meta.env.VITE_API_URL;

export const fetchDailySMA = async (ticker: string): Promise<any[]> => {
	const response = await fetch(`${api_url}/technicals/smas/${ticker}`);

	const rawData = await response.json();

	return rawData;
};
