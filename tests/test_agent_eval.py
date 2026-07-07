import json
import pytest
import os
import sys

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.evaluator import evaluate_answer, check_tool_match
from src.agent import run_agent_loop

def load_test_cases():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_cases.json")
    with open(file_path, "r") as f:
        return json.load(f)

test_cases = load_test_cases()

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
def test_evaluation_harness(case):
    # 1. Execute Target Agent
    result = run_agent(case["query"])
    
    # 2. Deterministic Check: Tool usage
    tool_match = check_tool_match(case["expected_tool_call"], result["actual_tool"])
    assert tool_match is True, f"Tool mismatch. Expected: {case['expected_tool_call']}, Actual: {result['actual_tool']}"
    
    # 3. Non-deterministic Check: LLM-as-a-judge
    score = evaluate_answer(case["expected_answer_context"], result["actual_answer"])
    
    assert "alignment_score" in score, "Missing alignment_score from judge output"
    assert "factual_correctness" in score, "Missing factual_correctness from judge output"
    
    assert score["alignment_score"] >= 4, f"Alignment too low: {score}"
    assert score["factual_correctness"] >= 4, f"Factuality too low: {score}"
