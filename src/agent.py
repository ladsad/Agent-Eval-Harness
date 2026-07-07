from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage

@tool
def search_financial_docs(ticker: str, year: int) -> str:
    """Search the 10-K or 10-Q financial documents for a specific company and year. Use this to find revenue, income, margins, etc."""
    return f"Mock financial data retrieved for {ticker} in {year}."

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Use this when you need to calculate growth, sums, or differences."""
    return "Mock calculation result."

@tool
def fetch_stock_price(ticker: str, date: str) -> str:
    """Fetch the historical stock price for a company on a specific date."""
    return f"Mock stock price for {ticker} on {date}."

def run_agent_loop(query: str):
    llm = ChatOllama(model="llama3", temperature=0)
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
