<script lang="ts">
	interface Props {
		headers: string[];
		class?: string;
		children?: import('svelte').Snippet;
	}

	let { headers, class: className = '', children }: Props = $props();
</script>

<table class="table {className}">
	<thead>
		<tr>
			{#each headers as header}
				<th>{header}</th>
			{/each}
		</tr>
	</thead>
	<tbody>
		{#if children}
			{@render children()}
		{/if}
	</tbody>
</table>
