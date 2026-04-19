<script lang="ts">
	import type { PageData } from './$types';
	import CommandLine from '$lib/components/cmd/CommandLine.svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Button from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Separator from '$lib/components/ui/separator';
	import { Terminal, Sparkles, Keyboard, Loader2 } from 'lucide-svelte';
	import LandingTutorial from '$lib/components/welcome/LandingTutorial.svelte';
	import CommandList from '$lib/components/welcome/CommandList.svelte';

	let { data }: { data: PageData } = $props();
	let showTutorial = $state(false);
	let showCommands = $state(false);
</script>

<div class="min-h-screen bg-gradient-to-b from-background to-muted">
		<div class="container mx-auto flex min-h-screen flex-col px-4 py-8">
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

			<div class="flex flex-1 justify-center">
				<div class="w-full max-w-4xl space-y-6">
					<Card.Root class="border-2 bg-background/95 backdrop-blur">
						<Card.Header class="flex items-center justify-between space-y-1">
							<Card.Title class="flex items-center gap-2 text-2xl font-bold tracking-tight">
								<Terminal class="h-6 w-6" />
								Terminal
							</Card.Title>
							<Button.Root variant="ghost" size="sm">Sign Out</Button.Root>
						</Card.Header>
						<Card.Content>
							<div class="flex flex-col items-center gap-6">
								<div class="flex flex-col items-center gap-2 text-center">
									<p class="flex items-center gap-2 text-lg font-medium">
										Welcome back
										<Sparkles class="h-4 w-4 animate-pulse text-primary" />
									</p>
									<div class="flex items-center gap-2 text-sm text-muted-foreground">
										<Keyboard class="h-4 w-4" />
										<span>Press <kbd class="rounded bg-muted px-1 py-0.5">/ </kbd> to start</span>
									</div>
								</div>

								<div class="relative w-full">
									<CommandLine />
								</div>

								<div class="w-full space-y-3">
									<div class="flex items-end justify-between gap-3">
										<h2 class="flex items-center gap-2 text-base font-semibold tracking-tight">
											Market Headlines
											{#await data.streamed.newsRecap}
												<Loader2
													class="h-4 w-4 animate-spin text-muted-foreground"
													aria-label="Loading market headlines"
												/>
											{:then _}{/await}
										</h2>
										<p class="text-xs text-muted-foreground">Weekly recap sources, scroll to browse</p>
									</div>

									{#await data.streamed.newsRecap}
										<div
											class="flex items-center gap-2 rounded-lg border border-dashed border-border/80 bg-muted/20 px-4 py-3 text-sm text-muted-foreground"
											role="status"
											aria-live="polite"
										>
											<Loader2 class="h-4 w-4 animate-spin" aria-hidden="true" />
											<span>Loading market headlines…</span>
										</div>
									{:then newsRecap}
										{@const articles = newsRecap?.articles ?? []}
										{#if articles.length}
											<div class="overflow-x-auto pb-1">
												<div class="flex snap-x snap-mandatory gap-4">
													{#each articles as article (article.id)}
														<a
															href={article.url}
															target="_blank"
															rel="noopener noreferrer"
															class="group min-w-[250px] max-w-[300px] shrink-0 snap-start overflow-hidden rounded-lg border border-border/80 bg-card/60 transition-colors hover:border-primary/50"
														>
															{#if article.thumbnail_url}
																<img
																	src={article.thumbnail_url}
																	alt={article.title}
																	class="h-32 w-full object-cover"
																	loading="lazy"
																/>
															{:else}
																<div
																	class="flex h-32 w-full items-center justify-center bg-muted/40 text-xs text-muted-foreground"
																>
																	No thumbnail
																</div>
															{/if}
															<div class="space-y-2 p-3">
																<p class="line-clamp-2 text-sm font-medium leading-snug">
																	{article.title}
																</p>
																<p class="text-xs text-muted-foreground">
																	{article.publisher}
																	{#if article.published_at}
																		<span aria-hidden="true"> · </span>
																		{new Date(article.published_at).toLocaleDateString()}
																	{/if}
																</p>
															</div>
														</a>
													{/each}
												</div>
											</div>
										{:else}
											<div
												class="rounded-lg border border-dashed border-border/80 bg-muted/20 px-4 py-3 text-sm text-muted-foreground"
											>
												No market headlines are available yet.
											</div>
										{/if}
									{:catch}
										<div
											class="rounded-lg border border-dashed border-border/80 bg-muted/20 px-4 py-3 text-sm text-muted-foreground"
										>
											Couldn't load market headlines. Please try again later.
										</div>
									{/await}
								</div>

								<div class="w-full space-y-4">
									<Separator.Root />
									<div class="flex justify-center gap-4 text-sm">
										<Dialog.Root bind:open={showTutorial}>
											<Dialog.Trigger
												class="inline-flex h-9 items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
											>
												Quick Tutorial
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
											<Dialog.Trigger
												class="inline-flex h-9 items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
											>
												Command List
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
						</Card.Content>
					</Card.Root>
				</div>
			</div>
		</div>
	</div>

<style>
	:global(.group) {
		transform: translateZ(0);
	}
	:global(.group:hover) {
		background-color: rgba(255, 255, 255, 0.02);
	}
</style>
