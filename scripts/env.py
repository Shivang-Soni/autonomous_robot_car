# env.py
"""
RobotEnv für Daisy – Autonomer Roboter
MLOps-tauglich & Shivang Soni
Features:
- Dummy-Modus für Simulation
- Hardware-Modus vorbereitet (Sensorwert-Einbindung)
- Reward, Distance, Done Status
"""

import random
from config import USE_HARDWARE, LOG_FILE
from memory.log import log_event

class RobotEnv:
    def __init__(self):
        self.critical_distance = 5
        self.distance = 300  # Initialwert, wird reset() überschreiben

    def reset(self):
        """
        Reset der Umgebung. Im Dummy-Modus zufällige Distanz.
        In Hardware-Modus später Sensorwert lesen.
        """
        if USE_HARDWARE:
            # TODO: Sensorwert von Ultrasonic einlesen
            self.distance = 300
        else:
            self.distance = random.randint(20, 100)
        log_event(f"Env reset: distance={self.distance}")
        return self._get_state()

    def _get_state(self):
        return self.distance

    def step(self, action):
        """
        Führt eine Aktion aus und gibt (next_state, reward, done)
        Aktionen: 0 = Stopp, 1 = Vorwärts, 2 = Links, 3 = Rechts
        """
        if action == 1:
            self.distance -= random.randint(5, 15)
        elif action in [2, 3]:
            self.distance += random.randint(0, 5)
        
        # Check für kritische Distanz
        if self.distance < self.critical_distance:
            reward = -10
            done = True
        else:
            reward = 1
            done = False

        log_event(f"Step: action={action}, distance={self.distance}, reward={reward}, done={done}")
        return self._get_state(), reward, done

    def render(self):
        print(f"Distance: {self.distance} cm")


if __name__ == "__main__":
    env = RobotEnv()
    state = env.reset()
    print(f"Initial Distance: {state} cm")
    
    for i in range(10):
        action = random.randint(0, 3)
        next_state, reward, done = env.step(action)
        env.render()
        print(f"Step {i+1}: Action={action}, Reward={reward}, Done={done}\n")
        if done:
            print("Episode beendet!")
            break
