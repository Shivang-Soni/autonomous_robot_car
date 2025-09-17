"""
plot.py
- Rewards aus Q-Learning Training visualisieren
- MLOps-tauglich: einfache Integration in Training/CI
Autor: Shivang Soni
"""

import matplotlib.pyplot as plt
import pickle

def plot_rewards(file_path: str = "rewards.pkl", window_size: int = 50):
    """
    Plottet die kumulativen Rewards und deren gleitenden Durchschnitt
    file_path: Pfad zur Pickle-Datei mit Reward-Liste
    window_size: Anzahl der letzten Episoden für gleitenden Durchschnitt
    """
    # Rewards laden
    with open(file_path, "rb") as f:
        rewards = pickle.load(f)

    # Gleitender Durchschnitt berechnen
    average_reward = []
    for i in range(len(rewards)):
        start = max(0, i - window_size + 1)
        avg = sum(rewards[start:i+1]) / (i - start + 1)
        average_reward.append(avg)

    # Plot erstellen
    plt.figure(figsize=(10, 5))
    plt.plot(rewards, label="Cumulative Rewards", alpha=0.7)
    plt.plot(average_reward, label=f"Average Reward (last {window_size})", linewidth=2)
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Q-Learning Training Performance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ==================== Testlauf ====================
if __name__ == "__main__":
    plot_rewards()
