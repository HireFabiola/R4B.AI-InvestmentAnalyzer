import { useState } from "react";
import axios from "axios";
import "./App.css";

type ScreeningResult = {
  next_action: string | null;
  recommendation: string | null;
  reasoning: string | null;
  flags: string[];
  key_flags: string[];
  positive_signals: string[];
  missing_information: string[];
  opportunity_score: number | null;
  screening_score: number | null;
  information_completeness: number | null;
  metrics: Record<string, number>;
};

type PropertyState = {
  screening: ScreeningResult;
  current_stage: string;
  workflow_status: string;
};

function App() {
  const [result, setResult] = useState<PropertyState | null>(null);
  const [loading, setLoading] = useState(false);

  const runScreening = async () => {
    setLoading(true);

    try {
      const response = await axios.post<PropertyState>(
        "http://localhost:8000/screening",
        {
          property_info: {
            address: "123 Test Street, Atlanta, GA",
            asking_price: 250000,
            description:
              "Cash only property with great curb appeal, updated interior, 3 bedrooms, and strong rental potential.",
            bedrooms: 3,
            bathrooms: 2,
            square_feet: 1400,
            year_built: 1998,
            photos: [
              "front exterior",
              "kitchen",
              "living room",
              "bedroom",
              "bathroom",
            ],
          },
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error("Screening failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const screening = result?.screening;

  return (
    <main className="app">
      <h1>R4B.AI Investment Analyzer</h1>
      <p>Opportunity Screening Agent</p>

      <button onClick={runScreening} disabled={loading}>
        {loading ? "Screening..." : "Run Screening"}
      </button>

      {screening && (
        <section className="results">
          <h2>Screening Result</h2>

          <p>
            <strong>Score:</strong>{" "}
            {screening.opportunity_score ?? screening.screening_score ?? "N/A"}
          </p>

          <p>
            <strong>Next Action:</strong> {screening.next_action ?? "N/A"}
          </p>

          <p>
            <strong>Recommendation:</strong>{" "}
            {screening.recommendation ?? "N/A"}
          </p>

          <p>
            <strong>Reasoning:</strong> {screening.reasoning ?? "N/A"}
          </p>

          <h3>Positive Signals</h3>
          <ul>
            {screening.positive_signals.map((signal) => (
              <li key={signal}>{signal}</li>
            ))}
          </ul>

          <h3>Flags</h3>
          <ul>
            {screening.flags.map((flag) => (
              <li key={flag}>{flag}</li>
            ))}
          </ul>

          <h3>Missing Information</h3>
          <ul>
            {screening.missing_information.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}

export default App;