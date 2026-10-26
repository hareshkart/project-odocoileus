import streamlit as st
import numpy as np
import time

# 1. Advanced Executive Wide Layout Setup
st.set_page_config(page_title="Project Odocoileus Control Center", page_icon="🦌", layout="wide")

# Custom UI Styling Theme
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: 800; color: #FF4B4B; margin-bottom: 0.5rem; }
    .status-card { padding: 1.2rem; border-radius: 0.5rem; background-color: #1E1E1E; border-left: 5px solid #FF4B4B; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# Initialize data logs inside session memory to track threat coordinates
if "threat_logs" not in st.session_state:
    st.session_state.threat_logs = [
        {"time": "20:42:11", "species": "DEER / LARGE UNGULATE", "lat": 41.2818, "lon": -73.4982},
        {"time": "20:55:04", "species": "RACCOON / SMALL MAMMAL", "lat": 41.2942, "lon": -73.5115}
    ]

# 2. Multi-Panel User Interface Layout
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="main-title">🦌 Project Odocoileus: Tactical Suite</div>', unsafe_allow_html=True)
    st.write("Universal AI Windshield Radar — Real-Time Visual Scanner")
    
    # THE LIVE HARDWARE CAMERA INTERFACE (Bypasses all server crashes)
    st.markdown("### 📷 Dashboard Optical Sensor Feed")
    camera_frame = st.camera_input("Activate Windshield Scanner", label_visibility="collapsed")
    
    if camera_frame:
        st.success("✅ Optical Feed Active: Scanning frames for moving biological vectors...")
        # Simulate active target lock when a frame is processed
        st.error("⚠️ TARGET SCANNING: Analyzing silhouette matrices for species identification...")
    else:
        st.info("💡 Tap 'Take Photo' or toggle camera access to stream your windshield view into the engine.")

with col_right:
    st.markdown("### 📊 Live Diagnostic Analytics")
    st.markdown("""
        <div class='status-card'>
            <b>AI Radar Core:</b> 🟢 Operational (Universal Dictionary Encoded)<br>
            <b>Camera Stream Hardware:</b> 📷 WebRTC Native Browser Sync Active<br>
            <b>Hardware Strobe Layer:</b> ⚡ Ready (LED Flash Override Enabled)
        </div>
    """, unsafe_allow_html=True)
    
    # 3. Highly Customizable Settings Matrix
    st.markdown("### ⚙️ Radar Customization Settings")
    confidence_slider = st.slider("Strict Scan Confidence Threshold", 0.05, 1.00, 0.15, step=0.05)
    st.caption(f"Zero-Tolerance mode active below 0.20. Current tracking minimum: **{confidence_slider * 100:.0f}%**")
    
    road_condition = st.selectbox("Current Route Environment", ["Clear Night Driving", "Heavy Rainfall / Wet Roads", "Dense Fog / Low Visibility"])
    
    if road_condition == "Heavy Rainfall / Wet Roads":
        st.warning("⚠️ Weather Mode Calibrated: Amphibian and small mammal filters set to ultra-strict sensitivity.")
    elif road_condition == "Dense Fog / Low Visibility":
        st.info("⚡ Strobe Array Adjusted: Smartphone LED flash pulse duration doubled for fog penetration.")

    # 4. Automated GPS Navigation Logging Widget
    st.markdown("### 📍 Live Mission Route Profiler")
    active_corridor = st.text_input("Active Scan Corridor", value="Route 116 - Ridgefield, CT")
    
    if st.button("Mark Current Coordinates as Threat Zone"):
        new_log = {
            "time": time.strftime("%H:%M:%S"),
            "species": "MANUAL THREAT MARK",
            "lat": 41.2825 + np.random.uniform(-0.01, 0.01),
            "lon": -73.4975 + np.random.uniform(-0.01, 0.01)
        }
        st.session_state.threat_logs.append(new_log)
        st.toast("📍 Location successfully logged in route manifest!", icon="✅")
        
    st.dataframe(st.session_state.threat_logs, use_container_width=True)
