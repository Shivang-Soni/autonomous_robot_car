# load_docs.py
"""
Dokumenten-Loader für RAG-Chain
- Lädt Textdateien aus einem Ordner
- Teilt große Texte in handhabbare Chunks für Embeddings
- MLOps-tauglich, Shivang Soni
"""
import os
import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)


def load_documents(folder_path: str):
    """
    Lädt alle .txt-Dateien aus einem Ordner und splittet sie in kleine Chunks.
    
    Args:
        folder_path (str): Pfad zum Dokumentenordner.

    Returns:
        List[Document]: Liste von LangChain Document Objekten.
    """
    documents = []

    if not os.path.exists(folder_path):
        print(f"[WARN] Ordner nicht gefunden: {folder_path}")
        return documents

    # Text in Chunks splitten
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,   # 500 Zeichen pro Chunk
            chunk_overlap=50  # 50 Zeichen Überlappung
            )

    for filename in os.listdir(folder_path):
        try:
            if filename.endswith(".md") or filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                    chunks = splitter.split_text(text)
                    for chunk in chunks:
                        documents.append(Document(page_content=chunk, metadata={"source": filename}))
        except Exception as e:
            logging.error(
                f"Fehler ist beim Laden der Datei {filename} aufgetreten: {e}"
                )

    logging.info(f"{len(documents)} Textblöcke aus {folder_path} geladen.")
    return documents


# ====== Testlauf ======
if __name__ == "__main__":
    folder = "data/docs"  # Pfad zum Dokumentenordner
    docs = load_documents(folder)
    if docs:
        logging.info("Dokumente wurden erfolgreich geladen!")
        logging.info(f"Erste 2 Dokumente: {docs[:2]}")
    else:
        logging.warning("[WARN] Keine Dokumente geladen.")
