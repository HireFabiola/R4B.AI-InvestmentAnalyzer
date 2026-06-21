# Architecture Decision Records (ADRs)

This document records the key architectural decisions made during the design of R4B.AI. Each Architecture Decision Record (ADR) explains what was decided, why the decision was made, and how it influences the overall system.

---

# ADR-001: Decision-Support Workflow Instead of a Generic Chatbot

**Status:** Accepted

## Decision

R4B.AI will function as an agentic decision-support system rather than a general-purpose conversational chatbot.

## Reason

Experienced real estate investors follow a structured decision-making process when evaluating acquisition opportunities. Modeling that process produces more transparent, explainable, and repeatable results than relying on a single open-ended AI conversation.

## Consequences

* The application follows a structured workflow.
* AI recommendations are explainable.
* Human decision-making remains central to the investment process.

---

# ADR-002: Python + FastAPI Backend

**Status:** Accepted

## Decision

The backend will use Python with FastAPI.

## Reason

Python provides excellent support for AI frameworks, data processing, and deterministic financial calculations. FastAPI offers strong typing, excellent documentation, and lightweight API development.

## Consequences

* Backend services will be implemented in Python.
* Financial calculations and AI orchestration remain separated from the frontend.
* REST APIs provide communication between frontend and backend.

---

# ADR-003: LangGraph Orchestration

**Status:** Accepted

## Decision

LangGraph will orchestrate the multi-agent workflow.

## Reason

The application requires stateful workflows where multiple specialized agents collaborate while sharing context. LangGraph provides explicit workflow control, shared state, branching, and predictable execution.

## Consequences

* Agent execution will be represented as a graph.
* Workflow state will be shared across agents.
* Future workflow expansion becomes straightforward.

---

# ADR-004: Deterministic Financial Calculations

**Status:** Accepted

## Decision

All financial calculations will be performed by deterministic Python services rather than language model reasoning.

## Reason

Investment calculations must be accurate, repeatable, testable, and explainable.

## Consequences

* Python performs the mathematics.
* AI interprets financial results.
* Financial calculations can be independently tested.

---

# ADR-005: Specialized Multi-Agent Architecture

**Status:** Accepted

## Decision

The MVP will consist of five specialized AI agents supported by one workflow step.

### Agents

* Opportunity Screening Agent
* Market Intelligence Agent
* Rehab & Condition Agent
* Financial Analysis Agent
* Investment Strategy Agent

### Workflow Step

* Property Intake

## Reason

Each agent owns a single investment decision while Property Intake simply prepares shared workflow data.

## Consequences

* Reduced agent complexity.
* Clear separation of responsibilities.
* Improved maintainability.
* Easier future expansion.

---

# ADR-006: Multi-Strategy Investment Platform

**Status:** Accepted

## Decision

R4B.AI will be designed as a multi-strategy investment platform.

## Reason

Although the initial financial implementation focuses on fix-and-flip analysis, the architecture should naturally support additional investment strategies including:

* Buy and Hold
* BRRRR
* Wholesale
* Value-Add Investments

This prevents architectural limitations as the platform evolves.

## Consequences

* Investment strategy remains extensible.
* New strategies can be added without redesigning the system.
* The architecture reflects the long-term product vision.

---

# ADR-007: Every Agent Owns One Decision

**Status:** Accepted

## Decision

Each AI agent is responsible for one primary investment decision.

## Reason

Specialized agents are easier to understand, test, maintain, and extend. This mirrors how experienced professionals specialize in one area of expertise before contributing to an overall recommendation.

## Consequences

* Minimal overlap between agents.
* Clear responsibilities.
* Explainable reasoning.
* Better alignment with the Single Responsibility Principle.

---

# ADR-008: Property Intake Is a Workflow Step

**Status:** Accepted

## Decision

Property Intake will be implemented as a workflow step rather than an AI agent.

## Reason

Property Intake collects, validates, and organizes data but does not make an independent decision. Since it does not own reasoning, it should not be implemented as an agent.

## Consequences

* Reduced AI complexity.
* Cleaner workflow.
* Better separation between data preparation and decision-making.
* Shared workflow state is established before agent execution begins.
