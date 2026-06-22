# R4B.AI

## Agentic Real Estate Investment Analysis Platform

R4B.AI is an agentic AI platform designed to help real estate investors evaluate acquisition opportunities through a structured, multi-agent workflow.

Rather than relying on a single AI conversation, the platform breaks the investment analysis process into specialized agents responsible for opportunity screening, market intelligence, rehabilitation assessment, financial analysis, and investment strategy. Property information is collected through a structured workflow before being analyzed by specialized agents that contribute to a shared understanding of the opportunity.

Each AI agent owns a single investment decision while contributing information to a shared workflow state.

The long-term vision is to support multiple investment strategies—including fix-and-flip, buy-and-hold, BRRRR, wholesale, and value-add acquisitions—while providing investors with transparent, explainable, and data-driven recommendations.

The initial MVP focuses on establishing an explainable multi-agent architecture capable of evaluating real estate investment opportunities through deterministic financial analysis and AI-driven reasoning. While the first financial models will support fix-and-flip analysis, the architecture is intentionally designed to accommodate additional investment strategies as the platform evolves.

## Tech Stack

* React
* TypeScript
* Python
* FastAPI
* LangGraph
* Deterministic financial calculation services

## MVP Overview

The MVP establishes the foundation for an agentic real estate investment analysis platform. It demonstrates how a multi-agent workflow can evaluate a real estate acquisition opportunity by combining deterministic financial calculations with AI-driven reasoning.

The initial release will:

* Screen opportunities using listing-level information.
* Collect and organize property data through a structured workflow.
* Analyze market context and comparable properties.
* Evaluate property condition and rehabilitation risk.
* Perform deterministic financial analysis using Python services.
* Recommend the investment strategy best suited to the opportunity while providing transparent reasoning.

The primary objective of the MVP is not to build every investment model immediately, but to establish a scalable, explainable, and extensible agentic AI architecture that can grow alongside the business.

## Agent Workflow Summary

R4B.AI uses a five-agent workflow supported by one structured data collection step:

1. **Opportunity Screening Agent** evaluates whether a property deserves deeper investigation and recommends the next best action.
2. **Property Intake** collects, validates, and organizes property information into the shared workflow state.
3. **Market Intelligence Agent** analyzes neighborhood trends, comparable properties, and valuation context.
4. **Rehab & Condition Agent** evaluates visible property condition and renovation risk.
5. **Financial Analysis Agent** performs deterministic financial calculations and evaluates investment viability.
6. **Investment Strategy Agent** recommends the investment strategy best suited to the opportunity while explaining its reasoning.

LangGraph will orchestrate the workflow so each step has a defined responsibility and predictable handoff.

## Backend Setup

From the project root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Tests can be run from the project root:

```bash
python3 -m unittest discover -s tests
```

## Documentation

* [Architecture](docs/architecture.md)
* [Architecture Decisions](docs/architecture-decisions.md)
* [Agent Design](docs/agent-design.md)
* [Workflow](docs/workflow.md)
* [Investment Philosophy](docs/investment-philosophy.md)
* [Fabiola's Investment Playbook](docs/fabiola-investment-playbook.md)
* [Learning Journal](docs/learning-journal.md)
