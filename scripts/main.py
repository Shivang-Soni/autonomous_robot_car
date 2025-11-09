# main.py
"""
Hauptskript für autonome Roboterplattform 'Daisy'
--------------------------------------------------
- Q-Learning-Training mit optionalem Hardware-Support (ESP32 via MQTT)
- Simulation/Dummy-Modus möglich, wenn USE_HARDWARE = False
- Robuste Speicherung & Wiederherstellung der Q-Tabelle
- Autor: Shivang Soni
"""

import pickle
import logging
from time import sleep, time
from env import RobotEnv, USE_HARDWARE
from q_learning_agent import QLearningAgent
from memory.log import log_event
from ml_models.rag_transformer import interactive_loop
from scripts.train_sim_env import execute
from scripts.config import USE_HARDWARE, MAX_RUNNING_TIME
import paho.mqtt.client as mqtt

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# ================= MQTT SETUP =================
def on_message(client, userdata, msg):
    """Callback für eingehende MQTT-Nachrichten vom ESP32."""
    logging.info(f"[ESP32] Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)  # MQTT-Broker-Adresse
mqtt_client.subscribe("esp32/status")
mqtt_client.loop_start()

def send_command_to_motor(command: str):
    """Sende einen Steuerbefehl über MQTT an den ESP32."""
    mqtt_client.publish("esp32/motors", command)
    logging.info(f"[MQTT] COMMAND gesendet: {command}")

# ================= HAUPTPROGRAMM =================
if __name__ == "__main__":
    # ==== Q-LEARNING INITIALISIERUNG ====
    actions = [0, 1, 2, 3]  # 0=stop, 1=forward, 2=left, 3=right
    agent = QLearningAgent(actions=actions, alpha=0.1, gamma=0.9, epsilon=0.2)

    # ==== HARDWARE-LOGIK ====
    if USE_HARDWARE:
        # MQTT-Befehle als Lambda-Funktionen (vereinfachter Aufruf)
        stop = lambda: send_command_to_motor("stop")
        forward = lambda: send_command_to_motor("forward")
        left = lambda: send_command_to_motor("left")
        right = lambda: send_command_to_motor("right")

        # Reihenfolge entspricht actions = [0,1,2,3]
        commands = [stop, forward, left, right]

        save_loc = "q_table.pkl"
        num_episodes = 50

        # ==== Q-TABELLE LADEN ====
        try:
            with open(save_loc, "rb") as f:
                agent.q_table = pickle.load(f)
                logging.info("✅ Q-Tabelle erfolgreich geladen.")
        except FileNotFoundError:
            logging.warning("⚠️  Keine Q-Tabelle gefunden – starte neues Training.")

        # ==== TRAINING ====
        try:
            start_time = time()
            last_save_time = start_time
            env = RobotEnv()
            interactive_loop(False)  # Kein Blockieren während Training

            episode = 0
            total_reward = 0

            while True:
                state = env.reset()
                done = False
                episode += 1
                episode_reward = 0

                while not done:
                    # 1️⃣ Aktion wählen
                    action = agent.choose_action(state)

                    # 2️⃣ Ausführen der Aktion auf der Hardware
                    commands[action]()

                    # 3️⃣ Umgebungsschritt durchführen (Sensorwerte & Belohnung)
                    next_state, reward, done = env.step(action)

                    # 4️⃣ Q-Learning-Update
                    agent.learn(state, action, reward, next_state)

                    # 5️⃣ Zustand & Belohnung aktualisieren
                    state = next_state
                    episode_reward += reward

                    # 6️⃣ Fortschritt visualisieren
                    env.render()
                    sleep(0.2)

                total_reward += episode_reward
                logging.info(f"[EPISODE {episode}] Reward: {episode_reward:.2f}")

                # Zeitlimit prüfen
                elapsed_time = time() - start_time
                if elapsed_time >= int(MAX_RUNNING_TIME) * 60:
                    logging.info("⏱️  Maximale Laufzeit erreicht – Training wird beendet.")
                    break

                # Q-Tabelle regelmäßig speichern
                if time() - last_save_time >= 5:
                    try:
                        with open(save_loc, "wb") as f:
                            pickle.dump(agent.q_table, f)
                        logging.info(
                            f"💾 Q-Tabelle gespeichert | Laufzeit: {elapsed_time:.1f}s | "
                            f"Gesamt-Reward: {total_reward:.1f} | Episode: {episode}"
                        )
                    except Exception as e:
                        logging.warning(f"⚠️  Fehler beim Speichern der Q-Tabelle: {e}")
                    last_save_time = time()

        except KeyboardInterrupt:
            logging.info("🛑 Training manuell beendet (Ctrl+C).")

        except Exception as e:
            logging.error(f"[ERROR] Unerwarteter Fehler im Hauptloop: {e}", exc_info=True)

        finally:
            # Sicherheits-Stopp für Motoren & MQTT-Thread
            stop()
            mqtt_client.loop_stop()
            logging.info("✅ System heruntergefahren und Motor gestoppt.")

    # ==== SIMULATIONSMODUS ====
    else:
        execute()
