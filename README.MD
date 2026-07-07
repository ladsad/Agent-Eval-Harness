# Agent Eval Harness

An automated framework for evaluating agentic AI systems, specifically designed to test tool-calling accuracy, reasoning, and alignment using an LLM-as-a-judge approach. 

Built with LangChain, Pytest, and local models via Ollama. 

## Features
- **Deterministic Evaluation**: Asserts that the exact expected tools (and arguments) are invoked.
- **Non-Deterministic Evaluation**: Uses an LLM (Llama-3-8B) as a judge to score factual correctness and alignment based on strict JSON outputs.
- **Real-World Dataset**: Evaluates against a subset of FinanceBench queries (Financial QA).

## Project Structure
- `/src` - Core evaluation logic and judge modules.
- `/tests` - Pytest wrappers for executing the evaluation loop.
- `/data` - Golden dataset with test cases and expected tool call targets.
- `/documentation` - Project plans, timelines, and architectural insights.

## Quick Start
To run the evaluation harness locally:

1. Install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Ensure Ollama is running locally with `llama3`.

3. Run the evaluation suite:
   ```bash
   pytest tests/test_agent_eval.py -v
   ```

## Status
- [x] Phase 1: Core Evaluation Engine & Test Data
- [x] Phase 2: Agent Integration & Tool-Calling Evaluation
- [ ] Phase 3: Observability & Dashboards
- [ ] Phase 4: CI/CD Pipeline Integration
