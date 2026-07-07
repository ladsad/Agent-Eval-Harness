# Project Plan: Automated AI Evaluation Harness & Regression Detector

This plan outlines the architecture and implementation steps to build the evaluation harness exactly as described on your HackerRank resume. 

## 🏗️ Architecture Overview
- **Agent Frameworks:** LangChain / CrewAI (Target systems to be evaluated)
- **Evaluation Engine:** Python (pytest) + LLM-as-a-judge (LangChain)
- **Test Data Storage:** Local JSON/YAML (for the 500+ test cases)
- **CI/CD:** GitHub Actions
- **Observability/Dashboards:** Langfuse or local Streamlit + SQLite

---

## Phase 1: Core Evaluation Engine & Test Data (Days 1-2)
**Goal:** Build the foundational testing logic and the "golden dataset."

1. **Initialize the Repository**
   - Create a standard Python repository structure (`/src`, `/tests`, `/data`).
   - Setup `requirements.txt` (`pytest`, `langchain`, `langfuse`, `openai`/`anthropic`).
2. **Create the Golden Dataset (`/data/test_cases.json`)**
   - Write 15-20 initial test cases (you can script an LLM to generate the other 480+ later).
   - Each test case needs: `input_query`, `expected_tool_call` (name and arguments), and `expected_answer_context`.
3. **Build the LLM-as-a-Judge Module**
   - Create a LangChain prompt template that takes the `expected_answer` and `actual_agent_answer`.
   - The judge must output a strict JSON score: `{"alignment_score": 1-5, "factual_correctness": 1-5, "reasoning": "..."}`.
4. **Implement the Pytest Wrapper**
   - Write a `pytest` harness that iterates over `test_cases.json`.
   - For each case: execute a dummy LangChain agent, capture the output, and run it through the deterministic checks (exact tool match) and non-deterministic checks (LLM judge).

## Phase 2: Agent Integration & Tool-Calling Evaluation (Days 3-4)
**Goal:** Hook up a real agent and measure its tool-calling accuracy.

1. **Build a Dummy Target Agent**
   - Create a simple LangChain or CrewAI agent equipped with 2-3 mock tools (e.g., `get_user_data`, `fetch_financials`).
2. **Implement Tool Execution Tracking**
   - Intercept the agent's execution to capture which tools it decided to call and with what arguments.
3. **Write Regression Assertions**
   - `assert actual_tool_called == expected_tool_called`
   - `assert llm_judge_score >= 4.0` (Fails the test if the agent hallucinates or scores poorly).

## Phase 3: Observability & Dashboards (Days 5-6)
**Goal:** Track the metrics and visualize them as stated in the resume.

1. **Integrate Langfuse (Recommended for speed)**
   - Wrap your dummy agent and evaluator with the Langfuse Python SDK.
   - This automatically creates the "real-time dashboards for metrics tracking."
2. **Alternative: Build a Custom Streamlit Dashboard**
   - If you want it completely self-hosted, write the pytest results to a local SQLite database.
   - Build a quick `app.py` in Streamlit that reads the SQLite DB and charts the pass/fail rate, average latency, and judge scores over time.

## Phase 4: CI/CD Pipeline Integration (Day 7)
**Goal:** Catch prompt regressions automatically on pull requests.

1. **Create GitHub Actions Workflow (`.github/workflows/eval.yml`)**
   - Trigger on `pull_request` to `main`.
   - Setup Python, install dependencies.
   - Run `pytest tests/test_agent_eval.py`.
2. **Simulate a Regression**
   - Commit a "bad" system prompt to a branch (e.g., tell the agent to ignore instructions).
   - Verify that the GitHub Action fails and blocks the PR because the LLM judge scores drop below the threshold.

---

## 🚀 Quick Start Commands
Run these in your terminal to get started immediately:

```bash
mkdir Agent-Eval-Harness
cd Agent-Eval-Harness
python -m venv venv
venv\Scripts\activate
pip install langchain langchain-openai pytest pydantic langfuse
mkdir src tests data
type nul > data\test_cases.json
type nul > tests\test_evaluator.py
git init
```
