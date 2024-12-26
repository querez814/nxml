<script lang="ts">
	import '../app.css';
	import SignIn from 'clerk-sveltekit/client/SignIn.svelte'
	import SignUp from 'clerk-sveltekit/client/SignUp.svelte'
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte'
	import SignedOut from 'clerk-sveltekit/client/SignedOut.svelte'
	import SignOutButton from 'clerk-sveltekit/client/SignOutButton.svelte'
	import SignInButton from 'clerk-sveltekit/client/SignInButton.svelte'
	import SignUpButton from 'clerk-sveltekit/client/SignUpButton.svelte'
	import UserButton from 'clerk-sveltekit/client/UserButton.svelte'
	import ThemeToggle from '../lib/components/common/theme-toggle.svelte'
	import DarkBannerDots from '$lib/components/common/dark-banner-dots.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import Spotlight from '$lib/components/ui/Spotlight/Spotlight.svelte';
	import { ArrowRight, Check, CircleCheck, Minus  } from 'lucide-svelte'
	import HackerNews from '$lib/../media/images/hacker-news-logo-white.webp';
	import ProductHunt from '$lib/../media/images/product-hunt-logo-horizontal-white.avif';
	import FeatureIcon from '$lib/components/common/feature-icon.svelte';
	import Card from '$lib/components/ui/card/card.svelte';
	import * as Accordion from "$lib/components/ui/accordion/index.js";
	import PricingCard from '$lib/components/common/pricing-card.svelte';
	import Badge from '$lib/components/ui/badge/badge.svelte';
	import { Separator } from "$lib/components/ui/separator/index.js";
	import WebBanner from '$lib/components/web/web-banner.svelte';
	import WebHeader from '$lib/components/web/web-header.svelte';
	import FeatureSection from '$lib/components/web/feature-section.svelte';

	const features = [
      { name: "5 users", included: true },
      { name: "20 projects", included: true },
      { name: "20GB storage", included: true },
      { name: "Priority support", included: true },
      { name: "Advanced analytics", included: false },
    ]
</script>

<div class="flex flex-col  min-h-screen w-full items-center mx-auto gap-8">

	<div class="relative flex flex-col w-full [&>*:not(span)]:z-[999]">
		<Spotlight className="-top-40 left-0 md:left-60 md:-top-20" fill="gray" />	
		<span class="absolute -z-[999] inset-0 h-full w-full bg-background bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]" ></span>
		<div class="absolute h-full w-full bg-gradient-to-b from-transparent via-background/60 to-background"></div>
		<!-- this is a comment! -->
		<WebBanner>
			This bar serves as a means to notify visitors of important updates.
		</WebBanner>
		<!-- this is a comment! -->
		<WebHeader />
		<!-- this is a comment! -->
		<section class="flex flex-col gap-6 mb-12">
			<div class="flex flex-col">
				<h1 class="mt-16 px-16 pb-3 mb-0 relative z-10 bg-gradient-to-b  from-neutral-200 to-neutral-600 bg-clip-text text-center font-sans text-lg font-semibold text-transparent md:text-6xl">
					Seize Market Opportunities <br/> with Immediate Insights
				</h1>
				<p class="my-3 text-lg text-foreground/50 leading-snug tracking-tight text-center max-w-[38rem] mx-auto">
					Cut through market noise with data that matters. Our terminal provides the essential insights you need to make informed, strategic investment decisions.
				</p>
			</div>
			<div class="flex flex-col items-center mx-auto">
				<div class="flex flex-row gap-4">
					<SignedOut>
						<Button size="sm" class="px-6">
							Start Making Data-Driven Decisions Today
						</Button>
					</SignedOut>
					<SignedIn>
						<Button size="sm" variant="default" class="px-6">
							Go to the Terminal
						</Button>
					</SignedIn>
					<Button size="sm" variant="secondary" class="gap-2 px-6">
						Learn more
						<ArrowRight size={18} />
					</Button>
				</div>
				<p class="text-[0.815rem] text-center py-4">Lorem ipsum damut, lorem ipsum damut</p>
				<div class="flex items-center gap-4 my-6">
					<span class="font-semibold text-sm tracking-wide text-foreground/75">As seen on:</span>
					<div class="flex items-center gap-2 opacity-65">
						<img class="h-5" src={HackerNews} alt="">
						<img class="h-[2.825rem]" src={ProductHunt} alt="">
					</div>
				</div>
			 </div>
		</section>
	</div>

	<section class="flex flex-wrap justify-around gap-24 py-12">
		<FeatureSection>
			Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
		</FeatureSection>
		<FeatureSection>
			Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
		</FeatureSection>
		<FeatureSection>
			Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
		</FeatureSection>
	</section>

	<section  class="flex flex-col gap-4 items-center w-full px-20 py-12">
		<h3 class="mt-16 px-16 pb-3 mb-10 relative z-10 bg-gradient-to-b  from-neutral-200 to-neutral-600 bg-clip-text text-center font-sans text-4xl font-semibold text-transparent ">
			Simple and Transparent Pricing
		</h3>
		<div class="flex flex-row flex-wrap gap-32">
			<Card class="p-4 w-72 bg-muted/60 border-foreground/25 hover:shadow hover:shadow-foreground/50">
				<div class="flex justify-between">
					<h3 class="tracking-tight font-semibold">Subscription Tier</h3>
				</div>
				<div class="flex items-end py-3">
					<h3 class="text-3xl font-semibold text-foreground">$40.00</h3>
					<p class="text-sm text-muted-foreground">/mo</p>
				</div>
				<Button size="sm" variant="default" class="w-full h-7 my-3 shadow-xl"> Start Free Trial</Button>
				<div class="px-1 my-2">
					<Separator class="bg-foreground/25" orientation="horizontal" />
				</div>
				<ul class="space-y-3 px-3 py-3">
					{#each features as feature}
						<li class="flex items-center text-sm">
						{#if feature.included}
							<Check class="mr-2 h-4 w-4 text-primary flex-shrink-0" />
						{:else}
							<Minus class="mr-2 h-4 w-4 text-muted-foreground flex-shrink-0" />
						{/if}
						<span class={feature.included ? "text-foreground" : "text-muted-foreground"}>
							{feature.name}
						</span>
						</li>
					{/each}
				</ul>
			</Card>
			<Card class="p-4 w-72 bg-muted/60 border-foreground/25 hover:shadow hover:shadow-foreground/50">
				<div class="flex justify-between">
					<h3 class="tracking-tight font-semibold">Subscription Tier</h3>
					<Badge class="rounded-sm">Popular</Badge>
				</div>
				<div class="flex items-end py-3">
					<h3 class="text-3xl font-semibold text-foreground">$800.00</h3>
					<p class="text-sm text-muted-foreground">/once</p>
				</div>
				<Button size="sm" variant="default" class="w-full h-7 my-3 shadow-xl"> Start Free Trial</Button>
				<div class="px-1 my-2">
					<Separator class="bg-foreground/25" orientation="horizontal" />
				</div>
				<ul class="space-y-3 px-3 py-3">
					{#each features as feature}
						<li class="flex items-center text-sm">
							{#if feature.included}
								<Check class="mr-2 h-4 w-4 text-primary flex-shrink-0" />
							{:else}
								<Minus class="mr-2 h-4 w-4 text-muted-foreground flex-shrink-0" />
							{/if}
							<span class={feature.included ? "text-foreground" : "text-muted-foreground"}>
								{feature.name}
							</span>
						</li>
					{/each}
				</ul>
			</Card>
		</div>
		<div class="flex items-center gap-4 my-6">
			<span class="font-semibold text-sm tracking-wide text-foreground/75">As seen on:</span>
			<div class="flex items-center gap-2 opacity-65">
				<img class="h-5" src={HackerNews} alt="">
				<img class="h-[2.825rem]" src={ProductHunt} alt="">
			</div>
		</div>
	</section>
	

	<section  class="flex flex-col gap-6 items-center w-full px-20 py-12">
		<h3 class="mt-16 px-16 pb-3 mb-0 relative z-10 bg-gradient-to-b  from-neutral-200 to-neutral-600 bg-clip-text text-center font-sans text-4xl font-semibold text-transparent ">
			Frequently Asked Questions
		</h3>
		<Accordion.Root class="w-full  max-w-4xl">
			<Accordion.Item value="item-1">
			  	<Accordion.Trigger>Is it accessible?</Accordion.Trigger>
			  	<Accordion.Content>
					Yes. It adheres to the WAI-ARIA design pattern.
				</Accordion.Content>
			</Accordion.Item>
			<Accordion.Item value="item-2">
				<Accordion.Trigger>Is it styled?</Accordion.Trigger>
				<Accordion.Content>
					Yes. It comes with default styles that matches the other components'
					aesthetic.
				</Accordion.Content>
			</Accordion.Item>
			<Accordion.Item value="item-3">
				<Accordion.Trigger>Is it animated?</Accordion.Trigger>
				<Accordion.Content>
					Yes. It's animated by default, but you can disable it if you prefer.
				</Accordion.Content>
			</Accordion.Item>
		  </Accordion.Root>
	</section>

	<section class="flex justify-center w-full px-20 py-16">
		<Card class="relative z-9 flex flex-col gap-4 items-center bg-primary p-8 w-full max-w-5xl shadow border border-foreground/30">
			<h3 class="text-3xl font-semibold max-w-96 text-center">
				Lorem ipsum dolor sit amet, consectetur adipiscing elit.
			</h3>

			<p class="text-base tracking-tight text-center max-w-96">
				Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut metus nunc, fermentum id ex non.
			</p>

			<div class="flex flex-wrap justify-around gap-6 px-8  md:px-16 my-6 font-semibold">
				<div class="flex flex-row items-center gap-2">
					<CircleCheck size={18} />
					<span class="text-sm">Lorem ipsum dolor.</span>
				</div>
				<div class="flex flex-row items-center gap-2">
					<CircleCheck size={18} />
					<span class="text-sm">Lorem ipsum dolor.</span>
				</div>
				<div class="flex flex-row items-center gap-2">
					<CircleCheck size={18} />
					<span class="text-sm">Lorem ipsum dolor.</span>
				</div>

			</div>

			<Button size="sm" variant="outline" class="group bg-primary mt-4 gap-2 px-6 border-foreground hover:bg-foreground hover:text-primary">
				Get Started
				<ArrowRight className="group-hover:fill-primary" size={18} />
			</Button>
		</Card>
	</section>
	
	<ThemeToggle />
</div>

<style>
	:global(body) {
		min-height: 100vh;
		margin: 0;
	}
</style>