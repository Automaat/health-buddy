export interface HealthGoal {
	id: number;
	owner: string;
	name: string;
	goal_type: string;
	target_value: number;
	target_unit: string;
	target_date?: string;
	current_value?: number;
	start_value?: number;
	is_completed: boolean;
	created_at: string;
	updated_at: string;
}

export interface HealthGoalCreate {
	owner: string;
	name: string;
	goal_type: string;
	target_value: number;
	target_unit: string;
	target_date?: string;
	current_value?: number;
	start_value?: number;
}

export interface HealthGoalUpdate {
	name?: string;
	goal_type?: string;
	target_value?: number;
	target_unit?: string;
	target_date?: string;
	current_value?: number;
	start_value?: number;
	is_completed?: boolean;
}
