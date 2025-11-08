import random
import logging
import os
import numpy as np

from scripts.generate_sim_env import SimEnv
from scripts.q_learning_agent import QLearningAgent

logging.basicConfig(level=logging.INFO)


def random_start(env: SimEnv):
    """Wählt eine zufällige freie Startposition im Grid."""
    free_positions = [
        (x, y)
        for x in range(env.grid_size[0])
        for y in range(env.grid_size[1])
        if (x, y) not in env.obstacles and (x, y) != env.goal_pos
    ]
    return random.choice(free_positions)


def train(grid_size=(5, 5), random_obstacles=True, num_random_obstacles=3,
          num_episodes=1000, num_samples=50):
    
    actions = [0, 1, 2, 3]
    agent = QLearningAgent(actions)
    q_table_file = "q_table.pkl"

    # Q-Tabelle laden, falls vorhanden
    if os.path.exists(q_table_file):
        agent.load_q_table(q_table_file)
        logging.info("[INFO] Q-Tabelle geladen.")

    all_sample_rewards = []

    for sample in range(num_samples):
        env = SimEnv(
            grid_size=grid_size,
            random_obstacles=random_obstacles,
            num_random_obstacles=random.randint(0, num_random_obstacles)
        )
        logging.info(f"[SAMPLE {sample}] Neues Environment mit {env.num_random_obstacles} Hindernissen")

        sample_rewards = []

        for episode in range(num_episodes):
            state = env.reset()
            env.position = random_start(env)
            total_reward = 0

            for step in range(50):
                valid_actions = env.get_valid_actions() or actions
                action = agent.choose_action(state, valid_actions)

                if action not in valid_actions:
                    logging.warning(f"Achtung! Agent wählte ungültige Aktion: {action}")

                next_state, reward, done = env.step(action)
                valid_next_actions = env.get_valid_actions()
                agent.learn(
                    state,
                    action,
                    reward,
                    next_state,
                    valid_next_actions
                    )

                total_reward += reward
                state = next_state

                if done:
                    break

            sample_rewards.append(total_reward)

        avg_reward = np.mean(sample_rewards)
        logging.info(f"[SAMPLE {sample}] Durchschnittlicher Reward pro Episode: {avg_reward:.2f}")
        all_sample_rewards.append(avg_reward)

    # Gesamt-Performance
    overall_avg = np.mean(all_sample_rewards)
    logging.info(f"Gesamt-Durchschnitts-Reward über alle Samples: {overall_avg:.2f}")

    # Q-Tabelle speichern
    agent.save_q_table(q_table_file)
    logging.info(f"[INFO] Q-Tabelle gespeichert in {q_table_file}")


if __name__ == "__main__":
    max_grid_size = (40, 40)
    # zufällige Grid-Größe wählen
    grid_size = (random.randint(5, max_grid_size[0]), random.randint(5, max_grid_size[1]))
    # max. Hindernisse begrenzen
    num_random_obstacles = grid_size[0] * grid_size[1] // 4

    train(
        grid_size=grid_size,
        random_obstacles=True,
        num_random_obstacles=num_random_obstacles,
        num_episodes=1000,
        num_samples=100
    )
