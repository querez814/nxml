import {
	PUBLIC_API_URL,
	PUBLIC_BASE_APP_URL,
	PUBLIC_BASE_URL,
	PUBLIC_NODE_ENV
} from '$env/static/public';
import type { PricingFeature, TierFrequency } from '$lib/types/types';

const siteMetadata = {
	title: 'Due Diligence',
	author: 'The Team :)',
	headerTitle: 'Due Diligence',
	description: '',
	theme: 'system',
	locale: 'en-US',
	language: 'en-us',
	urls: {
		app: {
			api: PUBLIC_API_URL ?? '',
			base: PUBLIC_BASE_APP_URL ?? ''
		},
		web: {
			landing: PUBLIC_BASE_URL ?? 'https://www.yourduediligence.app',
			notFound: PUBLIC_BASE_URL ?? '',
			pricing: PUBLIC_BASE_URL ? PUBLIC_BASE_URL + '#pricing' : '#pricing',
			privacyPolicy: '/legal/privacy-policy',
			termsOfService: '/legal/terms-of-service'
		},
		auth: {
			signin:
				PUBLIC_NODE_ENV === 'development'
					? 'https://strong-possum-2.accounts.dev/sign-in'
					: 'https://strong-possum-2.accounts.dev/sign-in',
			signup:
				PUBLIC_NODE_ENV === 'development'
					? 'https://strong-possum-2.accounts.dev/sign-up'
					: 'https://strong-possum-2.accounts.dev/sign-up',
			userProfile:
				PUBLIC_NODE_ENV === 'development'
					? 'https://strong-possum-2.accounts.dev/user'
					: 'https://strong-possum-2.accounts.dev/user',
			fallback: PUBLIC_BASE_URL
		},
		subscription: {
			portal:
				PUBLIC_NODE_ENV === 'development'
					? 'https://billing.stripe.com/p/login/test_5kA7stcTv74H1DW7ss'
					: '#'
		}
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
