import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import random

st.set_page_config(
    page_title="Phishing Simulation Platform",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced styling
st.markdown("""
<style>
    /* Main header with gradient animation */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #FF4B4B, #FF8C8C, #FF4B4B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        animation: gradient 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.8rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
        transition: transform 0.3s, box-shadow 0.3s;
        border: 1px solid rgba(255,255,255,0.1);
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
        animation: countUp 1s;
    }
    
    .metric-label {
        font-size: 1.1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-change {
        font-size: 1rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .positive-change {
        background: rgba(0,255,0,0.2);
        color: #00ff00;
    }
    
    .negative-change {
        background: rgba(255,0,0,0.2);
        color: #ff4444;
    }
    
    /* Dashboard cards */
    .dashboard-card {
        background: white;
        padding: 1.8rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #f0f2f6;
        transition: all 0.3s;
    }
    
    .dashboard-card:hover {
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .card-header {
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 1.2rem;
        color: #333;
        border-bottom: 3px solid #FF4B4B;
        padding-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-header-icon {
        font-size: 1.8rem;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        text-align: center;
    }
    
    .status-active {
        background: #00ff0022;
        color: #00aa00;
        border: 1px solid #00ff00;
    }
    
    .status-warning {
        background: #ffaa0022;
        color: #ffaa00;
        border: 1px solid #ffaa00;
    }
    
    .status-danger {
        background: #ff444422;
        color: #ff4444;
        border: 1px solid #ff4444;
    }
    
    /* Live indicator */
    .live-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #00ff00;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
        box-shadow: 0 0 10px #00ff00;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.3); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Quick action buttons */
    .quick-action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem;
        border-radius: 15px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        margin: 0.3rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
    }
    
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Activity timeline */
    .timeline-item {
        padding: 1rem;
        border-left: 3px solid #FF4B4B;
        margin: 1rem 0;
        background: #f8f9fa;
        border-radius: 0 10px 10px 0;
        transition: all 0.3s;
    }
    
    .timeline-item:hover {
        background: #e8f4fd;
        transform: translateX(5px);
    }
    
    /* Progress bar */
    .progress-container {
        background: #f0f2f6;
        border-radius: 10px;
        height: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #FF4B4B, #FF8C8C);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
</style>
""", unsafe_allow_html=True)

# Get API URL from secrets
try:
    API_URL = st.secrets["API_URL"].rstrip('/')
except:
    API_URL = "https://phishing-simulation-6.onrender.com/api"

# Test backend connection
backend_connected = False
available_endpoints = {}

try:
    test_response = requests.get(f"{API_URL}/test", timeout=5)
    if test_response.status_code == 200:
        backend_connected = True
        data = test_response.json()
        available_endpoints = data.get('endpoints', {})
except:
    pass

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'selected_metric' not in st.session_state:
    st.session_state.selected_metric = None
if 'dashboard_view' not in st.session_state:
    st.session_state.dashboard_view = "overview"

# Function to call API
def call_api(endpoint_type, method="GET", data=None):
    if not backend_connected or endpoint_type not in available_endpoints:
        return generate_mock_data(endpoint_type)
    
    endpoint = available_endpoints[endpoint_type]
    url = f"{API_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=3)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=3)
        else:
            return generate_mock_data(endpoint_type)
            
        if response.status_code == 200:
            return response.json()
        return generate_mock_data(endpoint_type)
    except:
        return generate_mock_data(endpoint_type)

# Generate mock data for visualizations
def generate_mock_data(data_type):
    if data_type == "vishing":
        return {
            "active_calls": [
                {"caller": f"+1-555-{random.randint(1000,9999)}", "risk": random.choice(["low", "medium", "high"]), "duration": random.randint(60, 300)}
                for _ in range(random.randint(2, 5))
            ],
            "total_calls": random.randint(800, 1500),
            "suspicious_calls": random.randint(100, 300),
            "blocked_calls": random.randint(50, 150)
        }
    elif data_type == "blockchain":
        return {
            "total_certificates": random.randint(1000, 2000),
            "verified_certificates": random.randint(800, 1800),
            "last_block": random.randint(89000, 90000)
        }
    elif data_type == "mobile":
        return {
            "devices": [
                {"device_name": random.choice(["iPhone 14", "Pixel 7", "Samsung S23"]), "status": random.choice(["active", "inactive"]), "device_type": random.choice(["iOS", "Android"])}
                for _ in range(random.randint(2, 5))
            ]
        }
    elif data_type == "gamification":
        return {
            "leaderboard": [
                {"username": random.choice(["Alex", "Jordan", "Casey", "Riley", "Taylor"]), "points": random.randint(1000, 5000), "level": random.randint(5, 15)}
                for _ in range(10)
            ]
        }
    return {}

# Login function
def do_login(username, password):
    if username == "demo_user" and password == "password":
        st.session_state.logged_in = True
        st.session_state.username = username
        return True, "Login successful"
    return False, "Invalid credentials"

# Main UI
if not st.session_state.logged_in:
    # Login page (simplified for this example)
    st.markdown("<h1 class='main-header'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Login")
            username = st.text_input("Username", value="demo_user")
            password = st.text_input("Password", type="password", value="password")
            if st.form_submit_button("Login", use_container_width=True):
                success, message = do_login(username, password)
                if success:
                    st.rerun()
                else:
                    st.error(message)
    st.stop()

# Main app after login
st.markdown("<h1 class='main-header'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)

# Top bar with user info and live indicator
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown(f"<span class='live-indicator'></span> **LIVE** {datetime.now().strftime('%H:%M:%S')}", unsafe_allow_html=True)
with col2:
    st.markdown(f"### 👋 Welcome, **{st.session_state.username}**!", unsafe_allow_html=True)
with col3:
    st.markdown(f"**Role:** User | **Level:** {random.randint(5, 10)}")

# Navigation
st.markdown("---")
nav_cols = st.columns(6)
nav_items = [
    ("🏠", "Home"),
    ("🏆", "Leaderboard"),
    ("📊", "Analytics"),
    ("📞", "Vishing"),
    ("⛓️", "Blockchain"),
    ("📱", "Mobile")
]

for idx, (icon, name) in enumerate(nav_items):
    with nav_cols[idx]:
        if st.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.session_state.dashboard_view = "overview"
            st.rerun()

st.markdown("---")

# ==================== ADVANCED HOME DASHBOARD ====================
if st.session_state.page == "Home":
    
    # Fetch real-time data
    vishing_data = call_api("vishing")
    blockchain_data = call_api("blockchain")
    mobile_data = call_api("mobile")
    gamification_data = call_api("gamification")
    
    # === TOP METRICS SECTION ===
    st.markdown("## 📊 Real-Time Dashboard")
    
    metric_cols = st.columns(4)
    
    # Metric 1: Active Calls (Clickable)
    with metric_cols[0]:
        active_calls = len(vishing_data.get('active_calls', [])) if vishing_data else 3
        change = random.randint(-5, 15)
        change_class = "positive-change" if change >= 0 else "negative-change"
        change_symbol = "↑" if change >= 0 else "↓"
        
        if st.button("📞", key="metric_calls", use_container_width=True):
            st.session_state.dashboard_view = "calls"
        
        st.markdown(f"""
        <div class='metric-card' onclick=''>
            <div class='metric-label'>📞 Active Calls</div>
            <div class='metric-value'>{active_calls}</div>
            <div class='metric-change {change_class}'>{change_symbol} {abs(change)}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Metric 2: Certificates
    with metric_cols[1]:
        total_certs = blockchain_data.get('total_certificates', 1234) if blockchain_data else 1234
        
        if st.button("⛓️", key="metric_certs", use_container_width=True):
            st.session_state.dashboard_view = "certificates"
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>⛓️ Certificates</div>
            <div class='metric-value'>{total_certs:,}</div>
            <div class='metric-change positive-change'>↑ 12%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Metric 3: Active Devices
    with metric_cols[2]:
        devices = mobile_data.get('devices', []) if mobile_data else []
        active_devices = len([d for d in devices if d.get('status') == 'active']) if devices else 2
        
        if st.button("📱", key="metric_devices", use_container_width=True):
            st.session_state.dashboard_view = "devices"
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>📱 Active Devices</div>
            <div class='metric-value'>{active_devices}</div>
            <div class='metric-change positive-change'>↑ 8%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Metric 4: Risk Score
    with metric_cols[3]:
        risk_score = random.randint(65, 95)
        risk_class = "positive-change" if risk_score >= 80 else "negative-change" if risk_score <= 70 else "status-warning"
        
        if st.button("⚠️", key="metric_risk", use_container_width=True):
            st.session_state.dashboard_view = "risk"
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>⚠️ Security Score</div>
            <div class='metric-value'>{risk_score}%</div>
            <div class='metric-change {risk_class}'>{'↑' if risk_score >= 80 else '↓'} 3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === DETAILED VIEW SECTION ===
    if st.session_state.dashboard_view == "overview":
        # Default overview with multiple charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Activity Chart
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'><span class='card-header-icon'>📈</span> 24-Hour Activity</div>", unsafe_allow_html=True)
            
            # Generate sample data
            hours = [f"{i:02d}:00" for i in range(24)]
            activity_data = pd.DataFrame({
                'Hour': hours,
                'Calls': [random.randint(5, 30) for _ in range(24)],
                'Tests': [random.randint(3, 25) for _ in range(24)]
            })
            
            fig = px.line(activity_data, x='Hour', y=['Calls', 'Tests'], 
                         title='Real-Time Activity Monitoring',
                         labels={'value': 'Count', 'variable': 'Type'})
            fig.update_layout(height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02))
            fig.update_traces(line=dict(width=3))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Risk Distribution
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'><span class='card-header-icon'>🎯</span> Risk Distribution</div>", unsafe_allow_html=True)
            
            risk_data = pd.DataFrame({
                'Risk': ['Low', 'Medium', 'High'],
                'Count': [random.randint(300, 500), random.randint(400, 600), random.randint(150, 300)]
            })
            
            fig = px.pie(risk_data, values='Count', names='Risk', 
                         color_discrete_map={'Low':'#00ff00', 'Medium':'#ffaa00', 'High':'#ff4444'},
                         hole=0.4)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Live Calls
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'><span class='card-header-icon'>📞</span> Live Calls</div>", unsafe_allow_html=True)
            
            if vishing_data and vishing_data.get('active_calls'):
                for call in vishing_data['active_calls'][:4]:
                    risk_color = "status-active" if call['risk'] == 'low' else "status-warning" if call['risk'] == 'medium' else "status-danger"
                    st.markdown(f"""
                    <div class='timeline-item'>
                        <div style='display: flex; justify-content: space-between;'>
                            <span><strong>{call['caller']}</strong></span>
                            <span class='status-badge {risk_color}'>{call['risk'].upper()}</span>
                        </div>
                        <div style='display: flex; gap: 2rem; margin-top: 0.5rem;'>
                            <span>⏱️ {call['duration']}s</span>
                            <span>🎙️ Live</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                for i in range(3):
                    risk = random.choice(["low", "medium", "high"])
                    risk_color = "status-active" if risk == "low" else "status-warning" if risk == "medium" else "status-danger"
                    st.markdown(f"""
                    <div class='timeline-item'>
                        <div style='display: flex; justify-content: space-between;'>
                            <span><strong>+1-555-{random.randint(1000,9999)}</strong></span>
                            <span class='status-badge {risk_color}'>{risk.upper()}</span>
                        </div>
                        <div style='display: flex; gap: 2rem; margin-top: 0.5rem;'>
                            <span>⏱️ {random.randint(60,300)}s</span>
                            <span>🎙️ Live</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if st.button("📊 View All Calls", use_container_width=True):
                st.session_state.page = "Vishing"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Quick Actions
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'><span class='card-header-icon'>⚡</span> Quick Actions</div>", unsafe_allow_html=True)
            
            action_cols = st.columns(2)
            with action_cols[0]:
                if st.button("🎯 New Challenge", use_container_width=True):
                    st.success("Challenge created!")
                if st.button("📊 Generate Report", use_container_width=True):
                    st.info("Generating report...")
            with action_cols[1]:
                if st.button("📞 Start Call", use_container_width=True):
                    st.warning("Call simulator started")
                if st.button("🔍 Audit Logs", use_container_width=True):
                    st.info("Viewing logs...")
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.dashboard_view == "calls":
        st.markdown("### 📞 Detailed Call Analytics")
        # Detailed call view
        call_data = pd.DataFrame({
            'Time': [f"{random.randint(0,23):02d}:{random.randint(0,59):02d}" for _ in range(10)],
            'Caller': [f"+1-555-{random.randint(1000,9999)}" for _ in range(10)],
            'Duration': [f"{random.randint(1,5)}:{random.randint(10,59)}" for _ in range(10)],
            'Risk': [random.choice(['Low', 'Medium', 'High']) for _ in range(10)],
            'Status': [random.choice(['Active', 'Completed', 'Blocked']) for _ in range(10)]
        })
        st.dataframe(call_data, use_container_width=True)
        
    elif st.session_state.dashboard_view == "certificates":
        st.markdown("### ⛓️ Certificate Overview")
        cert_data = pd.DataFrame({
            'ID': [f"CERT-{random.randint(1000,9999)}" for _ in range(8)],
            'Name': [f"Certificate {i}" for i in range(8)],
            'User': [random.choice(['Alex', 'Jordan', 'Casey']) for _ in range(8)],
            'Status': [random.choice(['Verified', 'Pending']) for _ in range(8)],
            'Issued': [(datetime.now() - timedelta(days=random.randint(1,30))).strftime('%Y-%m-%d') for _ in range(8)]
        })
        st.dataframe(cert_data, use_container_width=True)
        
    elif st.session_state.dashboard_view == "devices":
        st.markdown("### 📱 Device Management")
        device_data = pd.DataFrame({
            'Device': [f"{random.choice(['iPhone', 'iPad', 'Pixel'])} {random.randint(10,15)}" for _ in range(5)],
            'Type': [random.choice(['iOS', 'Android']) for _ in range(5)],
            'Status': [random.choice(['Active', 'Inactive']) for _ in range(5)],
            'Last Active': [(datetime.now() - timedelta(minutes=random.randint(5,120))).strftime('%H:%M') for _ in range(5)]
        })
        st.dataframe(device_data, use_container_width=True)
        
    elif st.session_state.dashboard_view == "risk":
        st.markdown("### ⚠️ Security Risk Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            # Risk trend
            risk_trend = pd.DataFrame({
                'Day': [f"Day {i}" for i in range(1,8)],
                'Risk Score': [random.randint(60, 95) for _ in range(7)]
            })
            fig = px.line(risk_trend, x='Day', y='Risk Score', title='Risk Trend (7 Days)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk factors
            factors = pd.DataFrame({
                'Factor': ['Phishing', 'Vishing', 'Malware', 'Social Engineering'],
                'Count': [random.randint(20,50), random.randint(15,40), random.randint(10,30), random.randint(5,25)]
            })
            fig = px.bar(factors, x='Factor', y='Count', title='Risk Factors', color='Count')
            st.plotly_chart(fig, use_container_width=True)

# ==================== OTHER PAGES ====================
elif st.session_state.page == "Leaderboard":
    st.markdown("## 🏆 Global Leaderboard")
    data = call_api("gamification")
    if data and 'leaderboard' in data:
        df = pd.DataFrame(data['leaderboard'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Leaderboard data loading...")

elif st.session_state.page == "Vishing":
    st.markdown("## 📞 Vishing Protection")
    data = call_api("vishing")
    if data:
        st.json(data)
    else:
        st.info("Vishing data loading...")

elif st.session_state.page == "Blockchain":
    st.markdown("## ⛓️ Blockchain Certificates")
    data = call_api("blockchain")
    if data:
        st.json(data)
    else:
        st.info("Blockchain data loading...")

elif st.session_state.page == "Mobile":
    st.markdown("## 📱 Mobile Integration")
    data = call_api("mobile")
    if data:
        st.json(data)
    else:
        st.info("Mobile data loading...")

# Logout button
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()
