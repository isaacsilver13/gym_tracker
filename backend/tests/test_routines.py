def _routine_payload():
    return {
        "name": "Push Pull Legs",
        "gym_days": [
            {
                "name": "Push Day",
                "exercises": [
                    {
                        "muscle_group": "Chest",
                        "name": "Bench Press",
                        "sets": 4,
                        "rep_range_low": 6,
                        "rep_range_high": 10,
                    },
                    {
                        "muscle_group": "Shoulders",
                        "name": "Overhead Press",
                        "sets": 3,
                        "rep_range_low": 8,
                        "rep_range_high": 12,
                    },
                ],
            },
            {
                "name": "Pull Day",
                "exercises": [
                    {
                        "muscle_group": "Back",
                        "name": "Deadlift",
                        "sets": 3,
                        "rep_range_low": 5,
                        "rep_range_high": 5,
                    }
                ],
            },
        ],
    }


def test_create_routine_and_fetch_detail(auth_client):
    created = auth_client.post("/api/v1/routines", json=_routine_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["name"] == "Push Pull Legs"
    assert len(body["gym_days"]) == 2
    assert len(body["gym_days"][0]["exercises"]) == 2

    fetched = auth_client.get(f"/api/v1/routines/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body


def test_list_routines_returns_summaries(auth_client):
    auth_client.post("/api/v1/routines", json=_routine_payload())
    response = auth_client.get("/api/v1/routines")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Push Pull Legs"


def test_log_session_and_read_back(auth_client):
    routine = auth_client.post("/api/v1/routines", json=_routine_payload()).json()
    push_day = routine["gym_days"][0]
    bench = push_day["exercises"][0]
    overhead = push_day["exercises"][1]

    response = auth_client.post(
        f"/api/v1/routines/{routine['id']}/sessions",
        json={
            "gym_day_id": push_day["id"],
            "results": [
                {"exercise_definition_id": bench["id"], "weight_lb": 185, "reps_done": 8},
                {"exercise_definition_id": overhead["id"], "weight_lb": 95, "reps_done": 10},
            ],
        },
    )
    assert response.status_code == 201
    assert len(response.json()["results"]) == 2

    sessions = auth_client.get(f"/api/v1/routines/{routine['id']}/sessions")
    assert sessions.status_code == 200
    assert len(sessions.json()) == 1


def test_log_session_rejects_exercise_from_another_day(auth_client):
    routine = auth_client.post("/api/v1/routines", json=_routine_payload()).json()
    push_day = routine["gym_days"][0]
    pull_day_exercise = routine["gym_days"][1]["exercises"][0]

    response = auth_client.post(
        f"/api/v1/routines/{routine['id']}/sessions",
        json={
            "gym_day_id": push_day["id"],
            "results": [
                {
                    "exercise_definition_id": pull_day_exercise["id"],
                    "weight_lb": 225,
                    "reps_done": 5,
                }
            ],
        },
    )
    assert response.status_code == 400


def test_exercise_progress_tracks_multiple_sessions(auth_client):
    routine = auth_client.post("/api/v1/routines", json=_routine_payload()).json()
    push_day = routine["gym_days"][0]
    bench = push_day["exercises"][0]

    for weight in (185, 190, 195):
        auth_client.post(
            f"/api/v1/routines/{routine['id']}/sessions",
            json={
                "gym_day_id": push_day["id"],
                "results": [
                    {"exercise_definition_id": bench["id"], "weight_lb": weight, "reps_done": 8}
                ],
            },
        )

    progress = auth_client.get(f"/api/v1/exercises/{bench['id']}/progress")
    assert progress.status_code == 200
    assert [point["weight_lb"] for point in progress.json()] == [185, 190, 195]


def test_routine_is_isolated_per_user(client):
    client.post("/api/v1/auth/register", json={"username": "alice", "password": "correct-horse"})
    routine = client.post("/api/v1/routines", json=_routine_payload()).json()
    client.post("/api/v1/auth/logout")

    client.post("/api/v1/auth/register", json={"username": "bob", "password": "another-password"})
    response = client.get(f"/api/v1/routines/{routine['id']}")
    assert response.status_code == 404


def test_delete_routine(auth_client):
    routine = auth_client.post("/api/v1/routines", json=_routine_payload()).json()
    response = auth_client.delete(f"/api/v1/routines/{routine['id']}")
    assert response.status_code == 204
    assert auth_client.get(f"/api/v1/routines/{routine['id']}").status_code == 404
