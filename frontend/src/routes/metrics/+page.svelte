<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import { Card, CardHeader, CardTitle, CardContent, Button, Select, Modal } from '@mskalski/home-ui';
	import MetricForm from '$lib/components/MetricForm.svelte';
	import ChartCard from '$lib/components/ChartCard.svelte';
	import { METRIC_TYPES, METRIC_TYPE_LABELS } from '$lib/constants';
	import { formatDateTime } from '$lib/utils/format';
	import type { PageData } from './$types';
	import type { EChartsOption } from 'echarts';
	import type { HealthMetric } from '$lib/types/health-metric';

	export let data: PageData;

	$: ({ metrics, selectedType } = data);

	let showModal = false;
	let editingMetric: HealthMetric | null = null;

	// Metric type selector options
	const metricTypeOptions = Object.entries(METRIC_TYPE_LABELS).map(([value, label]) => ({
		value,
		label
	}));

	// Handle metric type change
	async function handleMetricTypeChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const url = new URL($page.url);
		url.searchParams.set('type', target.value);
		await goto(url.toString());
	}

	// Chart data
	$: chartOptions = {
		tooltip: {
			trigger: 'axis' as const,
			formatter: (params: any) => {
				const point = params[0];
				return `${point.name}<br/>${point.seriesName}: ${point.value} ${metrics[0]?.unit || ''}`;
			}
		},
		xAxis: {
			type: 'category' as const,
			data: metrics.map((m) => new Date(m.measured_at).toLocaleDateString())
		},
		yAxis: {
			type: 'value' as const,
			name: metrics[0]?.unit || ''
		},
		series: [
			{
				name: METRIC_TYPE_LABELS[selectedType],
				data: metrics.map((m) => m.value),
				type: 'line' as const,
				smooth: true,
				itemStyle: { color: '#5e81ac' }
			}
		]
	};

	function openAddModal() {
		editingMetric = null;
		showModal = true;
	}

	function openEditModal(metric: HealthMetric) {
		editingMetric = metric;
		showModal = true;
	}

	function closeModal() {
		showModal = false;
		editingMetric = null;
		invalidateAll();
	}

	async function handleDelete(id: number) {
		if (confirm('Are you sure you want to delete this metric?')) {
			try {
				const formData = new FormData();
				formData.append('id', id.toString());

				const response = await fetch('?/delete', {
					method: 'POST',
					body: formData
				});

				if (!response.ok) {
					console.error('Failed to delete metric');
					alert('Failed to delete metric. Please try again.');
					return;
				}

				invalidateAll();
			} catch (error) {
				console.error('Error deleting metric:', error);
				alert('Failed to delete metric. Please try again.');
			}
		}
	}
</script>

<svelte:head>
	<title>Health Metrics - Health Buddy</title>
</svelte:head>

<div class="metrics-page">
	<div class="header">
		<h1>Health Metrics</h1>
		<Button on:click={openAddModal}>Add Metric</Button>
	</div>

	<Card>
		<CardContent>
			<div class="filters">
				<div class="filter-group">
					<label for="metric-type">Metric Type</label>
					<Select
						id="metric-type"
						name="metric_type"
						options={metricTypeOptions}
						value={selectedType}
						on:change={handleMetricTypeChange}
					/>
				</div>
			</div>
		</CardContent>
	</Card>

	{#if metrics.length > 0}
		<ChartCard
			title="{METRIC_TYPE_LABELS[selectedType]} Trend"
			options={chartOptions}
			height="400px"
			variant="blue"
		/>

		<Card>
			<CardHeader>
				<CardTitle>All Readings</CardTitle>
			</CardHeader>
			<CardContent>
				<div class="table-wrapper">
					<table>
					<thead>
						<tr>
							<th>Date & Time</th>
							<th>Value</th>
							<th>Unit</th>
							<th>Notes</th>
							<th>Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each metrics as metric}
							<tr>
								<td>{formatDateTime(metric.measured_at)}</td>
								<td>{metric.value}</td>
								<td>{metric.unit}</td>
								<td>{metric.notes || '-'}</td>
								<td>
									<div class="actions">
										<button class="action-btn edit" on:click={() => openEditModal(metric)} aria-label={`Edit metric from ${formatDateTime(metric.measured_at)}`}>
											Edit
										</button>
										<button class="action-btn delete" on:click={() => handleDelete(metric.id)} aria-label={`Delete metric from ${formatDateTime(metric.measured_at)}`}>
											Delete
										</button>
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
					</table>
				</div>
			</CardContent>
		</Card>
	{:else}
		<Card>
			<CardContent>
				<p class="empty-state">No metrics recorded for {METRIC_TYPE_LABELS[selectedType]} yet.</p>
			</CardContent>
		</Card>
	{/if}
</div>

<Modal bind:open={showModal} title={editingMetric ? 'Edit Metric' : 'Add Metric'}>
	<MetricForm metric={editingMetric} onClose={closeModal} />
</Modal>

<style>
	.metrics-page {
		padding: var(--size-4) 0;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--size-4);
	}

	h1 {
		margin: 0;
	}

	h2 {
		margin-bottom: var(--size-4);
	}

	.filters {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: var(--size-4);
	}

	.filter-group label {
		display: block;
		margin-bottom: var(--size-2);
		font-weight: 600;
	}

	.table-wrapper {
		overflow-x: auto;
	}

	table {
		width: 100%;
		border-collapse: collapse;
	}

	thead {
		background: var(--color-bg-secondary);
	}

	th {
		padding: var(--size-3);
		text-align: left;
		font-weight: 600;
		border-bottom: 2px solid var(--color-border);
	}

	td {
		padding: var(--size-3);
		border-bottom: 1px solid var(--color-border);
	}

	.actions {
		display: flex;
		gap: var(--size-2);
	}

	.action-btn {
		padding: var(--size-1) var(--size-2);
		border: none;
		border-radius: var(--radius-2);
		font-size: 0.875rem;
		cursor: pointer;
		transition: all 0.2s;
	}

	.action-btn.edit {
		background: var(--color-primary);
		color: white;
	}

	.action-btn.edit:hover {
		opacity: 0.8;
	}

	.action-btn.delete {
		background: var(--color-error);
		color: white;
	}

	.action-btn.delete:hover {
		opacity: 0.8;
	}

	.empty-state {
		text-align: center;
		color: var(--color-text-secondary);
		padding: var(--size-6);
	}

	@media (max-width: 768px) {
		.header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--size-2);
		}

		.filters {
			grid-template-columns: 1fr;
		}
	}
</style>
