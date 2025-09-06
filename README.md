Traffic Light Detection & Voice Assistant for Self-Driving Cars
Overview

This project implements a real-time traffic light detection system for self-driving cars using YOLOv8 and a Gemini AI voice assistant.

The system can:

Detect red, yellow, and green traffic lights in real-time using an IP webcam.

Provide voice instructions via Gemini AI, e.g., “Red light detected, please stop”.

Assist drivers in maintaining safety and compliance with traffic rules.

Features

Real-time traffic light detection using YOLOv8.

IP webcam integration for live video input.

Voice-based alerts using Gemini AI (gemini_assistant.py).

Easily extensible for additional traffic rules or obstacle alerts.

Installation
Clone the repository
git clone https://github.com/heisumesh2006/traffic_light_detection.git
cd YOLO_REALTIME_AGENT

Setup virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

Install dependencies
pip install -r requirements.txt

Configure API keys

Add Gemini AI API credentials to .env.

Dataset Setup
Download from Kaggle

Create a Kaggle account.

Download a traffic light dataset (e.g., Traffic Light Dataset
).

Use Kaggle API to download:

pip install kaggle
kaggle datasets download -d <dataset-owner>/<dataset-name>
unzip <dataset-file>.zip -d dataset/

Convert dataset to YOLO format
python convert_json_to_yolo.py --input_dir dataset/annotations --output_dir labels/

IP Webcam Setup

Install an IP Webcam app on your phone:

Android: IP Webcam

iOS: Any IP webcam app.

Start the camera and note the IP URL (e.g., http://192.168.1.5:8080/video).

Update realtime_detect.py:

ip_url = "http://192.168.1.5:8080/video"

Running the Project
Real-time traffic light detection
python realtime_detect.py

Run main script (if needed)
python main.py

Observe detection

The system detects traffic lights and provides voice instructions automatically.

Directory Structure
YOLO_REALTIME_AGENT/
│── dataset/                       # Dataset folder
│── images/                        # Images for training/detection
│── labels/                        # YOLO formatted labels
│── runs/                          # Training/testing results
│── templates/
│    └── index.html                # Optional web template
│── .env                           # API keys
│── .gitignore
│── app.py                         # Optional web app script
│── best.pt                        # Pre-trained YOLOv8 weights
│── convert_json_to_yolo.py        # Conversion script
│── data.yaml                       # YOLOv8 dataset config
│── gemini_assistant.py            # Gemini AI voice assistant
│── main.py                        # Main project script
│── realtime_detect.py             # Real-time detection script
│── traffic_signal_final.ipynb     # Notebook for experimentation
│── train.json                      # Dataset annotations

Notes

Ensure your phone and computer are on the same network for IP Webcam.

You can retrain YOLOv8 using your dataset by updating data.yaml and running:

!yolo train data=data.yaml model=yolov8n.pt epochs=100 imgsz=640
