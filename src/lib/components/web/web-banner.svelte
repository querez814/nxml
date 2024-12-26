<script lang="ts">
	import DarkBannerDots from '$lib/components/common/dark-banner-dots.svelte';

	const bgSrc = 'https://assets.website-files.com/63e36d09413f83c58ac5d998/63f498f97df68f71bd38f2b5_Banner%20Light.svg';

	$: bgImage = `background-image: url("${bgSrc}");`;
	$: bgPosition = 'background-position: 50%;';
	$: bgRepeat = 'background-repeat: no-repeat;';
	$: bgSize = 'background-size: cover;';
</script>


<div class="w-full max-w-screen p-3">
    <div class="relative flex items-center justify-center w-full h-10 bg-muted rounded-sm border border-border" style="{bgImage} {bgPosition} {bgRepeat} {bgSize}">
        <span class="text-[0.815rem]">
            <slot />
        </span>
        <div class="absolute top-4 left-4">
            <DarkBannerDots />
        </div>
    </div>
</div>

