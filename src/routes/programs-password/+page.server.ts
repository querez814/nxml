import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

const GATE_COOKIE = 'app_gate';

function grantGate(cookies: Parameters<PageServerLoad>[0]['cookies']): void {
	cookies.set(GATE_COOKIE, '1', {
		path: '/',
		httpOnly: true,
		secure: process.env.NODE_ENV === 'production',
		sameSite: 'lax',
		maxAge: 60 * 60 * 24 * 30
	});
}

// Access to the DDP app is now granted immediately. Any visit to this route
// sets the gate cookie and bounces the visitor straight into the app. The
// password form is preserved as a fallback so existing links don't break.
export const load: PageServerLoad = ({ cookies }) => {
	grantGate(cookies);
	redirect(303, '/app');
};

export const actions: Actions = {
	default: ({ cookies }) => {
		grantGate(cookies);
		redirect(303, '/app');
	}
};
