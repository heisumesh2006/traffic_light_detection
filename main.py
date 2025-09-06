from realtime_detect import detect_traffic_light
from gemini_assistant import get_gemini_response

def analyze_auto():
    frame, label, distance = detect_traffic_light()
    if label:
        prompt = f"There is a {label} signal {distance} meters ahead. What should I do?"
        response = get_gemini_response(prompt)
    else:
        response = "No traffic light detected in the current frame."

    return frame, label, distance, response
