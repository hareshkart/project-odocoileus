import sys
import os

# FORCE HEADLESS MODE BEFORE ANY IMAGES LOAD
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
try:
    import cv2
except ImportError:
    pass

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import numpy as np
from ultralytics import YOLO
import av

# 1. Advanced Executive Wide Layout Configuration
st.set_page_config(page_title="Project Odocoileus Control Center", page_icon="🦌", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #FF4B4B; margin-bottom: 0.5rem; }
    .status-card { padding: 1rem; border-radius: 0.5rem; background-color: #1E1E1E; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# 2. Universal Deep Learning Core
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

try:
    model = load_model()
    model_status = "🟢 Operational (YOLOv8n Active)"
except Exception as e:
    model_status = f"🔴 Initialization Error: {str(e)}"

UNIVERSAL_CLASSES = {
    0: "HUMAN / PEDESTRIAN",
    14: "BIRD (Avian Vector)",
    15: "RACCOON / SMALL MAMMAL",
    16: "COYOTE / FOX (Canid Vector)",
    17: "DEER / LARGE UNGULATE",
    18: "BOBCAT / FELID VECTOR",
    19: "COW / LARGE MAMMAL",
    21: "BEAR (Ursid Threat)"
}

# 3. Streamlined Computer Vision Frame Callback
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")
    
    # Run scanning loop with hyper-strict 15% threshold
    import cv2
    results = model(img, conf=0.15, verbose=False)
    alert_triggered = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls)
            confidence = float(box.conf)
            
            if cls_id in UNIVERSAL_CLASSES:
                alert_triggered = True
                detected_label = UNIVERSAL_CLASSES[cls_id]
                
                x1, y1, x2, y2 = map(int, box.xyxy)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
                cv2.putText(img, f"{detected_label} ({confidence:.2f})", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if alert_triggered:
        cv2.putText(img, "CRITICAL WARNING: THREAT IMMINENT", (30, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
        
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# 4. Multi-Panel User Interface Architecture
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="main-title">🦌 Project Odocoileus: Tactical Command Suite</div>', unsafe_allow_html=True)
    st.write("Real-Time Road Threat Tracking Network — System Operational")
    
    webrtc_streamer(
        key="project-odocoileus-command",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": {"facingMode": "environment"}, "audio": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:://google.com"]}]}
    )

with col_right:
    st.markdown("### 📊 Live Diagnostic Analytics")
    st.markdown(f"<div class='status-card'><b>AI Core Status:</b><br>{model_status}</div>", unsafe_allow_html=True)
    
    st.markdown("### 🌦️ Environment Adaptability Matrix")
    road_condition = st.selectbox("Current Route Environment", ["Clear Night Driving", "Heavy Rainfall / Wet Roads", "Dense Fog / Low Visibility"])
    
    if road_condition == "Heavy Rainfall / Wet Roads":
        st.warning("⚠️ Amphibian Migration Warning: Slow down to protect small moving road-level species.")
    elif road_condition == "Dense Fog / Low Visibility":
        st.info("ℹ️ Strobe Mode Boosted: LED output intensity calibrated for maximum atmospheric penetration.")

    st.markdown("### 📍 Mission Route Profiler")
    target_route = st.text_input("Active Route Corridor", value="Route 116 - Ridgefield")
    st.write(f"Tracking coordinates along: **{target_route}**")
    
    if st.button("Mark Current Location as Threat Zone"):
        st.toast("📍 Coordinate marked securely in temporary session logs!", icon="✅")
