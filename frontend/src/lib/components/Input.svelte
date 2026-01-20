<script lang="ts">
	interface Props {
		type?: 'text' | 'number' | 'email' | 'password' | 'date' | 'datetime-local' | 'time';
		name: string;
		value?: string | number;
		placeholder?: string;
		required?: boolean;
		disabled?: boolean;
		class?: string;
		min?: string | number;
		max?: string | number;
		step?: string | number;
		oninput?: (event: Event) => void;
	}

	let {
		type = 'text',
		name,
		value = $bindable(),
		placeholder = '',
		required = false,
		disabled = false,
		class: className = '',
		min,
		max,
		step,
		oninput
	}: Props = $props();
</script>

<input
	{type}
	{name}
	bind:value
	{placeholder}
	{required}
	{disabled}
	{min}
	{max}
	{step}
	class="input {className}"
	{oninput}
/>
