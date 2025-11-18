import pathway as pw
from app.connectors.simulated_stream import simulated_stream
from app.rag.live_index import make_index
from app.rag.llm_pipeline import build_pipeline

def run_pathway():
    # In this template, we create index and pipeline. For a real demo, wire the stream to transformations.
    index = make_index()
    rag_answer = build_pipeline(index)

    # Expose rag_answer via a module-level variable for server to use
    global RAG_ANSWER
    RAG_ANSWER = rag_answer

if __name__ == '__main__':
    run_pathway()
    # Run Pathway program loop if needed
    pw.run()
