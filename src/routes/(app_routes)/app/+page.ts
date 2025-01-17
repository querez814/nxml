import type { PageLoad } from './$types';
import { frontPageNews } from '../../../api/media/generalnews';
export const load = (async () => {
	const data = await frontPageNews();
	return data;
}) satisfies PageLoad;
