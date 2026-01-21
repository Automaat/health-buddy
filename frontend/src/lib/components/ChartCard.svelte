<script lang="ts">
	import { onMount } from 'svelte';
	import { Card, CardHeader, CardTitle, CardContent } from '@mskalski/home-ui';
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

	onMount(() => {
		import('echarts').then((echarts) => {
			chart = echarts.init(chartElement);
			chart.setOption(options);

			const handleResize = () => {
				chart?.resize();
			};

			window.addEventListener('resize', handleResize);
		});

		return () => {
			if (chart) {
				window.removeEventListener('resize', () => chart?.resize());
				chart.dispose();
			}
		};
	});

	$effect(() => {
		if (chart && options) {
			chart.setOption(options);
		}
	});
</script>

<Card {variant}>
	<CardHeader>
		<CardTitle>{title}</CardTitle>
	</CardHeader>
	<CardContent>
		<div bind:this={chartElement} style="width: 100%; height: {height};"></div>
	</CardContent>
</Card>
