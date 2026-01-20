export interface Allergy {
	id: number;
	owner: string;
	allergen: string;
	reaction_type: string;
	severity: string;
	identified_date?: string;
	notes?: string;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface AllergyCreate {
	owner: string;
	allergen: string;
	reaction_type: string;
	severity: string;
	identified_date?: string;
	notes?: string;
}

export interface AllergyUpdate {
	allergen?: string;
	reaction_type?: string;
	severity?: string;
	identified_date?: string;
	notes?: string;
	is_active?: boolean;
}
