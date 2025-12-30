from realtime_detect import detect_single_frame
from gemini_assistant import get_gemini_response

def analyze_auto():
    """
    This function MUST process exactly ONE frame and return immediately.
    Flask controls the loop, not this function.
    """

    frame, label, distance = detect_single_frame()

    if label:
        prompt = f"There is a {label} signal {distance} meters ahead. What should I do?"
        response = get_gemini_response(prompt)
    else:
        response = "No traffic light detected in the current frame."

    return frame, label, distance, response
