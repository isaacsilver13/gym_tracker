import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import * as api from "../api/client";
import type { ExerciseProgressPoint } from "../types";

export function ExerciseProgressChart({ exerciseId }: { exerciseId: number }) {
  const [points, setPoints] = useState<ExerciseProgressPoint[] | null>(null);

  useEffect(() => {
    setPoints(null);
    api.getExerciseProgress(exerciseId).then(setPoints);
  }, [exerciseId]);

  if (points === null) {
    return <p className="muted">Loading...</p>;
  }

  if (points.length === 0) {
    return <p className="muted">No sessions logged for this exercise yet.</p>;
  }

  const data = points.map((point) => ({
    date: new Date(point.logged_at).toLocaleDateString(),
    weight_lb: point.weight_lb,
    reps_done: point.reps_done,
  }));

  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height={240}>
        <LineChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
          <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
          <YAxis stroke="#94a3b8" fontSize={12} />
          <Tooltip
            contentStyle={{
              background: "#1a2035",
              border: "1px solid rgba(255,255,255,0.12)",
              borderRadius: 8,
            }}
          />
          <Line type="monotone" dataKey="weight_lb" name="Weight (lb)" stroke="#667eea" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
