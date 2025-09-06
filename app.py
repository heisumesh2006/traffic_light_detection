from flask import Flask, render_template, Response, jsonify
import cv2
from main import analyze_auto

app = Flask(__name__)

# Shared memory
last_result = {
    "frame": None,
    "label": None,
    "distance": None,
    "response": "No traffic light detected yet."
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    def generate():
        global last_result
        while True:
            frame, label, distance, response = analyze_auto()

            if frame is None:
                continue

            if label:
                last_result = {
                    "frame": frame,
                    "label": label,
                    "distance": distance,
                    "response": response
                }

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/latest_detection')
def latest_detection():
    return jsonify({
        "detection": last_result["label"],
        "distance": last_result["distance"],
        "response": last_result["response"]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
