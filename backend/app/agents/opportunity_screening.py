from ..models.property_state import PropertyState


MAJOR_CONCERN_KEYWORDS = {
    "foundation": "Possible foundation concern",
    "structural": "Possible structural concern",
    "sloping floor": "Possible structural concern",
    "mold": "Possible environmental concern",
    "fire damage": "Possible major repair concern",
    "water damage": "Possible water intrusion concern",
    "roof leak": "Possible roof concern",
    "gut renovation": "Possible full gut renovation",
    "full gut": "Possible full gut renovation",
}

OPPORTUNITY_KEYWORDS = {
    "cosmetic": "Cosmetic improvement opportunity",
    "tlc": "Needs TLC, potential value-add opportunity",
    "good bones": "Potential good-bones opportunity",
    "hardwood": "Potential character feature",
    "large windows": "Natural light / window appeal",
    "natural light": "Natural light appeal",
    "character": "Architectural character",
    "spacious": "Spaciousness signal",
    "curb appeal": "Curb appeal potential",
    "updated": "Some updates already present",
}


class OpportunityScreeningAgent:
    """Evaluates listing-level opportunity before deeper analysis."""

    def run(self, state: PropertyState) -> PropertyState:
        return opportunity_screening_agent(state)


def opportunity_screening_agent(state: PropertyState) -> PropertyState:
    """
    Screens a property using listing-level information only.

    This agent does not determine whether to buy.
    It recommends the next best action for deeper investigation.
    """

    property_info = state.property_info
    screening = state.screening

    screening.flags = []
    screening.positive_signals = []
    screening.missing_information = []
    screening.metrics = {}

    if not property_info.address:
        return _request_more_information(
            state,
            "Address is missing, so the property cannot be screened.",
            "Missing address",
            information_completeness=0.95,
        )

    if property_info.asking_price <= 0:
        return _request_more_information(
            state,
            "Asking price is missing or invalid.",
            "Missing asking price",
            information_completeness=0.95,
        )

    opportunity_score = 50

    opportunity_score += _evaluate_core_facts(state)
    opportunity_score += _evaluate_price_per_square_foot(state)
    opportunity_score += _evaluate_listing_quality(state)
    opportunity_score += _evaluate_description_signals(state)

    opportunity_score = max(0, min(100, opportunity_score))
    screening.opportunity_score = opportunity_score
    screening.information_completeness = _calculate_information_completeness(state)
    screening.next_action = _choose_next_action(state)
    screening.reasoning = _build_reasoning(state)
    _sync_screening_aliases(state)

    state.current_stage = "screening_complete"
    return state


def _request_more_information(
    state: PropertyState,
    reasoning: str,
    flag: str,
    information_completeness: float,
) -> PropertyState:
    state.screening.next_action = "Request More Information"
    state.screening.reasoning = reasoning
    state.screening.flags = [flag]
    state.screening.opportunity_score = 0
    state.screening.information_completeness = information_completeness
    _sync_screening_aliases(state)
    state.current_stage = "screening"
    return state


def _sync_screening_aliases(state: PropertyState) -> None:
    screening = state.screening
    screening.screening_score = screening.opportunity_score
    screening.recommendation = screening.next_action
    screening.key_flags = list(screening.flags)


def _evaluate_core_facts(state: PropertyState) -> int:
    property_info = state.property_info
    screening = state.screening
    score_delta = 0

    if property_info.bedrooms is None:
        screening.missing_information.append("Bedroom count")
        score_delta -= 4
    elif property_info.bedrooms <= 0:
        screening.flags.append("Invalid bedroom count")
        score_delta -= 12
    elif property_info.bedrooms >= 3:
        screening.positive_signals.append("Three or more bedrooms")
        score_delta += 5

    if property_info.bathrooms is None:
        screening.missing_information.append("Bathroom count")
        score_delta -= 4
    elif property_info.bathrooms <= 0:
        screening.flags.append("Invalid bathroom count")
        score_delta -= 12
    elif property_info.bathrooms >= 2:
        screening.positive_signals.append("Two or more bathrooms")
        score_delta += 5
    elif property_info.bathrooms == 1:
        screening.flags.append("Only one bathroom")
        score_delta -= 4

    if property_info.square_feet is None:
        screening.missing_information.append("Square footage")
        score_delta -= 8
    elif property_info.square_feet <= 0:
        screening.flags.append("Invalid square footage")
        score_delta -= 18
    elif property_info.square_feet < 700:
        screening.flags.append("Property is too small for current target market")
        score_delta -= 10
    # Square footage thresholds reflect Fabiola's current investment philosophy,
    # not universal real estate rules.
    elif property_info.square_feet < 1000:
        pass
    elif property_info.square_feet <= 1700:
        screening.positive_signals.append("Ideal property size for current strategy")
        score_delta += 8
    elif property_info.square_feet <= 2000:
        screening.positive_signals.append("Slightly above ideal size, but still favorable")
        score_delta += 4
    elif property_info.square_feet <= 2500:
        pass
    elif property_info.square_feet <= 3500:
        screening.flags.append("Larger property may increase renovation and holding costs")
        score_delta -= 6
    elif property_info.square_feet > 3500:
        screening.flags.append("Property size is outside current investment strategy")
        score_delta -= 10

    if property_info.year_built is None:
        screening.missing_information.append("Year built")
        score_delta -= 2
    # Year-built thresholds reflect R4B.AI's preference for system predictability
    # and due diligence, not a belief that older homes are automatically bad.
    elif property_info.year_built < 1950:
        screening.flags.append(
            "Verify roof, HVAC, plumbing, and electrical due to property age"
        )
        score_delta -= 6
    elif property_info.year_built <= 1979:
        screening.flags.append(
            "Verify major systems due to mid-century property age"
        )
        score_delta -= 4
    elif property_info.year_built <= 1989:
        screening.flags.append(
            "Confirm major systems have been maintained or updated"
        )
        score_delta -= 1

    return score_delta


def _evaluate_price_per_square_foot(state: PropertyState) -> int:
    property_info = state.property_info
    screening = state.screening

    if not property_info.square_feet or property_info.square_feet <= 0:
        return 0

    price_per_square_foot = property_info.asking_price / property_info.square_feet
    screening.metrics["price_per_square_foot"] = round(price_per_square_foot, 2)

    if price_per_square_foot < 100:
        screening.positive_signals.append("Low preliminary price per square foot")
        return 10

    if price_per_square_foot <= 200:
        screening.positive_signals.append("Moderate preliminary price per square foot")
        return 4

    if price_per_square_foot > 275:
        screening.flags.append("High preliminary price per square foot")
        return -10

    screening.flags.append("Elevated preliminary price per square foot")
    return -4


def _evaluate_listing_quality(state: PropertyState) -> int:
    property_info = state.property_info
    screening = state.screening
    score_delta = 0

    if property_info.listing_url:
        screening.positive_signals.append("Listing URL available")
        score_delta += 2
    else:
        screening.missing_information.append("Listing URL")
        score_delta -= 2

    if property_info.photos:
        photo_count = len(property_info.photos)
        screening.metrics["photo_count"] = photo_count

        if photo_count >= 8:
            screening.positive_signals.append("Enough photos for preliminary review")
            score_delta += 6
        elif photo_count >= 3:
            screening.flags.append("Limited photos")
            score_delta -= 2
        else:
            screening.flags.append("Very limited photos")
            score_delta -= 6
    else:
        screening.missing_information.append("Listing photos")
        score_delta -= 8

    if property_info.description:
        screening.positive_signals.append("Listing description available")
        score_delta += 2
    else:
        screening.missing_information.append("Listing description")
        score_delta -= 4

    return score_delta


def _evaluate_description_signals(state: PropertyState) -> int:
    description = state.property_info.description
    screening = state.screening

    if not description:
        return 0

    score_delta = 0
    description_text = description.lower()

    for keyword, flag in MAJOR_CONCERN_KEYWORDS.items():
        if keyword in description_text and flag not in screening.flags:
            screening.flags.append(flag)
            score_delta -= 14

    for keyword, signal in OPPORTUNITY_KEYWORDS.items():
        if keyword in description_text and signal not in screening.positive_signals:
            screening.positive_signals.append(signal)
            score_delta += 4

    if "cash only" in description_text:
        # Cash-only is an investigation trigger, not a direct score penalty.
        screening.flags.append("Cash-only listing: verify why financing is restricted")

    if "as-is" in description_text or "as is" in description_text:
        screening.flags.append("As-is listing requires careful inspection")
        score_delta -= 4

    return score_delta


def _calculate_information_completeness(state: PropertyState) -> float:
    available_data_points = 2
    expected_data_points = 8
    property_info = state.property_info

    optional_values = [
        property_info.bedrooms,
        property_info.bathrooms,
        property_info.square_feet,
        property_info.year_built,
        property_info.listing_url,
        property_info.description,
    ]

    available_data_points += sum(
        value is not None and value != "" for value in optional_values
    )

    if property_info.photos:
        available_data_points += 1

    information_completeness = available_data_points / expected_data_points

    if state.screening.flags:
        information_completeness = min(information_completeness + 0.05, 0.95)

    return round(information_completeness, 2)


def _choose_next_action(state: PropertyState) -> str:
    screening = state.screening
    major_concerns = [
        flag
        for flag in screening.flags
        if "foundation" in flag.lower()
        or "structural" in flag.lower()
        or "full gut" in flag.lower()
        or "mold" in flag.lower()
        or "fire damage" in flag.lower()
    ]

    if major_concerns and (screening.opportunity_score or 0) < 45:
        return "Pass"

    if (
        len(screening.missing_information) >= 3
        or (screening.information_completeness or 0) < 0.65
    ):
        return "Request More Information"

    if screening.opportunity_score is not None and screening.opportunity_score >= 70:
        return "Schedule Property Visit"

    if screening.opportunity_score is not None and screening.opportunity_score >= 55:
        return "Contact Listing Agent"

    return "Request More Information"


def _build_reasoning(state: PropertyState) -> str:
    screening = state.screening
    opportunity_score = (
        screening.opportunity_score if screening.opportunity_score is not None else 0
    )
    information_completeness = screening.information_completeness or 0

    summary = (
        f"Listing-level opportunity score is {opportunity_score}/100 with "
        f"{information_completeness:.0%} information completeness."
    )

    if screening.next_action == "Pass":
        return (
            f"{summary} The listing contains major concern language that conflicts with the "
            "investor's preference for structurally predictable opportunities."
        )

    if screening.next_action == "Schedule Property Visit":
        return (
            f"{summary} The property has enough listing detail and positive early signals to "
            "justify an in-person visit before deeper market, rehab, and financial analysis."
        )

    if screening.next_action == "Contact Listing Agent":
        return (
            f"{summary} The opportunity may be worth exploring, but the next best step is to "
            "contact the listing agent to clarify condition, pricing support, and missing facts."
        )

    return (
        f"{summary} The listing is not ready for deeper analysis because important screening "
        "details are missing or preliminary risk is too high."
    )
