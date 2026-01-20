<script lang="ts">
	interface Props {
		type?: 'button' | 'submit' | 'reset';
		variant?: 'primary' | 'success' | 'default';
		class?: string;
		onclick?: (event: MouseEvent) => void;
		disabled?: boolean;
		children?: import('svelte').Snippet;
	}

	let {
		type = 'button',
		variant = 'primary',
		class: className = '',
		onclick,
		disabled = false,
		children
	}: Props = $props();

	const variantClass = variant !== 'default' ? `btn-${variant}` : '';
</script>

<button
	{type}
	class="btn {variantClass} {className}"
	{onclick}
	{disabled}
>
	{#if children}
		{@render children()}
	{/if}
</button>
