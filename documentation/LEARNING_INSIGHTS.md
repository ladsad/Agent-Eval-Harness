# Learning & Insights Log

This document serves as an ongoing repository for technical insights, challenges faced, and architectural decisions made during the development of the Agent Eval Harness.

## Decisions Made
- [x] **Dataset Source:** FinanceBench
- [x] **LLM Judge Model:** Llama-3-8B (via Ollama)
- [x] **Target Agent Framework:** LangChain
- [x] **Target Agent Tools:** `search_financial_docs`, `calculator`, `fetch_stock_price` (to start)
- [x] **Observability Stack:** Langfuse Cloud

## Architectural Decisions
*(Log key choices here, e.g., why Langfuse vs local Streamlit, or LLM-as-a-judge model selection)*
*   **[2026-07-07]** - *Decision*: Use Ollama's `format="json"` parameter for the LLM judge. -> *Rationale*: Ensures strict JSON output from local models like Llama-3-8B without relying on complex LangChain parser workarounds, preventing test parsing failures.
*   **[2026-07-07]** - *Decision*: Manually extract a subset of FinanceBench for the Golden Dataset. -> *Rationale*: The full dataset is unstructured for direct tool-calling evaluation. Mapping Q&A pairs to expected `search_financial_docs` and `calculator` tools creates a deterministic ground truth for initial development.

## Technical Challenges & Solutions
*(Log bugs, API issues, or infrastructure hurdles and how they were resolved)*
*   **[YYYY-MM-DD]** - *Challenge*: ... -> *Solution*: ...

## Evaluation Insights
*(Observations on agent behavior, common failure modes, or prompt engineering discoveries)*
*   **[YYYY-MM-DD]** - *Insight*: ...

## General Notes & Future Ideas
*(Ideas for V2, optimization thoughts, or helpful commands)*
*   ...
