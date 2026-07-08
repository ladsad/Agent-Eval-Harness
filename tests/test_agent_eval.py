import json
import pytest
import os

# Fix for Git Bash / Conda environments with broken SSL_CERT_FILE paths
if "SSL_CERT_FILE" in os.environ and not os.path.exists(os.environ["SSL_CERT_FILE"]):
    del os.environ["SSL_CERT_FILE"]

import sys
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from langfuse.decorators import observe, langfuse_context

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.evaluator import evaluate_answer, check_tool_match
from src.agent import run_agent_loop

def load_test_cases():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_cases.json")
    with open(file_path, "r") as f:
        return json.load(f)

test_cases = load_test_cases()

def log_metric(record):
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "metrics.jsonl")
    with open(file_path, "a") as f:
        f.write(json.dumps(record) + "\n")

def run_agent(query: str):
    try:
        return run_agent_loop(query)
    except Exception as e:
        # Fallback if agent crashes (e.g. tool parsing failure from local LLM)
        return {
            "actual_tool": {},
            "actual_answer": f"Agent crashed: {str(e)}"
        }

@pytest.mark.parametrize("case", test_cases, ids=[c["id"] for c in test_cases])
@observe()
def test_evaluation_harness(case):
    start_time = time.time()
    
    # 1. Execute Target Agent
    result = run_agent(case["query"])
    agent_latency = time.time() - start_time
    
    # 2. Deterministic Check: Tool usage
    tool_match = check_tool_match(case["expected_tool_call"], result["actual_tool"])
    
    # 3. Non-deterministic Check: LLM-as-a-judge
    score = evaluate_answer(case["expected_answer_context"], result["actual_answer"])
    
    alignment = score.get("alignment_score", 1)
    factual = score.get("factual_correctness", 1)
    
    # Log metrics for future comparison
    log_metric({
        "timestamp": datetime.utcnow().isoformat(),
        "case_id": case["id"],
        "latency_seconds": round(agent_latency, 2),
        "tool_match": tool_match,
        "alignment_score": alignment,
        "factual_correctness": factual
    })
    
    if os.environ.get("LANGFUSE_PUBLIC_KEY"):
        langfuse_context.score_current_trace(name="tool_match", value=1 if tool_match else 0)
        langfuse_context.score_current_trace(name="alignment", value=alignment)
        langfuse_context.score_current_trace(name="factual_correctness", value=factual)
    
    assert tool_match is True, f"Tool mismatch. Expected: {case['expected_tool_call']}, Actual: {result['actual_tool']}"
    assert "alignment_score" in score, "Missing alignment_score from judge output"
    assert "factual_correctness" in score, "Missing factual_correctness from judge output"
    
    assert alignment >= 4, f"Alignment too low: {score}"
    assert factual >= 4, f"Factuality too low: {score}"
    
    # Flush traces before exit
    langfuse_context.flush()
