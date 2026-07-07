import json
import re
from datasets import load_dataset
import os

def generate_cases():
    print("Downloading FinanceBench dataset...")
    # Financebench is hosted on HF
    ds = load_dataset("patronus-ai/financebench")
    
    # The dataset typically has a 'train' split
    data = ds['train']
    
    cases = []
    # Fetch exactly 20 real questions
    for i in range(20):
        row = data[i]
        
        doc_name = row.get('doc_name', '')
        
        # Extract ticker from document name (e.g., 'AAPL_2022_10K')
        ticker = "UNKNOWN"
        match = re.search(r'^([A-Z]+)_', doc_name)
        if match:
            ticker = match.group(1)
            
        case = {
            "id": row.get("financebench_id", f"fb_{i}"),
            "query": row.get("question"),
            "expected_tool_call": {
                "name": "search_financial_docs",
                "arguments": {"ticker": ticker}
            },
            "expected_answer_context": row.get("answer", "")
        }
        cases.append(case)
        
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_cases.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cases, f, indent=2)
        
    print(f"Successfully wrote {len(cases)} cases to data/test_cases.json")

if __name__ == "__main__":
    generate_cases()
