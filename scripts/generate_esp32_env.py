from pathlib import Path
from dotenv import load_dotenv
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

# ===================== .env-Datei laden =====================
env_path = Path(__file__).parent / ".env"

if not env_path.exists():
    logging.error("[ERROR]Fehler: .env-Datei nicht gefunden!")
    sys.exit(1)

load_dotenv(env_path)  # Variablen ins Environment laden
logging.info(".env-Datei erfolgreich geladen!")

# =====================  Variablen auslesen =====================
required_vars = ["WIFI_SSID", "WIFI_PASSWORD", "MQTT_SERVER", "USE_HARDWARE"]

variables = {}
for var in required_vars:
    value = os.getenv(var)
    if value is None:
        logging.info(f"[WARN] {var} nicht in .env gefunden!")
    variables[var] = value or ""

# Debug-Ausgabe
logging.info("[INFO]Gefundene Werte:")
for k, v in variables.items():
    logging.info(f"  {k} = {v}")

# ===================== Ziel-Datei prüfen =====================
header_file = Path(__file__).parent.parent / "esp32" / "esp32_env.h"
header_file.parent.mkdir(exist_ok=True, parents=True)

# ===================== Header-Datei generieren =====================
with open(header_file, "w") as f:
    f.write("/* Auto-generated esp32_env.h by Shivang Soni */\n\n")
    f.write(f'const char* WIFI_SSID = "{variables["WIFI_SSID"]}";\n')
    f.write(f'const char* WIFI_PASSWORD = "{variables["WIFI_PASSWORD"]}";\n')
    f.write(f'const char* MQTT_SERVER = "{variables["MQTT_SERVER"]}";\n')

    # Python-Boolean in C++-Literal umwandeln
    use_hw = str(variables["USE_HARDWARE"]).lower() in ["true", "1", "yes"]
    f.write(f'const bool USE_HARDWARE = {"true" if use_hw else "false"};\n')

logging.info(f"\n[INFO]Header wird geschrieben nach: {header_file}")
