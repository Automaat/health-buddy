<script lang="ts">
	interface Props {
		name: string;
		value?: string | number;
		options: Array<{ label: string; value: string | number }>;
		required?: boolean;
		disabled?: boolean;
		class?: string;
		placeholder?: string;
		onchange?: (event: Event) => void;
	}

	let {
		name,
		value = $bindable(),
		options,
		required = false,
		disabled = false,
		class: className = '',
		placeholder,
		onchange
	}: Props = $props();
</script>

<select
	{name}
	bind:value
	{required}
	{disabled}
	class="select {className}"
	{onchange}
>
	{#if placeholder}
		<option value="" disabled selected={value === '' || value == null}>{placeholder}</option>
	{/if}
	{#each options as option}
		<option value={option.value}>{option.label}</option>
	{/each}
</select>
