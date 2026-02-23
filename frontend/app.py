import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import numpy as np

st.set_page_config(page_title="Phishing Platform", page_icon="🎣", layout="wide")

# Custom CSS for interactive elements
st.markdown("""
<style>
    /* Interactive metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
        border: 2px solid transparent;
    }
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        border-color: white;
    }
    .metric-card.selected {
        border-color: #FFD700;
        box-shadow: 0 0 20px #FFD700;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Dashboard cards */
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #f0f2f6;
        transition: all 0.3s;
    }
    .dashboard-card:hover {
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .card-header {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #333;
        border-bottom: 2px solid #FF4B4B;
        padding-bottom: 0.5rem;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
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
        width: 10px;
        height: 10px;
        background: #00ff00;
        border-radius: 50%;
        margin-right: 5px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Interactive elements */
    .clickable-row {
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .clickable-row:hover {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Get API URL from secrets
try:
    API_URL = st.secrets["API_URL"].rstrip('/')
    st.sidebar.success(f"✅ Connected to: {API_URL}")
except:
    API_URL = "https://phishing-simulation-6.onrender.com/api"
    st.sidebar.warning("⚠️ Using default API URL")

# Test backend connection
backend_connected = False
available_endpoints = {}

try:
    test_response = requests.get(f"{API_URL}/test", timeout=5)
    if test_response.status_code == 200:
        backend_connected = True
        data = test_response.json()
        available_endpoints = data.get('endpoints', {})
        st.sidebar.success("✅ Backend connected")
        st.sidebar.write("📋 Available endpoints:")
        for key, value in available_endpoints.items():
            st.sidebar.write(f"  • {key}: {value}")
    else:
        st.sidebar.error(f"❌ Backend returned {test_response.status_code}")
except Exception as e:
    st.sidebar.error(f"❌ Cannot connect to backend: {e}")

# Add API Documentation links in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 API Documentation")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.markdown("[![Swagger](https://img.shields.io/badge/Swagger-UI-green)](https://phishing-simulation-6.onrender.com/docs)")
with col2:
    st.markdown("[![ReDoc](https://img.shields.io/badge/ReDoc-Docs-blue)](https://phishing-simulation-6.onrender.com/redoc)")

st.sidebar.markdown("---")

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
if 'selected_call' not in st.session_state:
    st.session_state.selected_call = None

# Function to generate realistic mock data
def generate_mock_data(data_type):
    if data_type == "vishing":
        return {
            "active_calls": [
                {"id": i, "caller": f"+1-555-{random.randint(1000,9999)}", 
                 "risk": random.choice(["low", "medium", "high"]), 
                 "duration": random.randint(60, 300),
                 "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 30))).strftime('%H:%M:%S')}
                for i in range(random.randint(3, 6))
            ],
            "total_calls": random.randint(800, 1500),
            "suspicious_calls": random.randint(100, 300),
            "blocked_calls": random.randint(50, 150)
        }
    elif data_type == "blockchain":
        return {
            "total_certificates": random.randint(1000, 2000),
            "verified_certificates": random.randint(800, 1800),
            "last_block": random.randint(89000, 90000),
            "recent_certificates": [
                {"name": f"Cert-{i}", "user": random.choice(["Alex", "Jordan", "Casey"]), 
                 "status": random.choice(["verified", "pending"])}
                for i in range(5)
            ]
        }
    elif data_type == "mobile":
        devices = []
        for i in range(random.randint(3, 5)):
            devices.append({
                "device_name": random.choice(["iPhone 14 Pro", "iPad Air", "Pixel 7", "Samsung S23"]),
                "status": random.choice(["active", "inactive"]),
                "device_type": random.choice(["iOS", "Android"]),
                "last_active": (datetime.now() - timedelta(minutes=random.randint(1, 120))).strftime('%H:%M')
            })
        return {"devices": devices}
    elif data_type == "gamification":
        users = ["Alex Thompson", "Jordan Lee", "Casey Morgan", "Riley Cooper", "Taylor Swift"]
        return {
            "leaderboard": [
                {"username": users[i], "points": random.randint(1000, 5000), 
                 "level": random.randint(5, 15), "badges": random.randint(3, 20)}
                for i in range(len(users))
            ]
        }
    elif data_type == "integrations":
        return {
            "webhooks": [
                {"name": "Slack", "status": "active", "events": ["phishing.detected"]},
                {"name": "Teams", "status": "active", "events": ["user.login"]},
                {"name": "Email", "status": "inactive", "events": ["alerts"]}
            ],
            "hris": {"status": "connected", "last_sync": "5 min ago"},
            "siem": {"status": "active", "events_today": random.randint(5000, 10000)}
        }
    return {}

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

# Login function
def do_login(username, password):
    if username == "demo_user" and password == "password":
        st.session_state.logged_in = True
        st.session_state.username = username
        return True, "Login successful"
    return False, "Invalid credentials"

# Main UI
if not st.session_state.logged_in:
    st.title("🎣 Phishing Simulation Platform")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login")
        with st.form("login_form"):
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
st.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)

# Top bar
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown(f"<span class='live-indicator'></span> **LIVE** {datetime.now().strftime('%H:%M:%S')}", unsafe_allow_html=True)
with col2:
    st.markdown(f"### 👋 Welcome, **{st.session_state.username}**!")
with col3:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# Navigation
st.markdown("---")
nav_cols = st.columns(5)
nav_items = [("🏠 Home", "Home"), ("🏆 Leaderboard", "Leaderboard"), 
             ("📊 Stats", "Stats"), ("📞 Vishing", "Vishing"), ("📚 API Docs", "API Docs")]

for idx, (icon, name) in enumerate(nav_items):
    with nav_cols[idx]:
        if st.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.session_state.dashboard_view = "overview"
            st.session_state.selected_metric = None
            st.rerun()

st.markdown("---")

# ==================== INTERACTIVE HOME PAGE ====================
if st.session_state.page == "Home":
    
    # Fetch data
    vishing_data = call_api("vishing")
    blockchain_data = call_api("blockchain")
    mobile_data = call_api("mobile")
    gamification_data = call_api("gamification")
    integrations_data = call_api("integrations")
    
    # === INTERACTIVE METRICS ROW ===
    st.markdown("## 📊 Interactive Dashboard")
    st.markdown("*Click on any metric to see detailed analytics*")
    
    metric_cols = st.columns(4)
    
    # Metric 1: Active Calls
    with metric_cols[0]:
        active_calls = len(vishing_data.get('active_calls', [])) if vishing_data else 3
        selected_class = "selected" if st.session_state.selected_metric == "calls" else ""
        
        if st.button("📞 View Calls", key="btn_calls", use_container_width=True):
            st.session_state.selected_metric = "calls"
            st.session_state.dashboard_view = "detail"
        
        st.markdown(f"""
        <div class='metric-card {selected_class}' onclick=''>
            <div class='metric-label'>📞 Active Calls</div>
            <div class='metric-value'>{active_calls}</div>
            <div>🔴 {vishing_data.get('suspicious_calls', 12)} suspicious</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Metric 2: Certificates
    with metric_cols[1]:
        total_certs = blockchain_data.get('total_certificates', 1234) if blockchain_data else 1234
        verified = blockchain_data.get('verified_certificates', 1189) if blockchain_data else 1189
        selected_class = "selected" if st.session_state.selected_metric == "certs" else ""
        
        if st.button("⛓️ View Certs", key="btn_certs", use_container_width=True):
            st.session_state.selected_metric = "certs"
            st.session_state.dashboard_view = "detail"
        
        st.markdown(f"""
        <div class='metric-card {selected_class}'>
            <div class='metric-label'>⛓️ Certificates</div>
            <div class='metric-value'>{total_certs:,}</div>
            <div>✅ {verified} verified</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Metric 3: Active Devices
    with metric_cols[2]:
        devices = mobile_data.get('devices', []) if mobile_data else []
        active_devices = len([d for d in devices if d.get('status') == 'active']) if devices else 2
        selected_class = "selected" if st.session_state.selected_metric == "devices" else ""
        
        if st.button("📱 View Devices", key="btn_devices", use_container_width=True):
            st.session_state.selected_metric = "devices"
            st.session_state.dashboard_view = "detail"
        
        st.markdown(f"""
        <div class='metric-card {selected_class}'>
            <div class='metric-label'>📱 Active Devices</div>
            <div class='metric-value'>{active_devices}</div>
            <div>📊 {len(devices)} total</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Metric 4: Webhooks
    with metric_cols[3]:
        webhooks = integrations_data.get('webhooks', []) if integrations_data else []
        active_webhooks = len([w for w in webhooks if w.get('status') == 'active']) if webhooks else 3
        selected_class = "selected" if st.session_state.selected_metric == "webhooks" else ""
        
        if st.button("🔌 View Webhooks", key="btn_webhooks", use_container_width=True):
            st.session_state.selected_metric = "webhooks"
            st.session_state.dashboard_view = "detail"
        
        st.markdown(f"""
        <div class='metric-card {selected_class}'>
            <div class='metric-label'>🔌 Active Webhooks</div>
            <div class='metric-value'>{active_webhooks}</div>
            <div>⚡ {integrations_data.get('siem', {}).get('events_today', 5000):,} events</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === DETAILED VIEW BASED ON SELECTION ===
    if st.session_state.dashboard_view == "overview":
        # Default overview with charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Activity Chart
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'>📈 24-Hour Activity</div>", unsafe_allow_html=True)
            
            hours = [f"{i:02d}:00" for i in range(24)]
            df = pd.DataFrame({
                'Hour': hours,
                'Calls': [random.randint(5, 30) for _ in range(24)],
                'Tests': [random.randint(3, 25) for _ in range(24)]
            })
            
            fig = px.line(df, x='Hour', y=['Calls', 'Tests'], 
                         title='Real-Time Monitoring',
                         labels={'value': 'Count', 'variable': 'Type'})
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Live Calls Feed
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'>📞 Live Calls Feed</div>", unsafe_allow_html=True)
            
            calls = vishing_data.get('active_calls', [])
            if calls:
                for call in calls[:3]:
                    risk_color = "status-active" if call['risk'] == 'low' else "status-warning" if call['risk'] == 'medium' else "status-danger"
                    st.markdown(f"""
                    <div class='clickable-row' onclick=''>
                        <div style='display: flex; justify-content: space-between;'>
                            <span><strong>{call['caller']}</strong></span>
                            <span class='status-badge {risk_color}'>{call['risk'].upper()}</span>
                        </div>
                        <div>⏱️ {call['duration']}s | 🕒 {call.get('timestamp', 'Now')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Risk Distribution
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'>⚠️ Risk Analysis</div>", unsafe_allow_html=True)
            
            risk_data = pd.DataFrame({
                'Risk': ['Low', 'Medium', 'High'],
                'Count': [random.randint(300, 500), random.randint(400, 600), random.randint(150, 300)]
            })
            
            fig = px.pie(risk_data, values='Count', names='Risk', hole=0.4,
                        color_discrete_map={'Low':'#00ff00', 'Medium':'#ffaa00', 'High':'#ff4444'})
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Recent Certificates
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'>⛓️ Recent Certificates</div>", unsafe_allow_html=True)
            
            certs = blockchain_data.get('recent_certificates', [])
            if certs:
                for cert in certs[:3]:
                    status_color = "status-active" if cert['status'] == 'verified' else "status-warning"
                    st.markdown(f"""
                    <div class='clickable-row'>
                        <div style='display: flex; justify-content: space-between;'>
                            <span><strong>{cert['name']}</strong></span>
                            <span class='status-badge {status_color}'>{cert['status'].upper()}</span>
                        </div>
                        <div>👤 {cert['user']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.dashboard_view == "detail":
        st.markdown(f"### 📊 Detailed Analytics: {st.session_state.selected_metric}")
        
        if st.button("← Back to Overview"):
            st.session_state.dashboard_view = "overview"
            st.session_state.selected_metric = None
            st.rerun()
        
        if st.session_state.selected_metric == "calls":
            # Detailed calls view
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Calls Today", vishing_data.get('total_calls', 1245))
                st.metric("Suspicious", vishing_data.get('suspicious_calls', 234))
            with col2:
                st.metric("Blocked", vishing_data.get('blocked_calls', 89))
                st.metric("Success Rate", f"{random.randint(75, 85)}%")
            
            # Call history table
            calls_df = pd.DataFrame(vishing_data.get('active_calls', []))
            if not calls_df.empty:
                st.dataframe(calls_df, use_container_width=True)
        
        elif st.session_state.selected_metric == "certs":
            # Detailed certificates view
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", blockchain_data.get('total_certificates', 1234))
            with col2:
                st.metric("Verified", blockchain_data.get('verified_certificates', 1189))
            with col3:
                st.metric("Last Block", f"#{blockchain_data.get('last_block', 89237)}")
        
        elif st.session_state.selected_metric == "devices":
            # Detailed devices view
            devices_df = pd.DataFrame(mobile_data.get('devices', []))
            if not devices_df.empty:
                st.dataframe(devices_df, use_container_width=True)
        
        elif st.session_state.selected_metric == "webhooks":
            # Detailed webhooks view
            webhooks_df = pd.DataFrame(integrations_data.get('webhooks', []))
            if not webhooks_df.empty:
                st.dataframe(webhooks_df, use_container_width=True)

# ==================== OTHER PAGES ====================
elif st.session_state.page == "Leaderboard":
    st.markdown("## 🏆 Global Leaderboard")
    data = call_api("gamification")
    if data and 'leaderboard' in data:
        df = pd.DataFrame(data['leaderboard'])
        st.dataframe(df, use_container_width=True)

elif st.session_state.page == "Vishing":
    st.markdown("## 📞 Vishing Protection")
    data = call_api("vishing")
    if data:
        st.json(data)

elif st.session_state.page == "API Docs":
    st.markdown("## 📚 API Documentation")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🚀 Open Swagger UI", "https://phishing-simulation-6.onrender.com/docs", use_container_width=True)
    with col2:
        st.link_button("📚 Open ReDoc", "https://phishing-simulation-6.onrender.com/redoc", use_container_width=True)
    
    if available_endpoints:
        st.markdown("### Available Endpoints")
        for key, value in available_endpoints.items():
            st.code(f"{key}: {value}")
