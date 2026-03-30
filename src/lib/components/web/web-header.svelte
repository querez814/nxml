<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import siteMetadata from '$lib/config/site-metadata';
</script>

<header class="my-6 flex flex-row justify-between px-4 md:px-12 [&>*:not(ul)]:w-64">
	<a href="/" class="text-xl font-bold md:text-2xl"> Due Diligence </a>
	<ul class="flex *:md:hidden"></ul>
	<div class="hidden justify-end gap-6 md:flex">
		<a href={siteMetadata.urls.auth.signin}>
			<Button size="sm" variant="default" class="px-6 hover:text-foreground">Login</Button>
		</a>
		<a href={siteMetadata.urls.auth.signup}>
			<Button size="sm" variant="secondary" class="px-6">Sign Up</Button>
		</a>
	</div>
</header>
