import { redirect, fail } from '@sveltejs/kit';
import { timingSafeEqual } from 'crypto';
import type { Actions } from './$types';

const GATE_COOKIE = 'app_gate';

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const password = data.get('password');

		if (typeof password !== 'string' || !password) {
			return fail(400, { error: 'Password is required.' });
		}

		const expected = process.env.APP_GATE_PASSWORD ?? '';
		if (!expected) {
			return fail(500, { error: 'Gate not configured.' });
		}

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
