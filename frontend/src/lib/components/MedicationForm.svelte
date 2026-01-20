<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from './Button.svelte';
	import Input from './Input.svelte';
	import Select from './Select.svelte';
	import { MEDICATION_FREQUENCIES } from '$lib/constants';
	import type { Medication } from '$lib/types/medication';

	export let medication: Medication | null = null;
	export let onClose: () => void;
	export let owner = 'default';

	const isEdit = !!medication;

	const frequencyOptions = MEDICATION_FREQUENCIES.map((freq) => ({
		value: freq,
		label: freq
	}));

	function formatDateForInput(dateStr: string | null): string {
		if (!dateStr) return '';
		return new Date(dateStr).toISOString().slice(0, 10);
	}
</script>

<form method="POST" action={isEdit ? '?/update' : '?/create'} use:enhance>
	{#if isEdit}
		<input type="hidden" name="id" value={medication?.id} />
	{/if}
	<input type="hidden" name="owner" value={owner} />

	<div class="form-group">
		<label for="name">Medication Name *</label>
		<Input id="name" name="name" type="text" value={medication?.name || ''} required />
	</div>

	<div class="form-row">
		<div class="form-group">
			<label for="dosage">Dosage *</label>
			<Input id="dosage" name="dosage" type="text" value={medication?.dosage || ''} required />
		</div>

		<div class="form-group">
			<label for="unit">Unit *</label>
			<Input id="unit" name="unit" type="text" value={medication?.unit || ''} required placeholder="mg, ml, etc." />
		</div>
	</div>

	<div class="form-group">
		<label for="frequency">Frequency *</label>
		<Select
			id="frequency"
			name="frequency"
			options={frequencyOptions}
			value={medication?.frequency || MEDICATION_FREQUENCIES[0]}
		/>
	</div>

	<div class="form-group">
		<label for="purpose">Purpose</label>
		<Input id="purpose" name="purpose" type="text" value={medication?.purpose || ''} />
	</div>

	<div class="form-row">
		<div class="form-group">
			<label for="start_date">Start Date *</label>
			<Input
				id="start_date"
				name="start_date"
				type="date"
				value={formatDateForInput(medication?.start_date || new Date().toISOString())}
				required
			/>
		</div>

		<div class="form-group">
			<label for="end_date">End Date</label>
			<Input
				id="end_date"
				name="end_date"
				type="date"
				value={formatDateForInput(medication?.end_date || null)}
			/>
		</div>
	</div>

	<div class="form-group">
		<label for="prescribing_doctor">Prescribing Doctor</label>
		<Input
			id="prescribing_doctor"
			name="prescribing_doctor"
			type="text"
			value={medication?.prescribing_doctor || ''}
		/>
	</div>

	<div class="form-group">
		<label for="refill_reminder_date">Refill Reminder Date</label>
		<Input
			id="refill_reminder_date"
			name="refill_reminder_date"
			type="date"
			value={formatDateForInput(medication?.refill_reminder_date || null)}
		/>
	</div>

	<div class="form-group">
		<label for="notes">Notes</label>
		<textarea id="notes" name="notes" rows="3">{medication?.notes || ''}</textarea>
	</div>

	<div class="form-actions">
		<Button type="button" variant="secondary" onclick={onClose}>Cancel</Button>
		<Button type="submit" variant="primary">{isEdit ? 'Update' : 'Add'} Medication</Button>
	</div>
</form>

<style>
	.form-group {
		margin-bottom: var(--size-4);
	}

	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--size-4);
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

	@media (max-width: 768px) {
		.form-row {
			grid-template-columns: 1fr;
		}
	}
</style>
