<script lang="ts">
	import { onMount } from 'svelte';
	import Card from './Card.svelte';
	import type { EChartsOption } from 'echarts';

	interface Props {
		title: string;
		options: EChartsOption;
		height?: string;
		variant?: 'default' | 'blue' | 'green' | 'yellow' | 'red' | 'teal';
	}

	let { title, options, height = '300px', variant = 'default' }: Props = $props();

	let chartElement: HTMLDivElement;
	let chart: any;

	onMount(async () => {
		const echarts = await import('echarts');
		chart = echarts.init(chartElement);
		chart.setOption(options);

		const handleResize = () => {
			chart?.resize();
		};

		window.addEventListener('resize', handleResize);

		return () => {
			window.removeEventListener('resize', handleResize);
			chart?.dispose();
		};
	});

	$effect(() => {
		if (chart && options) {
			chart.setOption(options);
		}
	});
</script>

<Card {variant}>
	<h3>{title}</h3>
	<div bind:this={chartElement} style="width: 100%; height: {height};"></div>
</Card>

<style>
	h3 {
		margin-bottom: var(--size-3);
	}
</style>
