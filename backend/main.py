from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes import live_data, weather, safety, language, food, booking, auth
from database import init_db
from logger import get_logger

log = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Tourism Support API",
    description="One-stop backend for travel info, weather, safety, language, food, and booking.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all: log unexpected failures, return generic message to client."""
    log.error("Unhandled exception on %s %s: %s", request.method, request.url, exc, exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred. Please try again later."})


app.include_router(auth.router)
app.include_router(live_data.router)
app.include_router(weather.router)
app.include_router(safety.router)
app.include_router(language.router)
app.include_router(food.router)
app.include_router(booking.router)


@app.get("/", tags=["Health"])
def root():
    return {"app": "Tourism Support API", "status": "running", "docs": "/docs"}
