from ..agents.opportunity_screening import opportunity_screening_agent
from ..models.property_state import PropertyState

try:
    from fastapi import APIRouter
except ModuleNotFoundError:
    APIRouter = None


if APIRouter:
    router = APIRouter()

    @router.post("/screening")
    def screen_property(state: PropertyState) -> PropertyState:
        return opportunity_screening_agent(state)
else:
    router = None
