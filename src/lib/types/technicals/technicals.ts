import type { MasterResponse } from './technicalinterfaces';
const api_url = import.meta.env.VITE_API_URL;

export const fetchTechnicals = async (
	ticker: string,
	interval: string
): Promise<MasterResponse> => {
	const response = await fetch(`${api_url}/technicals/technical-analysis/${interval}/${ticker}`);

	if (!response.ok) {
		throw new Error(`HTTP error! status: ${response.status}`);
	}

	const data = await response.json();
	return data as MasterResponse;
};
