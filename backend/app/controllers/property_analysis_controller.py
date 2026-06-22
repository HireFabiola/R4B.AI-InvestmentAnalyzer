from dataclasses import asdict

from ..models.property_state import PropertyInfo, PropertyState
from ..orchestrators.analysis_orchestrator import AnalysisOrchestrator


def analyze_property(request_data: dict) -> dict:
    property_state = _build_property_state(request_data)
    updated_state = AnalysisOrchestrator().run(property_state)

    return asdict(updated_state)


def _build_property_state(request_data: dict) -> PropertyState:
    if not isinstance(request_data, dict):
        raise ValueError("Request data must be a JSON object.")

    property_data = request_data.get("property_info", request_data)

    if not isinstance(property_data, dict):
        raise ValueError("Property information must be a JSON object.")

    try:
        property_info = PropertyInfo(**property_data)
    except TypeError as error:
        raise ValueError(f"Invalid property information: {error}") from error

    return PropertyState(property_info=property_info)
