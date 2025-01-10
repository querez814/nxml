import {
	PUBLIC_API_URL,
	PUBLIC_BASE_APP_URL,
	PUBLIC_BASE_URL,
	PUBLIC_NODE_ENV
} from '$env/static/public';
import type { PricingFeature, TierFrequency } from '$lib/types';

// Force bypass in development mode
const BYPASS_STRIPE = true; // Changed to force bypass

const siteMetadata = {
	title: 'InvestorTerminal',
	author: 'InvestorTerminal',
	headerTitle: 'InvestorTerminal',
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
			landing: PUBLIC_BASE_URL ?? '',
			notFound: PUBLIC_BASE_URL ?? '',
			pricing: PUBLIC_BASE_URL ? PUBLIC_BASE_URL + '#pricing' : '#pricing',
			privacyPolicy: '/legal/privacy-policy',
			termsOfService: '/legal/terms-of-service'
		},
		auth: {
			// Force to app route in development
			signin: '/app',
			signup: '/app',
			userProfile: '/app',
			fallback: '/app'
		},
		subscription: {
			portal: '/app' // Force to app route
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
				price: 25,
				currency: 'USD',
				frequency: 'mo' as TierFrequency
			}
		}
	}
};

export default siteMetadata;
