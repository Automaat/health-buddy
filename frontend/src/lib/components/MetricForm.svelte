<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from './Button.svelte';
	import Input from './Input.svelte';
	import Select from './Select.svelte';
	import { METRIC_TYPES, METRIC_TYPE_LABELS, UNITS } from '$lib/constants';
	import type { HealthMetric } from '$lib/types/health-metric';

	export let metric: HealthMetric | null = null;
	export let onClose: () => void;
	export let owner = 'default';

	const isEdit = !!metric;

	// Metric type options
	const metricTypeOptions = Object.entries(METRIC_TYPE_LABELS).map(([value, label]) => ({
		value,
		label
	}));

	// Get default unit for metric type
	function getDefaultUnit(metricType: string): string {
		switch (metricType) {
			case METRIC_TYPES.BLOOD_PRESSURE_SYSTOLIC:
			case METRIC_TYPES.BLOOD_PRESSURE_DIASTOLIC:
				return UNITS.MMHG;
			case METRIC_TYPES.HEART_RATE:
				return UNITS.BPM;
			case METRIC_TYPES.WEIGHT:
				return UNITS.KG;
			case METRIC_TYPES.GLUCOSE:
				return UNITS.MG_DL;
			case METRIC_TYPES.SPO2:
				return UNITS.PERCENT;
			case METRIC_TYPES.TEMPERATURE:
				return UNITS.CELSIUS;
			case METRIC_TYPES.SLEEP_HOURS:
				return UNITS.HOURS;
			case METRIC_TYPES.STEPS:
			case METRIC_TYPES.HRV:
				return UNITS.COUNT;
			default:
				return '';
		}
	}

	let selectedMetricType = metric?.metric_type || METRIC_TYPES.WEIGHT;
	let unit = metric?.unit || getDefaultUnit(selectedMetricType);

	$: {
		if (!isEdit) {
			unit = getDefaultUnit(selectedMetricType);
		}
	}

	// Format datetime for input
	function formatDateTimeForInput(dateStr: string): string {
		const date = new Date(dateStr);
		return date.toISOString().slice(0, 16);
	}

	let measuredAt =
		metric?.measured_at ? formatDateTimeForInput(metric.measured_at) : new Date().toISOString().slice(0, 16);
</script>

<form method="POST" action={isEdit ? '?/update' : '?/create'} use:enhance>
	{#if isEdit}
		<input type="hidden" name="id" value={metric?.id} />
	{/if}
	<input type="hidden" name="owner" value={owner} />

	<div class="form-group">
		<label for="metric_type">Metric Type</label>
		<Select
			id="metric_type"
			name="metric_type"
			options={metricTypeOptions}
			bind:value={selectedMetricType}
			disabled={isEdit}
		/>
	</div>

	<div class="form-group">
		<label for="value">Value</label>
		<Input
			id="value"
			name="value"
			type="number"
			step="0.01"
			value={metric?.value?.toString() || ''}
			required
		/>
	</div>

	<div class="form-group">
		<label for="unit">Unit</label>
		<Input id="unit" name="unit" type="text" bind:value={unit} readonly />
	</div>

	<div class="form-group">
		<label for="measured_at">Measured At</label>
		<Input id="measured_at" name="measured_at" type="datetime-local" bind:value={measuredAt} required />
	</div>

	<div class="form-group">
		<label for="notes">Notes</label>
		<textarea id="notes" name="notes" rows="3">{metric?.notes || ''}</textarea>
	</div>

	<div class="form-actions">
		<Button type="button" variant="secondary" onclick={onClose}>Cancel</Button>
		<Button type="submit" variant="primary">{isEdit ? 'Update' : 'Add'} Metric</Button>
	</div>
</form>

<style>
	.form-group {
		margin-bottom: var(--size-4);
	}

	label {
		display: block;
		margin-bottom: var(--size-2);
		font-weight: 600;
		color: var(--color-text);
	}

	textarea {
		width: 100%;
		padding: var(--size-2);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-2);
		background: var(--color-bg);
		color: var(--color-text);
		font-family: inherit;
		resize: vertical;
	}

	textarea:focus {
		outline: none;
		border-color: var(--color-primary);
	}

	.form-actions {
		display: flex;
		gap: var(--size-2);
		justify-content: flex-end;
		margin-top: var(--size-4);
	}
</style>
