# Agent Eval Harness

An enterprise-grade automated framework designed to programmatically evaluate the tool-calling accuracy, context retention, and reasoning quality of AI agents (LangChain & CrewAI systems). 

Built with **LangChain**, **CrewAI**, **Pytest**, and local execution via **Ollama (Llama 3.1)**.

## Core Features
- **Massive Scale**: Evaluates AI systems across **500+ dynamic test cases** representing real-world financial queries.
- **Deterministic & Non-Deterministic Evaluation**: 
  - *Tool Matching*: Asserts that exact expected tool schemas and arguments are invoked.
  - *LLM-as-a-Judge*: Utilizes prompt-based local models (Llama-3.1) returning strict JSON to score agent outputs on alignment (1-5) and factual correctness (1-5).
- **Observability**: Real-time dashboards using **Langfuse Cloud** to track pass/fail rates, latency drops, and trace sub-spans.
- **CI/CD Integration**: Fully integrated into **GitHub Actions**, automatically catching prompt regressions and execution hallucinations before production merges.

## Project Structure
- `/src` - Core agent execution loops (LangChain/CrewAI wrappers) and LLM-as-a-judge evaluators.
- `/tests` - Pytest wrappers that dynamically execute the 500+ case evaluation loop.
- `/data` - The golden dataset (`test_cases.json`) and local metric logs (`metrics.jsonl`).
- `/documentation` - Deep dive into architecture, timelines, and technical insights.

## Quick Start
1. Install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Ensure Ollama is running locally and you have pulled the required model:
   ```bash
   ollama pull llama3.1
   ```
3. Set your observability keys in `.env`:
   ```env
   LANGFUSE_PUBLIC_KEY="pk-lf-..."
   LANGFUSE_SECRET_KEY="sk-lf-..."
   LANGFUSE_HOST="https://cloud.langfuse.com"
   ```
4. Run the evaluation suite:
   ```bash
   pytest tests/test_agent_eval.py -v
   ```

## Status
- [x] Phase 1: Core Evaluation Engine & Test Data (500+ Cases)
- [x] Phase 2: Agent Integration (LangChain & CrewAI Support)
- [x] Phase 3: Observability Dashboards (Langfuse)
- [x] Phase 4: CI/CD Pipeline Integration (GitHub Actions)
