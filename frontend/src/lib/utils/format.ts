export function formatDate(dateString: string): string {
	const date = new Date(dateString);
	return date.toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	});
}

export function formatDateTime(dateString: string): string {
	const date = new Date(dateString);
	return date.toLocaleString('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
		hour: '2-digit',
		minute: '2-digit'
	});
}

export function formatMetricValue(value: number, unit: string): string {
	return `${value.toFixed(1)} ${unit}`;
}

export function formatLabValue(
	value: string,
	unit: string,
	referenceRange?: string
): string {
	let result = `${value} ${unit}`;
	if (referenceRange) {
		result += ` (Ref: ${referenceRange})`;
	}
	return result;
}

export function formatBloodPressure(systolic: number, diastolic: number): string {
	return `${systolic}/${diastolic} mmHg`;
}

export function calculateBMI(weight: number, heightCm: number): number {
	const heightM = heightCm / 100;
	return weight / (heightM * heightM);
}

export function formatGoalProgress(current: number, target: number, start: number): string {
	const totalChange = target - start;
	const currentChange = current - start;
	const progress = (currentChange / totalChange) * 100;
	return `${Math.round(progress)}%`;
}

export function isUpcomingDate(dateString: string, daysAhead: number = 7): boolean {
	const date = new Date(dateString);
	const today = new Date();
	const futureDate = new Date(today);
	futureDate.setDate(today.getDate() + daysAhead);

	return date >= today && date <= futureDate;
}

export function isPastDate(dateString: string): boolean {
	const date = new Date(dateString);
	const today = new Date();
	today.setHours(0, 0, 0, 0);
	return date < today;
}

export function getRelativeTime(dateString: string): string {
	const date = new Date(dateString);
	const now = new Date();
	const diffMs = now.getTime() - date.getTime();
	const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

	if (diffDays === 0) return 'Today';
	if (diffDays === 1) return 'Yesterday';
	if (diffDays < 7) return `${diffDays} days ago`;
	if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
	if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
	return `${Math.floor(diffDays / 365)} years ago`;
}
