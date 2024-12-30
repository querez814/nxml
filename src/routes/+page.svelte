<script lang="ts">
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
	import SignedOut from 'clerk-sveltekit/client/SignedOut.svelte'
	import Button from '$lib/components/ui/button/button.svelte';
	import Spotlight from '$lib/components/ui/Spotlight/Spotlight.svelte';
	import { ArrowRight, Check, CircleCheck, Minus  } from 'lucide-svelte'

	import Card from '$lib/components/ui/card/card.svelte';
	import * as Accordion from "$lib/components/ui/accordion/index.js";
	import WebBanner from '$lib/components/web/web-banner.svelte';
	import WebHeader from '$lib/components/web/web-header.svelte';
	import FeatureSection from '$lib/components/web/feature-section.svelte';
	import AsSeenOn from '$lib/components/common/as-seen-on.svelte';
	import PricingCard from '$lib/components/common/pricing-card.svelte';
	import siteMetaData from '$lib/config/site-metadata';
	import WebFooter from '$lib/components/web/web-footer.svelte';
	import CtaCard from '$lib/components/web/cta-card.svelte';
	
	const learnMoreLink = "#features";

	const features = [
      { name: "5 users", included: true },
      { name: "20 projects", included: true },
      { name: "20GB storage", included: true },
      { name: "Priority support", included: true },
      { name: "Advanced analytics", included: false },
    ]


	const faq = [
		{
			question: "Is it accessible?",
			answer: "Yes. It adheres to the WAI-ARIA design pattern."
		},
		{
			question: "Is it styled?",
			answer: "Yes. It comes with default styles that matches the other components' aesthetic."
		},
		{
			question: "Is it animated?",
			answer: "Yes. It's animated by default, but you can disable it if you prefer."
		}
	]

	const appMainFeature = [
		{
		 	icon: null,
			description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
		},
		{
		 	icon: null,
			description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
		},
		{
		 	icon: null,
			description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
		},
		{
		 	icon: null,
			description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
		},
	]
</script>

<div class="flex flex-col  min-h-screen w-full items-center mx-auto gap-8">
	<div class="relative flex flex-col w-full [&>*:not(span)]:z-[999]">
		<Spotlight className="-top-40 left-0 md:left-60 md:-top-20" fill="gray" />	
		<span class="absolute -z-[999] inset-0 h-full w-full bg-background bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]" ></span>
		<div class="absolute h-full w-full bg-gradient-to-b from-transparent via-background/60 to-background"></div>
		
		<WebBanner>This bar serves as a means to notify visitors of important updates.</WebBanner>
		<WebHeader />

		<section class="flex flex-col gap-6 mb-12">
			<div class="flex flex-col">
				<h1 class="mt-16 md:px-16 pb-3 mb-0 relative z-10 bg-gradient-to-b  from-neutral-200 to-neutral-600 bg-clip-text text-center font-sans text-2xl font-semibold text-transparen md:text-5xl xl:text-6xl">
					Seize Market Opportunities <br/> with Immediate Insights
				</h1>
				<p class="my-3 text-base  md:text-lg text-foreground/50 leading-snug tracking-tight text-center max-w-md md:!max-w-[40rem] mx-auto px-6">
					Cut through market noise with data that matters. Our terminal provides the essential insights you need to make informed, strategic investment decisions.
				</p>
			</div>
			<div class="flex flex-col items-center mx-auto">
				<div class="flex flex-col items-center md:flex-row gap-4">
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
				<p class="text-[0.815rem] text-center py-4">Lorem ipsum damut, lorem ipsum damut</p>
				<AsSeenOn />
			 </div>
		</section>
	</div>
	<!-- this is a comment! -->
	<section id="features" class="flex flex-wrap justify-around gap-24 py-12">
		{#each appMainFeature as { icon, description }}
			<FeatureSection>
				{ description }
			</FeatureSection>
		{/each}
	</section>
	<!-- this is a comment! -->
	<section id="pricing" class="flex flex-col gap-4 items-center w-full px-6 md:px-20 py-12">
		<h3 class="mt-16 mx-2 md:px-16 pb-3 mb-10 relative z-10 bg-gradient-to-b  from-neutral-200 to-neutral-600 bg-clip-text text-center font-sans text-3xl md:text-4xl font-semibold text-transparent ">
			Simple and Transparent Pricing
		</h3>
		<div class="flex flex-row flex-wrap justify-center gap-32">
			<SignedOut>
				{#each Object.entries(siteMetaData.subscriptionTiers) as [planType, planDetails]}
					<PricingCard 
						tierName={planType} 
						features={features} 
						tierPrice={planDetails.monthly.price} 
						tierFrequency={planDetails.monthly.frequency }  
						buttonText="Log In to Purchase" 
						buttonLink={siteMetaData.urls.auth.signin} 
					/>
				{/each}
			</SignedOut>
			<SignedIn>
				{#each Object.entries(siteMetaData.subscriptionTiers) as [planType, planDetails]}
					<PricingCard 
						tierName={planType} 
						features={features} 
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
	<!-- this is a comment! -->
	<section id="faq" class="flex flex-col gap-6 items-center w-full px-6 md:px-20 py-12">
		<h3 class="mt-16 px-16 pb-3 mb-0 relative z-10 bg-gradient-to-b  from-neutral-200 to-neutral-600 bg-clip-text text-center font-sans text-4xl font-semibold text-transparent ">
			Frequently Asked Questions
		</h3>
		<Accordion.Root class="w-full  max-w-4xl px-2">
			{#each faq as { question, answer }}
				<Accordion.Item value={question} class="box-content" >
					<Accordion.Trigger>{question}</Accordion.Trigger>
					<Accordion.Content>{answer}</Accordion.Content>
				</Accordion.Item>
			{/each}
		</Accordion.Root>
	</section>
	<!-- this is a comment! -->
	<section id="cta" class="flex justify-center w-full px-6 md:px-20 py-16">
		<CtaCard />
	</section>
	
	<WebFooter />
</div>