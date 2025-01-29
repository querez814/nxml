<script lang="ts">
	import CommandLine from '$lib/components/cmd/CommandLine.svelte';
	import SignOutButton from 'clerk-sveltekit/client/SignOutButton.svelte';
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte';
	import { Badge } from '$lib/components/ui/badge';
	import * as Card from '$lib/components/ui/card';
	import * as Button from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Separator from '$lib/components/ui/separator';
	import {
		Terminal,
		Sparkles,
		Keyboard,
		TrendingUp,
		Newspaper,
		ExternalLink,
		Video,
		FileText
	} from 'lucide-svelte';
	import WelcomeCarousel from '$lib/components/welcome/WelcomeCarousel.svelte';
	import LandingTutorial from '$lib/components/welcome/LandingTutorial.svelte';
	import CommandList from '$lib/components/welcome/CommandList.svelte';
	import type { PageData } from './$types';
	import MarketGauge from '$lib/components/technicals/Market/MarketGauge.svelte';
	import MarketGaugeExplanation from '$lib/components/technicals/Market/MarketGaugeExplanation.svelte';

	let showGaugeExplanation = $state(false);
	let showTutorial = $state(false);
	let showCommands = $state(false);

	let { data }: { data: PageData } = $props();
	let newsResponse = data.news;

	function formatDate(dateStr: string): string {
		try {
			const date = new Date(dateStr);
			return new Intl.DateTimeFormat('en-US', {
				hour: 'numeric',
				minute: 'numeric',
				month: 'short',
				day: 'numeric',
				hour12: true
			}).format(date);
		} catch {
			return 'Recent';
		}
	}

	function getNewsIcon(type: string) {
		switch (type.toLowerCase()) {
			case 'video':
				return Video;
			case 'article':
				return FileText;
			default:
				return Newspaper;
		}
	}

	function getSentimentColor(sentiment: string): string {
		switch (sentiment.toLowerCase()) {
			case 'positive':
				return 'text-green-400 border-green-400/20';
			case 'negative':
				return 'text-red-400 border-red-400/20';
			default:
				return 'text-blue-400 border-blue-400/20';
		}
	}
</script>

<SignedIn let:user>
	<div class="min-h-screen bg-gradient-to-b from-background to-muted">
		<div class="container mx-auto px-4 py-8">
			<div class="mb-12 flex flex-col items-center">
				<h1
					class="animate-pulse bg-gradient-to-r from-primary to-primary/50 bg-clip-text text-center text-4xl font-bold tracking-tighter text-transparent sm:text-5xl"
				>
					Your Terminal, Your Edge
				</h1>
				<p
					class="mt-4 max-w-[42rem] animate-[fade-in_0.5s_ease-out] text-center text-muted-foreground"
				>
					Fundamental, Essential Financial Data and Metrics used by the pros, at your fingertips
				</p>
			</div>
			<div class="mb-12">
				<Card.Root
					class="mx-auto w-full max-w-3xl border-2 bg-background/95 backdrop-blur transition-all duration-300 hover:border-primary/50 supports-[backdrop-filter]:bg-background/80"
				>
					<Card.Header class="flex items-center justify-between space-y-1">
						<Card.Title class="flex items-center gap-2 text-2xl font-bold tracking-tight">
							<Terminal class="h-6 w-6" />
							Due Diligence
						</Card.Title>
						<SignOutButton>
							<Button.Root variant="ghost" size="sm">Sign Out</Button.Root>
						</SignOutButton>
					</Card.Header>
					<Card.Content>
						<div class="flex flex-col items-center gap-6">
							<div class="flex flex-col items-center gap-2 text-center">
								<p class="flex items-center gap-2 text-lg font-medium">
									Welcome back, {user?.username}
									<Sparkles class="h-4 w-4 animate-pulse text-primary" />
								</p>
								<div class="flex items-center gap-2 text-sm text-muted-foreground">
									<Keyboard class="h-4 w-4" />
									<span>Press <kbd class="rounded bg-muted px-1 py-0.5">/ </kbd> to start</span>
								</div>
							</div>
							<div class="w-full">
								<div class="relative z-10">
									<div class="mb-4 flex justify-end">
										{#if !showGaugeExplanation}
											<button
												class="rounded border border-green-400/20 px-3 py-1 font-mono text-xs text-green-400 hover:text-green-300"
												onclick={() => (showGaugeExplanation = true)}
											>
												Click here to learn how this is calculated
											</button>
										{/if}
									</div>
									<div class="top-2"><MarketGauge /></div>
								</div>
								{#if showGaugeExplanation}
									<div class="mb-5">
										<div class="relative">
											<MarketGaugeExplanation />
											<button
												class="absolute right-4 top-4 font-mono text-xs text-gray-400 hover:text-gray-300"
												onclick={() => (showGaugeExplanation = false)}
											>
												✕ Close
											</button>
										</div>
									</div>
								{/if}
								<div class="relative w-full">
									<div class="absolute -top-6 left-1/2 -translate-x-1/2 transform">
										<TrendingUp class="h-5 w-5 animate-bounce text-primary" />
									</div>
									<CommandLine />
								</div>

								<div class="w-full space-y-4">
									<Separator.Root />
									<div class="flex justify-center gap-4 text-sm">
										<Dialog.Root bind:open={showTutorial}>
											<Dialog.Trigger>
												<Button.Root variant="ghost" size="sm">Quick Tutorial</Button.Root>
											</Dialog.Trigger>
											<Dialog.Portal>
												<Dialog.Overlay />
												<Dialog.Content class="sm:max-w-2xl">
													<LandingTutorial />
													<Dialog.Close>
														<Button.Root variant="outline" size="sm" class="mt-4"
															>Close Tutorial</Button.Root
														>
													</Dialog.Close>
												</Dialog.Content>
											</Dialog.Portal>
										</Dialog.Root>

										<Dialog.Root bind:open={showCommands}>
											<Dialog.Trigger>
												<Button.Root variant="ghost" size="sm">Command List</Button.Root>
											</Dialog.Trigger>
											<Dialog.Portal>
												<Dialog.Overlay />
												<Dialog.Content class="sm:max-w-2xl">
													<CommandList />
													<Dialog.Close>
														<Button.Root variant="outline" size="sm" class="mt-4"
															>Close Commands</Button.Root
														>
													</Dialog.Close>
												</Dialog.Content>
											</Dialog.Portal>
										</Dialog.Root>
									</div>
								</div>
							</div>
						</div></Card.Content
					>
				</Card.Root>
			</div>

			<div class="mx-auto max-w-4xl px-4">
				<Card.Root
					class="border-2 bg-background/95 backdrop-blur transition-all duration-300 hover:border-primary/50 supports-[backdrop-filter]:bg-background/80"
				>
					<Card.Header>
						<Card.Title class="flex items-center gap-2 text-2xl font-bold tracking-tight">
							<Newspaper class="h-6 w-6" />
							Market Pulse
						</Card.Title>
						<Card.Description>Latest market updates and financial news</Card.Description>
					</Card.Header>

					<Card.Content>
						<div class="space-y-6">
							{#each newsResponse as news, index}
								<div class="group relative">
									<div class="flex gap-4">
										<div class="hidden sm:block">
											<img
												src={news.image_url}
												alt={news.title}
												class="h-24 w-24 rounded-lg object-cover transition-transform duration-300 group-hover:scale-105"
											/>
										</div>

										<div class="flex flex-1 flex-col space-y-2">
											<div class="flex items-start justify-between gap-4">
												<h3 class="font-medium leading-snug text-primary">{news.title}</h3>
												<time class="whitespace-nowrap text-sm text-muted-foreground"
													>{formatDate(news.date)}</time
												>
											</div>

											<p class="text-sm text-muted-foreground">{news.text}</p>

											<div class="flex flex-wrap items-center gap-2">
												<Badge variant="outline" class="flex items-center gap-1">
													{@const NewsIcon = getNewsIcon(news.type)}
													<NewsIcon class="h-3 w-3" />
													<span>{news.source_name}</span>
												</Badge>

												<Badge variant="outline" class={getSentimentColor(news.sentiment)}>
													{news.sentiment}
												</Badge>

												{#if news.topics?.length}
													{#each news.topics as topic}
														<span class="text-xs text-muted-foreground">#{topic}</span>
													{/each}
												{/if}

												<a
													href={news.news_url}
													target="_blank"
													rel="noopener noreferrer"
													class="ml-auto inline-flex items-center gap-1 text-xs text-primary hover:underline"
												>
													Read more
													<ExternalLink class="h-3 w-3" />
												</a>
											</div>
										</div>
									</div>

									{#if index < newsResponse.length - 1}
										<Separator.Root class="my-4" />
									{/if}
								</div>
							{/each}
						</div>
					</Card.Content>
				</Card.Root>
			</div>

			<div class="mb-8">
				<WelcomeCarousel />
			</div>

			<footer class="text-center text-sm text-muted-foreground">
				<p>Start with any ticker symbol - e.g., "AAPL", "MSFT", "TSLA" 🚀</p>
			</footer>
		</div>
	</div>
</SignedIn>

<style>
	:global(.group) {
		transform: translateZ(0);
	}

	:global(.group:hover) {
		background-color: rgba(255, 255, 255, 0.02);
	}
</style>
