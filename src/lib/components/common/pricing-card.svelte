<script lang="ts">
    import { onMount } from 'svelte';
    import { Check, Minus } from 'lucide-svelte';
	import { Button } from '../ui/button';
	import { Card } from '../ui/card';
  
    interface Feature {
      name: string;
      included: boolean;
    }
  
    interface PricingTier {
      name: string;
      originalPrice: number;
      discountedPrice?: number;
      description: string;
      features: Feature[];
      cta: string;
    }
  
    export let tier: PricingTier;
    export let isLoggedIn: boolean;
  
    let savings = 0;
  
    $: if (tier.discountedPrice) {
      savings = tier.originalPrice - tier.discountedPrice;
    }
  
    function handleAction() {
      if (isLoggedIn) {
        console.log(`Upgrading to ${tier.name} tier`);
      } else {
        console.log("Redirecting to sign up page");
      }
    }
  </script>
  
  <Card class="border w-[300px] overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-foreground/15">
    <div class="card-header p-6">
      <h3 class="text-2xl font-semibold text-foreground">{tier.name}</h3>
      <p class="text-sm text-muted-foreground mt-2">{tier.description}</p>
    </div>
    <div class="card-content p-6">
      <div class="mb-6">
        <div class="flex items-baseline justify-center space-x-2">
          <span class="text-4xl font-bold text-foreground">
            ${(tier.discountedPrice || tier.originalPrice).toFixed(2)}
          </span>
          <span class="text-sm text-muted-foreground">/mo</span>
        </div>
        {#if tier.discountedPrice}
          <div class="mt-2 text-center">
            <span class="text-sm text-muted-foreground line-through mr-2">
              ${tier.originalPrice.toFixed(2)}
            </span>
            <span class="badge badge-secondary text-xs">
              Save ${savings.toFixed(2)}/mo
            </span>
          </div>
        {/if}
      </div>
      <ul class="space-y-3">
        {#each tier.features as feature}
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
    </div>
    <div class="card-footer p-6">
      <Button
        class="btn btn-primary w-full"
        on:click={handleAction}
      >
        {isLoggedIn ? tier.cta : "Sign up"}
    </Button>
    </div>
</Card>
  
  <style>
  
    .badge {
      background-color: var(--secondary);
      color: var(--secondary-foreground);
      padding: 0.25rem 0.5rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 500;
    }
  
    .btn {
      padding: 0.5rem 1rem;
      border-radius: var(--radius);
      font-weight: 500;
      transition: background-color 0.3s ease;
    }
  
    .btn-primary {
      background-color: var(--primary);
      color: var(--primary-foreground);
    }
  
    .btn-primary:hover {
      background-color: var(--primary-hover);
    }
  </style>