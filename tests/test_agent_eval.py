import json
import pytest
import os
import sys

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.evaluator import evaluate_answer, check_tool_match

def load_test_cases():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_cases.json")
    with open(file_path, "r") as f:
        return json.load(f)

test_cases = load_test_cases()

def mock_agent_execution(query: str):
    # Simulates Phase 2 target agent execution. 
    # Returning dummy responses that match expected to ensure Phase 1 harness works.
    if "Apple" in query:
        return {
            "actual_tool": {"name": "search_financial_docs", "arguments": {"ticker": "AAPL", "year": 2022}},
            "actual_answer": "Apple's total net sales in 2022 reached $394,328 million."
        }
    elif "Microsoft" in query:
        return {
            "actual_tool": {"name": "search_financial_docs", "arguments": {"ticker": "MSFT", "year": 2022}},
            "actual_answer": "Microsoft reported a net income of $72,738 million in 2022, which is higher than the $61,271 million reported in 2021."
        }
    else:
        return {
            "actual_tool": {"name": "calculator", "arguments": {}},
            "actual_answer": "Tesla's YoY revenue growth in 2022 was approximately 51%."
        }

@pytest.mark.parametrize("case", test_cases, ids=[c["id"] for c in test_cases])
def test_evaluation_harness(case):
    # 1. Execute Target Agent
    result = mock_agent_execution(case["query"])
    
    # 2. Deterministic Check: Tool usage
    tool_match = check_tool_match(case["expected_tool_call"], result["actual_tool"])
    assert tool_match is True, f"Tool mismatch. Expected: {case['expected_tool_call']}, Actual: {result['actual_tool']}"
    
    # 3. Non-deterministic Check: LLM-as-a-judge
    score = evaluate_answer(case["expected_answer_context"], result["actual_answer"])
    
    assert "alignment_score" in score, "Missing alignment_score from judge output"
    assert "factual_correctness" in score, "Missing factual_correctness from judge output"
    
    assert score["alignment_score"] >= 4, f"Alignment too low: {score}"
    assert score["factual_correctness"] >= 4, f"Factuality too low: {score}"
