import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def get_gemini_response(prompt):
    try:
        prompt += " Please answer in 1-2 short sentences."  # Force brevity
        print(f"\n🧠 Prompting Gemini with: {prompt}")
        response = model.generate_content(prompt).text

        # Take only the first 1-2 sentences
        short_response = response.split(". ")[0:2]
        response = ". ".join(short_response).strip() + "."

        print("💬 Gemini says:", response)
        return response
    except Exception as e:
        print("❌ Gemini error:", repr(e))
        return "Gemini failed to respond."
