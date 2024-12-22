import type { HandleClientError } from '@sveltejs/kit'
// To use Clerk components:
import { initializeClerkClient } from 'clerk-sveltekit/client'
// Or for headless mode:
// import { initializeClerkClient } from 'clerk-sveltekit/headless'
import { PUBLIC_CLERK_PUBLISHABLE_KEY } from '$env/static/public'

console.log(PUBLIC_CLERK_PUBLISHABLE_KEY)

initializeClerkClient(PUBLIC_CLERK_PUBLISHABLE_KEY, {
	afterSignInUrl: '/app/',
	afterSignUpUrl: '/app/',
	signInUrl: 'https://strong-possum-2.accounts.dev/sign-in',
	signUpUrl: 'https://strong-possum-2.accounts.dev/sign-up',
})

export const handleError: HandleClientError = async ({ error, event }) => {
	console.error(error, event)
}