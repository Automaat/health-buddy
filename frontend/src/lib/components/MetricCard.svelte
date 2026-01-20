<script lang="ts">
	import Card from './Card.svelte';
	import { formatMetricValue, formatDateTime } from '$lib/utils/format';

	interface Props {
		title: string;
		value: number;
		unit: string;
		measuredAt?: string;
		variant?: 'blue' | 'green' | 'yellow' | 'red' | 'teal';
		trend?: 'up' | 'down' | 'stable';
		class?: string;
	}

	let {
		title,
		value,
		unit,
		measuredAt,
		variant = 'blue',
		trend,
		class: className = ''
	}: Props = $props();

	const trendSymbol = $derived(
		trend === 'up' ? '↑' : trend === 'down' ? '↓' : trend === 'stable' ? '→' : ''
	);
</script>

<Card {variant} class={className}>
	<div class="metric-card-content">
		<h3 class="metric-title">{title}</h3>
		<div class="metric-value">
			{formatMetricValue(value, unit)}
			{#if trendSymbol}
				<span class="trend trend-{trend}">{trendSymbol}</span>
			{/if}
		</div>
		{#if measuredAt}
			<p class="metric-time">{formatDateTime(measuredAt)}</p>
		{/if}
	</div>
</Card>

<style>
	.metric-card-content {
		display: flex;
		flex-direction: column;
		gap: var(--size-2);
	}

	.metric-title {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		margin: 0;
	}

	.metric-value {
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--color-text);
		display: flex;
		align-items: center;
		gap: var(--size-2);
	}

	.trend {
		font-size: 1.25rem;
	}

	.trend-up {
		color: var(--color-success);
	}

	.trend-down {
		color: var(--color-error);
	}

	.trend-stable {
		color: var(--color-text-secondary);
	}

	.metric-time {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		margin: 0;
	}
</style>
