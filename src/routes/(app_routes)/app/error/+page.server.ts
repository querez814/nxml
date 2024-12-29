import { error } from '@sveltejs/kit';

export function load() {
	error(420, 'Big Scary Error');
}
