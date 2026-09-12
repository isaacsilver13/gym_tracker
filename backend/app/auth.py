import bcrypt
from fastapi import Cookie, Depends, HTTPException, Response, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy.orm import Session

from app.config import load_settings
from app.db import get_db
from app.models import User

SESSION_COOKIE_NAME = "gym_session"
SESSION_MAX_AGE_SECONDS = 60 * 60 * 24 * 30  # 30 days

_settings = load_settings()
_serializer = URLSafeTimedSerializer(_settings.session_secret, salt="gym-tracker-session")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except ValueError:
        # A malformed/non-bcrypt password_hash must never crash the login path.
        return False


def issue_session_cookie(response: Response, user_id: int) -> None:
    token = _serializer.dumps({"user_id": user_id})
    response.set_cookie(
        SESSION_COOKIE_NAME,
        token,
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
        secure=_settings.app_env != "development",
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE_NAME)


def get_current_user(
    gym_session: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if not gym_session:
        raise unauthorized
    try:
        data = _serializer.loads(gym_session, max_age=SESSION_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        raise unauthorized from None
    user = db.get(User, data.get("user_id"))
    if user is None:
        raise unauthorized
    return user
