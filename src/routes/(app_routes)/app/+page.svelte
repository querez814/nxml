<script lang="ts">
	import CommandLine from '$lib/components/cmd/CommandLine.svelte';
	import TopGainers from '$lib/components/welcome/TopGainers.svelte';
	import TopLosers from '$lib/components/welcome/TopLosers.svelte';
	import TopMovers from '$lib/components/welcome/TopMovers.svelte';
	import SignOutButton from 'clerk-sveltekit/client/SignOutButton.svelte';
	import { fetchGainers, fetchLosers, fetchMostTraded } from '../../../api/movers/movers';
	import SignedIn from 'clerk-sveltekit/client/SignedIn.svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Button from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Separator from '$lib/components/ui/separator';
	import { Terminal, Sparkles, Keyboard, TrendingUp, ExternalLink } from 'lucide-svelte';
	import WelcomeCarousel from '$lib/components/welcome/WelcomeCarousel.svelte';
	import LandingTutorial from '$lib/components/welcome/LandingTutorial.svelte';
	import CommandList from '$lib/components/welcome/CommandList.svelte';
	import type { PageData } from './$types';

	let showTutorial = $state(false);
	let showCommands = $state(false);

	function formatTimestamp(timestamp: number): string {
		return new Date(timestamp * 1000).toLocaleString();
	}
	let { data }: { data: PageData } = $props();
	const newsItems = data || [];
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
					Financial Data and Metrics used by the pros, at your fingertips
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
													<Button.Root variant="outline" size="sm" class="mt-4">
														Close Tutorial
													</Button.Root>
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
													<Button.Root variant="outline" size="sm" class="mt-4">
														Close Commands
													</Button.Root>
												</Dialog.Close>
											</Dialog.Content>
										</Dialog.Portal>
									</Dialog.Root>
								</div>
							</div>
						</div>
					</Card.Content>
				</Card.Root>
			</div>

			<div class="mb-6">
				<h2 class="text-2xl font-bold tracking-tight">Latest Market News</h2>
			</div>
			<div class="mb-12 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
				{#each newsItems?.data as article}
					<Card.Root class="h-full cursor-pointer overflow-hidden transition-all hover:shadow-lg">
						<div
							role="button"
							tabindex="0"
							class="group h-full"
							on:click={() => {
								if (article.url) {
									window.open(article.url, '_blank', 'noopener,noreferrer');
								}
							}}
							on:keydown={(e) => {
								if (e.key === 'Enter' || e.key === ' ') {
									if (article.url) {
										window.open(article.url, '_blank', 'noopener,noreferrer');
									}
								}
							}}
						>
							{#if article.url?.resolutions?.[0]?.url}
								<img
									src={article.url.resolutions[0].url}
									alt={article.title}
									class="h-48 w-full object-cover transition-transform group-hover:scale-105"
								/>
							{/if}

							<Card.Header>
								<Card.Title
									class="line-clamp-2 flex items-start gap-2 text-lg group-hover:text-primary"
								>
									{article.title}
									<ExternalLink
										class="h-4 w-4 flex-shrink-0 opacity-0 transition-opacity group-hover:opacity-100"
									/>
								</Card.Title>
								<Card.Description class="mt-2 text-sm text-muted-foreground">
									{article.publisher} • {formatTimestamp(article.providerPublishTime)}
								</Card.Description>
							</Card.Header>

							{#if article.relatedTickers?.length}
								<Card.Content>
									<div class="flex flex-wrap gap-2">
										{#each article.relatedTickers as ticker}
											<span
												class="rounded bg-primary/10 px-2 py-1 text-xs"
												on:click|stopPropagation={() => {
													window.open(
														`https://finance.yahoo.com/quote/${ticker}`,
														'_blank',
														'noopener,noreferrer'
													);
												}}
											>
												${ticker}
											</span>
										{/each}
									</div>
								</Card.Content>
							{/if}
						</div>
					</Card.Root>
				{/each}
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
