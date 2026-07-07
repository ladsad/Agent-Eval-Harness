# Implementation Timeline: Agent Eval Harness

This timeline tracks the step-by-step implementation of the project plan.

## Phase 1: Core Evaluation Engine & Test Data (Days 1-2)
- [x] **Decision:** Select the source and domain for the real dataset (FinanceBench).
- [x] **Step 1.1:** Initialize the repository structure (`/src`, `/tests`, `/data`) and install dependencies (`requirements.txt`).
- [x] **Step 1.2:** Acquire and format Real Data into the Golden Dataset (`/data/test_cases.json`) with the initial 15-20 test cases.
- [x] **Decision:** Choose the LLM model for the LLM-as-a-judge (Llama-3-8B).
- [x] **Step 1.3:** Build the LLM-as-a-Judge Module (LangChain prompt template, JSON score validation).
- [x] **Step 1.4:** Implement the Pytest Wrapper to iterate over test cases and run checks.

## Phase 2: Agent Integration & Tool-Calling Evaluation (Days 3-4)
- [x] **Decision:** Select the Agent Framework (LangChain vs CrewAI) for the target agent.
- [x] **Decision:** Define the real-world tools the agent needs access to (e.g., SQL DB query, API fetch) based on the real dataset.
- [x] **Step 2.1:** Build the Target Agent equipped with the defined real tools.
- [x] **Step 2.2:** Implement Tool Execution Tracking to intercept tool choices and arguments.
- [x] **Step 2.3:** Write Regression Assertions (asserting tool accuracy and judge score thresholds).

## Phase 3: Observability & Dashboards (Days 5-6)
- [x] **Decision:** Choose observability platform (Langfuse SDK vs local Streamlit + SQLite).
- [x] **Step 3.1:** Setup observability backend based on the decision.
- [x] **Step 3.2:** Verify dashboards capture pass/fail rates, latency, and average judge scores.

## Phase 4: CI/CD Pipeline Integration (Day 7)
- [x] **Step 4.1:** Create GitHub Actions Workflow (`.github/workflows/eval.yml`) triggering on `main` PRs.
- [x] **Step 4.2:** Simulate a regression (bad prompt) to verify the pipeline correctly fails the CI check.
