import type { Handle } from '@sveltejs/kit';

const GATE_COOKIE = 'app_gate';
const PROTECTED_PREFIX = '/app';

// Access to the DDP app is granted immediately. We still set the gate cookie
// so any downstream code that reads it keeps working, but visitors are no
// longer bounced to the password screen.
export const handle: Handle = ({ resolve, event }) => {
	if (event.url.pathname.startsWith(PROTECTED_PREFIX)) {
		const gate = event.cookies.get(GATE_COOKIE);
		if (gate !== '1') {
			event.cookies.set(GATE_COOKIE, '1', {
				path: '/',
				httpOnly: true,
				secure: process.env.NODE_ENV === 'production',
				sameSite: 'lax',
				maxAge: 60 * 60 * 24 * 30
			});
		}
	}

	return resolve(event);
};
