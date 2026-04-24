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

        engine.stop()  

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

        error_message = str(e)

        # 🔧 Smart fallback handling
        if "503" in error_message or "UNAVAILABLE" in error_message:
            fallback = "AI analysis temporarily unavailable due to high demand."
            print("⚠️", fallback)
            speak("AI analysis is temporarily unavailable. Please wait.")
            return fallback

        elif "API_KEY" in error_message or "expired" in error_message:
            fallback = "AI service unavailable due to API key issue."
            print("⚠️", fallback)
            speak("API key error. Please check configuration.")
            return fallback

        else:
            fallback = "AI analysis failed due to an unexpected error."
            print("⚠️", fallback)
            speak("There was an internal error.")
            return fallback