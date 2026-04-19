import { redirect, fail } from '@sveltejs/kit';
import { timingSafeEqual } from 'crypto';
import { env as privateEnv } from '$env/dynamic/private';
import type { Actions } from './$types';

const GATE_COOKIE = 'app_gate';

/** Last resort if neither ``APP_GATE_PASS`` nor legacy ``APP_GATE_PASSWORD`` is set. */
const DEFAULT_GATE_PASSWORD = 'yXtFund70#';

/** In a ``.env`` file, ``#`` starts a comment unless the value is quoted, e.g. ``APP_GATE_PASS="yXtFund70#"``. */
function expectedGateSecret(): string {
	const fromPass =
		privateEnv.APP_GATE_PASS?.trim() || process.env.APP_GATE_PASS?.trim();
	const fromLegacy =
		privateEnv.APP_GATE_PASSWORD?.trim() || process.env.APP_GATE_PASSWORD?.trim();
	return fromPass || fromLegacy || DEFAULT_GATE_PASSWORD;
}

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const password = data.get('password');

		if (typeof password !== 'string' || !password) {
			return fail(400, { error: 'Password is required.' });
		}

		const expected = expectedGateSecret();

		const a = Buffer.from(password, 'utf-8');
		const b = Buffer.from(expected, 'utf-8');
		const valid = a.length === b.length && timingSafeEqual(a, b);

		if (!valid) {
			return fail(401, { error: 'Incorrect password.' });
		}

		cookies.set(GATE_COOKIE, '1', {
			path: '/',
			httpOnly: true,
			secure: process.env.NODE_ENV === 'production',
			sameSite: 'lax',
			maxAge: 60 * 60 * 24 * 30
		});

		redirect(303, '/app');
	}
};
