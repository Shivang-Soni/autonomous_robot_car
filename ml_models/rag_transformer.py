# rag_transformer.py
"""
RAG + LLaMA Integration (LangChain 1.0.3 kompatibel)
- Autor: Shivang Soni
"""
import logging
import os

from transformers import pipeline
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import CTransformers
from langchain_core.prompts import ChatPromptTemplate

from scripts.load_docs import load_documents
from scripts.speech import speak, speech_to_text

# ====================== Logging Setup ======================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_cached_chain = None


def create_rag_chain(documents,
                     vector_db_path="data/vector_database",
                     model_path="ml_models/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q4_K_M.gguf"
                     ):
    """Erstellt eine RAG-ähnliche Pipeline für LangChain 1.0.3"""
    # ====================== Embeddings ======================
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # ====================== Vector Store ======================
    if os.path.exists(vector_db_path):
        logger.info("Vektordatenbank gefunden und geladen.")
        vector_db = Chroma(persist_directory=vector_db_path, embedding_function=embeddings)
    else:
        logger.info("Erstelle neue Vektordatenbank...")
        vector_db = Chroma.from_documents(documents, embeddings, persist_directory=vector_db_path)

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # ====================== LLaMA Modell ======================
    llm = CTransformers(
        model=model_path,
        model_type="llama",
        config={
            "temperature": 0.7,
            "max_new_tokens": 512,
            "context_length": 2048,
        }
    )

    # ====================== Prompt ======================
    prompt = ChatPromptTemplate.from_template("""
    Du bist ein präziser Roboterassistent.
    Verwende ausschließlich den unten angegebenen Kontext, um zu antworten.

    Benutzeranfrage: {input}

    Kontext:
    {context}

    Regeln:
    - Bei Steuerkommandos (vorwärts, rückwärts, links, rechts, stop) antworte NUR:
      COMMAND:<Befehl>
    - Wenn keine relevanten Infos vorhanden sind:
      "Es tut mir leid, darüber habe ich keine Auskünfte."
    """)

    def rag_pipeline(query: str):
        docs = retriever.invoke(query)
        context = "\n".join([d.page_content for d in docs])
        formatted_prompt = prompt.format(context=context, input=query)
        response = llm.invoke(formatted_prompt)
        return response

    return rag_pipeline


def run(query: str):
    """Führt Anfrage aus"""
    global _cached_chain
    if _cached_chain is None:
        logger.info("Erstelle RAG-Chain...")
        docs = load_documents("data/docs")
        _cached_chain = create_rag_chain(docs)
    return _cached_chain(query)


# ====================== TESTLAUF ======================
if __name__ == "__main__":
    query = speech_to_text()
    if query:
        answer = run(query)
        speak(answer)
