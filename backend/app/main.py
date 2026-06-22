"""FastAPI application entry point for R4B.AI."""

try:
    from fastapi import FastAPI
except ModuleNotFoundError:
    FastAPI = None

from .api.screening import router as screening_router
from .routes.property_analysis import router as property_analysis_router


if FastAPI:
    app = FastAPI(title="R4B.AI Investment Analyzer")

    if property_analysis_router:
        app.include_router(property_analysis_router)

    if screening_router:
        app.include_router(screening_router)
else:
    app = None
