import { get, post, put, del } from '$lib/utils/api';
import type { HealthMetric } from '$lib/types/health-metric';
import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ url }) => {
	const metricType = url.searchParams.get('type') || 'weight';
	const startDate = url.searchParams.get('start_date');
	const endDate = url.searchParams.get('end_date');

	try {
		let endpoint = `/api/health-metrics?metric_type=${metricType}`;
		if (startDate) endpoint += `&start_date=${startDate}`;
		if (endDate) endpoint += `&end_date=${endDate}`;

		const metrics = await get<HealthMetric[]>(endpoint);
		return {
			metrics,
			selectedType: metricType
		};
	} catch (error) {
		console.error('Failed to load metrics:', error);
		return {
			metrics: [],
			selectedType: metricType
		};
	}
};

export const actions: Actions = {
	create: async ({ request }) => {
		const data = await request.formData();
		const metricData = {
			metric_type: data.get('metric_type'),
			value: parseFloat(data.get('value') as string),
			unit: data.get('unit'),
			measured_at: data.get('measured_at'),
			notes: data.get('notes') || null,
			owner: data.get('owner') || 'default'
		};

		try {
			await post('/api/health-metrics', metricData);
			return { success: true };
		} catch (error) {
			return fail(400, { error: 'Failed to create metric' });
		}
	},

	update: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');
		const metricData = {
			metric_type: data.get('metric_type'),
			value: parseFloat(data.get('value') as string),
			unit: data.get('unit'),
			measured_at: data.get('measured_at'),
			notes: data.get('notes') || null
		};

		try {
			await put(`/api/health-metrics/${id}`, metricData);
			return { success: true };
		} catch (error) {
			return fail(400, { error: 'Failed to update metric' });
		}
	},

	delete: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');

		try {
			await del(`/api/health-metrics/${id}`);
			return { success: true };
		} catch (error) {
			return fail(400, { error: 'Failed to delete metric' });
		}
	}
};
