<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import { ArrowRight, CircleCheck } from 'lucide-svelte'
	import Card from '$lib/components/ui/card/card.svelte';
	import siteMetaData from '$lib/config/site-metadata';
</script>

<Card class="relative z-9 flex flex-col gap-4 items-center bg-primary p-8 w-full max-w-5xl shadow border border-foreground/30">
    <h3 class="text-3xl font-semibold max-w-96 text-center">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    </h3>

    <p class="text-base tracking-tight text-center max-w-96">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut metus nunc, fermentum id ex non.
    </p>

    <div class="flex flex-wrap justify-around gap-6 px-8  md:px-16 my-6 font-semibold">
        <div class="flex flex-row items-center gap-2">
            <CircleCheck size={18} />
            <span class="text-sm">Lorem ipsum dolor.</span>
        </div>
        <div class="flex flex-row items-center gap-2">
            <CircleCheck size={18} />
            <span class="text-sm">Lorem ipsum dolor.</span>
        </div>
        <div class="flex flex-row items-center gap-2">
            <CircleCheck size={18} />
            <span class="text-sm">Lorem ipsum dolor.</span>
        </div>

    </div>
    <a href={siteMetaData.urls.auth.signup}>
        <Button size="sm" variant="outline" class="group bg-primary mt-4 gap-2 px-6 border-foreground hover:bg-foreground hover:text-primary">
            Get Started
            <ArrowRight className="group-hover:fill-primary" size={18} />
        </Button>
    </a> 
</Card>