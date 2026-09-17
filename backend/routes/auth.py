from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
import os

from database import get_db
from db_models import User
from logger import get_logger

log = get_logger("auth")
router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_in_production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24


class RegisterRequest(BaseModel):
    email: str
    password: str
    mobile: str


class LoginRequest(BaseModel):
    email: str
    password: str


def _create_token(data: dict) -> str:
    payload = {**data, "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # ── client validation (actionable errors) ────────────────────────────────
    if not req.email or "@" not in req.email:
        raise HTTPException(status_code=422, detail="Enter a valid email address.")
    if len(req.password) < 6:
        raise HTTPException(status_code=422, detail="Password must be at least 6 characters.")
    if not req.mobile.strip().isdigit() or len(req.mobile.strip()) != 10:
        raise HTTPException(status_code=422, detail="Enter a valid 10-digit mobile number.")

    user = User(
        email=req.email.lower().strip(),
        password=pwd_context.hash(req.password),
        mobile=req.mobile.strip(),
    )
    try:
        db.add(user)
        db.commit()          # ← atomic: rolls back automatically on failure via get_db
        db.refresh(user)
        log.info("New user registered: %s", user.email)
    except IntegrityError:
        # get_db already rolled back; give actionable message to client
        log.warning("Registration conflict for email=%s mobile=%s", req.email, req.mobile)
        raise HTTPException(status_code=409, detail="Email or mobile number is already registered.")
    except Exception as exc:
        # unexpected failure — log full detail, return generic message to client
        log.error("Unexpected error during register: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Registration failed. Please try again later.")

    return {"message": "Registration successful.", "user": {"id": user.id, "email": user.email, "mobile": user.mobile}}


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == req.email.lower().strip()).first()
    except Exception as exc:
        log.error("DB error during login lookup: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Login failed. Please try again later.")

    # single actionable message — do not reveal which field is wrong
    if not user or not pwd_context.verify(req.password, user.password):
        log.warning("Failed login attempt for email=%s", req.email)
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = _create_token({"sub": str(user.id), "email": user.email})
    log.info("User logged in: %s", user.email)
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "mobile": user.mobile}}
