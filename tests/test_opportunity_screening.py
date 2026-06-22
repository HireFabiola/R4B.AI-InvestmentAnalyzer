import unittest

from backend.app.agents.opportunity_screening import opportunity_screening_agent
from backend.app.models.property_state import PropertyInfo, PropertyState


class OpportunityScreeningAgentTests(unittest.TestCase):
    def test_complete_listing_with_value_add_signals_recommends_visit(self):
        property_info = PropertyInfo(
            address="123 Main St",
            asking_price=225000,
            listing_url="https://example.com/listing/123-main",
            description=(
                "Charming home with good bones, hardwood floors, large windows, "
                "natural light, and mostly cosmetic updates needed."
            ),
            bedrooms=3,
            bathrooms=2,
            square_feet=1500,
            year_built=1985,
            photos=[f"photo-{index}.jpg" for index in range(10)],
        )
        state = PropertyState(property_info=property_info)

        result = opportunity_screening_agent(state)

        self.assertEqual(result.screening.next_action, "Schedule Property Visit")
        self.assertEqual(result.screening.recommendation, "Schedule Property Visit")
        self.assertEqual(result.current_stage, "screening_complete")
        self.assertGreaterEqual(result.screening.opportunity_score, 70)
        self.assertEqual(
            result.screening.screening_score,
            result.screening.opportunity_score,
        )
        self.assertGreaterEqual(result.screening.information_completeness, 0.9)
        self.assertIn(
            "Ideal property size for current strategy",
            result.screening.positive_signals,
        )
        self.assertIn("price_per_square_foot", result.screening.metrics)

    def test_square_footage_scoring_reflects_current_investment_strategy(self):
        scenarios = [
            (650, -10, [], ["Property is too small for current target market"]),
            (850, 0, [], []),
            (1500, 8, ["Ideal property size for current strategy"], []),
            (
                1850,
                4,
                ["Slightly above ideal size, but still favorable"],
                [],
            ),
            (2250, 0, [], []),
            (
                3000,
                -6,
                [],
                ["Larger property may increase renovation and holding costs"],
            ),
            (
                3600,
                -10,
                [],
                ["Property size is outside current investment strategy"],
            ),
        ]

        for square_feet, expected_delta, expected_signals, expected_flags in scenarios:
            with self.subTest(square_feet=square_feet):
                property_info = PropertyInfo(
                    address="123 Main St",
                    asking_price=square_feet * 150,
                    listing_url="https://example.com/listing/123-main",
                    description="Clean listing with updated cosmetic finishes.",
                    bedrooms=3,
                    bathrooms=2,
                    square_feet=square_feet,
                    year_built=1985,
                    photos=[f"photo-{index}.jpg" for index in range(10)],
                )
                state = PropertyState(property_info=property_info)

                result = opportunity_screening_agent(state)

                baseline_without_square_footage = 81
                self.assertEqual(
                    result.screening.opportunity_score,
                    baseline_without_square_footage + expected_delta,
                )

                for signal in expected_signals:
                    self.assertIn(signal, result.screening.positive_signals)

                for flag in expected_flags:
                    self.assertIn(flag, result.screening.flags)

    def test_year_built_scoring_reflects_system_predictability_strategy(self):
        scenarios = [
            (None, -2, "Year built", None),
            (
                1945,
                -6,
                None,
                "Verify roof, HVAC, plumbing, and electrical due to property age",
            ),
            (
                1965,
                -4,
                None,
                "Verify major systems due to mid-century property age",
            ),
            (
                1985,
                -1,
                None,
                "Confirm major systems have been maintained or updated",
            ),
            (1995, 0, None, None),
        ]

        for year_built, expected_delta, missing_info, expected_flag in scenarios:
            with self.subTest(year_built=year_built):
                property_info = PropertyInfo(
                    address="123 Main St",
                    asking_price=225000,
                    listing_url="https://example.com/listing/123-main",
                    description="Clean listing with updated cosmetic finishes.",
                    bedrooms=3,
                    bathrooms=2,
                    square_feet=1500,
                    year_built=year_built,
                    photos=[f"photo-{index}.jpg" for index in range(10)],
                )
                state = PropertyState(property_info=property_info)

                result = opportunity_screening_agent(state)

                baseline_without_year_built = 90
                self.assertEqual(
                    result.screening.opportunity_score,
                    baseline_without_year_built + expected_delta,
                )

                if missing_info:
                    self.assertIn(missing_info, result.screening.missing_information)

                if expected_flag:
                    self.assertIn(expected_flag, result.screening.flags)

    def test_cash_only_listing_flags_investigation_without_score_penalty(self):
        base_property = PropertyInfo(
            address="123 Main St",
            asking_price=225000,
            listing_url="https://example.com/listing/123-main",
            description="Clean listing with updated cosmetic finishes.",
            bedrooms=3,
            bathrooms=2,
            square_feet=1500,
            year_built=1995,
            photos=[f"photo-{index}.jpg" for index in range(10)],
        )
        cash_only_property = PropertyInfo(
            address="123 Main St",
            asking_price=225000,
            listing_url="https://example.com/listing/123-main",
            description="Clean listing with updated cosmetic finishes. Cash only.",
            bedrooms=3,
            bathrooms=2,
            square_feet=1500,
            year_built=1995,
            photos=[f"photo-{index}.jpg" for index in range(10)],
        )

        base_result = opportunity_screening_agent(
            PropertyState(property_info=base_property)
        )
        cash_only_result = opportunity_screening_agent(
            PropertyState(property_info=cash_only_property)
        )

        self.assertEqual(
            cash_only_result.screening.opportunity_score,
            base_result.screening.opportunity_score,
        )
        self.assertIn(
            "Cash-only listing: verify why financing is restricted",
            cash_only_result.screening.flags,
        )

    def test_missing_address_requests_more_information(self):
        property_info = PropertyInfo(
            address="",
            asking_price=225000,
            bedrooms=3,
            bathrooms=2,
            square_feet=1500,
        )
        state = PropertyState(property_info=property_info)

        result = opportunity_screening_agent(state)

        self.assertEqual(result.screening.next_action, "Request More Information")
        self.assertEqual(result.screening.opportunity_score, 0)
        self.assertEqual(result.screening.screening_score, 0)
        self.assertEqual(result.screening.flags, ["Missing address"])
        self.assertEqual(result.screening.key_flags, ["Missing address"])
        self.assertEqual(result.current_stage, "screening")

    def test_sparse_listing_requests_more_information(self):
        property_info = PropertyInfo(
            address="456 Oak Ave",
            asking_price=180000,
        )
        state = PropertyState(property_info=property_info)

        result = opportunity_screening_agent(state)

        self.assertEqual(result.screening.next_action, "Request More Information")
        self.assertLess(result.screening.information_completeness, 0.65)
        self.assertIn("Square footage", result.screening.missing_information)
        self.assertIn("Listing photos", result.screening.missing_information)

    def test_major_structural_concern_can_recommend_pass(self):
        property_info = PropertyInfo(
            address="789 Pine Rd",
            asking_price=310000,
            listing_url="https://example.com/listing/789-pine",
            description=(
                "Investor special sold as-is. Full gut renovation needed with "
                "possible foundation and structural issues."
            ),
            bedrooms=2,
            bathrooms=1,
            square_feet=1000,
            year_built=1920,
            photos=["front.jpg", "kitchen.jpg", "bath.jpg"],
        )
        state = PropertyState(property_info=property_info)

        result = opportunity_screening_agent(state)

        self.assertEqual(result.screening.next_action, "Pass")
        self.assertLess(result.screening.opportunity_score, 45)
        self.assertTrue(
            any("foundation" in flag.lower() for flag in result.screening.flags)
        )
        self.assertTrue(
            any("structural" in flag.lower() for flag in result.screening.flags)
        )


if __name__ == "__main__":
    unittest.main()
