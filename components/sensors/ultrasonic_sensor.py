"""
ultrasonic_sensor.py
Hardware-unabhängiger Ultraschall-Sensor (HC-SR04) für ESP32
Dummy-Modus für Simulation ohne Sensoren
Autor: Shivang Soni
"""

import time
import random  # Für Dummy-Daten

# ====================== KONFIGURATION ======================
USE_HARDWARE = False  # True = echte Sensoren, False = Dummy-Modus

if USE_HARDWARE:
    from machine import Pin, time_pulse_us

    # Pins anpassen je nach Verkabelung
    TRIGGER_PIN = 5
    ECHO_PIN = 18

    trigger = Pin(TRIGGER_PIN, Pin.OUT)
    echo = Pin(ECHO_PIN, Pin.IN)

# ====================== ABSTANDSMESSUNG ======================
def get_distance():
    """
    Misst den Abstand in cm mit HC-SR04 oder liefert Dummy-Wert.
    """
    if USE_HARDWARE:
        # Sensor initialisieren
        trigger.value(0)
        time.sleep_us(2)
        trigger.value(1)
        time.sleep_us(10)
        trigger.value(0)

        duration = time_pulse_us(echo, 1, 30000)  # Timeout 30ms
        if duration < 0:
            return None  # Kein Echo empfangen

        distance_cm = (duration / 2) / 29.1
        return round(distance_cm, 1)
    else:
        # Dummy: zufälliger Abstand zwischen 5 und 100 cm
        distance_cm = random.uniform(5, 100)
        print(f"[Dummy] get_distance -> {distance_cm:.1f} cm")
        return round(distance_cm, 1)

# ====================== TESTLAUF ======================
if __name__ == "__main__":
    print("Testlauf Ultraschall-Sensor (Dummy-Modus: {})".format(not USE_HARDWARE))
    for _ in range(10):
        d = get_distance()
        time.sleep(0.5)
