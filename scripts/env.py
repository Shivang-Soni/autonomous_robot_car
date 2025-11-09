# env.py
"""
RobotEnv für Daisy – ESP32-tauglich
"""

import random
import time
import machine
import logging
from scripts.config import USE_HARDWARE

# Logging Konfiguration
logging.basicConfig(level=logging.INFO)


class RobotEnv:
    def __init__(self):
        self.critical_distance = 10  # cm
        self.distance = 300

        if USE_HARDWARE:
            # Pins anpassen für dein Board
            self.trig = machine.Pin(5, machine.Pin.OUT)
            self.echo = machine.Pin(18, machine.Pin.IN)
            self.motor_left = machine.Pin(12, machine.Pin.OUT)
            self.motor_right = machine.Pin(13, machine.Pin.OUT)

    def read_distance(self):
        if USE_HARDWARE:
            # HC-SR04 Messung
            self.trig.value(0)
            time.sleep_us(2)
            self.trig.value(1)
            time.sleep_us(10)
            self.trig.value(0)
            
            duration = machine.time_pulse_us(self.echo, 1, 30000)  # Timeout 30ms
            distance_cm = (duration / 2) / 29.1
            self.distance = max(distance_cm, 0)
        else:
            self.distance = random.randint(20, 100)
        return self.distance

    def reset(self):
        return self.read_distance()

    def execute_action(self, action):
        # Actions: 0=Stop, 1=Forward, 2=Left, 3=Right
        if USE_HARDWARE:
            if action == 0:
                self.motor_left.value(0)
                self.motor_right.value(0)
            elif action == 1:
                self.motor_left.value(1)
                self.motor_right.value(1)
            elif action == 2:  # Links
                self.motor_left.value(0)
                self.motor_right.value(1)
            elif action == 3:  # Rechts
                self.motor_left.value(1)
                self.motor_right.value(0)
            time.sleep(0.2)
            self.motor_left.value(0)
            self.motor_right.value(0)
        else:
            # Dummy-Modus: Distance ändert sich zufällig
            if action == 1:
                self.distance -= random.randint(5, 15)
            elif action in [2, 3]:
                self.distance += random.randint(0, 5)

    def step(self, action):
        self.execute_action(action)
        dist = self.read_distance()

        if dist < self.critical_distance:
            reward = -10
            done = True
        else:
            reward = 1
            done = False

        return dist, reward, done

    def render(self):
        logging.info(f"Distance: {self.distance:.1f} cm")
