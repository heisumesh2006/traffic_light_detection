# Traffic Light Detection & Voice Assistant for Self-Driving Cars

## Overview
This project implements a real-time traffic light detection system for self-driving cars. It uses **YOLOv8** for object detection and **Gemini AI** as a voice assistant to provide driver alerts based on traffic signals.

The system can:
- Detect red, yellow, and green traffic lights in real-time using an IP webcam.
- Send detection results to Gemini AI, which gives voice instructions like “Red light detected, please stop” or “Green light, continue driving”.
- Assist drivers in maintaining safety and compliance with traffic rules.

## Features
- Real-time traffic light detection using YOLOv8.
- IP webcam integration for live video input.
- Voice-based alerts using Gemini AI.
- Designed for self-driving car applications.
- Easily extensible for additional features like drowsiness detection and obstacle alerts.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/heisumesh2006/traffic_light_detection.git
cd traffic_light_detection

Create a virtual environment and activate it:

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Set up your .env file for any API keys (e.g., Gemini AI credentials).

Setup / Usage
IP Webcam Setup

Install an IP Webcam app on your phone (Android Play Store or iOS equivalent).

Start the camera and note the IP URL it provides (e.g., http://192.168.1.5:8080/video).

Update the URL in your project:

Open realtime_detect.py.

Replace the default ip_url with your phone’s IP Webcam URL.

Run the project

Real-time traffic light detection:

python realtime_detect.py


Run the main project script (if needed):

python main.py


The system will detect traffic lights and provide voice instructions automatically.

License

This project is open-source and available under the MIT License
.


---

✅ This version is **organized, clean, and user-friendly** for GitHub.  

If you want, I can also **add a “Demo GIF / Screenshot” section** so anyone visiting the repo sees the detection in action immediately—it makes it much more professional.  

Do you want me to add that?
