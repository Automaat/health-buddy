import { describe, it, expect } from 'vitest';
import {
	formatDate,
	formatDateTime,
	formatMetricValue,
	formatLabValue,
	formatBloodPressure,
	calculateBMI,
	formatGoalProgress,
	isUpcomingDate,
	isPastDate,
	getRelativeTime
} from './format';

describe('format utilities', () => {
	describe('formatDate', () => {
		it('formats date correctly', () => {
			const result = formatDate('2024-01-15T10:30:00');
			expect(result).toBe('Jan 15, 2024');
		});
	});

	describe('formatDateTime', () => {
		it('formats datetime correctly', () => {
			const result = formatDateTime('2024-01-15T10:30:00');
			expect(result).toContain('Jan 15, 2024');
			expect(result).toContain('10:30');
		});
	});

	describe('formatMetricValue', () => {
		it('formats number with 1 decimal place', () => {
			expect(formatMetricValue(123.456, 'kg')).toBe('123.5 kg');
		});

		it('formats integer correctly', () => {
			expect(formatMetricValue(100, 'bpm')).toBe('100.0 bpm');
		});

		it('formats string value without decimal conversion', () => {
			expect(formatMetricValue('120/80', 'mmHg')).toBe('120/80 mmHg');
		});
	});

	describe('formatBloodPressure', () => {
		it('formats blood pressure correctly', () => {
			expect(formatBloodPressure(120, 80)).toBe('120/80 mmHg');
		});
	});

	describe('calculateBMI', () => {
		it('calculates BMI correctly', () => {
			const bmi = calculateBMI(70, 175);
			expect(bmi).toBeCloseTo(22.86, 2);
		});
	});

	describe('formatGoalProgress', () => {
		it('calculates progress correctly', () => {
			expect(formatGoalProgress(75, 80, 70)).toBe('50%');
		});

		it('handles completed goal', () => {
			expect(formatGoalProgress(80, 80, 70)).toBe('100%');
		});

		it('handles zero change target', () => {
			expect(formatGoalProgress(70, 70, 70)).toBe('100%');
		});
	});

	describe('formatLabValue', () => {
		it('formats value without reference range', () => {
			expect(formatLabValue('120', 'mg/dL')).toBe('120 mg/dL');
		});

		it('formats value with reference range', () => {
			expect(formatLabValue('120', 'mg/dL', '70-100')).toBe('120 mg/dL (Ref: 70-100)');
		});
	});

	describe('isUpcomingDate', () => {
		it('returns true for date within 7 days', () => {
			const tomorrow = new Date();
			tomorrow.setDate(tomorrow.getDate() + 1);
			expect(isUpcomingDate(tomorrow.toISOString())).toBe(true);
		});

		it('returns false for date beyond 7 days', () => {
			const future = new Date();
			future.setDate(future.getDate() + 10);
			expect(isUpcomingDate(future.toISOString())).toBe(false);
		});

		it('returns false for past date', () => {
			const past = new Date();
			past.setDate(past.getDate() - 1);
			expect(isUpcomingDate(past.toISOString())).toBe(false);
		});

		it('respects custom daysAhead parameter', () => {
			const future = new Date();
			future.setDate(future.getDate() + 15);
			expect(isUpcomingDate(future.toISOString(), 20)).toBe(true);
		});
	});

	describe('isPastDate', () => {
		it('returns true for past date', () => {
			const past = new Date();
			past.setDate(past.getDate() - 1);
			expect(isPastDate(past.toISOString())).toBe(true);
		});

		it('returns false for today', () => {
			const today = new Date();
			expect(isPastDate(today.toISOString())).toBe(false);
		});

		it('returns false for future date', () => {
			const future = new Date();
			future.setDate(future.getDate() + 1);
			expect(isPastDate(future.toISOString())).toBe(false);
		});
	});

	describe('getRelativeTime', () => {
		it('returns "Today" for current date', () => {
			const now = new Date();
			expect(getRelativeTime(now.toISOString())).toBe('Today');
		});

		it('returns "Yesterday" for 1 day ago', () => {
			const yesterday = new Date();
			yesterday.setDate(yesterday.getDate() - 1);
			expect(getRelativeTime(yesterday.toISOString())).toBe('Yesterday');
		});

		it('returns days for less than a week', () => {
			const daysAgo = new Date();
			daysAgo.setDate(daysAgo.getDate() - 5);
			expect(getRelativeTime(daysAgo.toISOString())).toBe('5 days ago');
		});

		it('returns weeks for less than a month', () => {
			const weeksAgo = new Date();
			weeksAgo.setDate(weeksAgo.getDate() - 14);
			expect(getRelativeTime(weeksAgo.toISOString())).toBe('2 weeks ago');
		});

		it('returns months for less than a year', () => {
			const monthsAgo = new Date();
			monthsAgo.setDate(monthsAgo.getDate() - 60);
			expect(getRelativeTime(monthsAgo.toISOString())).toBe('2 months ago');
		});

		it('returns years for more than a year', () => {
			const yearsAgo = new Date();
			yearsAgo.setDate(yearsAgo.getDate() - 400);
			expect(getRelativeTime(yearsAgo.toISOString())).toBe('1 years ago');
		});
	});
});
