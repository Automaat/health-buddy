<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import Modal from '$lib/components/Modal.svelte';
	import LabResultCard from '$lib/components/LabResultCard.svelte';
	import LabResultForm from '$lib/components/LabResultForm.svelte';
	import Card from '$lib/components/Card.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	$: ({ labResults } = data);

	let showModal = false;

	function openAddModal() {
		showModal = true;
	}

	function closeModal() {
		showModal = false;
		invalidateAll();
	}

	async function handleDelete(id: number) {
		if (confirm('Are you sure you want to delete this lab result?')) {
			try {
				const formData = new FormData();
				formData.append('id', id.toString());

				const response = await fetch('?/delete', {
					method: 'POST',
					body: formData
				});

				if (!response.ok) {
					alert('Failed to delete lab result. Please try again.');
					return;
				}

				invalidateAll();
			} catch (error) {
				console.error('Error deleting lab result:', error);
				alert('Failed to delete lab result. Please try again.');
			}
		}
	}

	// Sort lab results by test_date descending (newest first)
	$: sortedLabResults = [...labResults].sort(
		(a, b) => new Date(b.test_date).getTime() - new Date(a.test_date).getTime()
	);
</script>

<svelte:head>
	<title>Lab Results - Health Buddy</title>
</svelte:head>

<div class="lab-results-page">
	<div class="header">
		<h1>Lab Results</h1>
		<Button onclick={openAddModal}>Add Lab Result</Button>
	</div>

	{#if sortedLabResults.length > 0}
		<div class="lab-results-list">
			{#each sortedLabResults as labResult}
				<LabResultCard {labResult} onDelete={handleDelete} />
			{/each}
		</div>
	{:else}
		<Card>
			<p class="empty-state">
				No lab results recorded yet. Click "Add Lab Result" to track your test results.
			</p>
		</Card>
	{/if}
</div>

<Modal bind:open={showModal} title="Add Lab Result" large>
	<LabResultForm onClose={closeModal} />
</Modal>

<style>
	.lab-results-page {
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

	.lab-results-list {
		display: flex;
		flex-direction: column;
		gap: var(--size-4);
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
	}
</style>
