# main.py
"""
Hauptskript für autonome Roboterplattform
- MLOps-tauglich: Logging, State Management, Testmodus ohne Hardware
- Hardware-ready: ESP32, Motoren, Sensorik via MQTT
- Autor: Shivang Soni
"""

from load_docs import load_documents
import pickle
from ml_models import create_rag_chain, load_llama
from speech import speech_to_text, speak
from autonomous_drive import autonomous_drive_'
from llm_control import llm_controller
from memory.conversation import add_message
from memory.log import log_event
from q_learning_agent import QLearningAgent
from env import RobotEnv

import paho.mqtt.client as mqtt

# ================= MQTT SETUP =================
def on_message(client, userdata, msg):
    print(f"[ESP32] Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)  # MQTT Broker-Adresse anpassen
client.subscribe("esp32/status")
client.loop_start()

def send_command_to_motor(command):
    """
    Sendet Fahrbefehle an ESP32 via MQTT
    """
    client.publish("esp32/motors", command)
    print(f"[MQTT] COMMAND: {command} an den Fahrzeug-Roboter geschickt!")

# ================= HARDWARE/MODE =================
USE_HARDWARE = True  # True = echte Hardware, False = Dummy-Modus

# ================= Q-LEARNING AGENT =================
actions = [0, 1, 2, 3]  # 0=stop,1=forward,2=left,3=right
agent = QLearningAgent(actions=actions, alpha=0.1, gamma=0.9, epsilon=0.2)

# ================= RAG & LLM =================
file = "data/docs"
docs = load_documents(file)
retriever, rag_chain = create_rag_chain(docs)
model, tokenizer = load_llama()

# ================= HARDWARE-FUNKTIONEN =================
if USE_HARDWARE:
    from sensors.ultrasonic_sensor import get_distance

    # Motorfunktionen umleiten auf MQTT
    forward = lambda: send_command_to_motor("forward")
    backward = lambda: send_command_to_motor("backward")
    right = lambda: send_command_to_motor("right")
    left = lambda: send_command_to_motor("left")
    stop = lambda: send_command_to_motor("stop")
else:
    # Dummy/Simulation: Q-Learning testen ohne Hardware
    save_loc = "q_table.pkl"
    num_episodes = 50
    cum_rewards = []

    with open(save_loc, "rb") as f:
        agent.q_table = pickle.load(f)

    for _ in range(num_episodes):
        env = RobotEnv()
        state = env.reset()
        done = False
        reward_sum = 0
        step_count = 0
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            reward_sum += reward
            agent.learn(state, action, reward, next_state)
            state = next_state
            step_count += 1
        cum_rewards.append(reward_sum)
        print(f"Episode beendet nach {step_count} Schritten, Reward={reward_sum}")

    # Ergebnisse speichern
    with open(save_loc, "wb") as f:
        pickle.dump(agent.q_table, f)
    with open("rewards.pkl", "wb") as f:
        pickle.dump(cum_rewards, f)

# ================= HAUPT-LOOP =================
try:
    while True:
        query = speech_to_text(duration=5)
        if query.lower() in ["exit", "quit", "stop"]:
            print("Beende Programm...")
            break

        # LLM Controller
        res = llm_controller(query)
        add_message(query, res)
        print("Antwort:", res)

        # TTS nur, wenn keine COMMAND-Antwort
        if "COMMAND:" not in res:
            speak(res)
        else:
            log_event(res)

        # Autonomes Fahren
        if USE_HARDWARE:
            autonomous_drive(agent, get_distance, forward, left, right, stop)

except KeyboardInterrupt:
    print("Programm wurde frühzeitig beendet.")
