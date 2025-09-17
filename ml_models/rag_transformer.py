# rag_transformer.py
"""
RAG + LLaMA Integration
- Autor: Shivang Soni
- Hardware-unabhängig testbar
- MLOps-tauglich: persistente Vektordatenbank, HuggingFace Embeddings, LangChain Pipeline
"""

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import retrieval_qa
from langchain.llms import huggingface_pipeline
from transformers import pipeline
from load_docs import load_documents
from speech import speak, speech_to_text

def create_rag_chain(documents, vector_db_path: str = "../data/vector_database", model_path: str = "./models/llama-2-7b-4bit"):
    """
    Erstellt RAG-Chain:
    - documents: Liste von Text-Dokumenten
    - vector_db_path: Speicherort Vektor-Datenbank
    - model_path: Pfad zum quantisierten LLaMA Modell
    Rückgabe: (retriever, rag_chain)
    """
    # ====================== Embeddings ======================
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # ====================== Vektor-Datenbank ======================
    vector_db = Chroma.from_documents(documents, embeddings, persist_directory=vector_db_path)
    retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # ====================== LLaMA Pipeline ======================
    llm_pipeline = pipeline(
        task="text-generation",
        model=model_path,
        tokenizer=model_path,
        device="mps",          # macOS GPU/CPU automatisch
        max_length=1024,
        do_sample=True,
        temperature=0.7
    )
    llm = huggingface_pipeline(pipeline=llm_pipeline)

    # ====================== RAG-Chain ======================
    rag_chain = retrieval_qa.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return retriever, rag_chain

# ====================== TESTLAUF ======================
if __name__ == "__main__":
    file_to_load = "../data/docs/docs1.txt"
    docs = load_documents(file_to_load)

    retriever, rag_chain = create_rag_chain(docs)
    print("RAG-Chain erfolgreich erstellt!")

    # Sprachbefehl -> RAG -> TTS
    query = speech_to_text()      # Aufnahme via Mikrofon
    if query:
        res = rag_chain.run(query)
        speak(res)
