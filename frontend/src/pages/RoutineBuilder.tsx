import { useState, type FormEvent } from "react";

import * as api from "../api/client";
import { GlassCard } from "../components/GlassCard";
import type { ExerciseDefinitionInput, GymDayInput } from "../types";

function emptyExercise(): ExerciseDefinitionInput {
  return { muscle_group: "", name: "", sets: 3, rep_range_low: 8, rep_range_high: 12 };
}

function emptyDay(index: number): GymDayInput {
  return { name: `Day ${index + 1}`, exercises: [emptyExercise()] };
}

interface RoutineBuilderProps {
  onCreated: (routineId: number) => void;
  onCancel: () => void;
}

export function RoutineBuilder({ onCreated, onCancel }: RoutineBuilderProps) {
  const [name, setName] = useState("");
  const [days, setDays] = useState<GymDayInput[]>([emptyDay(0)]);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  function updateDay(dayIndex: number, patch: Partial<GymDayInput>) {
    setDays((current) =>
      current.map((day, index) => (index === dayIndex ? { ...day, ...patch } : day)),
    );
  }

  function updateExercise(
    dayIndex: number,
    exerciseIndex: number,
    patch: Partial<ExerciseDefinitionInput>,
  ) {
    setDays((current) =>
      current.map((day, index) => {
        if (index !== dayIndex) return day;
        return {
          ...day,
          exercises: day.exercises.map((exercise, eIndex) =>
            eIndex === exerciseIndex ? { ...exercise, ...patch } : exercise,
          ),
        };
      }),
    );
  }

  function addDay() {
    setDays((current) => [...current, emptyDay(current.length)]);
  }

  function removeDay(dayIndex: number) {
    setDays((current) => current.filter((_, index) => index !== dayIndex));
  }

  function addExercise(dayIndex: number) {
    setDays((current) =>
      current.map((day, index) =>
        index === dayIndex ? { ...day, exercises: [...day.exercises, emptyExercise()] } : day,
      ),
    );
  }

  function removeExercise(dayIndex: number, exerciseIndex: number) {
    setDays((current) =>
      current.map((day, index) =>
        index === dayIndex
          ? { ...day, exercises: day.exercises.filter((_, eIndex) => eIndex !== exerciseIndex) }
          : day,
      ),
    );
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const routine = await api.createRoutine({ name, gym_days: days });
      onCreated(routine.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to create routine");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section>
      <div className="section-heading">
        <h2>Build a routine</h2>
        <button type="button" className="link-button" onClick={onCancel}>
          Cancel
        </button>
      </div>
      <form onSubmit={handleSubmit} className="routine-builder-form">
        <label>
          Routine name
          <input value={name} onChange={(event) => setName(event.target.value)} required />
        </label>

        {days.map((day, dayIndex) => (
          <GlassCard className="day-builder" key={dayIndex}>
            <div className="day-builder-heading">
              <input
                className="day-name-input"
                value={day.name}
                onChange={(event) => updateDay(dayIndex, { name: event.target.value })}
                required
              />
              {days.length > 1 && (
                <button type="button" className="link-button" onClick={() => removeDay(dayIndex)}>
                  Remove day
                </button>
              )}
            </div>

            {day.exercises.map((exercise, exerciseIndex) => (
              <div className="exercise-row" key={exerciseIndex}>
                <input
                  placeholder="Muscle group"
                  value={exercise.muscle_group}
                  onChange={(event) =>
                    updateExercise(dayIndex, exerciseIndex, { muscle_group: event.target.value })
                  }
                  required
                />
                <input
                  placeholder="Exercise name"
                  value={exercise.name}
                  onChange={(event) =>
                    updateExercise(dayIndex, exerciseIndex, { name: event.target.value })
                  }
                  required
                />
                <input
                  type="number"
                  min={1}
                  max={20}
                  aria-label="Sets"
                  value={exercise.sets}
                  onChange={(event) =>
                    updateExercise(dayIndex, exerciseIndex, { sets: Number(event.target.value) })
                  }
                  required
                />
                <input
                  type="number"
                  min={1}
                  max={100}
                  aria-label="Rep range low"
                  value={exercise.rep_range_low}
                  onChange={(event) =>
                    updateExercise(dayIndex, exerciseIndex, {
                      rep_range_low: Number(event.target.value),
                    })
                  }
                  required
                />
                <span aria-hidden>&ndash;</span>
                <input
                  type="number"
                  min={1}
                  max={100}
                  aria-label="Rep range high"
                  value={exercise.rep_range_high}
                  onChange={(event) =>
                    updateExercise(dayIndex, exerciseIndex, {
                      rep_range_high: Number(event.target.value),
                    })
                  }
                  required
                />
                {day.exercises.length > 1 && (
                  <button
                    type="button"
                    className="link-button"
                    onClick={() => removeExercise(dayIndex, exerciseIndex)}
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
            <button type="button" className="link-button" onClick={() => addExercise(dayIndex)}>
              + Add exercise
            </button>
          </GlassCard>
        ))}

        <button type="button" className="link-button" onClick={addDay}>
          + Add gym day
        </button>

        {error && <p className="form-error">{error}</p>}
        <button type="submit" disabled={submitting}>
          Save routine
        </button>
      </form>
    </section>
  );
}
