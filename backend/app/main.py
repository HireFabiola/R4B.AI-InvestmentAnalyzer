"""FastAPI application entry point for R4B.AI."""

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
except ModuleNotFoundError:
    FastAPI = None
    CORSMiddleware = None

from .api.screening import router as screening_router
from .routes.property_analysis import router as property_analysis_router


if FastAPI:
    app = FastAPI(title="R4B.AI Investment Analyzer")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if property_analysis_router:
        app.include_router(property_analysis_router)

    if screening_router:
        app.include_router(screening_router)
else:
    app = None