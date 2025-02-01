<script lang="ts">
	import posthog from "posthog-js";
  import type { UserResource } from '@clerk/types';

	let { user, children } = $props<{
    user: UserResource
    children: any
  }>();

   
  posthog.identify(user.id, {
    email: user.primaryEmailAddress.toString(),
  });
  

</script>

{@render children()}
