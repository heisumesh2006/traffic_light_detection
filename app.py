from flask import Flask, render_template, Response, jsonify
import cv2
import threading
import time

from main import analyze_auto
from realtime_detect import camera_loop

app = Flask(__name__)

# ==========================
# SHARED STATE
# ==========================
last_result = {
    "frame": None,
    "label": None,
    "distance": None,
    "response": "No traffic light detected yet."
}

# ==========================
# BACKGROUND YOLO LOOP
# ==========================
def detection_loop():
    print("🟢 Detection loop started")
    while True:
        frame, label, distance, response = analyze_auto()

        if frame is not None:
            last_result["frame"] = frame

        if label:
            last_result["label"] = label
            last_result["distance"] = distance
            last_result["response"] = response

        time.sleep(0.02)


# ==========================
# START THREADS ONCE
# ==========================
threads_started = False
lock = threading.Lock()

@app.before_request
def start_threads():
    global threads_started
    if not threads_started:
        with lock:
            if not threads_started:
                print("📷 Starting camera thread")
                threading.Thread(target=camera_loop, daemon=True).start()

                print("🚀 Starting detection thread")
                threading.Thread(target=detection_loop, daemon=True).start()

                threads_started = True


# ==========================
# ROUTES
# ==========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    def generate():
        while True:
            frame = last_result["frame"]

            if frame is None:
                time.sleep(0.05)
                continue

            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )

            time.sleep(0.03)  # ~30 FPS max

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/latest_detection")
def latest_detection():
    return jsonify({
        "detection": last_result["label"],
        "distance": last_result["distance"],
        "response": last_result["response"]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
