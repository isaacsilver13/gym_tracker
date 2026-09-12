from datetime import UTC, datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)

    routines: Mapped[list["Routine"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Routine(Base):
    __tablename__ = "routines"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)

    user: Mapped["User"] = relationship(back_populates="routines")
    gym_days: Mapped[list["GymDay"]] = relationship(
        back_populates="routine",
        cascade="all, delete-orphan",
        order_by="GymDay.order_index",
    )


class GymDay(Base):
    __tablename__ = "gym_days"

    id: Mapped[int] = mapped_column(primary_key=True)
    routine_id: Mapped[int] = mapped_column(
        ForeignKey("routines.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str]
    order_index: Mapped[int]

    routine: Mapped["Routine"] = relationship(back_populates="gym_days")
    exercises: Mapped[list["ExerciseDefinition"]] = relationship(
        back_populates="gym_day",
        cascade="all, delete-orphan",
        order_by="ExerciseDefinition.order_index",
    )
    sessions: Mapped[list["LoggedSession"]] = relationship(
        back_populates="gym_day", cascade="all, delete-orphan"
    )


class ExerciseDefinition(Base):
    __tablename__ = "exercise_definitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    gym_day_id: Mapped[int] = mapped_column(
        ForeignKey("gym_days.id", ondelete="CASCADE"), index=True
    )
    muscle_group: Mapped[str]
    name: Mapped[str]
    sets: Mapped[int]
    rep_range_low: Mapped[int]
    rep_range_high: Mapped[int]
    order_index: Mapped[int]

    gym_day: Mapped["GymDay"] = relationship(back_populates="exercises")
    results: Mapped[list["LoggedExerciseResult"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )


class LoggedSession(Base):
    __tablename__ = "logged_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    gym_day_id: Mapped[int] = mapped_column(
        ForeignKey("gym_days.id", ondelete="CASCADE"), index=True
    )
    logged_at: Mapped[datetime] = mapped_column(default=_utcnow, index=True)

    gym_day: Mapped["GymDay"] = relationship(back_populates="sessions")
    results: Mapped[list["LoggedExerciseResult"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class LoggedExerciseResult(Base):
    __tablename__ = "logged_exercise_results"
    __table_args__ = (
        UniqueConstraint("session_id", "exercise_definition_id", name="uq_session_exercise"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("logged_sessions.id", ondelete="CASCADE"), index=True
    )
    exercise_definition_id: Mapped[int] = mapped_column(
        ForeignKey("exercise_definitions.id", ondelete="CASCADE"), index=True
    )
    weight_lb: Mapped[float]
    reps_done: Mapped[int]

    session: Mapped["LoggedSession"] = relationship(back_populates="results")
    exercise: Mapped["ExerciseDefinition"] = relationship(back_populates="results")
