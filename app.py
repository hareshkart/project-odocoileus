import streamlit as st
import cv2
import numpy as np
import time
from ultralytics import YOLO

st.set_page_config(
    page_title="Project Odocoileus - Wildlife Radar",
    page_icon="🦌",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .alert-banner {
        background-color: #da3633;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_yolo_model():
    """Loads the pre-trained lightweight YOLOv8n model with st.cache_resource."""
    try:
        model = YOLO("yolov8n.pt")
        return model
    except Exception as e:
        st.error(f"Failed to load YOLOv8 model: {e}")
        return None

# Target COCO dataset class IDs for wildlife, large mammals, and birds:
# bird(14), cat(15), dog(16), horse(17), sheep(18), cow(19), bear(21)
TARGET_ANIMALS = [14, 15, 16, 17, 18, 19, 21]

st.sidebar.title("🌲 Odocoileus Control Panel")
st.sidebar.markdown("---")
st.sidebar.info("Dashboard-mounted smartphone active scanning radar for wildlife roadkill prevention.")

# Dominant checkbox titled as requested
sensor_active = st.sidebar.checkbox("🟢 Activate Project Odocoileus Sensor Grid", value=False)

conf_threshold = st.sidebar.slider("AI Detection Confidence Threshold", 0.1, 0.9, 0.40, 0.05)
st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:** " + ("🟢 ACTIVE & SCANNING" if sensor_active else "🔴 STANDBY"))

st.title("🦌 Project Odocoileus: Active Wildlife Radar")
st.markdown("Transforms your dashboard-mounted smartphone into an active AI scanning radar to prevent roadkill.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><h4>Target Classes</h4><p>Wildlife, Large Mammals & Birds</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><h4>Confidence Filter</h4><p>{conf_threshold * 100:.0f}% Threshold</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><h4>Hardware Interface</h4><p>cv2.VideoCapture(0)</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Center placeholder window for live video feed
st.subheader("Live Radar Stream & Optical Sensor Feed")
video_placeholder = st.empty()
alert_placeholder = st.empty()

if sensor_active:
    model = load_yolo_model()
    if model is None:
        st.error("Model initialization failed. Please verify dependencies.")
    else:
        # Access smartphone camera feed using cv2.VideoCapture(0)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("Error: Could not access the camera via cv2.VideoCapture(0). Please verify device permissions.")
        else:
            stop_button = st.sidebar.button("Stop Radar Scan")
            
            while cap.isOpened() and sensor_active and not stop_button:
                ret, frame = cap.read()
                if not ret:
                    st.warning("Failed to grab frame from camera feed.")
                    break
                
                # Perform AI detection inference with YOLOv8
                results = model(frame, conf=conf_threshold, verbose=False)
                animal_detected_in_frame = False
                
                # Process detection results against TARGET_ANIMALS
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        if cls_id in TARGET_ANIMALS:
                            animal_detected_in_frame = True
                            
                            # Extract bounding box coordinates
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            conf = float(box.conf[0])
                            class_name = model.names[cls_id]
                            
                            # Draw thick bounding box around detected animal
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                            
                            # Label animal detection
                            label = f"⚠️ ANIMAL DETECTED ({class_name} {conf:.2f})"
                            cv2.putText(frame, label, (x1, max(y1 - 10, 20)), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

                # Two-Way Safety Alert Trigger execution
                if animal_detected_in_frame:
                    # Internal Warning: Project massive on-screen warning banner and text
                    cv2.putText(frame, "CRITICAL ALERT: HIT BRAKES", (30, 60), 
                                cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
                    
                    # Trigger dynamic native browser notification using st.toast()
                    st.toast("🚨 CRITICAL ALERT: ANIMAL DETECTED ON ROADWAY! HIT BRAKES!", icon="⚠️")
                    
                    # EXTERNAL WARNING LAYER: Smartphone Physical LED Strobe Flashlight Trigger
                    # ---------------------------------------------------------------------------------
                    # [DEVELOPER NOTE / INTEGRATION POINT]:
                    # Insert your JavaScript wrapper function here or bind to navigator.mediaDevices track 
                    # constraints to flash the physical LED camera flashlight as a defensive strobe light:
                    #
                    # Example JavaScript Wrapper Hook:
                    # st.markdown(\"\"\"
                    #     <script>
                    #     async function flashLedStrobe() {
                    #         try {
                    #             const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
                    #             const track = stream.getVideoTracks()[0];
                    #             // Toggle torch constraint for defensive strobe flash
                    #             await track.applyConstraints({ advanced: [{ torch: true }] });
                    #             setTimeout(async () => { await track.applyConstraints({ advanced: [{ torch: false }] }); }, 200);
                    #         } catch (err) { console.error('Torch error:', err); }
                    #     }
                    #     flashLedStrobe();
                    #     </script>
                    # \"\"\", unsafe_allow_html=True)
                    # ---------------------------------------------------------------------------------
                    
                    alert_placeholder.markdown(
                        '<div class="alert-banner">🚨 CRITICAL ALERT: HIT BRAKES! Wildlife detected in sensor path!</div>', 
                        unsafe_allow_html=True
                    )
                else:
                    alert_placeholder.empty()

                # Stream processed frames smoothly to active st.image placeholder
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
                
                # Frame rate throttling for optimal mobile performance
                time.sleep(0.03)
                
            cap.release()
else:
    video_placeholder.info("Sensor Grid is currently in STANDBY mode. Toggle the checkbox in the sidebar to activate the active scanning radar.")
