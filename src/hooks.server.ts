import { redirect, type Handle } from '@sveltejs/kit';

const GATE_COOKIE = 'app_gate';
const PROTECTED_PREFIX = '/app';

export const handle: Handle = ({ resolve, event }) => {
	if (event.url.pathname.startsWith(PROTECTED_PREFIX)) {
		const gate = event.cookies.get(GATE_COOKIE);
		if (gate !== '1') {
			redirect(302, '/');
		}
	}

	return resolve(event);
};
