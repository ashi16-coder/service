import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ── Isolated in-memory database (never touches PostgreSQL) ───────────────────
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def isolated_db():
    """
    Each test gets a fresh schema — tables created before, dropped after.
    This guarantees tests never share state.
    """
    from database import Base
    import db_models  # noqa: F401 — registers all models with Base
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(isolated_db):
    """TestClient with get_db overridden to use the isolated SQLite DB."""
    from main import app
    from database import get_db

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
