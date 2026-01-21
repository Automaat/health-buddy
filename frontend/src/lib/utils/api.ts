import { browser } from '$app/environment';
import { API_BASE_URL } from '$lib/constants';

function getApiUrl(): string {
	if (browser) {
		return API_BASE_URL;
	}
	return process.env.API_URL_INTERNAL || API_BASE_URL;
}

export class APIError extends Error {
	constructor(
		message: string,
		public status: number,
		public body?: unknown
	) {
		super(message);
		this.name = 'APIError';
	}
}

export async function fetchAPI<T>(
	endpoint: string,
	options: RequestInit = {}
): Promise<T> {
	const url = `${getApiUrl()}${endpoint}`;

	const defaultHeaders: HeadersInit = {
		'Content-Type': 'application/json'
	};

	const config: RequestInit = {
		...options,
		headers: {
			...defaultHeaders,
			...options.headers
		}
	};

	try {
		const response = await fetch(url, config);

		if (!response.ok) {
			let errorBody: unknown;
			try {
				errorBody = await response.json();
			} catch {
				errorBody = await response.text();
			}

			throw new APIError(
				`API request failed: ${response.statusText}`,
				response.status,
				errorBody
			);
		}

		if (response.status === 204) {
			return null as T;
		}

		return await response.json();
	} catch (error) {
		if (error instanceof APIError) {
			throw error;
		}

		throw new APIError(
			`Network request failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
			0
		);
	}
}

export async function get<T>(endpoint: string): Promise<T> {
	return fetchAPI<T>(endpoint, { method: 'GET' });
}

export async function post<T>(endpoint: string, data: unknown): Promise<T> {
	return fetchAPI<T>(endpoint, {
		method: 'POST',
		body: JSON.stringify(data)
	});
}

export async function put<T>(endpoint: string, data: unknown): Promise<T> {
	return fetchAPI<T>(endpoint, {
		method: 'PUT',
		body: JSON.stringify(data)
	});
}

export async function del<T>(endpoint: string): Promise<T> {
	return fetchAPI<T>(endpoint, { method: 'DELETE' });
}
