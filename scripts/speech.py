import threading
import pyttsx3
import simpleaudio as sa
import sounddevice as sd
import numpy as np
import tempfile
from faster_whisper import WhisperModel
import wavio
import logging
import time

# ===================== Thread Lock & Flag =====================
speech_lock = threading.Lock()
is_speaking = False  # globales Flag

# ==================== Text-to-Speech ====================
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", "com.apple.voice.compact.de-DE.Anna")
engine.setProperty("rate", 165)
engine.setProperty("volume", 0.9)

# ==================== Speech-to-Text ====================
model = WhisperModel("small")


def play_beep():
    wav_obj = sa.WaveObject.from_wave_file("scripts/beep.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()


def speak(text: str):
    """
    Wandelt Text in Sprache um und gibt ihn aus.
    Blockiert STT durch globales Flag.
    Sleep basierend auf Textlänge
    """
    global is_speaking
    if not text.strip():
        return
    with speech_lock:
        is_speaking = True
        engine.say(text)
        engine.runAndWait()
        # einfacher Hack: ca. 120ms pro Zeichen Nachhall
        time.sleep(len(text) * 0.12)
        is_speaking = False


def speak_threadsafe(text: str):
    """Spreche Text nur, wenn gerade keine andere TTS läuft."""
    global is_speaking
    if is_speaking or not text.strip():
        return
    speak(text)


def record_audio(duration: int = 5, fs: int = 16000):
    """
    Nimmt Audio über das Standardmikrofon auf
    Wartet, bis TTS fertig ist
    """
    global is_speaking
    # warten, bis TTS fertig ist
    while is_speaking:
        logging.info("Warte auf Ende der Sprachausgabe...")
        time.sleep(0.1)

    print("Aufnahme gestartet...")
    play_beep()
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Aufnahme beendet.")
    play_beep()
    return audio.flatten(), fs


def speech_to_text(duration: int = 5):
    """
    Wandelt gesprochene Sprache in Text um
    """
    audio, fs = record_audio(duration=duration)
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmpfile:
        wavio.write(tmpfile.name, audio, fs, sampwidth=2)
        segments, info = model.transcribe(tmpfile.name)
        result = " ".join([segment.text for segment in segments])
        return result


# ==================== Testlauf ====================
if __name__ == "__main__":
    text = speech_to_text(duration=2)
    speak("Sie haben folgendes gesagt: " + text)
