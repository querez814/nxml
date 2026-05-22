<script lang="ts">
	type Article = {
		title?: string;
		url?: string;
		source?: string;
	};

	let {
		sentiment
	}: {
		sentiment: Promise<Record<string, unknown> | null>;
	} = $props();

	function articlesFrom(data: Record<string, unknown> | null): Article[] {
		if (!data || typeof data !== 'object' || 'error' in data) return [];
		const raw = data.top_articles;
		if (!Array.isArray(raw)) return [];
		return raw.filter(
			(a): a is Article =>
				!!a && typeof a === 'object' && typeof (a as Article).title === 'string'
		);
	}
</script>

{#await sentiment}
	<p class="tzr-headlines-status" role="status" aria-live="polite">Loading market headlines…</p>
{:then data}
	{@const items = articlesFrom(data)}
	{#if items.length > 0}
		<section class="market-headlines" aria-labelledby="tzr-headlines-heading">
			<h2 id="tzr-headlines-heading" class="market-headlines-heading">Market headlines</h2>
			<ul class="market-headlines-list">
				{#each items.slice(0, 5) as item (item.url ?? item.title)}
					<li>
						<a href={item.url} rel="noopener noreferrer" target="_blank" class="market-headlines-link">
							<span class="market-headlines-title-text">{item.title}</span>
							{#if item.source}
								<span class="market-headlines-source">{item.source}</span>
							{/if}
						</a>
					</li>
				{/each}
			</ul>
		</section>
	{/if}
{/await}
