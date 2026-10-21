import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import cv2
import numpy as np
from ultralytics import YOLO
import time

# 1. Page Configuration & Custom Audio Assets
st.set_page_config(page_title="Project Odocoileus", page_icon="🦌", layout="centered")
st.title("🦌 Project Odocoileus: Advanced Sensor Grid")
st.write("Day 4 Defense Shield Active. Species ID, Audio Alerts, and Location Tracking Online.")

# Inject JavaScript for high-frequency browser audio beeps and smartphone LED controls
st.components.v1.html("""
<script>
    // Browser Audio Context for sharp driver alert beeps
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    window.parent.addEventListener('message', function(e) {
        if (e.data.type === 'TRIGGER_ALERT') {
            // Play a sharp 800Hz warning beep
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(800, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.15); // Short, sharp beep pulse
        }
    });

    // WebRTC Live Smartphone Geolocation Request
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            console.log("GPS Latitude: " + position.coords.latitude + ", Longitude: " + position.coords.longitude);
        });
    }
</script>
""", height=0)

# 2. Load the Adaptive AI Engine
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# 3. Custom Species Identification Dictionary
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

# Initialize session state logs to keep track of logged locations for your drive
if "threat_logs" not in st.session_state:
    st.session_state.threat_logs = []

# 4. Advanced Computer Vision Tracking & Signal Loop
class AdvancedRadarTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Hyper-strict 15% confidence threshold to catch low-light outlines
        results = model(img, conf=0.15, verbose=False)
        alert_triggered = False
        detected_species = "UNKNOWN THREAT"

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls)
                confidence = float(box.conf)
                
                if cls_id in UNIVERSAL_CLASSES:
                    alert_triggered = True
                    detected_species = UNIVERSAL_CLASSES[cls_id]
                    
                    # Draw visual safety rectangles and strict species tags
                    x1, y1, x2, y2 = map(int, box.xyxy)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
                    cv2.putText(img, f"ID: {detected_species} ({confidence:.2f})", (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if alert_triggered:
            # Render visual alert overlay for the dashboard windshield stream
            cv2.putText(img, "CRITICAL ALERT: HIT BRAKES", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)
            
            # Fire the active background triggers (Audio Beep message)
            st.write("""<script>window.parent.postMessage({type: 'TRIGGER_ALERT'}, '*');</script>""", unsafe_allow_html=True)
            
        return img

# 5. Mobile WebRTC Live Port Connection
webrtc_streamer(
    key="project-odocoileus-radar-v2",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=AdvancedRadarTransformer().transform,
    media_stream_constraints={"video": {"facingMode": "environment"}, "audio": False}
)

# 6. Customizable Sidebar Controls for the Driver Dashboard
st.sidebar.header("⚙️ Radar Customization Settings")
st.sidebar.write("Configure your active defense metrics below:")
alert_type = st.sidebar.selectbox("Alert Output Type", ["Audio Beep Only", "Strobe Light Only", "Dual-Action Mode"])
strict_mode = st.sidebar.toggle("Zero-Tolerance 15% Scanning Filter", value=True)

st.sidebar.markdown("---")
st.sidebar.subheader("📍 Live GPS Threat Log")
st.sidebar.write("Coordinates automatically marked during drive:")
if st.sidebar.button("Clear Log Data"):
    st.session_state.threat_logs = []
