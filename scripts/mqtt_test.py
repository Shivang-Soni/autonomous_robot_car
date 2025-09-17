"""
MQTT Testskript für ESP32 / Roboterkommunikation
- Testet publish/subscribe auf MQTT Broker
- MLOps-tauglich: Logging, Dummy-Mode möglich
Autor: Shivang Soni
"""

import paho.mqtt.client as mqtt
import time

# ==================== KONFIGURATION ====================
BROKER = "localhost"  # MQTT Broker-Adresse, z.B. "broker.hivemq.com"
TOPIC = "test"
USE_HARDWARE = False  # True = reale Hardware, False = Dummy-Modus

# ==================== CALLBACK ====================
def on_message(client, userdata, msg):
    """
    Wird aufgerufen, wenn eine Nachricht empfangen wird
    """
    print(f"[MQTT] Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")

# ==================== MQTT CLIENT ====================
client = mqtt.Client()
client.on_message = on_message

if USE_HARDWARE:
    client.connect(BROKER, 1883)
    client.subscribe(TOPIC)
    client.loop_start()

    # Testnachricht senden
    client.publish(TOPIC, "Hallo vom Gehirn!")
    print(f"[MQTT] Nachricht gesendet an {TOPIC}")

# ==================== DUMMY / SIMULATION ====================
else:
    print("[DUMMY MODE] Keine Verbindung zum Broker, nur Testausgabe")
    print("[DUMMY MODE] Nachricht simuliert: 'Hallo vom Gehirn!'")

# ==================== SCRIPT-LAUF ====================
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("MQTT Test beendet.")
    if USE_HARDWARE:
        client.loop_stop()
