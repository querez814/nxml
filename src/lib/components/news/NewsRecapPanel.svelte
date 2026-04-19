<script lang="ts">
	import type { NewsRecapPayload } from '$lib/api/newsRecap';
	import * as Card from '$lib/components/ui/card';
	import { marked } from 'marked';
	import DOMPurify from 'isomorphic-dompurify';

	let {
		recap,
		heading = 'News — past week'
	}: {
		recap: NewsRecapPayload | null;
		heading?: string;
	} = $props();

	const recapHtml = $derived(
		recap?.ai?.recap_md
			? (DOMPurify.sanitize(marked.parse(recap.ai.recap_md) as string, {
					USE_PROFILES: { html: true }
				}) as string)
			: ''
	);
</script>

{#if recap}
	<Card.Root class="border-2 bg-background/95 backdrop-blur">
		<Card.Header>
			<Card.Title class="text-xl font-semibold tracking-tight">{heading}</Card.Title>
			{#if recap.ai?.week_start}
				<p class="text-xs text-muted-foreground">Week {recap.ai.week_start} · {recap.ai.model}</p>
			{/if}
		</Card.Header>
		<Card.Content class="space-y-6">
			{#if recap.ai?.error}
				<p class="text-sm text-amber-600/90">AI recap unavailable: {recap.ai.error}</p>
			{:else if recapHtml}
				<div class="prose prose-invert max-w-none text-sm prose-headings:font-semibold">
					<!-- eslint-disable-next-line svelte/no-at-html-tags -->
					{@html recapHtml}
				</div>
			{/if}

			{#if recap.ai?.themes?.length}
				<div>
					<h3 class="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">Themes</h3>
					<ul class="flex flex-wrap gap-2">
						{#each recap.ai.themes as t (t)}
							<li
								class="rounded-md border border-border bg-muted/40 px-2 py-1 text-xs text-foreground/90"
							>
								{t}
							</li>
						{/each}
					</ul>
				</div>
			{/if}

			{#if recap.ai?.watch_items?.length}
				<div>
					<h3 class="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
						Watch list
					</h3>
					<ul class="list-inside list-disc space-y-1 text-sm text-muted-foreground">
						{#each recap.ai.watch_items as w (w)}
							<li>{w}</li>
						{/each}
					</ul>
				</div>
			{/if}

			<div>
				<h3 class="mb-3 text-xs font-medium uppercase tracking-wide text-muted-foreground">Articles</h3>
				{#if recap.articles?.length}
					<ul class="max-h-80 space-y-3 overflow-y-auto pr-1 text-sm">
						{#each recap.articles as a (a.id + a.published_at)}
							<li class="rounded-md border border-border/60 bg-muted/20 p-3">
								<a
									href={a.url}
									target="_blank"
									rel="noopener noreferrer"
									class="font-medium text-primary underline-offset-4 hover:underline"
								>
									{a.title || 'Untitled'}
								</a>
								<p class="mt-1 text-xs text-muted-foreground">
									{a.publisher}
									{#if a.source_symbol}
										· {a.source_symbol}
									{/if}
									· {a.published_at?.slice(0, 10) ?? ''}
								</p>
							</li>
						{/each}
					</ul>
				{:else}
					<p class="text-sm text-muted-foreground">
						No Yahoo Finance headlines in the last 7 days for this view.
					</p>
				{/if}
			</div>
		</Card.Content>
	</Card.Root>
{:else}
	<Card.Root class="border-2 border-dashed border-border/60 bg-background/60 backdrop-blur">
		<Card.Header>
			<Card.Title class="text-xl font-semibold tracking-tight">{heading}</Card.Title>
		</Card.Header>
		<Card.Content>
			<p class="text-sm text-muted-foreground">
				No news recap for this symbol yet, or the recap service did not return data. Try again later.
			</p>
		</Card.Content>
	</Card.Root>
{/if}
