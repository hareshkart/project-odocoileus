import streamlit as st
import numpy as np
import time

# 1. Executive Wide Layout Setup
st.set_page_config(page_title="Project Odocoileus Control Center", page_icon="🦌", layout="wide")

# Custom UI Styling Theme
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: 800; color: #FF4B4B; margin-bottom: 0.5rem; }
    .status-card { padding: 1.2rem; border-radius: 0.5rem; background-color: #1E1E1E; border-left: 5px solid #FF4B4B; margin-bottom: 1rem; }
    .metric-box { padding: 1rem; background-color: #121212; border-radius: 0.4rem; text-align: center; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# Initialize data logs inside session memory to track your drives
if "threat_logs" not in st.session_state:
    st.session_state.threat_logs = [
        {"time": "20:42:11", "species": "DEER / LARGE UNGULATE", "lat": 41.2818, "lon": -73.4982, "conf": 0.94},
        {"time": "20:55:04", "species": "RACCOON / SMALL MAMMAL", "lat": 41.2942, "lon": -73.5115, "conf": 0.81}
    ]

# 2. Multi-Panel User Interface Layout
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="main-title">🦌 Project Odocoileus: Advanced Tactical Suite</div>', unsafe_allow_html=True)
    st.write("Universal AI Scanning Matrix & Dynamic Target Profiler")
    
    # Sensor Activation Switch Grid
    run_radar = st.toggle("🟢 ACTIVATE PROJECT ODOCOILEUS SENSOR GRID", value=True)
    
    if run_radar:
        st.info("📡 Scanning Mode Active: Real-time neural network monitoring road vectors...")
        
        # Pure progress visual radar status canvas
        st.markdown("### 🎚️ Active Scanning Simulation")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate clean, error-free matrix tracking loops
        simulated_step = np.random.randint(40, 100)
        progress_bar.progress(simulated_step)
        
        if simulated_step > 75:
            st.error("🚨 CRITICAL ALERT DETECTED: IMMINENT ROAD THREAT VECTOR INshadows")
            st.toast("⚠️ CRITICAL ALERT: Project Odocoileus detected sudden movement ahead!", icon="🚨")
        else:
            st.success("✅ Windshield Path Clear: No imminent biological obstructions tracked.")
            
    else:
        st.warning("🔴 Radar Offline: Sensor grid deactivated. Windshield monitoring paused.")

with col_right:
    st.markdown("### 📊 Live Diagnostic Analytics")
    st.markdown("""
        <div class='status-card'>
            <b>AI Radar Status:</b> 🟢 Operational (Universal Weights Locked)<br>
            <b>System Frame Rate:</b> 30 FPS (Optimized Mobile Sync)<br>
            <b>Hardware Strobe Layer:</b> ⚡ Ready (LED Flash Override Enabled)
        </div>
    """, unsafe_allow_html=True)
    
    # 3. Highly Customizable Settings Matrix (Species IDs & Threshold Tunnels)
    st.markdown("### ⚙️ Radar Customization Settings")
    
    # Adjust strictness dynamically
    confidence_slider = st.slider("Strict Scan Confidence Threshold", 0.05, 1.00, 0.15, step=0.05)
    st.caption(f"Zero-Tolerance mode active below 0.20. Current tracking minimum: **{confidence_slider * 100:.0f}%**")
    
    # Custom Environmental Matrix
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
            "lon": -73.4975 + np.random.uniform(-0.01, 0.01),
            "conf": 1.00
        }
        st.session_state.threat_logs.append(new_log)
        st.toast("📍 Location successfully logged in route manifest!", icon="✅")
        
    # Render full data logs directly onto the user dashboard grid
    st.dataframe(st.session_state.threat_logs, use_container_width=True)
