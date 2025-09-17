# Daisy – Autonomer Selbstfahrendes Fahrzeug Roboter mit ESP32 & LLaMA-2 RAG Integration

Autor: Shivang Soni  
Projekt status: Hardware-Ready / MLOps-tauglich

---

## Projektübersicht

Daisy ist ein autonomer 4-Rad-Roboter, der sowohl in **Hardware** als auch in **Simulationsmodus** betrieben werden kann. Er kombiniert:

- ESP32 Mikrocontroller zur Steuerung der Motoren und Sensoren  
- L298N Motor-Treiber für 4-Wheel Chassis  
- HC-SR04 Ultraschall-Sensor für Hinderniserkennung  
- Q-Learning-Agent für autonome Navigation  
- LLaMA-2 basierte RAG-LLM für Sprachsteuerung & intelligente Antworten  
- MQTT für Kommunikation zwischen Python-Backend und ESP32

Das Projekt ist MLOps-tauglich, d.h. es lässt sich lokal testen, versionieren, loggen und auf Hardware oder Dummy-Modus umschalten.

---

## Features

1. Motorsteuerung
   - Vorwärts, Rückwärts, Links, Rechts, Stopp  
   - PWM-gesteuerte Geschwindigkeit  
   - Hardware- und Dummy-Modus verfügbar

2. Sensorik
   - Ultraschall-Abstandsmessung (HC-SR04)  
   - Sicherheitsstopp bei zu geringem Abstand (konfigurierbar über `config.py`)

3. Intelligente Sprachsteuerung
   - Spracherkennung via `faster-whisper`  
   - Sprachgenerierung via `pyttsx3`  
   - RAG-LLM beantwortet Fragen und interpretiert Fahrzeugkommandos

4. Autonome Navigation
   - Q-Learning-Agent lernt in Simulationsumgebung  
   - Autonomes Fahren in Hardware möglich

5. MLOps / Logging
   - Alle Aktionen & Zustände werden in JSON-Dateien geloggt  
   - Rewards, Q-Table & Logs persistent gespeichert

---


## Installation

1. Python-Abhängigkeiten installieren
```bash
pip install -r requirements.txt
````

2. MQTT-Broker starten

```bash
mosquitto
```

3. .env-Datei erstellen

```env
WIFI_SSID="dein-wifi"
WIFI_PASSWORD="dein-passwort"
MQTT_SERVER="broker-ip"
USE_HARDWARE=True
```

4. ESP32 Header erstellen

```bash
python scripts/generate_esp32_env.py
```

5. LLaMA-2 Modell vorbereiten

```bash
# Stelle sicher, dass die quantisierte Version im models/ Verzeichnis liegt
```

---

## Hardware Setup

* Montiere 4WD Chassis, Motoren, Räder und Ultraschallsensor
* Verdrahtung nach `motor_controller.py` (MicroPython) oder Arduino Sketch Pins
* Spannungsteiler für ECHO (HC-SR04) auf ESP32 beachten
* Akku: 7.4V Li-Ion empfohlen, GND mit ESP32 verbinden
* Teste zuerst Motoren einzeln, dann Sensor, dann MQTT, dann Integration

---

## Nutzung

1. Hardware-Modus aktivieren

```python
USE_HARDWARE = True
```

2. Simulationsmodus aktivieren

```python
USE_HARDWARE = False
```

3. Roboter starten

```bash
python main.py
```

* Sprachkommandos werden erkannt
* Q-Learning Agent kann autonom fahren
* Aktionen & Rewards werden geloggt

4. MQTT Test

```bash
python mqtt_test.py
```

---

## Logging & Debugging

* Log-Dateien: `memory/robot_log.json`
* Q-Table: `q_table.pkl`
* Rewards: `rewards.pkl`
* Sensorwerte, Fahrbefehle und LLM-Antworten können über das Terminal verfolgt werden.

---


## Lizenz & Autor

* Autor: **Shivang Soni**
* Frei für persönliche & Forschungszwecke.

