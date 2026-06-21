# Architecture

R4B.AI is planned as a React + TypeScript frontend connected to a Python FastAPI backend. The backend will coordinate application services, deterministic financial calculations, and a LangGraph-based agent workflow.

## High-Level Components

- Frontend: User interface for property intake, analysis review, and investment recommendations.
- Backend API: FastAPI service that receives requests from the frontend and returns structured results.
- Services: Backend modules for reusable business logic such as calculations, data validation, and formatting.
- Agents: Specialized agent components responsible for specific parts of the acquisition workflow.
- Graphs: LangGraph definitions that control the order, state, and handoffs between agents.
- Tests: Automated tests for backend services, graph behavior, and important workflows.

## Initial Direction

The first version will focus on clarity and reliability. Financial math should be deterministic, while agents should handle interpretation, summarization, and recommendation support.
