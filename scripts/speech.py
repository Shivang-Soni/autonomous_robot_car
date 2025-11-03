"""
speech.py
- Text-to-Speech (TTS) & Speech-to-Text (STT) Modul für den Roboter
- MLOps-tauglich: Hardware-unabhängig testbar
Autor: Shivang Soni
"""

import pyttsx3
import sounddevice as sd
import numpy as np
import tempfile
from faster_whisper import WhisperModel
import wavio

# ==================== Text-to-Speech ====================
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Stimme wird festgelegt
engine.setProperty('voice', 'com.apple.voice.compact.de-DE.Anna')
engine.setProperty('rate', 165)
engine.setProperty('volume', 0.9)

def speak(text: str):
    """
    Wandelt Text in Sprache um und gibt ihn über Lautsprecher aus
    """
    if not text:
        return
    engine.say(text)
    engine.runAndWait()

# ==================== Speech-to-Text ====================
# Whisper STT Modell laden
model = WhisperModel("small")  # Alternativ "medium", "large" je nach Hardware

def record_audio(duration: int = 5, fs: int = 16000):
    """
    Nimmt Audio über das Standardmikrofon auf
    duration: Dauer in Sekunden
    fs: Sampling-Rate
    """
    print("Aufnahme gestartet...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Aufnahme beendet.")
    return audio.flatten(), fs

def speech_to_text(duration: int = 5):
    """
    Wandelt gesprochene Sprache in Text um
    """
    audio, fs = record_audio(duration=duration)
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmpfile:
        # Temporäre WAV-Datei schreiben
        wavio.write(tmpfile.name, audio, fs, sampwidth=2)
        segments, info = model.transcribe(tmpfile.name)
        # Alle Segmente zusammenfügen
        result = " ".join([segment.text for segment in segments])
        return result

# ==================== Testlauf ====================
if __name__ == "__main__":
    #speak("Hallo, ich bin Daisy, dein Roboterassistent.")
    text = speech_to_text(duration=2)
    speak("Sie haben folgendes gesagt: "+text)
