# autonomous_drive.py
"""
Autonomes Fahrmodul
- Autor: Shivang Soni
- Unterstützt: 
    - Simulation (Dummy-Modus, ohne Hardware)
    - Echte Hardware (ESP32 + Motoren + Sensorik über MQTT)
- Integration mit Q-Learning Agent und Sensorik
"""

import time
import random
from sensors.ultrasonic_sensor import get_distance
from motors.motor_controller import forward, backward, left, right, stop

# ====================== CONFIG ======================
USE_HARDWARE = False  # True = echte Motoren, False = Dummy-Modus (Simulation)
SAFE_DISTANCE = 15    # Mindestabstand in cm für Hindernisvermeidung

def autonomous_drive_step(sensor_reading=None, action=None):
    """
    Führt einen Fahrbefehl aus:
    - sensor_reading: optionaler Abstandswert (cm), sonst aus Sensor ermittelt
    - action: optional, "forward"/"backward"/"left"/"right"/"stop"
    Rückgabe: ausgeführte Aktion
    """
    if USE_HARDWARE:
        # ====================== Sensor lesen ======================
        if sensor_reading is None:
            distance = get_distance()
        else:
            distance = sensor_reading
    else:
        # Dummy-Modus: zufällige Hindernisse simulieren
        distance = random.randint(5, 50)

    # ====================== Hindernisprüfung ======================
    if distance is None:
        print("Sensorfehler: stoppe Roboter")
        if USE_HARDWARE: stop()
        return "stop"

    if distance < SAFE_DISTANCE:
        print(f"Hindernis erkannt ({distance}cm) → Rückwärts / Stopp")
        if USE_HARDWARE:
            stop()
        return "stop"

    # ====================== Aktion ausführen ======================
    if action is None:
        # Zufällige Aktion im Dummy-Testmodus
        action = random.choice(["forward", "left", "right"])

    print(f"Fahre: {action} | Abstand: {distance}cm")

    if USE_HARDWARE:
        if action == "forward":
            forward()
        elif action == "backward":
            backward()
        elif action == "left":
            left()
        elif action == "right":
            right()
        else:
            stop()

    return action

# ====================== TESTLAUF ======================
if __name__ == "__main__":
    print("Autonomous Drive Testlauf gestartet (Dummy-Modus)")
    for _ in range(10):
        a = autonomous_drive_step()
        print(f"Ausgeführte Aktion: {a}")
        time.sleep(1)
