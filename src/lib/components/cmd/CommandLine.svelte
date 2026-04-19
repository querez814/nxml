<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let { onTickerChange, currentTicker = '' } = $props<{
		onTickerChange?: (ticker: string, fullPath?: string) => void;
		currentTicker?: string;
	}>();
	let inputValue = $state('');
	let history: string[] = [];
	let historyIndex = -1;
	let inputRef: HTMLInputElement;

	const sectionAliases: Record<string, string> = {
		bs: 'balancesheet',
		cf: 'cashflow',
		is: 'incomestatement',
		val: 'valuation'
	};

	const subsectionAliases: Record<string, string> = {
		q: 'quarterly',
		a: 'annual'
	};

	/** Single-token shortcuts like ``brk.b`` or ``GOOGL`` — not section aliases. */
	const RESERVED_SINGLE = new Set(['bs', 'cf', 'is', 'val']);

	function isTickerToken(raw: string): boolean {
		if (!raw || RESERVED_SINGLE.has(raw.toLowerCase())) return false;
		return /^[A-Za-z][A-Za-z0-9.-]{0,14}$/.test(raw);
	}

	function parseCommand(input: string): void {
		const parts = input.trim().split(/\s+/).map((p) => p.trim()).filter(Boolean);
		const lower = parts.map((p) => p.toLowerCase());

		if (lower[0] === 'clear') {
			inputValue = '';
			return;
		}

		// On ticker page: "is q" = section + subsection for current ticker
		if (currentTicker && parts.length === 2) {
			const section = sectionAliases[lower[0] as keyof typeof sectionAliases] || lower[0];
			const subsection = subsectionAliases[lower[1] as keyof typeof subsectionAliases] || lower[1];
			if (Object.values(sectionAliases).includes(section) && Object.values(subsectionAliases).includes(subsection)) {
				const p = `/app/${currentTicker}/${section}/${subsection}`;
				goto(p);
				return;
			}
		}

		// Just a ticker → overview ``/app/{TICKER}`` (preserve dots, e.g. brk.b)
		if (parts.length === 1 && isTickerToken(parts[0])) {
			const sym = parts[0].toUpperCase();
			if (onTickerChange) {
				onTickerChange(sym);
			} else {
				goto(`/app/${sym}`);
			}
			return;
		}

		// Full form: "NTNX is q" or "AAPL bs q"
		if (parts.length > 0 && isTickerToken(parts[0])) {
			const ticker = parts[0].toUpperCase();
			let path = `/app/${ticker}`;

			if (parts[1]) {
				const section = sectionAliases[lower[1] as keyof typeof sectionAliases] || lower[1];
				if (section in sectionAliases || Object.values(sectionAliases).includes(section)) {
					path += `/${section}`;

					if (parts[2]) {
						const subsection =
							subsectionAliases[lower[2] as keyof typeof subsectionAliases] || lower[2];
						if (
							subsection in subsectionAliases ||
							Object.values(subsectionAliases).includes(subsection)
						) {
							path += `/${subsection}`;
						}
					}
				}
			}

			goto(path);
		}
	}

	function handleSubmit(event?: Event) {
		event?.preventDefault();
		event?.stopPropagation();
		if (inputValue.trim()) {
			history = [...history, inputValue];
			historyIndex = history.length;
			parseCommand(inputValue);
			inputValue = '';
		}
		return false;
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			event.preventDefault();
			handleSubmit();
		} else if (event.key === 'ArrowUp') {
			event.preventDefault();
			if (historyIndex > 0) {
				historyIndex--;
				inputValue = history[historyIndex];
			}
		} else if (event.key === 'ArrowDown') {
			event.preventDefault();
			if (historyIndex < history.length - 1) {
				historyIndex++;
				inputValue = history[historyIndex];
			} else if (historyIndex === history.length - 1) {
				historyIndex = history.length;
				inputValue = '';
			}
		}
	}

	function handleGlobalKeydown(event: KeyboardEvent) {
		if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey) {
			event.preventDefault();
			inputRef?.focus();
		}
	}

	onMount(() => {
		window.addEventListener('keydown', handleGlobalKeydown);
		// Ensure input gets focus so Enter works (autofocus can fail in some contexts)
		setTimeout(() => inputRef?.focus(), 100);
		return () => {
			window.removeEventListener('keydown', handleGlobalKeydown);
		};
	});
</script>

<form
	class="flex w-full flex-col"
	role="search"
	style="display: contents"
	onsubmit={(e) => {
		e.preventDefault();
		e.stopPropagation();
		handleSubmit(e);
		return false;
	}}
>
	<div
		class="flex w-full items-center gap-2 rounded-md border border-gray-800 bg-gray-900 p-3"
		role="button"
		tabindex="0"
		onclick={() => inputRef?.focus()}
		onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); inputRef?.focus(); } }}
	>
		<span class="mr-2 font-mono text-green-400">❯</span>
		<input
			bind:this={inputRef}
			type="text"
			bind:value={inputValue}
			onkeydown={handleKeydown}
			autofocus
			placeholder="Ticker (e.g. AAPL) or NTNX is q"
			class="flex-1 border-none bg-transparent font-mono text-sm text-gray-100 outline-none placeholder:text-gray-600"
			aria-label="Command line — type a ticker for overview, or ticker plus section e.g. NTNX is q"
		/>
		<button
			type="submit"
			class="rounded bg-green-600 px-3 py-1 text-sm font-medium text-white hover:bg-green-500"
		>
			Go
		</button>
	</div>
</form>
