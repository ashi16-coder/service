import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes import live_data, weather, safety, language, food, booking, auth
from database import init_db, engine
from logger import get_logger

log = get_logger("main")

# ── Debug mode must be OFF in production ─────────────────────────────────────
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Tourism Support API",
    description="One-stop backend for travel info, weather, safety, language, food, and booking.",
    version="1.0.0",
    lifespan=lifespan,
    debug=False,          # ← debug mode explicitly disabled
    docs_url="/docs" if DEBUG else None,   # hide docs in production
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all: log unexpected failures, never expose internals to client."""
    log.error("Unhandled exception on %s %s: %s", request.method, request.url, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


app.include_router(auth.router)
app.include_router(live_data.router)
app.include_router(weather.router)
app.include_router(safety.router)
app.include_router(language.router)
app.include_router(food.router)
app.include_router(booking.router)


# ── Health endpoint — checks all dependencies ─────────────────────────────────
@app.get("/health", tags=["Health"])
def health():
    checks = {}

    # 1. Database connectivity
    try:
        with engine.connect() as conn:
            conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:
        log.error("Health check — DB failed: %s", exc)
        checks["database"] = "unreachable"

    # 2. Required environment variables
    missing_env = [v for v in ("DATABASE_URL", "SECRET_KEY") if not os.getenv(v)]
    checks["env_vars"] = "ok" if not missing_env else f"missing: {missing_env}"

    # 3. Optional API keys (warn but don't fail)
    checks["openweather_api"] = "configured" if os.getenv("OPENWEATHER_API_KEY") else "not set (mock mode)"
    checks["translate_api"]   = "configured" if os.getenv("GOOGLE_TRANSLATE_API_KEY") else "not set (mock mode)"

    overall = "healthy" if all(v == "ok" or "configured" in str(v) or "mock" in str(v)
                               for v in checks.values()) else "degraded"

    status_code = 200 if checks["database"] == "ok" else 503
    return JSONResponse(status_code=status_code, content={"status": overall, "checks": checks})


@app.get("/", tags=["Health"])
def root():
    return {"app": "Tourism Support API", "status": "running", "health": "/health"}
