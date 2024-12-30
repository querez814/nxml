<script lang="ts" context="module">
    import { page } from '$app/state';
    import DOMPurify from "isomorphic-dompurify";
    import WebHeader from '$lib/components/web/web-header.svelte';
    import WebFooter from '$lib/components/web/web-footer.svelte';
</script>

<div class="flex flex-col  w-full">
    <WebHeader />
    <article class="prose prose-neutral  dark:prose-invert py-16 mx-auto px-6">
        {@html DOMPurify.sanitize(page.data.html, { USE_PROFILES: { html: true } })}
    </article>
    <WebFooter />
</div>