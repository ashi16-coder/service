"""
Auth tests — covers:
  - Happy paths   : register + login succeed with valid data
  - Failure paths : invalid inputs return correct status codes and messages
  - Auth regression: protected behaviour, duplicate detection, token not leaked on bad login
"""

VALID_USER = {"email": "tourist@example.com", "password": "secret123", "mobile": "9876543210"}


# ── Helpers ───────────────────────────────────────────────────────────────────

def register(client, payload=None):
    return client.post("/auth/register", json=payload or VALID_USER)


def login(client, email=VALID_USER["email"], password=VALID_USER["password"]):
    return client.post("/auth/login", json={"email": email, "password": password})


# ── Register — Happy Path ─────────────────────────────────────────────────────

def test_register_success(client):
    res = register(client)
    assert res.status_code == 201
    data = res.json()
    assert data["message"] == "Registration successful."
    assert data["user"]["email"] == VALID_USER["email"]
    assert "password" not in data["user"]          # password must never be returned


def test_register_returns_id(client):
    res = register(client)
    assert res.json()["user"]["id"] is not None


# ── Register — Failure Paths ──────────────────────────────────────────────────

def test_register_invalid_email(client):
    res = register(client, {**VALID_USER, "email": "not-an-email"})
    assert res.status_code == 422
    assert "email" in res.json()["detail"].lower()


def test_register_short_password(client):
    res = register(client, {**VALID_USER, "password": "abc"})
    assert res.status_code == 422
    assert "6 characters" in res.json()["detail"]


def test_register_invalid_mobile(client):
    res = register(client, {**VALID_USER, "mobile": "12345"})
    assert res.status_code == 422
    assert "mobile" in res.json()["detail"].lower()


def test_register_duplicate_email(client):
    register(client)                               # first registration
    res = register(client)                         # duplicate
    assert res.status_code == 409
    assert "already registered" in res.json()["detail"].lower()


def test_register_duplicate_mobile(client):
    register(client)
    res = register(client, {**VALID_USER, "email": "other@example.com"})
    assert res.status_code == 409


# ── Login — Happy Path ────────────────────────────────────────────────────────

def test_login_success(client):
    register(client)
    res = login(client)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == VALID_USER["email"]


def test_login_token_is_string(client):
    register(client)
    token = login(client).json()["access_token"]
    assert isinstance(token, str) and len(token) > 20


def test_login_email_case_insensitive(client):
    register(client)
    res = login(client, email="TOURIST@EXAMPLE.COM")
    assert res.status_code == 200


# ── Login — Failure Paths ─────────────────────────────────────────────────────

def test_login_wrong_password(client):
    register(client)
    res = login(client, password="wrongpass")
    assert res.status_code == 401
    assert "invalid" in res.json()["detail"].lower()


def test_login_nonexistent_user(client):
    res = login(client, email="ghost@example.com")
    assert res.status_code == 401


def test_login_missing_fields(client):
    res = client.post("/auth/login", json={"email": VALID_USER["email"]})
    assert res.status_code == 422


# ── Authorization Regression ──────────────────────────────────────────────────

def test_wrong_password_does_not_return_token(client):
    """Failed login must never leak a token."""
    register(client)
    res = login(client, password="badpassword")
    assert "access_token" not in res.json()


def test_register_does_not_expose_hashed_password(client):
    """Hashed password must never appear in any register response field."""
    res = register(client)
    assert "$2b$" not in str(res.json())


def test_login_does_not_expose_hashed_password(client):
    """Hashed password must never appear in any login response field."""
    register(client)
    res = login(client)
    assert "$2b$" not in str(res.json())


def test_duplicate_registration_does_not_corrupt_existing_user(client):
    """After a failed duplicate register, the original user can still log in."""
    register(client)
    register(client)                               # duplicate — should fail
    res = login(client)
    assert res.status_code == 200                  # original user unaffected


def test_register_empty_body(client):
    res = client.post("/auth/register", json={})
    assert res.status_code == 422


def test_login_empty_body(client):
    res = client.post("/auth/login", json={})
    assert res.status_code == 422
