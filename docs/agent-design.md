# Agent Design

## Overview

R4B.AI is designed as an **agentic decision-support system**. Rather than relying on a single AI conversation, the platform distributes responsibilities across specialized agents. Each agent owns a single decision within the investment workflow while contributing information to a shared system state.

This approach improves explainability, maintainability, and future extensibility.

---

# Workflow Overview

```
Opportunity Screening Agent
        ↓
Property Intake (Workflow Step)
        ↓
Market Intelligence Agent
        ↓
Rehab & Condition Agent
        ↓
Financial Analysis Agent
        ↓
Investment Strategy Agent
```

---

# Property Intake (Workflow Step)

Property Intake is **not** an AI agent.

Its responsibility is to collect, validate, and organize property information before deeper analysis begins.

Typical responsibilities include:

* Collect property address and property type
* Store asking price
* Capture listing information
* Record property characteristics (beds, baths, square footage, lot size, year built)
* Organize uploaded photos and documents
* Update the shared workflow state for downstream agents

Because Property Intake does not make an independent decision, it is implemented as a workflow step rather than an AI agent.

---

# Opportunity Screening Agent

## Primary Decision

> **Is this opportunity worth further investigation?**

The Opportunity Screening Agent performs an initial screening using only listing-level information. Its purpose is to determine whether a property appears promising enough to justify additional time, research, and due diligence.

This agent **does not** determine whether a property should ultimately be purchased.

---

## Responsibilities

- Evaluate the property's fundamental characteristics:
  - Bedrooms
  - Bathrooms
  - Square Footage
  - Year Built
- Compare the asking price against preliminary pricing metrics.
- Review listing photos for visible opportunities and obvious concerns.
- Analyze the listing description for positive signals, major concerns, and investigation triggers.
- Assess the completeness and quality of the available listing information.
- Determine whether the opportunity aligns with the investor's current investment philosophy.
- Recommend the next best action.

---

## Typical Outputs

- Schedule Property Visit
- Contact Listing Agent
- Request Additional Information
- Pass

---

## Evaluation Framework

The Opportunity Screening Agent evaluates every listing through four lenses.

### Strengths

Characteristics that increase the attractiveness of the opportunity.

**Examples**

- Three or more bedrooms
- Two or more bathrooms
- Preferred square footage range
- Favorable preliminary price per square foot
- Good listing transparency
- Strong opportunity language ("good bones", "cosmetic", etc.)

---

### Risks

Characteristics that may materially increase renovation cost, uncertainty, or investment risk.

**Examples**

- Foundation concerns
- Structural concerns
- Mold
- Fire damage
- Roof leaks
- Full gut renovation
- Extremely small properties
- Older properties requiring significant systems verification

---

### Investigation Triggers

Conditions that are **not automatically negative**, but require additional due diligence before making an informed investment decision.

**Examples**

- Cash-only listing
- As-is listing
- Missing square footage
- Missing listing photos
- Missing property description
- Unknown system ages
- Limited property information

---

### Data Completeness

Measures how complete the available listing information is.

The Opportunity Screening Agent uses this to determine whether sufficient information exists to make a reliable preliminary assessment.

Data completeness is **not** a statistical confidence score and should not be interpreted as the probability that the recommendation is correct.

---

## Scope

The Opportunity Screening Agent evaluates **listing-level information only**.

It does **not** replace:

- Property inspections
- Contractor estimates
- Financial analysis
- Market analysis
- Repair cost estimation
- Final investment decision-making

Those responsibilities belong to later agents in the R4B.AI pipeline.

---

## Design Philosophy

The Opportunity Screening Agent is intentionally conservative.

Its purpose is **not** to determine whether a property should be purchased.

Its purpose is to answer one question:

> **"Based on the information currently available, is this property worth investigating further?"**

---

# Market Intelligence Agent

## Primary Decision

**What is this property likely worth within its current market?**

Typical responsibilities:

* Review comparable sales
* Analyze neighborhood characteristics
* Evaluate local market conditions
* Identify pricing opportunities
* Highlight market-related risks

This agent provides market context but does not estimate repair costs or determine investment strategy.

---

# Rehab & Condition Agent

## Primary Decision

**What condition and renovation risks should the investor understand?**

Typical responsibilities:

* Evaluate visible property condition
* Organize repair categories
* Highlight potential structural concerns
* Identify missing inspection information
* Estimate renovation complexity

This agent focuses on renovation risk rather than financial performance.

---

# Financial Analysis Agent

## Primary Decision

**Do the financials support continued investment consideration?**

Typical responsibilities:

* Execute deterministic financial calculations
* Calculate projected profit
* Evaluate return on investment
* Identify assumptions that most affect profitability
* Prepare financial outputs for downstream reasoning

The Financial Analysis Agent does not generate financial mathematics using an LLM. All calculations are performed by deterministic Python services.

---

# Investment Strategy Agent

## Primary Decision

**Which investment strategy best fits this opportunity?**

Typical responsibilities:

* Combine market, condition, and financial analysis
* Recommend the most appropriate investment strategy
* Explain the reasoning behind the recommendation
* Identify remaining risks and assumptions
* Recommend next steps before committing to the investment

Potential strategies include:

* Fix and Flip
* Buy and Hold
* BRRRR
* Wholesale
* Pass

The Investment Strategy Agent supports investor decision-making by providing explainable recommendations while leaving the final investment decision to the investor.

---

# Design Principles

Every agent within R4B.AI follows these architectural principles:

* Own one primary decision.
* Contribute to a shared workflow state.
* Avoid overlapping responsibilities.
* Explain every recommendation.
* Use deterministic calculations whenever exact mathematics is required.
* Keep the investor in the decision-making loop.

Together, these principles create a transparent, explainable, and extensible agentic AI system that mirrors the workflow of an experienced real estate investor.
