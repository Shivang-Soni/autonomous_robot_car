"""
QLearningAgent für autonome Robotik
- Tabelle-basierter Reinforcement Learning Agent
- MLOps-tauglich: Speichern/Laden von Q-Tables möglich
Autor: Shivang Soni
"""

import random

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.2):
        """
        actions: Liste der möglichen Aktionen
        alpha: Lernrate
        gamma: Discount-Faktor
        epsilon: Explorationsrate (epsilon-greedy)
        """
        self.q_table = {}  # Q-Tabelle: state -> action -> Q-Wert
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q(self, state, action):
        """
        Q-Wert für einen Zustand und eine Aktion abrufen
        """
        return self.q_table.get(state, {}).get(action, 0.0)

    def choose_action(self, state):
        """
        Wählt eine Aktion basierend auf epsilon-greedy
        """
        if random.random() < self.epsilon:
            # Zufällige Aktion (Exploration)
            return random.choice(self.actions)
        # Beste Aktion (Exploitation)
        q_values = [self.get_q(state, a) for a in self.actions]
        max_q = max(q_values)
        best_actions = [a for a, q in zip(self.actions, q_values) if q == max_q]
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        """
        Q-Learning Update
        """
        old_q = self.get_q(state, action)
        next_max_q = max([self.get_q(next_state, a) for a in self.actions])
        new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)

        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q

# ==================== Testlauf ====================
if __name__ == "__main__":
    actions = [0, 1, 2, 3]
    agent = QLearningAgent(actions)
    state = 10
    next_state = 8
    action = agent.choose_action(state)
    print(f"Gewählte Aktion für state {state}: {action}")
    agent.learn(state, action, reward=5, next_state=next_state)
    print(f"Q-Tabelle nach Update: {agent.q_table}")
