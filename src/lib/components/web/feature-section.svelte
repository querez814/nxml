<script lang="ts">
	import { ArrowRight, Check, CircleCheck, Minus  } from 'lucide-svelte';
	import FeatureIcon from '$lib/components/common/feature-icon.svelte';
</script>

<div class="flex flex-col justify-center items-center w-72 gap-2">
    <FeatureIcon>
        <ArrowRight size={18} />
    </FeatureIcon>
    <p class="text-center tracking-wide text-sm px-6">
       <slot />
    </p>
</div>