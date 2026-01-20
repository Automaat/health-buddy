<script lang="ts">
	interface Props {
		class?: string;
		variant?: 'default' | 'blue' | 'green' | 'yellow' | 'red' | 'teal';
		children?: import('svelte').Snippet;
	}

	let { class: className = '', variant = 'default', children }: Props = $props();

	const variantClass = $derived(variant !== 'default' ? `metric-card ${variant}` : '');
</script>

<div class="card {variantClass} {className}">
	{#if children}
		{@render children()}
	{/if}
</div>
