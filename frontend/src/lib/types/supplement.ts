export interface Supplement {
	id: number;
	owner: string;
	name: string;
	dosage: string;
	unit: string;
	frequency: string;
	purpose?: string;
	start_date: string;
	end_date?: string;
	brand?: string;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface SupplementCreate {
	owner: string;
	name: string;
	dosage: string;
	unit: string;
	frequency: string;
	purpose?: string;
	start_date: string;
	end_date?: string;
	brand?: string;
}

export interface SupplementUpdate {
	name?: string;
	dosage?: string;
	unit?: string;
	frequency?: string;
	purpose?: string;
	start_date?: string;
	end_date?: string;
	brand?: string;
	is_active?: boolean;
}
