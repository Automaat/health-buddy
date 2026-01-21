<script lang="ts">
	import { Card, CardHeader, CardTitle, CardContent, Button } from '@mskalski/home-ui';
	import { API_BASE_URL } from '$lib/constants';
	import type { ImportResult } from '$lib/types/import';

	let isDragging = $state(false);
	let isUploading = $state(false);
	let result = $state<ImportResult | null>(null);
	let error = $state<string | null>(null);
	let fileInput: HTMLInputElement;

	function handleDragOver(e: DragEvent) {
		e.preventDefault();
		isDragging = true;
	}

	function handleDragLeave(e: DragEvent) {
		e.preventDefault();
		isDragging = false;
	}

	async function handleDrop(e: DragEvent) {
		e.preventDefault();
		isDragging = false;

		const file = e.dataTransfer?.files[0];
		if (file) {
			await uploadFile(file);
		}
	}

	function handleFileSelect(e: Event) {
		const input = e.target as HTMLInputElement;
		const file = input.files?.[0];
		if (file) {
			uploadFile(file);
		}
	}

	async function uploadFile(file: File) {
		if (!file.name.endsWith('.xml')) {
			error = 'Please select an XML file exported from Apple Health';
			return;
		}

		isUploading = true;
		error = null;
		result = null;

		const formData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch(`${API_BASE_URL}/api/import/apple-health`, {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				const data = await response.json();
				throw new Error(data.detail || 'Import failed');
			}

			result = await response.json();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Import failed';
		} finally {
			isUploading = false;
		}
	}

	function triggerFileInput() {
		fileInput?.click();
	}
</script>

<svelte:head>
	<title>Import - Health Buddy</title>
</svelte:head>

<div class="import-page">
	<div class="header">
		<h1>Import Health Data</h1>
	</div>

	<Card>
		<CardHeader>
			<CardTitle>Apple Health Export</CardTitle>
		</CardHeader>
		<CardContent>
			<div class="instructions">
				<h3>How to export from Apple Health:</h3>
				<ol>
					<li>Open the <strong>Health</strong> app on your iPhone</li>
					<li>Tap your profile picture in the top right</li>
					<li>Scroll down and tap <strong>Export All Health Data</strong></li>
					<li>Wait for the export to complete</li>
					<li>Share/save the <code>export.xml</code> file</li>
					<li>Upload it below</li>
				</ol>
			</div>

			<div
				class="dropzone"
				class:dragging={isDragging}
				class:uploading={isUploading}
				role="button"
				tabindex="0"
				ondragover={handleDragOver}
				ondragleave={handleDragLeave}
				ondrop={handleDrop}
				onclick={triggerFileInput}
				onkeydown={(e) => e.key === 'Enter' && triggerFileInput()}
			>
				<input
					type="file"
					accept=".xml"
					bind:this={fileInput}
					onchange={handleFileSelect}
					hidden
				/>

				{#if isUploading}
					<div class="loading">
						<span class="spinner"></span>
						<p>Processing...</p>
					</div>
				{:else}
					<div class="dropzone-content">
						<span class="icon">📁</span>
						<p>Drag & drop your <code>export.xml</code> here</p>
						<p class="or">or</p>
						<Button>Select File</Button>
					</div>
				{/if}
			</div>

			{#if error}
				<div class="message error">
					<strong>Error:</strong> {error}
				</div>
			{/if}

			{#if result}
				<div class="message success">
					<h3>Import Complete</h3>
					<div class="stats">
						<div class="stat">
							<span class="label">Total Records</span>
							<span class="value">{result.total_records}</span>
						</div>
						<div class="stat">
							<span class="label">Imported</span>
							<span class="value success-text">{result.imported}</span>
						</div>
						<div class="stat">
							<span class="label">Skipped</span>
							<span class="value">{result.skipped}</span>
						</div>
						<div class="stat">
							<span class="label">Errors</span>
							<span class="value" class:error-text={result.errors > 0}>{result.errors}</span>
						</div>
					</div>
				</div>
			{/if}
		</CardContent>
	</Card>

	<Card>
		<CardHeader>
			<CardTitle>Automatic Sync (Health Auto Export)</CardTitle>
		</CardHeader>
		<CardContent>
			<div class="instructions">
				<p>For automatic syncing, use the <strong>Health Auto Export</strong> app ($3 on App Store).</p>
				<h3>Setup:</h3>
				<ol>
					<li>Install <strong>Health Auto Export</strong> from the App Store</li>
					<li>Open the app and go to <strong>Automations</strong></li>
					<li>Create a new automation with <strong>REST API</strong> destination</li>
					<li>Use this webhook URL:</li>
				</ol>
				<div class="webhook-url">
					<code>{API_BASE_URL}/api/import/apple-health/webhook</code>
					<Button
						variant="secondary"
						on:click={() => navigator.clipboard.writeText(`${API_BASE_URL}/api/import/apple-health/webhook`)}
					>
						Copy
					</Button>
				</div>
				<ol start={5}>
					<li>Set method to <strong>POST</strong></li>
					<li>Enable the automation to run on a schedule</li>
				</ol>
			</div>
		</CardContent>
	</Card>
</div>

<style>
	.import-page {
		padding: var(--size-4) 0;
		display: flex;
		flex-direction: column;
		gap: var(--size-4);
	}

	.header {
		margin-bottom: var(--size-2);
	}

	h1 {
		margin: 0;
	}

	.instructions {
		margin-bottom: var(--size-4);
	}

	.instructions h3 {
		margin: 0 0 var(--size-2) 0;
		font-size: 1rem;
	}

	.instructions ol {
		margin: 0;
		padding-left: var(--size-4);
	}

	.instructions li {
		margin-bottom: var(--size-2);
		line-height: 1.5;
	}

	.instructions code {
		background: var(--color-bg-secondary);
		padding: 2px 6px;
		border-radius: var(--radius-1);
		font-size: 0.9em;
	}

	.dropzone {
		border: 2px dashed var(--color-border);
		border-radius: var(--radius-2);
		padding: var(--size-6);
		text-align: center;
		cursor: pointer;
		transition: all 0.2s;
		background: var(--color-bg-secondary);
	}

	.dropzone:hover,
	.dropzone.dragging {
		border-color: var(--color-primary);
		background: color-mix(in srgb, var(--color-primary) 5%, var(--color-bg-secondary));
	}

	.dropzone.uploading {
		cursor: wait;
		opacity: 0.8;
	}

	.dropzone-content .icon {
		font-size: 3rem;
		display: block;
		margin-bottom: var(--size-2);
	}

	.dropzone-content p {
		margin: var(--size-2) 0;
		color: var(--color-text-secondary);
	}

	.dropzone-content .or {
		font-size: 0.875rem;
	}

	.loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--size-2);
	}

	.spinner {
		width: 40px;
		height: 40px;
		border: 3px solid var(--color-border);
		border-top-color: var(--color-primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.message {
		margin-top: var(--size-4);
		padding: var(--size-4);
		border-radius: var(--radius-2);
	}

	.message.error {
		background: color-mix(in srgb, var(--color-error) 10%, var(--color-bg));
		border: 1px solid var(--color-error);
		color: var(--color-error);
	}

	.message.success {
		background: color-mix(in srgb, var(--color-success) 10%, var(--color-bg));
		border: 1px solid var(--color-success);
	}

	.message h3 {
		margin: 0 0 var(--size-3) 0;
		color: var(--color-success);
	}

	.stats {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
		gap: var(--size-3);
	}

	.stat {
		text-align: center;
	}

	.stat .label {
		display: block;
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		margin-bottom: var(--size-1);
	}

	.stat .value {
		font-size: 1.5rem;
		font-weight: 600;
	}

	.success-text {
		color: var(--color-success);
	}

	.error-text {
		color: var(--color-error);
	}

	.webhook-url {
		display: flex;
		align-items: center;
		gap: var(--size-2);
		margin: var(--size-3) 0;
		padding: var(--size-3);
		background: var(--color-bg-secondary);
		border-radius: var(--radius-2);
		overflow-x: auto;
	}

	.webhook-url code {
		flex: 1;
		font-size: 0.875rem;
		word-break: break-all;
	}

	@media (max-width: 768px) {
		.webhook-url {
			flex-direction: column;
			align-items: stretch;
		}

		.stats {
			grid-template-columns: repeat(2, 1fr);
		}
	}
</style>
