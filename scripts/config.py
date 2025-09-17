# config.py
"""
Zentrale Konfiguration für Roboterprojekt
Autor: Shivang Soni
"""

# ====================== Allgemein ======================
ROBOT_NAME = "Daisy"  # Name des Roboters

# ====================== Hindernis & Sicherheit ======================
MIN_DISTANCE_CM = 20  # Mindestabstand zum Hindernis in cm

# ====================== Logging & State ======================
LOG_FILE = "memory/robot_log.json"   # JSON-Log für Events
STATE_FILE = "memory/state.json"     # JSON-Datei für Robot-Zustand

# ====================== Hardware / Dummy ======================
USE_HARDWARE = False  # True = echte Motoren/Sensoren, False = Dummy-Modus (Simulation)
