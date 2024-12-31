<script lang="ts">
	import '../../../../app.css';
	import { goto } from '$app/navigation';

	let ticker: string = '';

	function changeTicker() {
		if (ticker.trim()) {
			goto(`/${ticker}`, { replaceState: true });
		}
	}
</script>

<div class="layout-container">
	<div class="ticker-input-container">
		<label for="ticker-input">Enter Ticker:</label>
		<input
			id="ticker-input"
			type="text"
			bind:value={ticker}
			placeholder="Type ticker (e.g., AAPL)"
		/>
		<button on:click={changeTicker}>Go</button>
	</div>
	<slot />
</div>

<style>
	.layout-container {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		padding: 1rem;
	}

	.ticker-input-container {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}

	#ticker-input {
		border: 1px solid #ccc;
		padding: 0.5rem;
		border-radius: 4px;
		width: 200px;
	}

	button {
		background-color: #007bff;
		color: white;
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	button:hover {
		background-color: #0056b3;
	}
</style>
