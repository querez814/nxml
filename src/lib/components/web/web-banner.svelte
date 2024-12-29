<script lang="ts">
	import DarkBannerDots from '$lib/components/common/dark-banner-dots.svelte';
    import BG from '$lib/../media/images/banner-light.svg';

	$: bgImage = `background-image: url("${BG}");`;
	$: bgPosition = 'background-position: 50%;';
	$: bgRepeat = 'background-repeat: no-repeat;';
	$: bgSize = 'background-size: cover;';
</script>


<div class="hidden lg:flex w-full max-w-screen p-3">
    <div class="relative flex items-center justify-center w-full h-10 bg-muted rounded-sm border border-border" style="{bgImage} {bgPosition} {bgRepeat} {bgSize}">
        <span class="text-[0.815rem]">
            <slot />
        </span>
        <div class="absolute top-4 left-4">
            <DarkBannerDots />
        </div>
    </div>
</div>

