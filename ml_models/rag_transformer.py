# rag_transformer.py
"""
RAG + LLaMA/Gemini Integration mit Daisy
- Kein Threading, keine Locks, keine Flags
- STT & TTS laufen sequenziell
- Autor: Shivang Soni
"""
import logging
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import CTransformers
from google import genai

from scripts.load_docs import load_documents
from scripts.speech import speak, speech_to_text
from scripts.config import GOOGLE_API_KEY, USE_GEMINI, GEMINI_MODEL_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
_cached_chain = None


def _truncate_context(text: str, max_chars: int = 2000) -> str:
    return text[:max_chars] if text else ""


def create_rag_chain(
    documents,
    vector_db_path="data/vector_database",
    model_path="ml_models/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q4_K_M.gguf",
):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(vector_db_path):
        logger.info("Vektordatenbank gefunden und geladen.")
        vector_db = Chroma(
            persist_directory=vector_db_path, embedding_function=embeddings
        )
    else:
        logger.info("Erstelle neue Vektordatenbank...")
        vector_db = Chroma.from_documents(
            documents, embeddings, persist_directory=vector_db_path
        )

    if USE_GEMINI.lower() == "true" and GOOGLE_API_KEY:
        logger.info("Gemini LLM wird verwendet.")
        client = genai.Client(api_key=GOOGLE_API_KEY)

        def llm_call(context: str, query: str) -> str:
            prompt = (
                "Du bist Daisy, ein Roboter-Assistent. "
                "Antworte nur anhand des Kontextes. "
                "Wenn keine Info vorhanden ist oder du jedoch aus eigenem Wissen beantworten kannst, "
                "dann sage: \"Ich habe leider keine Auskünfte dazu. "
                "Aber nach meiner Meinung möchte ich Ihnen etwas mitteilen: [kurze, präzise Antwort]\"\n\n"
                "Leere Antworten sind nicht erlaubt.\n\n"
                f"Kontext:\n{_truncate_context(context)}\n\n"
                f"Benutzeranfrage:\n{query}"
            )
            resp = client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
            )
            res = getattr(resp, "text", "") or resp.candidates[0].content.parts[0].text
            return res or "Ich habe leider keine Auskünfte dazu."

    else:
        llm = CTransformers(
            model=model_path,
            model_type="llama",
            config={"temperature": 0.7, "max_new_tokens": 512, "context_length": 2048},
        )

        def llm_call(context: str, query: str) -> str:
            full_prompt = f"Kontext:\n{context}\n\nBenutzeranfrage:\n{query}"
            return llm.invoke(full_prompt)

    def rag_pipeline(query: str):
        if not query:
            return ""
        docs = vector_db.similarity_search_with_score(query, k=3)
        filtered_docs = [d for d, s in docs if s >= 0.6]
        context = "\n".join([d.page_content for d in filtered_docs])
        logger.info(f"[INFO] Verwendeter Kontext: {context[:200]}...")
        return llm_call(context, query)

    return rag_pipeline


def run(query: str):
    global _cached_chain
    if _cached_chain is None:
        logger.info("Erstelle RAG-Chain...")
        docs = load_documents("data/docs")
        for i, doc in enumerate(docs):
            logger.info(f"Doc {i}: {doc.metadata['source']} | {doc.page_content[:50]}...")
        _cached_chain = create_rag_chain(docs)
    return _cached_chain(query)


def interactive_loop(speech_enabled: bool = True):
    run("")  # RAG-Chain initialisieren

    if speech_enabled:
        speak("Hallo Shivang! Ich bin Daisy. Was möchten Sie fragen?")

    while True:
        try:
            # STT starten
            if speech_enabled:
                query = speech_to_text(duration=5)
                if not query or query.strip() == "":
                    continue
            else:
                query = input("Was möchten Sie wissen?: ")

            logger.info(f"Sie haben gefragt: {query}")
            answer = run(query)
            logger.info(f"Antwort: {answer}")

            # TTS starten
            if speech_enabled:
                speak(answer)

        except KeyboardInterrupt:
            logger.info("Beende interaktive Schleife.")
            break
        except Exception as e:
            logger.error(f"Fehler: {e}")
            import time
            time.sleep(1)


if __name__ == "__main__":
    interactive_loop(True)
