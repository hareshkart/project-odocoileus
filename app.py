import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import cv2
import numpy as np
from ultralytics import YOLO

# 1. Page & Layout Setup
st.set_page_config(page_title="Project Odocoileus", page_icon="🦌", layout="centered")
st.title("🦌 Project Odocoileus: Universal Radar")
st.write("Universal Scanning Engine Online. Mount device facing windshield.")

# 2. Load the Adaptive AI Brain
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# 3. Universal Target Dictionary
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

# 4. Computer Vision Image Processing Loop
class UniversalRadarTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Hyper-strict 15% threshold for night road shadows
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
                    
                    # Draw visual safety rectangles
                    x1, y1, x2, y2 = map(int, box.xyxy)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
                    cv2.putText(img, f"{detected_label} ({confidence:.2f})", (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if alert_triggered:
            cv2.putText(img, "CRITICAL ALERT: HIT BRAKES", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)
            
        return img

# 5. Mobile WebRTC Live Port Connection (Simplified to fix parsing error)
webrtc_streamer(
    key="project-odocoileus-radar",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=UniversalRadarTransformer().transform,
    media_stream_constraints={"video": {"facingMode": "environment"}, "audio": False}
)
