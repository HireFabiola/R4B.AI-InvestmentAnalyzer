import unittest

from backend.app.controllers.property_analysis_controller import _build_property_state
from backend.app.models.property_state import PropertyInfo, PropertyState


class PropertyStateTests(unittest.TestCase):
    def test_property_state_creation(self):
        property_info = PropertyInfo(
            address="123 Main St",
            asking_price=225000,
            bedrooms=3,
            bathrooms=2,
            square_feet=1500,
        )

        state = PropertyState(property_info=property_info)

        self.assertEqual(state.property_info.address, "123 Main St")
        self.assertEqual(state.current_stage, "created")
        self.assertEqual(state.workflow_status, "in_progress")
        self.assertEqual(state.screening.flags, [])

    def test_controller_builds_property_state_from_request_data(self):
        state = _build_property_state(
            {
                "property_info": {
                    "address": "456 Oak Ave",
                    "asking_price": 180000,
                    "bedrooms": 3,
                }
            }
        )

        self.assertEqual(state.property_info.address, "456 Oak Ave")
        self.assertEqual(state.property_info.asking_price, 180000)


if __name__ == "__main__":
    unittest.main()
