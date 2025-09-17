# memory/robot_state.py
"""
Speichert und lädt den aktuellen Zustand des Roboters
- Position, Richtung, Batterie, letzte Aktion
- Autor: Shivang Soni
- MLOps-tauglich: JSON-basiert, einfache Persistenz
"""

import json
import os
from config import STATE_FILE  # Definiere STATE_FILE in config.py

# ====================== FUNKTIONEN ======================
def load_state() -> dict:
    """
    Lädt den Roboterzustand aus STATE_FILE.
    Wenn die Datei nicht existiert, wird ein Standardzustand zurückgegeben.
    """
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[WARN] STATE_FILE beschädigt, Standardzustand wird geladen.")
    # Standardzustand
    return {
        "position": None,
        "direction": None,
        "battery": 100,
        "last_action": None
    }

def save_state(state: dict):
    """
    Speichert den aktuellen Roboterzustand in STATE_FILE.
    """
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Zustand konnte nicht gespeichert werden: {e}")

# ====================== TESTLAUF ======================
if __name__ == "__main__":
    s = load_state()
    print("Aktueller Zustand:", s)
    # Beispiel: Zustand aktualisieren
    s["last_action"] = "forward"
    save_state(s)
    print("Zustand nach Update gespeichert.")
