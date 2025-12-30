import os
import pyttsx3
import threading
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# TTS engine (single instance)
engine = pyttsx3.init(driverName="sapi5")
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

# Speech control
speech_lock = threading.Lock()
is_speaking = False

def _speak_blocking(text):
    global is_speaking
    with speech_lock:
        is_speaking = True
        engine.say(text)
        engine.runAndWait()
        is_speaking = False

def speak(text):
    global is_speaking
    if is_speaking:
        return  # 🔕 Ignore if already speaking

    thread = threading.Thread(
        target=_speak_blocking,
        args=(text,),
        daemon=True
    )
    thread.start()

def get_gemini_response(prompt):
    try:
        prompt += " Please answer in 1-2 short sentences."

        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )

        reply = response.text.strip()
        print("💬 Gemini:", reply)

        speak(reply)  # 🔊 SAFE speech
        return reply

    except Exception as e:
        print("❌ Gemini error:", e)
        speak("Sorry, I could not respond.")
        return "Gemini failed."
