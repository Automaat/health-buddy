export interface Vaccination {
	id: number;
	owner: string;
	vaccine_name: string;
	date_administered: string;
	next_due_date?: string;
	location?: string;
	lot_number?: string;
	notes?: string;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface VaccinationCreate {
	owner: string;
	vaccine_name: string;
	date_administered: string;
	next_due_date?: string;
	location?: string;
	lot_number?: string;
	notes?: string;
}

export interface VaccinationUpdate {
	vaccine_name?: string;
	date_administered?: string;
	next_due_date?: string;
	location?: string;
	lot_number?: string;
	notes?: string;
	is_active?: boolean;
}
