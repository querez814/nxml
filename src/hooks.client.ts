import type { HandleClientError } from '@sveltejs/kit';
// To use Clerk components:
import { initializeClerkClient } from 'clerk-sveltekit/client';
// Or for headless mode:
// import { initializeClerkClient } from 'clerk-sveltekit/headless'
import { PUBLIC_CLERK_PUBLISHABLE_KEY } from '$env/static/public';
import siteMetaData from '$lib/config/site-metadata';

initializeClerkClient(PUBLIC_CLERK_PUBLISHABLE_KEY, {
	// NOTE: Looks like it adds this to query params in the base url need to make such handle it for now it is blank
	afterSignInUrl: 'https://www.yourduediligence.app/app', //siteMetaData.urls.app.base,
	afterSignUpUrl: 'https://www.yourduediligence.app', //siteMetaData.urls.app.base,
	signInUrl: siteMetaData.urls.auth.signin,
	signUpUrl: siteMetaData.urls.auth.signup
});

export const handleError: HandleClientError = async ({ error, event }) => {
	console.error(error, event);
};
