# memory/log.py
"""
Logging Modul für Shivang Soni's autonome Robotik
- Schreibt Events als JSON-Zeilen in eine Log-Datei
- Einfach integrierbar in MLOps Pipeline oder Analyse-Workflow
"""

import json
import time
from scripts.config import LOG_FILE  # Definiere LOG_FILE in scripts/config.py


# ====================== FUNKTIONEN ======================
def log_event(event: str):
    """
    Loggt ein Event mit Timestamp in die Log-Datei.
    :param event: Ereignisbeschreibung
    """
    if not event:
        return  # Leere Events werden ignoriert

    data = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event
    }
    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"[WARN] Logging fehlgeschlagen: {e}")


# ====================== TESTLAUF ======================
if __name__ == "__main__":
    log_event("Roboter gestartet")
    log_event("Erste Testnachricht")
    print(f"Events wurden in {LOG_FILE} geschrieben.")
