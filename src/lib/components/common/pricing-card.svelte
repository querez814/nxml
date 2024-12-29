<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import { Check, Minus  } from 'lucide-svelte'

	import Card from '$lib/components/ui/card/card.svelte';
	import { Separator } from "$lib/components/ui/separator/index.js";

  import type { PricingFeature, TierFrequency } from '$lib/types';


  let {
    tierName,
    features,
    tierPrice,
    tierFrequency,
    buttonText,
    buttonLink,
  } : {
    tierName: string,
    features: PricingFeature[]
    tierPrice: number
    tierFrequency: TierFrequency
    buttonText: string
    buttonLink: string
  } = $props();


</script>

<Card class="p-4 w-72 bg-muted/60 border-foreground/25 hover:shadow hover:shadow-foreground/50">
  <div class="flex justify-between">
    <h3 class="tracking-tight font-semibold capitalize">
      { tierName.replace(/_/g, " ") }
    </h3>
  </div>
  <div class="flex items-end py-3">
    <h3 class="text-3xl font-semibold text-foreground">
      ${tierPrice.toFixed(2)}
    </h3>
    <p class="text-sm text-muted-foreground">
      {"/" + tierFrequency}
    </p>
  </div>
  <a href={buttonLink} target="_blank">
    <Button size="sm" variant="default" class="w-full h-7 my-3 shadow hover:text-foreground"> 
      {buttonText}
    </Button>
  </a>
  <div class="px-1 my-2">
    <Separator class="bg-foreground/25" orientation="horizontal" />
  </div>
  <ul class="space-y-3 px-3 py-3">
    {#each features as feature}
      <li class="flex items-center text-sm">
      {#if feature.included}
        <Check class="mr-2 h-4 w-4 text-primary flex-shrink-0" />
      {:else}
        <Minus class="mr-2 h-4 w-4 text-muted-foreground flex-shrink-0" />
      {/if}
      <span class={feature.included ? "text-foreground" : "text-muted-foreground"}>
        {feature.name}
      </span>
      </li>
    {/each}
  </ul>
</Card>