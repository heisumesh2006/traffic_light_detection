import cv2
import threading
import time
from ultralytics import YOLO

# =====================
# CONFIG
# =====================
MODEL_PATH = "best.pt"
CAMERA_URL = "http://192.168.31.37:8080/video"
IMG_SIZE = 416
K = 2000  # focal length constant

# =====================
# LOAD MODEL
# =====================
print("🚀 Loading YOLO model...")
model = YOLO(MODEL_PATH)
model.fuse()
print("✅ Model loaded and fused")

# =====================
# CAMERA THREAD
# =====================
latest_camera_frame = None
camera_lock = threading.Lock()

def camera_loop():
    global latest_camera_frame

    cap = cv2.VideoCapture(CAMERA_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("❌ Camera failed to open")
        return

    print("📷 Camera thread started")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        with camera_lock:
            latest_camera_frame = frame

        time.sleep(0.01)


# =====================
# 🔥 ADD THIS (STATE TRACKING)
# =====================
last_detected_label = None


# =====================
# SINGLE FRAME DETECTION
# =====================
def detect_single_frame():
    global latest_camera_frame
    global last_detected_label

    with camera_lock:
        if latest_camera_frame is None:
            return None, None, None
        frame = latest_camera_frame.copy()

    frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    results = model(frame, conf=0.4, verbose=False)

    label = None
    distance = None
    new_detection = False

    for box in results[0].boxes:
        cls_id = int(box.cls[0].item())
        current_label = model.names[cls_id]

        # 🔥 ONLY TRIGGER IF NEW OBJECT
        if current_label != last_detected_label:
            label = current_label
            new_detection = True
            last_detected_label = current_label
        else:
            label = None  # ignore repeated detection

        xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
        box_width = xmax - xmin
        distance = round(K / box_width, 1) if box_width > 0 else None

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{current_label} {distance}m",
            (xmin, ymin - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        break  # one detection per frame

    # 🔁 RESET WHEN NOTHING DETECTED
    if label is None:
        last_detected_label = None

    return frame, label, distance