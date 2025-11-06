# rag_transformer.py
"""
RAG + LLaMA Integration (LangChain 1.0.3 kompatibel)
- Autor: Shivang Soni
- Funktioniert mit CTransformers oder Google Gemini 2.5 Flash
- Keine AttributeError mehr bei VectorStoreRetriever
"""
import logging
import os
import time

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import CTransformers
from langchain_core.prompts import ChatPromptTemplate
from google import genai

from scripts.load_docs import load_documents
from scripts.speech import speak, speech_to_text
from scripts.config import GOOGLE_API_KEY, USE_GEMINI, GEMINI_MODEL_NAME

# ====================== Logging Setup ======================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_cached_chain = None

# ====================== Utility ======================
def _truncate_context(text: str, max_chars: int = 2000) -> str:
    """Behalte den Anfang des Textes, wichtige Infos am Anfang"""
    if not text:
        return ""
    return text if len(text) <= max_chars else text[:max_chars]

# ====================== RAG-Chain erstellen ======================
def create_rag_chain(
    documents,
    vector_db_path="data/vector_database",
    model_path="ml_models/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q4_K_M.gguf"
):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Vector Store laden oder neu erstellen
    if os.path.exists(vector_db_path):
        logger.info("Vektordatenbank gefunden und geladen.")
        vector_db = Chroma(persist_directory=vector_db_path, embedding_function=embeddings)
    else:
        logger.info("Erstelle neue Vektordatenbank...")
        vector_db = Chroma.from_documents(documents, embeddings, persist_directory=vector_db_path)

    # ====================== LLM ======================
    if USE_GEMINI.lower() == "true" and GOOGLE_API_KEY:
        logger.info("Gemini LLM wird verwendet.")
        client = genai.Client(api_key=GOOGLE_API_KEY)

        def llm_call(context: str, query: str) -> str:
            full_prompt = (
                "Du bist Daisy, ein präziser Roboter-Assistent. "
                "Beantworte Fragen ausschließlich anhand des bereitgestellten Kontexts. "
                "Wenn keine Information vorhanden ist, sage exakt: "
                "\"Ich habe leider keine Auskünfte dazu.\"\n\n"
                f"Falls du es aus eignem Wissen beantworten kannst, tue dies präzise und knapp mit folgender Strukur: \"Ich habe leider keine Auskünfte dazu. Aber nach meiner Meinung möchte ich Ihnen etwas mitteilen: + Ihre Antwort\n\n"
                f"Kontext:\n{_truncate_context(context)}\n\n"
                f"Benutzeranfrage:\n{query}"
            )
            response = client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=[{"role": "user", "parts": [{"text": full_prompt}]}]
            )
            try:
                text = getattr(response, 'text', '') or response.candidates[0].content.parts[0].text
            except Exception:
                text = "Ich habe leider keine Auskünfte dazu."
            return text

    else:
        llm = CTransformers(
            model=model_path,
            model_type="llama",
            config={"temperature": 0.7, "max_new_tokens": 512, "context_length": 2048}
        )

        def llm_call(context: str, query: str) -> str:
            full_prompt = f"Kontext:\n{context}\n\nBenutzeranfrage:\n{query}"
            return llm.invoke(full_prompt)

    # ====================== Prompt ======================
    prompt = ChatPromptTemplate.from_template("""
Du bist Daisy, ein autonomes Roboterfahrzeug mit Sprachinteraktion.
Beantworte Fragen oder führe Steuerkommandos aus.

Benutzeranfrage: {input}

Kontext:
\"\"\"{context}\"\"\"
""")

    # ====================== Pipeline ======================
    def rag_pipeline(query: str):
        if not query:
            return ""
        docs = vector_db.similarity_search_with_score(query, k=3)
        filtered_docs = [doc for doc, score in docs if score >= 0.6]
        context = "\n".join([d.page_content for d in filtered_docs])
        logger.info(f"[INFO] Verwendeter Kontext: {context[:200]}...")
        return llm_call(context, query)

    return rag_pipeline

# ====================== Run ======================
def run(query: str):
    global _cached_chain
    if _cached_chain is None:
        logger.info("Erstelle RAG-Chain...")
        docs = load_documents("data/docs")
        for i, doc in enumerate(docs):
            logger.info(f"Doc {i}: {doc.metadata['source']} | {doc.page_content[:50]}...")
        _cached_chain = create_rag_chain(docs)
    return _cached_chain(query)

# ====================== Interaktiver Modus ======================
def interactive_loop(speech_enabled: bool = True):
    run("")  # RAG-Chain initialisieren
    time.sleep(1)
    if speech_enabled:
        speak("Hallo Shivang! Ich bin Daisy. Was möchten Sie fragen?")
        time.sleep(1)
    while True:
        try:
            query = speech_to_text() if speech_enabled else input("Was möchten Sie von mir wissen?: ")
            if query:
                logger.info("Sie haben gefragt: " + query)
                answer = run(query)
                logger.info(f"Antwort: {answer}")
                speak(answer)
                time.sleep(0.3)
        except KeyboardInterrupt:
            logger.info("Beende interaktive Schleife.")
            break
        except Exception as e:
            logger.error(f"Fehler erkannt: {e}")
            time.sleep(1)


# ====================== TESTLAUF ======================
if __name__ == "__main__":
    interactive_loop(True)  # True = Sprachmodus
