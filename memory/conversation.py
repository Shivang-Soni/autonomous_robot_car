# memory/conversation.py
"""
Conversation Memory Modul für Shivang Soni's autonome Robotik
- Nutzt LangChain ConversationBufferMemory
- Speichert Nachrichten zwischen User & AI
- Hardware-unabhängig, kann im MLOps Workflow integriert werden
"""

from langchain.memory import ConversationBufferMemory

# ====================== INITIALISIERUNG ======================
memory = ConversationBufferMemory(
    memory_key="conversation_history",  # Speicherort für die Unterhaltung
    return_messages=True                # Gibt Nachrichten als Liste zurück
)

# ====================== FUNKTIONEN ======================
def add_message(role: str, content: str):
    """
    Fügt eine Nachricht der Konversation hinzu.
    :param role: "user" oder "ai"
    :param content: Nachrichtentext
    """
    memory.chat_memory.add_message({"role": role, "content": content})

def get_memory():
    """
    Gibt die bisher gespeicherte Unterhaltung zurück.
    :return: Dictionary mit dem Schlüssel "conversation_history"
    """
    return memory.load_memory_variables({})

# ====================== TESTLAUF ======================
if __name__ == "__main__":
    add_message("user", "Hallo Roboter")
    add_message("ai", "Hallo! Ich bin Daisy")
    print(get_memory())
