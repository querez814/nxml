import { env } from '$env/dynamic/public';
import type { TierFrequency } from '$lib/types/types';

const publicBaseUrl = () => env.PUBLIC_BASE_URL ?? '';
const apiUrl = () =>
	(env.PUBLIC_API_URL as string | undefined) ||
	(import.meta.env.VITE_API_URL as string | undefined) ||
	'';
const baseAppUrl = () => (env.PUBLIC_BASE_APP_URL as string | undefined) ?? '';

const siteMetadata = {
	title: 'TZR Fund',
	author: 'The Team :)',
	headerTitle: 'TZR Fund',
	description: '',
	theme: 'system',
	locale: 'en-US',
	language: 'en-us',
	get urls() {
		const base = publicBaseUrl();
		return {
			app: {
				get api() {
					return apiUrl();
				},
				get base() {
					return baseAppUrl();
				}
			},
			web: {
				get landing() {
					return base || 'https://www.yourduediligence.app';
				},
				get notFound() {
					return base || '';
				},
				get pricing() {
					return base ? base + '#pricing' : '#pricing';
				},
				privacyPolicy: '/legal/privacy-policy',
				termsOfService: '/legal/terms-of-service'
			},
			auth: {
				signin: import.meta.env.DEV
					? 'https://strong-possum-2.accounts.dev/sign-in'
					: 'accounts.yourduediligence.app/sign-in',
				signup: import.meta.env.DEV
					? 'https://strong-possum-2.accounts.dev/sign-up'
					: 'accounts.yourduediligence.app/sign-up',
				userProfile: import.meta.env.DEV
					? 'https://strong-possum-2.accounts.dev/user'
					: 'https://accounts.yourduediligence.app/user',
				get fallback() {
					return base;
				}
			},
			subscription: {
				portal: import.meta.env.DEV
					? 'https://billing.stripe.com/p/login/test_5kA7stcTv74H1DW7ss'
					: '#'
			}
		};
	},
	social: {
		banner: '',
		mastodon: '',
		email: '',
		github: '',
		twitter: '',
		facebook: '',
		youtube: '',
		linkedin: '',
		threads: '',
		instagram: ''
	},
	subscriptionTiers: {
		premarket_subscription: {
			monthly: {
				link: '/app', // Force to app route
				priceId: 'test_price_id',
				price: 15,
				currency: 'USD',
				frequency: 'mo' as TierFrequency
			}
		}
	}
};

export default siteMetadata;
