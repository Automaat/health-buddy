export interface HealthMetric {
	id: number;
	owner: string;
	metric_type: string;
	value: number;
	unit: string;
	measured_at: string;
	notes?: string;
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
