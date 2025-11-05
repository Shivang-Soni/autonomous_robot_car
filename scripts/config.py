# config.py
"""
Zentrale Konfiguration für Roboterprojekt
Autor: Shivang Soni
"""
import os
from dotenv import load_dotenv


# Lade Umgebungsvariablen aus .env Datei
load_dotenv()


# ====================== Allgemein ======================
ROBOT_NAME = "Daisy"  # Name des Roboters

# ====================== Hindernis & Sicherheit ======================
MIN_DISTANCE_CM = 20  # Mindestabstand zum Hindernis in cm

# ====================== Logging & State ======================
LOG_FILE = "memory/robot_log.json"   # JSON-Log für Events
STATE_FILE = "memory/state.json"     # JSON-Datei für Robot-Zustand

# ====================== Hardware / Dummy ======================
USE_HARDWARE = False  # True = echte Motoren/Sensoren, False = Dummy-Modus

# ======================= Gemini API =======================
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # Google Gemini API-Schlüssel
USE_GEMINI = os.getenv("USE_GEMINI", "True")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")