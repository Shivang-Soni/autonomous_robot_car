# llm_control.py
"""
LLM Controller für Daisy – Autonomer Roboter
MLOps-tauglich & Shivang Soni
- Entscheidet zwischen Fahrbefehlen und normalen Antworten
- Dummy-Modus unterstützt Hardware-unabhängiges Testen
"""

from ml_models import rag_transformer
from motors.motor_controller import forward, backward, stop, left, right
from sensors.ultrasonic_sensor import get_distance
from config import USE_HARDWARE
from memory.log import log_event

def llm_controller(query: str):
    """
    Nimmt eine Nutzeranfrage entgegen und steuert den Roboter bzw. antwortet.
    """
    # ====== Sensorwert einlesen ======
    if USE_HARDWARE:
        distance = get_distance()
    else:
        # Dummy-Wert im Simulationsmodus
        distance = 50

    # ====== Prompt für RAG LLM ======
    prompt = f"""
    Du bist ein Roboterassistent.
    Variablen: distance={distance}
    User Input: {query}

    Wenn der Benutzer ein Fahrzeugsteuerkommando gibt (vorwärts, rückwärts, links, rechts, stop), antworte mit:
    COMMAND:<Befehl>
    Wenn der Benutzer eine Frage stellt, beantworte sie normal.
    """

    # ====== RAG LLM ausführen ======
    response = rag_transformer.run(query)

    # ====== Fahrbefehle erkennen und ausführen ======
    if "COMMAND:" in response:
        cmd = response.split("COMMAND:")[1].strip().lower()
        
        # Mapping deutsch -> Funktionen
        command_map = {
            "vorwärts": forward,
            "rückwärts": backward,
            "links": left,
            "rechts": right,
            "stopp": stop
        }

        if cmd in command_map:
            if USE_HARDWARE:
                command_map[cmd]()  # echte Hardware steuern
                log_event(f"Fahrbefehl ausgeführt: {cmd}")
            else:
                # Dummy-Modus nur Logging
                log_event(f"[SIM] Fahrbefehl simuliert: {cmd}")
            print(f"Fahrbefehl verarbeitet: {cmd}")
        else:
            print(f"Unbekannter Befehl: {cmd}")
        return cmd
    else:
        # ====== Normale Antwort ======
        log_event(f"LLM-Antwort: {response}")
        print(f"LLM-Antwort: {response}")
        return response


# ====== Testlauf ======
if __name__ == "__main__":
    test_queries = [
        "Fahre vorwärts",
        "Wie ist das Wetter?",
        "Dreh nach links",
        "Stopp!"
    ]

    for q in test_queries:
        print(f"\nUser Input: {q}")
        result = llm_controller(q)
        print(f"Ergebnis: {result}")
