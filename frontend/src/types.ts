export interface User {
  id: number;
  username: string;
}

export interface ExerciseDefinition {
  id: number;
  muscle_group: string;
  name: string;
  sets: number;
  rep_range_low: number;
  rep_range_high: number;
}

export interface GymDay {
  id: number;
  name: string;
  exercises: ExerciseDefinition[];
}

export interface RoutineSummary {
  id: number;
  name: string;
  is_active: boolean;
}

export interface Routine extends RoutineSummary {
  gym_days: GymDay[];
}

export interface ExerciseResult {
  exercise_definition_id: number;
  weight_lb: number;
  reps_done: number;
}

export interface LoggedSession {
  id: number;
  gym_day_id: number;
  logged_at: string;
  results: ExerciseResult[];
}

export interface ExerciseProgressPoint {
  logged_at: string;
  weight_lb: number;
  reps_done: number;
}

export interface ExerciseDefinitionInput {
  muscle_group: string;
  name: string;
  sets: number;
  rep_range_low: number;
  rep_range_high: number;
}

export interface GymDayInput {
  name: string;
  exercises: ExerciseDefinitionInput[];
}

export interface RoutineInput {
  name: string;
  gym_days: GymDayInput[];
}
