from fastapi import FastAPI
from pydantic import BaseModel
import importlib
import threading
import time

app = FastAPI()

class ChatInput(BaseModel):
    message: str

# import the pathway main to initialize index and model
try:
    import app.pathway_main as pm
except Exception as e:
    pm = None

# If pathway was run separately, pm.RAG_ANSWER should be available. If not, responses will be simulated.
def get_answer_fn():
    if pm and hasattr(pm, 'RAG_ANSWER') and pm.RAG_ANSWER:
        return pm.RAG_ANSWER
    else:
        # fallback function
        def fallback(q):
            return 'Pathway not initialized. This is a placeholder response. Run pathway_main to initialize the model and index.'
        return fallback

ANSWER_FN = get_answer_fn()

@app.post('/chat')
def chat(body: ChatInput):
    reply = ANSWER_FN(body.message)
    return {'reply': str(reply)}
