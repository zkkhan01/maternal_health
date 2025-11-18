# Simple agent orchestration stub. For advanced workflows, integrate LangGraph or LlamaIndex.
def agent_flow(question, index, metrics=None):
    # Use index and llm to create multi-step responses if needed.
    answer = index.search(question, k=3)  # placeholder
    return answer
