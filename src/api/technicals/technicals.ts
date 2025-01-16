const api_url = import.meta.env.VITE_API_URL;

export const fetchTechnicals = async (ticker: string, interval: string): Promise<any[]> => {
	const url = `${api_url}/technicals/technical-analysis/${interval}/${ticker}`;
	const response = await fetch(url);
	const rawData = await response.json();
	console.log(rawData);

	return rawData;
};
