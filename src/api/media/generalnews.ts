const api_url = import.meta.env.VITE_API_URL;

export interface News {
	title: string;
	publisher: string;
	providerPublishTime: string;
	relatedTickers: RelatedTickers;
	mediaUrl: MediaURL[];
}

interface RelatedTickers {
	ticker1: string;
	ticker2: string;
}

interface MediaURL {
	resolutions: Resolutions[];
}

interface Resolutions {
	resolution_1: ResSubsection;
	resolution_2: ResSubsection;
}

interface ResSubsection {
	url: string;
	width: number;
	height: number;
	tag: string;
}

export const frontPageNews = async (): Promise<News> => {
	const data = await fetch(`${api_url}/current/newnew`);
	if (!data.ok) {
		throw new Error('failed to fetch the front page news');
	}

	return data.json();
};
