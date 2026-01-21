<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button, Input } from '@mskalski/home-ui';
	import { LAB_TEST_TYPES } from '$lib/constants';

	export let onClose: () => void;
	export let owner = 'default';

	interface TestValue {
		test_name: string;
		value: string;
		unit: string;
		reference_range: string;
		is_abnormal: boolean;
	}

	let testDate = new Date().toISOString().slice(0, 10);
	let labName = '';
	let orderingDoctor = '';
	let notes = '';

	let values: TestValue[] = [
		{
			test_name: '',
			value: '',
			unit: '',
			reference_range: '',
			is_abnormal: false
		}
	];

	function addValue() {
		values = [
			...values,
			{
				test_name: '',
				value: '',
				unit: '',
				reference_range: '',
				is_abnormal: false
			}
		];
	}

	function removeValue(index: number) {
		values = values.filter((_, i) => i !== index);
	}

	function populateCommonTests() {
		values = [
			{
				test_name: LAB_TEST_TYPES.TOTAL_CHOLESTEROL,
				value: '',
				unit: 'mg/dL',
				reference_range: '<200',
				is_abnormal: false
			},
			{
				test_name: LAB_TEST_TYPES.LDL,
				value: '',
				unit: 'mg/dL',
				reference_range: '<100',
				is_abnormal: false
			},
			{
				test_name: LAB_TEST_TYPES.HDL,
				value: '',
				unit: 'mg/dL',
				reference_range: '>40',
				is_abnormal: false
			},
			{
				test_name: LAB_TEST_TYPES.TRIGLYCERIDES,
				value: '',
				unit: 'mg/dL',
				reference_range: '<150',
				is_abnormal: false
			}
		];
	}
</script>

<form
	method="POST"
	action="?/create"
	use:enhance={() => {
		return async ({ update }) => {
			await update();
			onClose();
		};
	}}
>
	<input type="hidden" name="owner" value={owner} />
	<input type="hidden" name="values" value={JSON.stringify(values)} />

	<div class="form-section">
		<h3>Test Information</h3>

		<div class="form-group">
			<label for="test_date">Test Date *</label>
			<Input id="test_date" name="test_date" type="date" bind:value={testDate} required />
		</div>

		<div class="form-group">
			<label for="lab_name">Lab Name *</label>
			<Input
				id="lab_name"
				name="lab_name"
				type="text"
				bind:value={labName}
				required
				placeholder="e.g., Quest Diagnostics"
			/>
		</div>

		<div class="form-group">
			<label for="ordering_doctor">Ordered By (Doctor)</label>
			<Input
				id="ordering_doctor"
				name="ordering_doctor"
				type="text"
				bind:value={orderingDoctor}
			/>
		</div>
	</div>

	<div class="form-section">
		<div class="section-header">
			<h3>Test Values</h3>
			<Button type="button" variant="secondary" size="small" on:click={populateCommonTests}>
				Pre-fill Lipid Panel
			</Button>
		</div>

		{#each values as value, index}
			<div class="value-card">
				<div class="value-header">
					<h4>Test {index + 1}</h4>
					{#if values.length > 1}
						<button
							type="button"
							class="remove-btn"
							on:click={() => removeValue(index)}
							aria-label="Remove test"
						>
							×
						</button>
					{/if}
				</div>

				<div class="form-group">
					<label for="test_name_{index}">Test Name *</label>
					<Input
						id="test_name_{index}"
						type="text"
						bind:value={value.test_name}
						required
						placeholder="e.g., Total Cholesterol"
					/>
				</div>

				<div class="form-row">
					<div class="form-group">
						<label for="value_{index}">Value *</label>
						<Input id="value_{index}" type="text" bind:value={value.value} required />
					</div>

					<div class="form-group">
						<label for="unit_{index}">Unit</label>
						<Input id="unit_{index}" type="text" bind:value={value.unit} placeholder="mg/dL" />
					</div>
				</div>

				<div class="form-group">
					<label for="reference_range_{index}">Reference Range</label>
					<Input
						id="reference_range_{index}"
						type="text"
						bind:value={value.reference_range}
						placeholder="e.g., <200"
					/>
				</div>

				<div class="form-group">
					<label class="checkbox-label">
						<input type="checkbox" bind:checked={value.is_abnormal} />
						<span>Mark as abnormal</span>
					</label>
				</div>
			</div>
		{/each}

		<Button type="button" variant="secondary" on:click={addValue}>+ Add Another Test</Button>
	</div>

	<div class="form-section">
		<div class="form-group">
			<label for="notes">Notes</label>
			<textarea id="notes" name="notes" rows="3" bind:value={notes}></textarea>
		</div>
	</div>

	<div class="form-actions">
		<Button type="button" variant="secondary" on:click={onClose}>Cancel</Button>
		<Button type="submit" variant="primary">Add Lab Result</Button>
	</div>
</form>

<style>
	.form-section {
		margin-bottom: var(--size-6);
		padding-bottom: var(--size-4);
		border-bottom: 1px solid var(--color-border);
	}

	.form-section:last-of-type {
		border-bottom: none;
	}

	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--size-4);
	}

	h3 {
		margin: 0 0 var(--size-4) 0;
		color: var(--color-text);
	}

	h4 {
		margin: 0;
		font-size: 0.875rem;
		color: var(--color-text);
	}

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
		font-size: 0.875rem;
	}

	.checkbox-label {
		display: flex;
		align-items: center;
		gap: var(--size-2);
		cursor: pointer;
	}

	.checkbox-label input[type='checkbox'] {
		width: auto;
	}

	.checkbox-label span {
		font-weight: normal;
	}

	.value-card {
		background: var(--color-bg-secondary);
		padding: var(--size-4);
		border-radius: var(--radius-2);
		margin-bottom: var(--size-4);
	}

	.value-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--size-3);
	}

	.remove-btn {
		background: var(--color-error);
		color: white;
		border: none;
		border-radius: 50%;
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		font-size: 1.25rem;
		line-height: 1;
	}

	.remove-btn:hover {
		opacity: 0.8;
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

		.section-header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--size-2);
		}
	}
</style>
