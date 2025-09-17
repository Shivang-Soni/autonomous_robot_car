"""
motor_controller.py
Hardware-unabhängiger Motor Controller für ESP32 / L298N
MLops-tauglich: Dummy-Modus für Simulation ohne echte Hardware
Autor: Shivang Soni
"""

import time

# ====================== KONFIGURATION ======================
USE_HARDWARE = False  # True = echte Motoren, False = Dummy-Modus

# ====================== PIN & PWM SETUP ======================
if USE_HARDWARE:
    from machine import Pin, PWM

    ENA = PWM(Pin(25), freq=1000)  # Enable A (PWM linker Motor)
    IN1 = Pin(26, Pin.OUT)
    IN2 = Pin(27, Pin.OUT)

    ENB = PWM(Pin(14), freq=1000)  # Enable B (PWM rechter Motor)
    IN3 = Pin(12, Pin.OUT)
    IN4 = Pin(13, Pin.OUT)

# ====================== HILFSFUNKTION ======================
def set_speed(left_speed, right_speed):
    if USE_HARDWARE:
        ENA.duty(left_speed)
        ENB.duty(right_speed)
    else:
        print(f"[Dummy] set_speed -> left: {left_speed}, right: {right_speed}")

# ====================== MOTORBEFEHLE ======================
def forward(speed=800):
    if USE_HARDWARE:
        IN1.value(1); IN2.value(0)
        IN3.value(1); IN4.value(0)
        set_speed(speed, speed)
    print(f"[Dummy] forward at speed {speed}")

def backward(speed=800):
    if USE_HARDWARE:
        IN1.value(0); IN2.value(1)
        IN3.value(0); IN4.value(1)
        set_speed(speed, speed)
    print(f"[Dummy] backward at speed {speed}")

def left(speed=800):
    if USE_HARDWARE:
        IN1.value(0); IN2.value(1)
        IN3.value(1); IN4.value(0)
        set_speed(speed, speed)
    print(f"[Dummy] left at speed {speed}")

def right(speed=800):
    if USE_HARDWARE:
        IN1.value(1); IN2.value(0)
        IN3.value(0); IN4.value(1)
        set_speed(speed, speed)
    print(f"[Dummy] right at speed {speed}")

def stop():
    if USE_HARDWARE:
        IN1.value(0); IN2.value(0)
        IN3.value(0); IN4.value(0)
        set_speed(0, 0)
    print(f"[Dummy] stop motors")

# ====================== TESTLAUF ======================
if __name__ == "__main__":
    print("Testlauf der Motorbefehle (Dummy-Modus: {})".format(not USE_HARDWARE))
    forward()
    time.sleep(2)
    stop()
    time.sleep(1)
    left()
    time.sleep(2)
    stop()
