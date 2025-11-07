"""
QLearningAgent für autonome Robotik
- Tabelle-basierter Reinforcement Learning Agent
- MLOps-tauglich: Speichern/Laden von Q-Tables möglich
Autor: Shivang Soni
"""
from __future__ import annotations

import json
import os
import pickle
import tempfile
from typing import Any, Dict, List, Iterable
import random
import logging

logging.basicConfig(level=logging.INFO)


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
    
    def _serialise_state(self, state: Any) -> str:
        """
        Wandelt jeden Zustand in eine hashbar, JSON kompatible Zeichenkette um
        """
        try:
            return json.dumps(state, sort_keys=True)
        except TypeError:
            return str(state)

    def get_q(self, state, action):
        """
        Q-Wert für einen Zustand und eine Aktion abrufen
        """
        key = self._serialise_state(state)
        return self.q_table.get(key, {}).get(action, 0.0)

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
        state_key = self._serialise_state(state)
        next_state_key = self._serialise_state(next_state)

        old_q = self.get_q(state, action)
        next_max_q = max([self.get_q(next_state, a) for a in self.actions])
        new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)

        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        self.q_table[state_key][action] = new_q

    def save_q_table(self, filepath: str):
        """
        Speichert die Q-Tabelle in einer Datei
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self.q_table, f)
            logging.info(
                f"[INFO] Q-Tabelle gespeichert in directory: {filepath}"
                )
    
    def load_q_table(self, filepath: str):
        """
        Lädt die Q-Tabelle aus einer Datei
        """
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.q_table = pickle.load(f)
                logging.info(
                    f"[INFO] Q-Tabelle geladen aus directory: {filepath}"
                )
        else:
            logging.warning(
                f"[WARN] Datei nicht gefunden: {filepath}."
                f" Q-Tabelle nicht geladen."
            )


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
