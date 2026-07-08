# Learning & Insights Log

This document serves as an ongoing repository for technical insights, challenges faced, and architectural decisions made during the development of the Agent Eval Harness.

## Decisions Made
- [x] **Dataset Source:** FinanceBench (Scaled to 505 test cases via script generation)
- [x] **LLM Judge Model:** Llama-3.1 (via Ollama)
- [x] **Target Agent Frameworks:** LangChain & CrewAI
- [x] **Observability Stack:** Langfuse Cloud & Local JSONL fallbacks
- [x] **CI/CD:** GitHub Actions

## Architectural Decisions
*   **[2026-07-07]** - *Decision*: Use Ollama's `format="json"` parameter for the LLM judge. -> *Rationale*: Ensures strict JSON output from local models like Llama-3 without relying on complex LangChain parser workarounds, preventing test parsing failures.
*   **[2026-07-07]** - *Decision*: Integrated Langchain's specific `CallbackHandler` for Langfuse rather than generic `@observe` for the target agent. -> *Rationale*: Captures deeper execution layers. (Note: Reverted to `@observe` due to versioning conflicts and legacy deprecations in Langchain ecosystem).
*   **[2026-07-08]** - *Decision*: Upgraded baseline testing model to `llama3.1`. -> *Rationale*: Older models like `llama3` threw HTTP 400 Bad Request errors when receiving strict JSON schema payloads from LangChain `bind_tools()`. Llama 3.1 natively supports these payloads at the Ollama API layer.

## Technical Challenges & Solutions
*   **[2026-07-07]** - *Challenge*: `httpx.ConnectError: [WinError 10061]` during Pytest runs. -> *Solution*: Ensure local Ollama daemon is offline. The test harness relies on `localhost:11434`.
*   **[2026-07-08]** - *Challenge*: LLM string representations breaking assertions (e.g., `2022` vs `"2022"`). -> *Solution*: Built a defensive type-coercion layer inside `check_tool_match` to cast tool arguments to lowercase strings prior to matching, drastically reducing false-negative evaluation failures.
*   **[2026-07-08]** - *Challenge*: CUDA Out of Memory errors. -> *Solution*: Standardized both the target agent and the LLM-as-a-judge to utilize the exact same model weights (`llama3.1`). This prevents Ollama from simultaneously loading 10GB+ of disparate models into local GPU VRAM.

## Evaluation Insights
*   **[2026-07-08]** - *Insight*: Agent evaluation is highly sensitive to the tool's return context. If the tool is merely a "mock" and does not inject the expected numeric ground truth back into the context window, the LLM-as-a-judge will aggressively (and correctly) penalize the model for factual hallucination. Real context injection is strictly required for passing alignment thresholds.
