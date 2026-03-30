<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import { Wallet } from 'lucide-svelte';
	import siteMetadata from '$lib/config/site-metadata';

	const customerPortalLink = siteMetadata.urls.subscription.portal;
</script>

<header class="font mono flex flex-row justify-between px-4 py-6 text-green-700 md:px-12">
	<div class="font-mono text-5xl motion-safe:animate-pulse md:motion-safe:animate-pulse">
		Due Diligence
	</div>

	<div class="hidden items-center justify-end gap-6 md:flex">
		<a href={customerPortalLink} target="_blank" rel="noopener noreferrer">
			<Button size="icon" variant="secondary" class=" hover:text-foreground">
				<Wallet class="stroke-white" size={24} />
			</Button>
		</a>
		<a href="/">
			<Button size="sm" variant="outline" class="hover:text-foreground">Home</Button>
		</a>
	</div>
</header>
