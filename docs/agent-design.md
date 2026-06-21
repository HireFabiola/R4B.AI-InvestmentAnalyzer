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

**Is this opportunity worth further investigation?**

Typical responsibilities:

* Review listing photos for visible opportunity and obvious concerns
* Compare the asking price against a preliminary market check
* Determine whether the property aligns with the investor's philosophy
* Recommend the next best action

Typical outputs:

* Schedule Property Visit
* Request Additional Information
* Contact Listing Agent
* Pass

The Opportunity Screening Agent evaluates only listing-level information. It does not replace a property inspection or final investment analysis.

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
