from ..agents.opportunity_screening import OpportunityScreeningAgent
from ..models.property_state import PropertyState


class AnalysisOrchestrator:
    """Runs property analysis agents in the configured sequence."""

    def __init__(self, agents: list | None = None):
        self.agents = agents or [OpportunityScreeningAgent()]

    def run(self, state: PropertyState) -> PropertyState:
        for agent in self.agents:
            state = agent.run(state)

        return state
