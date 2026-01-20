import { get, post, del } from '$lib/utils/api';
import type { LabResult } from '$lib/types/lab-result';
import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
	try {
		const labResults = await get<LabResult[]>('/api/lab-results');
		return {
			labResults
		};
	} catch (error) {
		console.error('Failed to load lab results:', error);
		return {
			labResults: []
		};
	}
};

export const actions: Actions = {
	create: async ({ request }) => {
		const data = await request.formData();
		const valuesJson = data.get('values');

		let values = [];
		if (valuesJson) {
			try {
				values = JSON.parse(valuesJson as string);
			} catch (_e) {
				return fail(400, { error: 'Invalid values format' });
			}
		}

		const labResultData = {
			test_date: data.get('test_date'),
			lab_name: data.get('lab_name'),
			ordering_doctor: data.get('ordering_doctor') || null,
			notes: data.get('notes') || null,
			owner: data.get('owner') || 'default',
			values
		};

		try {
			await post('/api/lab-results', labResultData);
			return { success: true };
		} catch (_error) {
			return fail(400, { error: 'Failed to create lab result' });
		}
	},

	delete: async ({ request }) => {
		const data = await request.formData();
		const id = Number(data.get('id'));

		try {
			await del(`/api/lab-results/${id}`);
			return { success: true };
		} catch (_error) {
			return fail(400, { error: 'Failed to delete lab result' });
		}
	}
};
