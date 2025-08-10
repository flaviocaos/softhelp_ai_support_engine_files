import os
from typing import Tuple, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
KB_DIR = os.path.join(os.path.dirname(__file__), 'kb')
DB_DIR = os.path.join(os.path.dirname(__file__), 'db')
EMBED_MODEL = os.getenv('EMBED_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
def _load_docs():
    docs = []
    for fn in os.listdir(KB_DIR):
        path = os.path.join(KB_DIR, fn)
        if fn.lower().endswith('.pdf'):
            docs += PyPDFLoader(path).load()
        elif fn.lower().endswith('.txt'):
            docs += TextLoader(path, encoding='utf-8').load()
    return docs
def build_or_load() -> Chroma:
    os.makedirs(DB_DIR, exist_ok=True)
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    if os.listdir(DB_DIR):
        return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(_load_docs())
    db = Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)
    db.persist()
    return db
def search(query: str, k: int = 4) -> Tuple[str, List[str]]:
    db = build_or_load()
    results = db.similarity_search(query, k=k)
    context = "\n\n".join([r.page_content for r in results])
    sources = list({ os.path.basename(r.metadata.get('source','')) for r in results })
    return context, sources
