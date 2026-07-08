from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langfuse.decorators import observe, langfuse_context

import json
import os

def _get_context_from_dataset(tool_name: str, **kwargs):
    try:
        with open(os.path.join("data", "test_cases.json"), "r") as f:
            cases = json.load(f)
        for case in cases:
            exp_tool = case.get("expected_tool_call", {})
            if exp_tool.get("name") == tool_name:
                match = True
                for k, v in exp_tool.get("arguments", {}).items():
                    if str(kwargs.get(k)).lower() != str(v).lower():
                        match = False
                        break
                if match:
                    return case.get("expected_answer_context", "Mock financial data.")
    except Exception:
        pass
    return "Mock financial data retrieved."

@tool
def search_financial_docs(ticker: str, year: int) -> str:
    """Search the 10-K or 10-Q financial documents for a specific company and year. Use this to find revenue, income, margins, etc."""
    return _get_context_from_dataset("search_financial_docs", ticker=ticker, year=year)

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Use this when you need to calculate growth, sums, or differences."""
    return _get_context_from_dataset("calculator", expression=expression)

@tool
def fetch_stock_price(ticker: str, date: str) -> str:
    """Fetch the historical stock price for a company on a specific date."""
    return f"Mock stock price for {ticker} on {date}."

@observe()
def run_agent_loop(query: str):
    langfuse_context.update_current_observation(input=query)
    llm = ChatOllama(model="llama3.1", temperature=0)
    tools = [search_financial_docs, calculator, fetch_stock_price]
    llm_with_tools = llm.bind_tools(tools)
    
    prompt = (
        "You are an expert financial assistant. YOU MUST NEVER ANSWER FROM YOUR OWN KNOWLEDGE. "
        "YOU MUST ALWAYS invoke one of the provided tools (search_financial_docs, calculator, or fetch_stock_price) "
        "before answering. Output ONLY the tool call."
    )
    
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=query)
    ]
    
    first_response = llm_with_tools.invoke(messages)
    messages.append(first_response)
    
    tool_calls = getattr(first_response, 'tool_calls', [])
    actual_tool = {}
    
    if tool_calls:
        tc = tool_calls[0]
        actual_tool = {"name": tc['name'], "arguments": tc['args']}
    elif first_response.content:
        import json
        import re
        # Fallback for local models that output JSON in text instead of native tool_calls
        try:
            match = re.search(r'\{.*\}', first_response.content.strip(), re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                # Map to tool if it looks like one
                if "name" in parsed:
                    actual_tool = {"name": parsed["name"], "arguments": parsed.get("arguments", {})}
                elif "search_financial_docs" in str(parsed):
                    actual_tool = {"name": "search_financial_docs", "arguments": parsed}
        except Exception:
            pass

    if actual_tool:
        tool_map = {t.name: t for t in tools}
        t_name = actual_tool["name"]
        if t_name in tool_map:
            t = tool_map[t_name]
            tool_msg = t.invoke(actual_tool["arguments"])
            messages.append(tool_msg)
                
        final_response = llm_with_tools.invoke(messages)
        actual_answer = final_response.content
    else:
        actual_answer = first_response.content
        
    return {
        "actual_tool": actual_tool,
        "actual_answer": actual_answer
    }
