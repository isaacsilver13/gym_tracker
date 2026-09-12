import { useEffect, useState } from "react";

import * as api from "../api/client";
import { GlassCard } from "../components/GlassCard";
import type { RoutineSummary } from "../types";

interface RoutineListProps {
  onSelect: (routineId: number) => void;
  onCreateNew: () => void;
}

export function RoutineList({ onSelect, onCreateNew }: RoutineListProps) {
  const [routines, setRoutines] = useState<RoutineSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listRoutines()
      .then(setRoutines)
      .catch((err) => setError(err instanceof Error ? err.message : "Unable to load routines"));
  }, []);

  return (
    <section>
      <div className="section-heading">
        <h2>Your routines</h2>
        <button type="button" onClick={onCreateNew}>
          + New routine
        </button>
      </div>
      {error && <p className="form-error">{error}</p>}
      {routines === null ? (
        <p className="muted">Loading...</p>
      ) : routines.length === 0 ? (
        <GlassCard className="empty-state">
          <p>No routines yet. Build your first one to start logging workouts.</p>
        </GlassCard>
      ) : (
        <div className="routine-grid">
          {routines.map((routine) => (
            <GlassCard
              className="routine-card"
              key={routine.id}
              onClick={() => onSelect(routine.id)}
              role="button"
              tabIndex={0}
            >
              <h3>{routine.name}</h3>
            </GlassCard>
          ))}
        </div>
      )}
    </section>
  );
}
