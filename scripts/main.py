# main.py
"""
Hauptskript für autonome Roboterplattform
- Hardware-ready: ESP32, Motoren, Sensorik via MQTT
- Simulation/Dummy-Modus für Q-Learning-Tests
- Autor: Shivang Soni
"""

import pickle
import logging
from time import sleep, time
from env import RobotEnv
from q_learning_agent import QLearningAgent
from memory.conversation import add_message
from memory.log import log_event

from ml_models.rag_transformer import interactive_loop
from scripts.train_sim_env import execute
from scripts.config import USE_HARDWARE, MAX_RUNNING_TIME
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO)

# ================= MQTT SETUP =================
def on_message(client, userdata, msg):
    logging.info(f"[ESP32] Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)  # Broker-Adresse
mqtt_client.subscribe("esp32/status")
mqtt_client.loop_start()

def send_command_to_motor(command: str):
    mqtt_client.publish("esp32/motors", command)
    logging.info(f"[MQTT] COMMAND gesendet: {command}")

if __name__ == "__main__":
    # ================= Q-LEARNING AGENT =================
    actions = [0, 1, 2, 3]  # 0=stop, 1=forward, 2=left, 3=right
    agent = QLearningAgent(actions=actions, alpha=0.1, gamma=0.9, epsilon=0.2)

    # ================= HARDWARE-FUNKTIONEN =================
    if USE_HARDWARE:

        # Motorfunktionen auf MQTT
        forward = lambda: send_command_to_motor("forward")
        backward = lambda: send_command_to_motor("backward")
        right = lambda: send_command_to_motor("right")
        left = lambda: send_command_to_motor("left")
        stop = lambda: send_command_to_motor("stop")
        commands = [forward, backward, left, right, stop]
        save_loc = "q_table.pkl"
        num_episodes = 50
        try:
            with open(save_loc, "rb") as f:
                agent.q_table = pickle.load(f)
                logging.info("Q-Tabelle geladen")
        except FileNotFoundError:
            logging.warning("Keine Q-Tabelle gefunden, starte neu")

        # ================= HAUPT-LOOP =================
        try:
            start_time = time()  # hier time
            last_save_time = start_time
            episode = 0
            env = RobotEnv()
            interactive_loop(True)
            done = False
            total_reward = 0
            while not done:
                state = env.reset()
                # Handlung auswählen
                action = agent.choose_action(state)
                # Handlung ausführen -> Zustand und Belohnung erhalten
                commands[action]()
                next_state, reward, done = env.step(action)
                agent.learn(state, action, reward, next_state)
                # Zustand aktualisieren
                state = next_state
                total_reward += reward
                episode += 1
                if (episode % 100 == 0):
                    env.render()

                elapsed_time = time()-start_time
                # Wenn die Laufzeit die festgelegte Grenze überschreitet
                if (elapsed_time >= int(MAX_RUNNING_TIME)*60):
                    logging.info(
                        "[INFO] Maximale Grenze eines Laufs erreicht"
                        "...wird beendet"
                        )
                    done = True
                    break
                # Alle 5 Sekunden die Q Tabelle speichern und reward loggen
                if (time() - last_save_time >= 5):
                    # Protokolliere und speichere Nachricht
                    message = (
                        f"[INFO] Time elapsed: {elapsed_time}"
                        f" | Total_reward: {total_reward}"
                        f" | Episode: {episode}"
                        )
                    logging.info(message)
                    log_event(message)
                    with open(save_loc, "wb") as f:
                        try:
                            pickle.dump(agent.q_table, f)
                        except Exception as e:
                            logging.warning(
                                f"[WARN] Q-Tabelle konnte"
                                f" nicht gespeichert werden: {e}"
                                )
                    
                    last_save_time = time()

        except KeyboardInterrupt:
            logging.info(
                "[INFO] Beendet vom Administrator durch den Befehl: Ctrl+C"
                )

        except Exception as e:
            logging.error(f"[ERROR] Fehler im Hauptloop: {e}", exc_info=True)
        finally:
            commands[-1]()
            mqtt_client.loop_stop()
    else:
        execute()
