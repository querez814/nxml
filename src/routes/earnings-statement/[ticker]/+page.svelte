<script lang="ts">
	export let data: { earnings_data?: any };

	const earnings_data = data?.earnings_data || [];

	const formattedData = Array.isArray(earnings_data)
		? earnings_data.map((entry: any) => ({
				reportedDate: entry.reportedDate || '-',
				reportedEPS: entry.reportedEPS || '0%',
				estimatedEPS: entry.estimatedEPS || '0%',
				surprise: entry.surprise || '0%',
				surprisePercentage: entry.surprisePercentage || '0%'
			}))
		: [];
</script>
