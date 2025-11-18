import pathway as pw
from app.connectors.simulated_stream import read_simulated_stream
from app.processing.feature_engineering import compute_trends
from app.rag.live_index import make_index
from app.rag.llm_pipeline import build_pipeline

def run_pathway():
    # Read from simulated subject into a Pathway table
    stream_table = read_simulated_stream(autocommit_duration_ms=1000)

    # Example transformation - compute rolling averages (placeholder)
    try:
        trends_table = compute_trends(stream_table)
        # Optionally write to csv for inspection
        pw.io.csv.write(trends_table, 'app/data/trends_output.csv')
    except Exception:
        # If compute_trends is a placeholder, ignore failure here
        pass

    # Build live RAG index from app/data/maternal_knowledge_base
    index = make_index()
    rag_answer = build_pipeline(index)

    # expose rag_answer for the API server to call
    global RAG_ANSWER
    RAG_ANSWER = rag_answer

if __name__ == '__main__':
    run_pathway()
    pw.run()
