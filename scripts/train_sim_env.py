import random
import logging
import os

from scripts.sim_env import SimEnv
from scripts.q_learning_agent import QLearningAgent

logging.basicConfig(level=logging.INFO)


def train():
    # Umgebung und Agent Initialisierung
    num_episodes = 100
    max_steps = 50
    env = SimEnv()
    actions = [0, 1, 2, 3]
    agent = QLearningAgent(actions)

    state = env.reset()
    logging.info(f"Startposition: {state}")

    q_table_file = "q_table.pkl"
    if os.path.exists(q_table_file):
        agent.load_q_table(q_table_file)
        logging.info("Q-Tabelle geladen.")

    for episode in range(num_episodes):
        state = env.reset()
        logging.info(f"[EPISODE {episode}] Startposition: {state}")

        for step in range(max_steps):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state)
            logging.info(
                f"[INFO]Step {step}: State:{state}, Action:{action}, "
                f"NextState: {next_state}, Reward: {reward}, Done: {done}"
                        )
            state = next_state
            if done:
                logging.info("Ziel erreicht!")
                break
    
        agent.save_q_table(q_table_file)
        logging.info(
            f"[INFO][EPISODE: {episode}]"
            f"Q-Tabelle gespeichert in {q_table_file}"
            )


if __name__ == "__main__":
    train()
