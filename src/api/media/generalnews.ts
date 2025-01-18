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

export const frontPageNews = async (): Promise<any[]> => {
	const data = await fetch(`http://127.0.0.1:8000/current/newnew`);
	if (!data.ok) {
		throw new Error('failed to fetch the front page news');
	}

	return data.json();
};
