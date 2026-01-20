export interface MedicalHistory {
	id: number;
	owner: string;
	event_type: string;
	description: string;
	event_date: string;
	provider?: string;
	notes?: string;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface MedicalHistoryCreate {
	owner: string;
	event_type: string;
	description: string;
	event_date: string;
	provider?: string;
	notes?: string;
}

export interface MedicalHistoryUpdate {
	event_type?: string;
	description?: string;
	event_date?: string;
	provider?: string;
	notes?: string;
	is_active?: boolean;
}
