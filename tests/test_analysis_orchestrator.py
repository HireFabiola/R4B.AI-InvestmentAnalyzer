import unittest

from backend.app.models.property_state import PropertyInfo, PropertyState
from backend.app.orchestrators.analysis_orchestrator import AnalysisOrchestrator


class StubAgent:
    def __init__(self):
        self.was_called = False

    def run(self, state):
        self.was_called = True
        state.screening.screening_score = 77
        state.screening.recommendation = "Contact Listing Agent"
        state.screening.key_flags = ["Stub flag"]
        state.screening.reasoning = "Stub reasoning"
        state.current_stage = "stub_complete"
        return state


class AnalysisOrchestratorTests(unittest.TestCase):
    def test_orchestrator_calls_configured_agent_and_returns_updated_state(self):
        property_info = PropertyInfo(address="123 Main St", asking_price=225000)
        state = PropertyState(property_info=property_info)
        agent = StubAgent()

        result = AnalysisOrchestrator(agents=[agent]).run(state)

        self.assertTrue(agent.was_called)
        self.assertIs(result, state)
        self.assertEqual(result.screening.screening_score, 77)
        self.assertEqual(result.screening.recommendation, "Contact Listing Agent")
        self.assertEqual(result.screening.key_flags, ["Stub flag"])
        self.assertEqual(result.current_stage, "stub_complete")

    def test_default_orchestrator_runs_opportunity_screening_first(self):
        property_info = PropertyInfo(
            address="123 Main St",
            asking_price=225000,
            description="Cosmetic updates with good bones.",
            bedrooms=3,
            bathrooms=2,
            square_feet=1500,
            year_built=1995,
            photos=[f"photo-{index}.jpg" for index in range(8)],
        )

        result = AnalysisOrchestrator().run(PropertyState(property_info=property_info))

        self.assertEqual(result.current_stage, "screening_complete")
        self.assertIsNotNone(result.screening.screening_score)
        self.assertEqual(result.screening.screening_score, result.screening.opportunity_score)
        self.assertEqual(result.screening.recommendation, result.screening.next_action)


if __name__ == "__main__":
    unittest.main()
