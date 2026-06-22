"""FastAPI application entry point for R4B.AI."""

try:
    from fastapi import FastAPI
except ModuleNotFoundError:
    FastAPI = None

from backend.app.routes.property_analysis import router as property_analysis_router


if FastAPI:
    app = FastAPI(title="R4B.AI Investment Analyzer")

    if property_analysis_router:
        app.include_router(property_analysis_router)
else:
    app = None
