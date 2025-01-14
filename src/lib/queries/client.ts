import { QueryClient } from '@tanstack/svelte-query';

export const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			staleTime: 30_000,
			gcTime: 5 * 60 * 1000,
			retry: 3,
			refetchOnWindowFocus: true,
			refetchOnMount: false
		}
	}
});
