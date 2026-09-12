from app.auth import hash_password, verify_password


def test_register_then_me(client):
    response = client.post(
        "/api/v1/auth/register", json={"username": "alice", "password": "correct-horse"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "alice"

    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["username"] == "alice"


def test_register_duplicate_username_rejected(client):
    client.post("/api/v1/auth/register", json={"username": "alice", "password": "correct-horse"})
    response = client.post(
        "/api/v1/auth/register", json={"username": "alice", "password": "another-password"}
    )
    assert response.status_code == 409


def test_login_wrong_password_rejected(client):
    client.post("/api/v1/auth/register", json={"username": "alice", "password": "correct-horse"})
    client.post("/api/v1/auth/logout")
    response = client.post(
        "/api/v1/auth/login", json={"username": "alice", "password": "wrong-password"}
    )
    assert response.status_code == 401


def test_login_correct_password_succeeds(client):
    client.post("/api/v1/auth/register", json={"username": "alice", "password": "correct-horse"})
    client.post("/api/v1/auth/logout")
    response = client.post(
        "/api/v1/auth/login", json={"username": "alice", "password": "correct-horse"}
    )
    assert response.status_code == 200


def test_me_without_session_is_unauthorized(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_logout_clears_session(client):
    client.post("/api/v1/auth/register", json={"username": "alice", "password": "correct-horse"})
    client.post("/api/v1/auth/logout")
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_verify_password_rejects_non_bcrypt_hash_without_crashing():
    # Regression guard: a malformed password_hash (e.g. from a bad
    # provisioning script) must fail closed, not raise.
    assert verify_password("anything", "not-a-real-bcrypt-hash") is False


def test_hash_password_round_trips():
    hashed = hash_password("correct-horse")
    assert verify_password("correct-horse", hashed) is True
    assert verify_password("wrong", hashed) is False
