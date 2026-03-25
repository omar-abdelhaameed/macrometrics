from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import os
import logging

load_dotenv()

from database import engine, Base
from routes import ingredients, meals, daily, users, auth, analytics, chat, supplements
from rate_limiter import limiter

logger = logging.getLogger("macrometrics")


# ==================== STARTUP: Auto-create tables ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run on startup — creates all DB tables if they don't exist."""
    try:
        import models  # noqa: F401 — ensures all models are registered
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables verified / created successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
    yield
    # (shutdown logic here if needed)


# ==================== APP ====================

app = FastAPI(
    title="MacroMetrics API",
    description="High-performance REST API for fitness & macro tracking",
    version="2.0.0",
    lifespan=lifespan,
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_preflights(request: Request, call_next):
    if request.method == "OPTIONS":
        logger.info(
            f"PREFLIGHT: {request.url} | "
            f"Origin: {request.headers.get('origin')} | "
            f"Headers: {request.headers.get('access-control-request-headers')}"
        )
    return await call_next(request)


# ==================== Global Exception Handlers ====================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"loc": e["loc"], "msg": e["msg"]} for e in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "detail": errors},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": "An unexpected error occurred"},
    )


# ==================== Routers ====================

app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(meals.router)
app.include_router(daily.router)
app.include_router(users.router)
app.include_router(analytics.router)
app.include_router(chat.router)
app.include_router(supplements.router)


# ==================== Base Routes ====================

@app.get("/")
def root():
    return {
        "app": "MacroMetrics API",
        "version": "2.0.0",
        "status": "operational",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": str(engine.url.render_as_string(hide_password=True)),
    }
