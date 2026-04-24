from realtime_detect import detect_single_frame
from gemini_assistant import get_gemini_response
import time

# 🔥 STATE CONTROL
last_spoken_label = None
last_spoken_time = 0
COOLDOWN = 5  # seconds (adjust if needed)


def analyze_auto():
    """
    Process exactly ONE frame and return immediately.
    """

    global last_spoken_label, last_spoken_time

    frame, label, distance = detect_single_frame()
    current_time = time.time()

    response = None

    if label:
        # 🔥 Only trigger if NEW or cooldown passed
        if (
            label != last_spoken_label or
            (current_time - last_spoken_time > COOLDOWN)
        ):
            prompt = f"There is a {label} signal {distance} meters ahead. What should I do?"
            response = get_gemini_response(prompt)

            last_spoken_label = label
            last_spoken_time = current_time
        else:
            # ❌ Skip repeated calls
            response = None
    else:
        # 🔁 Reset when nothing detected
        last_spoken_label = None
        response = "No traffic light detected in the current frame."

    return frame, label, distance, response