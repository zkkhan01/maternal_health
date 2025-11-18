import pathway as pw
from pathway.xpacks.llm.embeddings import SentenceTransformerEmbedder

def make_index():
    # Reads text files from the maternal knowledge base and indexes them
    docs = pw.io.fs.read('app/data/maternal_knowledge_base', format='txt')
    embedder = SentenceTransformerEmbedder('sentence-transformers/all-MiniLM-L6-v2')
    index = embedder.index(docs, name='maternal_index')
    return index
