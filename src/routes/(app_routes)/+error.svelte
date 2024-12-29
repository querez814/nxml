<!-- src/routes/app/$error.svelte -->
<script lang="ts">
    import { page } from '$app/state';
    import siteMetaData from '$lib/config/site-metadata';
    import Button from '$lib/components/ui/button/button.svelte';

    // NOTE: Add some custom error handling here need to store the error in a store/logs
</script>
  
<div class="flex flex-col gap-2 justify-center items-center min-h-screen w-full">
    <h1>Oops! An error occurred.</h1>
    <p>{page.status} - {page.error?.message}</p>
    <a href={siteMetaData.urls.app.base}>
        <Button size="sm" variant="default" class="px-6 hover:text-foreground my-6">
            Return to the app
        </Button>
    </a>
</div>