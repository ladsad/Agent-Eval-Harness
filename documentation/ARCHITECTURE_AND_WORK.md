# Architecture and Implementation Report: Agent Evaluation Harness

## Executive Summary
This document details the complete end-to-end architecture of the Agent Evaluation Harness. The project was conceived to programmatically evaluate the robustness of multi-agent AI systems (LangChain and CrewAI) without relying on expensive, slow human intervention. The harness validates tool-calling precision, context retention, and reasoning quality across a massive suite of 500+ dynamic edge-case scenarios.

## Core Architectural Pillars

### 1. Dual-Layer Evaluation Engine
The system employs a two-tiered evaluation approach to achieve both strictness and nuance:
- **Deterministic Tool Matching**: The harness intercepts the LLM's raw payload during the `bind_tools` execution layer. It mathematically asserts that the agent not only selected the correct tool (e.g., `search_financial_docs` instead of `calculator`), but also perfectly populated the arguments (e.g., `ticker: AAPL`, `year: 2022`), bypassing false negatives caused by integer/string type coercion.
- **LLM-as-a-Judge (Non-Deterministic)**: Using a local `llama3.1` model pinned to `temperature=0` and `format="json"`, the judge compares the agent's final synthesized answer against a verified "Golden Dataset" context. It grades the response on an integer scale of 1-5 for both **Alignment** (did it answer the prompt?) and **Factual Correctness** (are the numbers real?).

### 2. Massive Scalability (500+ Test Cases)
Testing agents against 10 queries is insufficient for production. The framework utilizes a procedural mutation engine that scales a subset of high-quality `FinanceBench` queries into **505 dynamic test cases**. By slightly mutating targets (e.g., swapping years from 2022 to 2016) and matching expected context dynamically, the harness ensures the agent isn't merely overfitting to a static prompt.

### 3. CI/CD Integration & Defense
The harness is deeply embedded into a **GitHub Actions** CI/CD workflow (`eval.yml`).
- **Pre-Merge Defense**: Any PR that modifies agent system prompts, updates the LangChain orchestration logic, or modifies CrewAI hierarchies triggers the suite.
- If the average Alignment score drops below a 4.0, or tool-calling failure rates spike (prompt regression), the pipeline immediately blocks the merge, preventing AI hallucinations from reaching production.

### 4. Real-Time Observability Stack
Local CLI testing is opaque. To solve this, the framework is wired directly into **Langfuse Cloud**.
- **Trace Spans**: Every Pytest execution creates a Parent Trace, with sub-spans capturing the exact latency of the LLM inference, the tool execution time, and the judge's scoring time.
- **Score Dashboards**: The numeric grades (Tool Match boolean, Alignment 1-5) are pushed to the Langfuse API. This generates a live dashboard allowing engineers to visually track agent degradation over time and filter traces strictly by "Failed Tool Calls" to debug specific prompt weaknesses.
- **Local Persistence**: A fallback `metrics.jsonl` tracks rolling latency and scores for offline analysis.

## Technical Deep Dive: The Data Flow
1. **Trigger**: Pytest executes `test_agent_eval.py`, loading a test case from `test_cases.json`.
2. **Agent Execution**: The LangChain wrapper initializes `llama3.1`. The system prompt strictly limits knowledge boundaries.
3. **Tool Interception**: The agent requests to fire a tool. The framework captures the `tool_call` payload.
4. **Mock Resolution**: The framework intercepts the tool, matches the arguments against the ground-truth JSON, and synthetically injects the real-world answer (e.g., "Apple's revenue was $394B") back into the context.
5. **Synthesis**: The agent formulates the final answer.
6. **Judgment**: The evaluator prompt is compiled, fed to the LLM-as-a-judge, and parsed for JSON scores.
7. **Assertion & Logging**: Pytest asserts thresholds, the Langfuse SDK flushes the trace asynchronously, and local files are appended.

## Framework Support
- **LangChain**: Fully implemented with custom tool binding and fallback regex parsers.
- **CrewAI**: Structural wrappers initialized (`src/crewai_agent.py`) to easily swap orchestrators and run the identical evaluation pipeline over CrewAI worker nodes.
