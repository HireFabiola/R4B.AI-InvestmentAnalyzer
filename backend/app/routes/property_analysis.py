from backend.app.controllers.property_analysis_controller import analyze_property

try:
    from fastapi import APIRouter, HTTPException
except ModuleNotFoundError:
    APIRouter = None
    HTTPException = None


if APIRouter:
    router = APIRouter()

    @router.post("/analyze-property")
    def analyze_property_route(request_data: dict) -> dict:
        try:
            return analyze_property(request_data)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
else:
    router = None
