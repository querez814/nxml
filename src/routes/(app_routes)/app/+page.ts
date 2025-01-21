import type { PageLoad } from './$types';
import { frontPageNews } from '../../../api/media/generalnews';
export const load = (async () => {
	const news = await frontPageNews();

	return { news };
}) satisfies PageLoad;
