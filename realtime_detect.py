import cv2
from ultralytics import YOLO

model = YOLO("best.pt")
camera_url = "http://192.168.31.37:8080/video"
K = 2000  # Focal length constant for distance

def detect_traffic_light():
    cap = cv2.VideoCapture(camera_url)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Failed to grab frame")
        return None, None, None

    frame = cv2.resize(frame, (640, 480))
    results = model(frame)
    boxes = results[0].boxes

    for box in boxes:
        cls_id = int(box.cls[0].item())
        class_name = model.names[cls_id]
        xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
        box_width = xmax - xmin
        distance = round(K / box_width, 1) if box_width > 0 else -1
        print(f"🔍 Detected: {class_name} - {distance}m")
        return frame, class_name, distance

    print("⚠️ No traffic light detected.")
    return frame, None, None
