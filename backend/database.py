import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()
log = get_logger("database")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/tourism_db"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency — yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()   # ← failed writes do not leave partial data
        raise
    finally:
        db.close()


def init_db():
    """Create all tables. Logs success or failure."""
    try:
        from db_models import User  # noqa: F401
        Base.metadata.create_all(bind=engine)
        log.info("Database tables created / verified OK.")
    except Exception as exc:
        log.error("Failed to initialise database: %s", exc)
        raise
