<script lang="ts">
	import { onMount } from 'svelte';

	export let screenshots: { src: string; alt: string }[];
	export let screenshotWidth: number;
	export let screenshotHeight: number;

	let currentScreenshotIndex = 0;

	onMount(() => {
		const intervalId = setInterval(() => {
			currentScreenshotIndex = (currentScreenshotIndex + 1) % screenshots.length;
		}, 5000);

		return () => clearInterval(intervalId);
	});
</script>

<div class="relative rounded-lg border bg-background shadow-xl" style="height: 600px;">
	{#each screenshots as screenshot, index}
		<img
			src={screenshot.src}
			alt={screenshot.alt}
			width={screenshotWidth}
			height={screenshotHeight}
			class="absolute left-0 top-0 h-[600px] w-full rounded-lg object-cover transition-opacity duration-500"
			class:opacity-100={index === currentScreenshotIndex}
			class:opacity-0={index !== currentScreenshotIndex}
		/>
	{/each}
	<div class="absolute bottom-4 left-1/2 flex -translate-x-1/2 transform space-x-2">
		{#each screenshots as _, index}
			<button
				class="h-3 w-3 rounded-full border-2 border-white"
				class:bg-white={index === currentScreenshotIndex}
				class:bg-transparent={index !== currentScreenshotIndex}
				on:click={() => (currentScreenshotIndex = index)}
				aria-label="View screenshot {index + 1}"
			></button>
		{/each}
	</div>
</div>
