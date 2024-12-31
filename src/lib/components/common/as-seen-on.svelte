<script lang="ts">
	import HackerNews from '$lib/../media/images/hacker-news-logo-white.webp';
	import ProductHunt from '$lib/../media/images/product-hunt-logo-horizontal-white.avif';

</script>

<div class="flex flex-col md:flex-row items-center gap-4 my-6">
    <span class="font-semibold text-sm tracking-wide text-foreground/75">As seen on:</span>
    <div class="flex items-center gap-2 opacity-65">
        <img class="h-5" src={HackerNews} alt="">
        <img class="h-[2.825rem]" src={ProductHunt} alt="">
    </div>
</div>