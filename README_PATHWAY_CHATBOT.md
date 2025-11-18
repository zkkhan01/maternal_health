# Maternal Health with Pathway Chatbot

This repository is your original maternal_health project enhanced with a Pathway-based chatbot skeleton that meets the hackathon requirements for live ingestion, streaming transforms, RAG, and LLM integration.

## What I added
- `app/connectors/simulated_stream.py` : Example simulated real-time stream connector using Pathway python_connector decorator
- `app/processing/feature_engineering.py` : Streaming transform placeholder
- `app/rag/live_index.py` : Pathway live index creation using SentenceTransformer embeddings
- `app/rag/llm_pipeline.py` : LLM pipeline using Pathway xpack BDH model
- `app/rag/agent.py` : Agent orchestrator stub
- `app/pathway_main.py` : Script to initialize index and pipeline. Run this to set up RAG_ANSWER for the server
- `app/server/api.py` : FastAPI server exposing `/api/chat`
- `frontend/chat-ui/index.html` : Simple chat UI that posts to `/api/chat`

## How to run locally (development)
1. Create a Python environment and install requirements from `requirements.txt`
2. Place any maternal knowledge text files into `app/data/maternal_knowledge_base/` as `.txt` files
3. Run Pathway program:
   - `python -m app.pathway_main`
   - This will create a module-level `RAG_ANSWER` function used by the API. In production, you may run pathway inside a separate process or container and expose the model via a server.
4. Run FastAPI server:
   - `uvicorn app.server.api:app --host 0.0.0.0 --port 8000 --reload`
5. Open the chat UI: `http://localhost:8000/frontend/chat-ui/index.html`

## Notes and placeholders
- The included Pathway files are templates that demonstrate how to wire up connectors, transforms, index, and LLM pipeline.
- You must install Pathway and xpack packages and configure licensing if required by Pathway. See Pathway docs at https://pathway.com/developers/
- Do not commit API keys to the repo. Use environment variables or secret managers.

## Requirements file
See `requirements.txt` for Python dependencies. Install them in a virtual env.
