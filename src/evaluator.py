import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langfuse.decorators import observe, langfuse_context

def get_judge_model():
    # Using Llama-3-8B locally via Ollama with strict JSON formatting
    return ChatOllama(model="llama3", temperature=0, format="json")

JUDGE_PROMPT = PromptTemplate.from_template("""
You are an expert evaluator. Compare the ACTUAL ANSWER provided by an AI agent to the EXPECTED CONTEXT.
Output a strict JSON object with exactly these three keys:
"alignment_score": integer from 1 to 5 indicating how well the actual answer aligns with the expected context.
"factual_correctness": integer from 1 to 5 on factual accuracy.
"reasoning": string with a brief explanation.

EXPECTED CONTEXT: {expected_context}
ACTUAL ANSWER: {actual_answer}
""")

@observe()
def evaluate_answer(expected_context: str, actual_answer: str) -> dict:
    langfuse_context.update_current_observation(input={"expected_context": expected_context, "actual_answer": actual_answer})
    model = get_judge_model()
    chain = JUDGE_PROMPT | model
    
    response = chain.invoke({"expected_context": expected_context, "actual_answer": actual_answer})
    try:
        if hasattr(response, "content"):
            return json.loads(response.content)
        return json.loads(response)
    except json.JSONDecodeError:
        return {"alignment_score": 1, "factual_correctness": 1, "reasoning": "Failed to parse judge JSON output."}

def check_tool_match(expected_tool: dict, actual_tool: dict) -> bool:
    if not expected_tool or not actual_tool:
        return False
    if expected_tool.get("name") != actual_tool.get("name"):
        return False
        
    exp_args = expected_tool.get("arguments", {})
    act_args = actual_tool.get("arguments", {})
    
    # Check that all expected arguments are present in the actual arguments
    for k, v in exp_args.items():
        if act_args.get(k) != v:
            return False
            
    return True
