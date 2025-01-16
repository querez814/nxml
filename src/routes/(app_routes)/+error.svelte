<script lang="ts">
	import { page } from '$app/state';
	import siteMetaData from '$lib/config/site-metadata';
	import Button from '$lib/components/ui/button/button.svelte';
</script>

<div class="flex min-h-screen w-full flex-col items-center justify-center gap-2">
	<h1>Oops! An error occurred.</h1>
	<p>{page.status} - {page.error?.message}</p>
	<a href={siteMetaData.urls.app.base}>
		<Button size="sm" variant="default" class="my-6 px-6 hover:text-foreground">
			Return to the app
		</Button>
	</a>
</div>
