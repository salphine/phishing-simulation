import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Phishing Simulation Platform",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #FF4B4B, #FF8C8C, #FF4B4B);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        animation: gradient 3s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
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
        50% { opacity: 0.5; transform: scale(1.3); box-shadow: 0 0 20px #00ff00; }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.8rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
        transform: rotate(45deg);
        transition: all 0.5s;
        opacity: 0;
    }
    .metric-card:hover::before {
        opacity: 1;
        transform: rotate(45deg) translate(10%, 10%);
    }
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
    }
    .metric-value {
        font-size: 3rem;
        font-weight: bold;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: countUp 1s ease-out;
    }
    .metric-label {
        font-size: 1.1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-trend {
        font-size: 0.9rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        background: rgba(255,255,255,0.2);
        margin-top: 0.5rem;
    }
    
    .dashboard-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.8rem;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 60px rgba(102, 126, 234, 0.15);
    }
    .card-header {
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        color: #333;
        border-bottom: 3px solid #FF4B4B;
        padding-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .card-header-icon {
        font-size: 1.8rem;
    }
    
    .status-badge {
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .status-active {
        background: #00ff0022;
        color: #00aa00;
        border: 1px solid #00ff00;
        box-shadow: 0 0 10px #00ff0055;
    }
    .status-warning {
        background: #ffaa0022;
        color: #ffaa00;
        border: 1px solid #ffaa00;
        box-shadow: 0 0 10px #ffaa0055;
    }
    .status-danger {
        background: #ff444422;
        color: #ff4444;
        border: 1px solid #ff4444;
        box-shadow: 0 0 10px #ff444455;
    }
    
    .activity-item {
        padding: 1rem;
        border-bottom: 1px solid #f0f2f6;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: background 0.3s;
        border-radius: 12px;
    }
    .activity-item:hover {
        background: #f8f9fa;
    }
    .activity-icon {
        font-size: 1.8rem;
        min-width: 40px;
        text-align: center;
    }
    .activity-content {
        flex-grow: 1;
    }
    .activity-time {
        color: #666;
        font-size: 0.8rem;
    }
    .activity-title {
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Auto-refresh every 10 seconds
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

if st.session_state.auto_refresh:
    refresh_count = st_autorefresh(interval=10000, key="data_refresh")

# Get API URL
try:
    API_URL = st.secrets["API_URL"].rstrip('/')
except:
    API_URL = "https://phishing-simulation-6.onrender.com/api"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = {
        'timestamps': [],
        'calls': [],
        'certificates': [],
        'devices': []
    }

# Function to fetch real-time data
def fetch_realtime_data():
    data = {
        'vishing': None,
        'blockchain': None,
        'mobile': None,
        'integrations': None,
        'gamification': None,
        'timestamp': datetime.now()
    }
    
    try:
        response = requests.get(f"{API_URL}/vishing/calls/active", timeout=2)
        if response.status_code == 200:
            data['vishing'] = response.json()
    except: pass
    
    try:
        response = requests.get(f"{API_URL}/blockchain/stats", timeout=2)
        if response.status_code == 200:
            data['blockchain'] = response.json()
    except: pass
    
    try:
        response = requests.get(f"{API_URL}/mobile/devices", timeout=2)
        if response.status_code == 200:
            data['mobile'] = response.json()
    except: pass
    
    try:
        response = requests.get(f"{API_URL}/integrations/webhooks", timeout=2)
        if response.status_code == 200:
            data['integrations'] = response.json()
    except: pass
    
    try:
        response = requests.get(f"{API_URL}/gamification/leaderboard?limit=10", timeout=2)
        if response.status_code == 200:
            data['gamification'] = response.json()
    except: pass
    
    return data

# Mock data generator for demo mode - FIXED SYNTAX
def generate_mock_data():
    # Generate random active calls
    active_calls = []
    for _ in range(random.randint(1, 3)):
        active_calls.append({
            'caller': f"+1-555-{random.randint(1000,9999)}", 
            'risk': random.choice(['low', 'medium', 'high']),
            'duration': random.randint(30, 300)
        })
    
    # Generate random devices
    devices = []
    device_names = ['iPhone 14 Pro', 'Pixel 7', 'Samsung S23', 'iPad Air', 'MacBook Pro']
    for _ in range(random.randint(2, 5)):
        devices.append({
            'device_name': random.choice(device_names),
            'status': random.choice(['active', 'active', 'active', 'inactive'])
        })
    
    # Generate random webhooks
    webhooks = []
    webhook_names = ['Slack', 'Teams', 'Email', 'Splunk', 'Discord', 'Webex']
    for _ in range(random.randint(3, 6)):
        webhooks.append({
            'name': random.choice(webhook_names),
            'status': random.choice(['active', 'active', 'active', 'paused'])
        })
    
    # Generate random leaderboard
    leaderboard = []
    usernames = ['Alex', 'Jordan', 'Casey', 'Riley', 'Taylor', 'Jamie', 'Quinn', 'Morgan', 'Avery', 'Parker']
    for i in range(10):
        leaderboard.append({
            'username': random.choice(usernames),
            'points': random.randint(1000, 5000)
        })
    
    return {
        'vishing': {'active_calls': active_calls},
        'blockchain': {
            'total_certificates': random.randint(1000, 1500),
            'verified_certificates': random.randint(900, 1400),
            'last_block': random.randint(89000, 90000)
        },
        'mobile': {'devices': devices},
        'integrations': {'webhooks': webhooks},
        'gamification': {'leaderboard': leaderboard}
    }

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown(f"<div style='display: flex; align-items: center;'><span class='live-indicator'></span><span style='font-weight: bold;'>LIVE</span><span style='margin-left: 10px; color: #666;'>{datetime.now().strftime('%H:%M:%S')}</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 class='main-header'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)
with col3:
    auto_refresh = st.checkbox("Auto-refresh (10s)", value=st.session_state.auto_refresh)
    if auto_refresh != st.session_state.auto_refresh:
        st.session_state.auto_refresh = auto_refresh
        st.rerun()

# Navigation
st.markdown("---")
nav_cols = st.columns(6)
nav_items = [
    ("🏠", "Home", "Dashboard"),
    ("🏆", "Leaderboard", "Rankings"),
    ("📊", "Analytics", "Deep Dive"),
    ("📞", "Vishing", "Calls"),
    ("⛓️", "Blockchain", "Certs"),
    ("📱", "Mobile", "Devices")
]

for idx, (icon, name, desc) in enumerate(nav_items):
    with nav_cols[idx]:
        if st.button(f"{icon}\n{name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

st.markdown("---")

# Fetch data
try:
    data = fetch_realtime_data()
    backend_connected = any([data['vishing'], data['blockchain'], data['mobile'], 
                            data['integrations'], data['gamification']])
    st.session_state.backend_connected = backend_connected
except:
    data = generate_mock_data()
    st.session_state.backend_connected = False

# Update historical data
if data['vishing']:
    st.session_state.historical_data['timestamps'].append(datetime.now())
    st.session_state.historical_data['calls'].append(len(data['vishing'].get('active_calls', [])))
    st.session_state.historical_data['certificates'].append(data['blockchain'].get('total_certificates', 0) if data['blockchain'] else 0)
    st.session_state.historical_data['devices'].append(len(data['mobile'].get('devices', [])) if data['mobile'] else 0)
    
    # Keep last 20 data points
    for key in ['timestamps', 'calls', 'certificates', 'devices']:
        if len(st.session_state.historical_data[key]) > 20:
            st.session_state.historical_data[key] = st.session_state.historical_data[key][-20:]

# ==================== HOME PAGE ====================
if st.session_state.page == "Home":
    st.markdown("## 📊 Real-Time Operations Dashboard")
    
    # KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_calls = len(data['vishing'].get('active_calls', [])) if data['vishing'] else 0
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>📞 Active Vishing Calls</div>
            <div class='metric-value'>{active_calls}</div>
            <div class='metric-trend'>🔴 {random.randint(0, active_calls)} high risk</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Details", key="btn_calls", use_container_width=True):
            st.session_state.page = "Vishing"
            st.rerun()
    
    with col2:
        total_certs = data['blockchain'].get('total_certificates', 0) if data['blockchain'] else 0
        verified = data['blockchain'].get('verified_certificates', 0) if data['blockchain'] else 0
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>⛓️ Blockchain Certificates</div>
            <div class='metric-value'>{total_certs:,}</div>
            <div class='metric-trend'>✅ {verified} verified</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Certificates", key="btn_certs", use_container_width=True):
            st.session_state.page = "Blockchain"
            st.rerun()
    
    with col3:
        devices = data['mobile'].get('devices', []) if data['mobile'] else []
        active_devices = len([d for d in devices if d.get('status') == 'active'])
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>📱 Mobile Devices</div>
            <div class='metric-value'>{len(devices)}</div>
            <div class='metric-trend'>📊 {active_devices} active</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Manage Devices", key="btn_devices", use_container_width=True):
            st.session_state.page = "Mobile"
            st.rerun()
    
    with col4:
        webhooks = data['integrations'].get('webhooks', []) if data['integrations'] else []
        active_webhooks = len([w for w in webhooks if w.get('status') == 'active'])
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>🔌 Active Webhooks</div>
            <div class='metric-value'>{active_webhooks}</div>
            <div class='metric-trend'>⚡ {len(webhooks)} total</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Configure", key="btn_webhooks", use_container_width=True):
            st.session_state.page = "Integrations"
            st.rerun()
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'><span class='card-header-icon'>📈</span> Real-Time Activity Trends</div>", unsafe_allow_html=True)
        
        if len(st.session_state.historical_data['timestamps']) > 1:
            df_trends = pd.DataFrame({
                'Time': st.session_state.historical_data['timestamps'],
                'Active Calls': st.session_state.historical_data['calls'],
                'Certificates (scaled)': [c/100 for c in st.session_state.historical_data['certificates']],
                'Devices': st.session_state.historical_data['devices']
            })
            
            fig = px.line(df_trends, x='Time', y=['Active Calls', 'Certificates (scaled)', 'Devices'],
                         title='Last 20 Data Points',
                         labels={'value': 'Count', 'variable': 'Metric'})
            fig.update_layout(
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_traces(line=dict(width=3))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Collecting historical data...")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'><span class='card-header-icon'>🥧</span> Risk Distribution</div>", unsafe_allow_html=True)
        
        risk_data = pd.DataFrame({
            'Risk': ['Low', 'Medium', 'High'],
            'Count': [random.randint(20, 50), random.randint(30, 60), random.randint(10, 30)]
        })
        
        fig = px.pie(risk_data, values='Count', names='Risk', 
                     title='Call Risk Analysis',
                     color_discrete_map={'Low':'#00ff00', 'Medium':'#ffaa00', 'High':'#ff4444'},
                     hole=0.4)
        fig.update_layout(height=350, showlegend=True)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Activity Feed
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'><span class='card-header-icon'>🔔</span> Live Activity Feed</div>", unsafe_allow_html=True)
        
        activities = [
            {"time": "Just now", "icon": "📞", "title": "New vishing call detected", "desc": f"+1-555-{random.randint(1000,9999)} - Risk: {random.choice(['Low', 'Medium', 'High'])}"},
            {"time": "2 min ago", "icon": "⛓️", "title": "Certificate issued", "desc": f"Phishing Expert - {random.choice(['Alex', 'Jordan', 'Casey'])}"},
            {"time": "5 min ago", "icon": "📱", "title": "Device synced", "desc": f"{random.choice(['iPhone 14 Pro', 'Pixel 7'])} - Battery {random.randint(60,100)}%"},
            {"time": "8 min ago", "icon": "🏆", "title": "Badge earned", "desc": f"{random.choice(['Streak Master', 'Early Bird', 'Phishing Expert'])}"},
            {"time": "12 min ago", "icon": "🔌", "title": "Webhook triggered", "desc": f"{random.choice(['Slack', 'Teams'])} - {random.randint(1,20)} events"}
        ]
        
        for act in activities:
            risk_class = ""
            if "High" in act['desc']:
                risk_class = "status-danger"
            elif "Medium" in act['desc']:
                risk_class = "status-warning"
            
            st.markdown(f"""
            <div class='activity-item'>
                <div class='activity-icon'>{act['icon']}</div>
                <div class='activity-content'>
                    <div class='activity-title'>{act['title']}</div>
                    <div style='display: flex; justify-content: space-between;'>
                        <span>{act['desc']}</span>
                        <span class='activity-time'>{act['time']}</span>
                    </div>
                </div>
                {f"<span class='status-badge {risk_class}' style='margin-left: 10px;'>{act['desc'].split('Risk: ')[-1] if 'Risk:' in act['desc'] else ''}</span>" if risk_class else ""}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'><span class='card-header-icon'>⚡</span> Quick Actions</div>", unsafe_allow_html=True)
        
        if st.button("🎯 Start Challenge", use_container_width=True):
            st.info("Challenge started! Complete 5 phishing tests today.")
        
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Generating PDF report...")
        
        if st.button("🔍 Run Security Scan", use_container_width=True):
            st.warning("Scanning for vulnerabilities...")
        
        if st.button("📱 Send Test Notification", use_container_width=True):
            st.success("Test notification sent to all devices!")
        
        if st.button("🔄 Sync All Integrations", use_container_width=True):
            with st.spinner("Syncing..."):
                time.sleep(2)
                st.success("All integrations synced!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; padding: 1rem;'>"
    "© 2026 Phishing Simulation Platform | Real-Time Operations Dashboard"
    "</div>",
    unsafe_allow_html=True
)
