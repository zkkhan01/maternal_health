import pathway as pw
from pathway.xpacks.llm.llms import BDH

model = BDH()

@pw.udf
def make_prompt(question, context):
    return f"""You are an assistant specialized in maternal health. Use the provided context and live data to answer accurately.

Context:
{context}

Question: {question}
"""

def build_pipeline(index):
    def answer(q):
        ctx = index.search(q, k=5)
        prompt = make_prompt(q, ctx)
        resp = model.generate(prompt)
        return resp
    return answer
