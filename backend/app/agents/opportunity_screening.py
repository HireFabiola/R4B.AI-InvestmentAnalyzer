from app.models.property_state import PropertyState


def opportunity_screening_agent(state: PropertyState) -> PropertyState:
    """
    Screens a property using listing-level information only.

    This agent does not determine whether to buy.
    It recommends the next best action.
    """

    property_info = state.property_info

    if not property_info.address:
        state.screening.next_action = "Request More Information"
        state.screening.confidence = 0.95
        state.screening.reasoning = "Address is missing, so the property cannot be screened."
        state.screening.flags.append("Missing address")
        state.current_stage = "screening"
        return state

    if property_info.asking_price <= 0:
        state.screening.next_action = "Request More Information"
        state.screening.confidence = 0.95
        state.screening.reasoning = "Asking price is missing or invalid."
        state.screening.flags.append("Missing asking price")
        state.current_stage = "screening"
        return state

    state.screening.next_action = "Schedule Property Visit"
    state.screening.confidence = 0.70
    state.screening.reasoning = (
        "The property has enough listing-level information to justify deeper review. "
        "A physical visit is recommended before making any investment decision."
    )
    state.current_stage = "screening_complete"

    return state