<script lang="ts">
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte';
	import SignedOut from 'clerk-sveltekit/client/SignedOut.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import Spotlight from '$lib/components/ui/Spotlight/Spotlight.svelte';
	import { ArrowRight, Check, CircleCheck, Minus } from 'lucide-svelte';

	import Card from '$lib/components/ui/card/card.svelte';
	import * as Accordion from '$lib/components/ui/accordion/index.js';
	import WebBanner from '$lib/components/web/web-banner.svelte';
	import WebHeader from '$lib/components/web/web-header.svelte';
	import FeatureSection from '$lib/components/web/feature-section.svelte';
	import AsSeenOn from '$lib/components/common/as-seen-on.svelte';
	import PricingCard from '$lib/components/common/pricing-card.svelte';
	import siteMetaData from '$lib/config/site-metadata';
	import WebFooter from '$lib/components/web/web-footer.svelte';
	import CtaCard from '$lib/components/web/cta-card.svelte';

	const learnMoreLink = '#features';

	const features = [
		{ name: '5 users', included: true },
		{ name: '20 projects', included: true },
		{ name: '20GB storage', included: true },
		{ name: 'Priority support', included: true },
		{ name: 'Advanced analytics', included: false }
	];

	const faq = [
		{
			question: 'Is it accessible?',
			answer: 'Yes. It adheres to the WAI-ARIA design pattern.'
		},
		{
			question: 'Is it styled?',
			answer: "Yes. It comes with default styles that matches the other components' aesthetic."
		},
		{
			question: 'Is it animated?',
			answer: "Yes. It's animated by default, but you can disable it if you prefer."
		}
	];

	const appMainFeature = [
		{
			icon: null,
			description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
		},
		{
			icon: null,
			description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
		},
		{
			icon: null,
			description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
		},
		{
			icon: null,
			description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
		}
	];
</script>

<div class="mx-auto flex min-h-screen w-full flex-col items-center gap-8">
	<div class="relative flex w-full flex-col [&>*:not(span)]:z-[999]">
		<Spotlight className="-top-40 left-0 md:left-60 md:-top-20" fill="gray" />
		<span
			class="absolute inset-0 -z-[999] h-full w-full bg-background bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"
		></span>
		<div
			class="absolute h-full w-full bg-gradient-to-b from-transparent via-background/60 to-background"
		></div>

		<WebBanner>This bar serves as a means to notify visitors of important updates.</WebBanner>
		<WebHeader />

		<section class="mb-12 flex flex-col gap-6">
			<div class="flex flex-col">
				<h1
					class="text-transparen relative z-10 mb-0 mt-16 bg-gradient-to-b from-neutral-200 to-neutral-600 bg-clip-text pb-3 text-center font-sans text-2xl font-semibold md:px-16 md:text-5xl xl:text-6xl"
				>
					Seize Market Opportunities <br /> with Immediate Insights
				</h1>
				<p
					class="mx-auto my-3 max-w-md px-6 text-center text-base leading-snug tracking-tight text-foreground/50 md:!max-w-[40rem] md:text-lg"
				>
					Cut through market noise with data that matters. Our terminal provides the essential
					insights you need to make informed, strategic investment decisions.
				</p>
			</div>
			<div class="mx-auto flex flex-col items-center">
				<div class="flex flex-col items-center gap-4 md:flex-row">
					<SignedOut>
						<a href={siteMetaData.urls.auth.signup}>
							<Button size="sm" class="px-6 hover:text-foreground">
								Start Making Data-Driven Decisions Today
							</Button>
						</a>
					</SignedOut>
					<SignedIn>
						<a href={siteMetaData.urls.app.base}>
							<Button size="sm" variant="default" class="px-6 hover:text-foreground">
								Go to the Terminal
							</Button>
						</a>
					</SignedIn>
					<a href={learnMoreLink}>
						<Button size="sm" variant="secondary" class="gap-2 px-6">
							Learn more
							<ArrowRight size={18} />
						</Button>
					</a>
				</div>
				<p class="py-4 text-center text-[0.815rem]">Lorem ipsum damut, lorem ipsum damut</p>
				<AsSeenOn />
			</div>
		</section>
	</div>
	<!-- this is a comment! -->
	<section id="features" class="flex flex-wrap justify-around gap-24 py-12">
		{#each appMainFeature as { icon, description }}
			<FeatureSection>
				{description}
			</FeatureSection>
		{/each}
	</section>
	<!-- this is a comment! -->
	<section id="pricing" class="flex w-full flex-col items-center gap-4 px-6 py-12 md:px-20">
		<h3
			class="relative z-10 mx-2 mb-10 mt-16 bg-gradient-to-b from-neutral-200 to-neutral-600 bg-clip-text pb-3 text-center font-sans text-3xl font-semibold text-transparent md:px-16 md:text-4xl"
		>
			Simple and Transparent Pricing
		</h3>
		<div class="flex flex-row flex-wrap justify-center gap-32">
			<SignedOut>
				{#each Object.entries(siteMetaData.subscriptionTiers) as [planType, planDetails]}
					<PricingCard
						tierName={planType}
						{features}
						tierPrice={planDetails.monthly.price}
						tierFrequency={planDetails.monthly.frequency}
						buttonText="Log In to Purchase"
						buttonLink={siteMetaData.urls.auth.signin}
					/>
				{/each}
			</SignedOut>
			<SignedIn>
				{#each Object.entries(siteMetaData.subscriptionTiers) as [planType, planDetails]}
					<PricingCard
						tierName={planType}
						{features}
						tierPrice={planDetails.monthly.price}
						tierFrequency={planDetails.monthly.frequency}
						buttonText="Start Free Trial"
						buttonLink={planDetails.monthly.link}
					/>
				{/each}
			</SignedIn>
		</div>
		<AsSeenOn />
	</section>
	<!-- this is aomment! -->
	<section id="faq" class="flex w-full flex-col items-center gap-6 px-6 py-12 md:px-20">
		<h3
			class="relative z-10 mb-0 mt-16 bg-gradient-to-b from-neutral-200 to-neutral-600 bg-clip-text px-16 pb-3 text-center font-sans text-4xl font-semibold text-transparent"
		>
			Frequently Asked Questions
		</h3>
		<Accordion.Root class="w-full  max-w-4xl px-2">
			{#each faq as { question, answer }}
				<Accordion.Item value={question} class="box-content">
					<Accordion.Trigger>{question}</Accordion.Trigger>
					<Accordion.Content>{answer}</Accordion.Content>
				</Accordion.Item>
			{/each}
		</Accordion.Root>
	</section>
	<!-- this is a comment! -->
	<section id="cta" class="flex w-full justify-center px-6 py-16 md:px-20">
		<CtaCard />
	</section>

	<WebFooter />
</div>
