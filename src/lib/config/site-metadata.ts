import {
    PUBLIC_API_URL,
    PUBLIC_BASE_APP_URL,
    PUBLIC_BASE_URL,
    PUBLIC_NODE_ENV
} from '$env/static/public'
import type { PricingFeature, TierFrequency } from '$lib/types';

const siteMetadata = {
    title: 'InvestorTerminal',
    author: 'InvestorTerminal',
    headerTitle: 'InvestorTerminal',
    description: '',
    theme: 'system', // system, dark or light
    locale: 'en-US',
    language: 'en-us',
    urls: {
        app: {
            api: PUBLIC_API_URL ?? "",
            base: PUBLIC_BASE_APP_URL ?? "",
        },
        web: {
            landing:  PUBLIC_BASE_URL ?? "",
            notFound: PUBLIC_BASE_URL ?? "",
            pricing: PUBLIC_BASE_URL ? ( PUBLIC_BASE_URL + '#pricing' ) : '#pricing',
            privacyPolicy: '/legal/privacy-policy',
            termsOfService: '/legal/terms-of-service',
        },
        auth: {
            signin: PUBLIC_NODE_ENV === 'development' ? 
                'https://strong-possum-2.accounts.dev/sign-in' : '#',
            signup: PUBLIC_NODE_ENV === 'development' ?
                'https://strong-possum-2.accounts.dev/sign-up' : '#',
            userProfile: PUBLIC_NODE_ENV === 'development' ?
                'https://strong-possum-2.accounts.dev/user' : '#',
            fallback: PUBLIC_BASE_URL
        },
        subscription: {
            portal: PUBLIC_NODE_ENV === 'development' ?
                'https://billing.stripe.com/p/login/test_5kA7stcTv74H1DW7ss' : '#',
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
        instagram: '',
    },
    subscriptionTiers: {
        early_adopter: {
            monthly: {
                link: PUBLIC_NODE_ENV === 'development' ?
                    'https://buy.stripe.com/test_28ocPt9t6eYBgpO6oo' : '#', 
                priceId: PUBLIC_NODE_ENV === 'development' ?
                    'price_1QZ9jRIXutq0kjUXUFf9Qrt9' : '#',
                price: 25,
                currency: 'USD',
                frequency: 'mo' as TierFrequency 
            },
        },
    },
}
  
export default siteMetadata; 