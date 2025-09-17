from pathlib import Path

# Pfad zur .env Datei
env_file = Path("/.env")

# Pfad zur Header-Datei im ESP32-Sketch-Ordner
header_file = Path("../esp32/esp32_env.h")

variables = {}
with open(env_file, "r") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            variables[k] = v

with open(header_file, "w") as f:
    f.write("/* Auto-generated esp32_env.h by Shivang Soni */\n\n")
    f.write(f'const char* WIFI_SSID = "{variables.get("WIFI_SSID", "")}";\n')
    f.write(f'const char* WIFI_PASSWORD = "{variables.get("WIFI_PASSWORD", "")}";\n')
    f.write(f'const char* MQTT_SERVER = "{variables.get("MQTT_SERVER", "")}";\n')
    f.write(f'const bool USE_HARDWARE = {variables.get("USE_HARDWARE", "false").lower() == "true"};\n')

print("esp32_env.h erfolgreich erstellt!")
