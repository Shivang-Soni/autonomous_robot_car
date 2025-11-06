Frage: Was ist Daisy?  
Antwort: Daisy ist ein autonomer 4-Rad-Roboter, der sowohl in Hardware als auch in Simulationsmodus betrieben werden kann, kombiniert ESP32, L298N Motor-Treiber, HC-SR04 Sensor, Q-Learning Agent und LLaMA-2 basierte RAG-LLM.

Frage: Welche Motorsteuerungen unterstützt Daisy?  
Antwort: Vorwärts, Rückwärts, Links, Rechts, Stopp. PWM-gesteuerte Geschwindigkeit, Hardware- und Dummy-Modus verfügbar.

Frage: Welche Sensorik hat Daisy?  
Antwort: Ultraschall-Abstandsmessung (HC-SR04), Sicherheitsstopp bei zu geringem Abstand konfigurierbar über config.py.

Frage: Wie funktioniert die Sprachsteuerung?  
Antwort: Spracherkennung via faster-whisper, Sprachgenerierung via pyttsx3, RAG-LLM beantwortet Fragen und interpretiert Fahrzeugkommandos.

Frage: Wie funktioniert die autonome Navigation?  
Antwort: Q-Learning-Agent lernt in Simulationsumgebung, autonomes Fahren in Hardware möglich.

Frage: Wie werden Logs und Rewards gespeichert?  
Antwort: Aktionen & Zustände werden in JSON-Dateien geloggt, Rewards, Q-Table & Logs werden persistent gespeichert.

Frage: Wie installiere ich Daisy?  
Antwort: Python-Abhängigkeiten mit `pip install -r requirements.txt`, MQTT-Broker starten, .env-Datei erstellen, ESP32 Header generieren, quantisiertes LLaMA-2 Modell vorbereiten.

Frage: Wie richte ich die Hardware ein?  
Antwort: 4WD Chassis, Motoren, Räder und Ultraschallsensor montieren, Pins laut motor_controller.py verbinden, Spannungsteiler für ECHO beachten, Akku 7.4V Li-Ion, Test Motoren → Sensor → MQTT → Integration.

Frage: Wie starte ich den Roboter?  
Antwort: Hardware-Modus aktivieren mit `USE_HARDWARE=True`, Simulationsmodus mit `USE_HARDWARE=False`, Roboter starten mit `python main.py`, Sprachkommandos werden erkannt, Q-Learning Agent kann autonom fahren.

Frage: Wie teste ich MQTT?  
Antwort: `python mqtt_test.py`.

Frage: Wo finde Logs und Debug-Informationen?  
Antwort: Log-Dateien in `memory/robot_log.json`, Q-Table in `q_table.pkl`, Rewards in `rewards.pkl`. Sensorwerte, Fahrbefehle und LLM-Antworten im Terminal.

Frage: Wer ist der Autor und welche Lizenz gilt?  
Antwort: Autor: Shivang Soni, frei für persönliche & Forschungszwecke.
