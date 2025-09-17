# load_docs.py
"""
Dokumenten-Loader für RAG-Chain
- Lädt Textdateien aus einem Ordner
- Teilt große Texte in handhabbare Chunks für Embeddings
- MLOps-tauglich, Shivang Soni
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

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

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                # Text in Chunks splitten
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,   # 500 Zeichen pro Chunk
                    chunk_overlap=50  # 50 Zeichen Überlappung
                )
                chunks = splitter.split_text(text)
                for chunk in chunks:
                    documents.append(Document(page_content=chunk))

    print(f"{len(documents)} Textblöcke aus {folder_path} geladen.")
    return documents

# ====== Testlauf ======
if __name__ == "__main__":
    folder = "../data/docs"  # Beispielpfad
    docs = load_documents(folder)
    if docs:
        print("Dokumente wurden erfolgreich geladen!")
    else:
        print("Keine Dokumente geladen.")
