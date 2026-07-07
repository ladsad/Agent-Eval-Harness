import json
import os

cases = []
companies = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN"]
years = [2021, 2022, 2023]

# Base 3
cases.append({
    "id": "fb_001",
    "query": "What is the total revenue for Apple in 2022?",
    "expected_tool_call": {"name": "search_financial_docs", "arguments": {"ticker": "AAPL", "year": 2022}},
    "expected_answer_context": "Apple's total net sales were $394,328 million in 2022."
})
cases.append({
    "id": "fb_002",
    "query": "Did Microsoft's net income increase from 2021 to 2022?",
    "expected_tool_call": {"name": "search_financial_docs", "arguments": {"ticker": "MSFT", "year": 2022}},
    "expected_answer_context": "Microsoft's net income in 2022 was $72,738 million, up from $61,271 million in 2021."
})
cases.append({
    "id": "fb_003",
    "query": "Calculate the year-over-year revenue growth for Tesla in 2022.",
    "expected_tool_call": {"name": "calculator", "arguments": {}},
    "expected_answer_context": "Tesla revenue grew by 51% YoY in 2022 (from 53.8B to 81.4B)."
})

# Generate 17 more
for i in range(4, 21):
    comp = companies[i % len(companies)]
    year = years[i % len(years)]
    if i % 2 == 0:
        query = f"What was the operating margin for {comp} in {year}?"
        expected_context = f"{comp} reported an operating margin of 25.4% in {year}."
        tool = {"name": "search_financial_docs", "arguments": {"ticker": comp, "year": year}}
    else:
        query = f"What is the sum of revenue for {comp} in {year} and {year-1}?"
        expected_context = f"The combined revenue for {comp} across {year} and {year-1} was $400 billion."
        tool = {"name": "calculator", "arguments": {}}
        
    cases.append({
        "id": f"fb_{i:03d}",
        "query": query,
        "expected_tool_call": tool,
        "expected_answer_context": expected_context
    })

output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_cases.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(cases, f, indent=2)

print("Generated 20 mock FinanceBench cases.")
