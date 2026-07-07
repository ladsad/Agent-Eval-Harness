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
*   **[2026-07-07]** - *Decision*: Integrated Langchain's specific `CallbackHandler` for Langfuse rather than generic `@observe` for the target agent. -> *Rationale*: Follows Langfuse best practices for frameworks; it captures deeper execution layers (prompts, intermediate steps) automatically compared to the generic decorator.

## Technical Challenges & Solutions
*(Log bugs, API issues, or infrastructure hurdles and how they were resolved)*
*   **[2026-07-07]** - *Challenge*: Langfuse decorators failed to pick up keys from `.env` during Pytest execution. -> *Solution*: Identified via Langfuse skills that `load_dotenv()` must be called *before* importing `langfuse.decorators`. Reordering the imports resolved the initialization failure.
*   **[2026-07-07]** - *Challenge*: `httpx.ConnectError: [WinError 10061]` during Pytest runs. -> *Solution*: This explicitly indicates the local Ollama daemon is offline. The test harness relies on `localhost:11434`. Starting the Ollama application resolves the connection refusal.

## Evaluation Insights
*(Observations on agent behavior, common failure modes, or prompt engineering discoveries)*
*   **[2026-07-07]** - *Insight*: The standard local `llama3:8b` model struggles significantly with zero-shot LangChain tool selection. It frequently fails to output deterministic JSON tool payloads (even with explicit prompt constraints), causing the evaluation assertions to correctly fail. This perfectly demonstrates the harness's ability to catch base-model regressions or poorly fine-tuned tool-calling capabilities.

## General Notes & Future Ideas
*(Ideas for V2, optimization thoughts, or helpful commands)*
*   ...
