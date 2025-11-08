# autonomous_drive.py
import time
from env import RobotEnv, USE_HARDWARE
from q_learning_agent import QLearningAgent


def drive(num_episodes=500, max_steps=50):
    actions = [0, 1, 2, 3]
    agent = QLearningAgent(actions)

    # Q-Table laden
    try:
        agent.load_q_table("q_table.pkl")
        print("[INFO] Q-Table geladen")
    except:
        print("[INFO] Keine Q-Table gefunden, Training startet von Null")

    for episode in range(num_episodes):
        env = RobotEnv()
        state = env.reset()
        total_reward = 0

        # Epsilon Decay
        agent.epsilon = max(0.05, agent.epsilon * 0.995)

        for step in range(max_steps):
            action = agent.choose_action(state, actions)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state, actions)
            total_reward += reward
            state = next_state

            env.render()
            if done:
                print(f"[Episode {episode}] Hindernis erkannt, Stop")
                break

        print(f"[Episode {episode}] Total Reward: {total_reward}")

    agent.save_q_table("q_table.pkl")
    print("[INFO] Q-Table gespeichert, Training beendet")


if __name__ == "__main__":
    print("Starte autonomes Fahren auf ESP32")
    if USE_HARDWARE:
        print("Hardware-Modus aktiviert")
    else:
        print("Simulation/Dummy-Modus aktiviert")

    drive()
