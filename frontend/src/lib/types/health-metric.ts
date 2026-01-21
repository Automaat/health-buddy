export type SourceType = 'manual' | 'apple_health_import' | 'apple_health_webhook';

export interface HealthMetric {
	id: number;
	owner: string;
	metric_type: string;
	value: number;
	unit: string;
	measured_at: string;
	notes?: string;
	source: SourceType;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface HealthMetricCreate {
	owner: string;
	metric_type: string;
	value: number;
	unit: string;
	measured_at: string;
	notes?: string;
}

export interface HealthMetricUpdate {
	metric_type?: string;
	value?: number;
	unit?: string;
	measured_at?: string;
	notes?: string;
	is_active?: boolean;
}
