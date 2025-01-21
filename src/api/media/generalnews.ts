const api_url = import.meta.env.VITE_API_URL;

export const frontPageNews = async (): Promise<any[]> => {
	const data = await fetch(`${api_url}/news/general`);
	if (!data.ok) {
		throw new Error('failed to fetch the front page news');
	}

	return data.json();
};
