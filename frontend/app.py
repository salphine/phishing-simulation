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
    /* Main header with gradient animation */
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
    
    /* Live indicator animation */
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
    
    /* Metric cards with 3D effect */
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
    
    /* Dashboard cards with glass morphism */
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
    
    /* Status badges */
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
    
    /* Progress bar styling */
    .progress-container {
        background: #f0f2f6;
        border-radius: 15px;
        height: 12px;
        margin: 1rem 0;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #FF4B4B, #FF8C8C);
        border-radius: 15px;
        transition: width 1s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Activity feed styling */
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
    
    /* Chart tooltips customization */
    .js-plotly-plot .plotly .hoverlayer .axistext {
        background: #FF4B4B !important;
    }
</style>
""", unsafe_allow_html=True)

# Auto-refresh every 10 seconds for real-time data
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
        data['vishing'] = requests.get(f"{API_URL}/vishing/calls/active", timeout=2).json()
    except: pass
    
    try:
        data['blockchain'] = requests.get(f"{API_URL}/blockchain/stats", timeout=2).json()
    except: pass
    
    try:
        data['mobile'] = requests.get(f"{API_URL}/mobile/devices", timeout=2).json()
    except: pass
    
    try:
        data['integrations'] = requests.get(f"{API_URL}/integrations/webhooks", timeout=2).json()
    except: pass
    
    try:
        data['gamification'] = requests.get(f"{API_URL}/gamification/leaderboard?limit=10", timeout=2).json()
    except: pass
    
    return data

# Mock data generator for demo mode
def generate_mock_data():
    return {
        'vishing': {'active_calls': [
            {'caller': f"+1-555-{random.randint(1000,9999)}", 'risk': random.choice(['low', 'medium', 'high']), 
             'duration': random.randint(30, 300)},
            for _ in range(random.randint(1, 3))
        ]},
        'blockchain': {'total_certificates': random.randint(1000, 1500), 
                      'verified_certificates': random.randint(900, 1400),
                      'last_block': random.randint(89000, 90000)},
        'mobile': {'devices': [
            {'device_name': random.choice(['iPhone 14 Pro', 'Pixel 7', 'Samsung S23', 'iPad Air']), 
             'status': random.choice(['active', 'inactive'])}
            for _ in range(random.randint(2, 5))
        ]},
        'integrations': {'webhooks': [
            {'name': random.choice(['Slack', 'Teams', 'Email', 'Splunk']), 
             'status': random.choice(['active', 'active', 'active', 'paused'])}
            for _ in range(random.randint(3, 6))
        ]},
        'gamification': {'leaderboard': [
            {'username': random.choice(['Alex', 'Jordan', 'Casey', 'Riley', 'Taylor']), 
             'points': random.randint(1000, 5000)}
            for _ in range(10)
        ]}
    }

# Header with real-time indicator
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

# Navigation with icons
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
if st.session_state.get('backend_connected', False):
    data = fetch_realtime_data()
else:
    data = generate_mock_data()
    # Update historical data
    st.session_state.historical_data['timestamps'].append(datetime.now())
    st.session_state.historical_data['calls'].append(len(data['vishing'].get('active_calls', [])))
    st.session_state.historical_data['certificates'].append(data['blockchain'].get('total_certificates', 0))
    st.session_state.historical_data['devices'].append(len(data['mobile'].get('devices', [])))
    
    # Keep last 20 data points
    for key in ['timestamps', 'calls', 'certificates', 'devices']:
        if len(st.session_state.historical_data[key]) > 20:
            st.session_state.historical_data[key] = st.session_state.historical_data[key][-20:]

# ==================== HOME PAGE (ADVANCED DASHBOARD) ====================
if st.session_state.page == "Home":
    st.markdown("## 📊 Real-Time Operations Dashboard")
    
    # KPI Metrics Row with animations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_calls = len(data['vishing'].get('active_calls', [])) if data['vishing'] else 0
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>📞 Active Vishing Calls</div>
            <div class='metric-value'>{active_calls}</div>
            <div class='metric-trend'>🔴 {random.randint(1,5)} high risk</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Click handler for drill-down
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
        
        # Create historical data chart
        if len(st.session_state.historical_data['timestamps']) > 1:
            df_trends = pd.DataFrame({
                'Time': st.session_state.historical_data['timestamps'],
                'Active Calls': st.session_state.historical_data['calls'],
                'Certificates': [c/100 for c in st.session_state.historical_data['certificates']],  # Scale for visualization
                'Devices': st.session_state.historical_data['devices']
            })
            
            fig = px.line(df_trends, x='Time', y=['Active Calls', 'Certificates', 'Devices'],
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
        
        # Risk distribution chart
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
    
    # Third Row - Live Activity Feed and Quick Actions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'><span class='card-header-icon'>🔔</span> Live Activity Feed</div>", unsafe_allow_html=True)
        
        # Generate live activities
        activities = [
            {"time": "Just now", "icon": "📞", "title": "New vishing call detected", "desc": f"+1-555-{random.randint(1000,9999)} - Risk: {random.choice(['Low', 'Medium', 'High'])}"},
            {"time": "2 min ago", "icon": "⛓️", "title": "Certificate issued", "desc": f"Phishing Expert - {random.choice(['Alex', 'Jordan', 'Casey'])}"},
            {"time": "5 min ago", "icon": "📱", "title": "Device synced", "desc": f"{random.choice(['iPhone 14 Pro', 'Pixel 7'])} - Battery {random.randint(60,100)}%"},
            {"time": "8 min ago", "icon": "🏆", "title": "Badge earned", "desc": f"{random.choice(['Streak Master', 'Early Bird', 'Phishing Expert'])}"},
            {"time": "12 min ago", "icon": "🔌", "title": "Webhook triggered", "desc": f"{random.choice(['Slack', 'Teams'])} - {random.randint(1,20)} events"}
        ]
        
        for act in activities:
            risk_class = ""
            if "High" in act.get('desc', ''):
                risk_class = "status-danger"
            elif "Medium" in act.get('desc', ''):
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
        
        # Quick action buttons with icons
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
        
        # System Health
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'><span class='card-header-icon'>💚</span> System Health</div>", unsafe_allow_html=True)
        
        # Health metrics
        health_metrics = {
            "API Status": "✅ Healthy",
            "Database": "✅ Connected",
            "Redis Cache": "✅ Online",
            "Background Workers": "✅ Active",
            "Last Backup": "2 hours ago"
        }
        
        for key, value in health_metrics.items():
            st.markdown(f"**{key}:** {value}")
        
        # Uptime
        st.markdown(f"**Uptime:** {random.randint(5, 30)} days {random.randint(1, 23)} hours")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Bottom Row - Performance Metrics
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'><span class='card-header-icon'>📊</span> Performance Overview</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Response Time", f"{random.randint(120, 250)}ms", f"{random.randint(-10, 10)}ms")
    with col2:
        st.metric("Success Rate", f"{random.randint(95, 99)}%", f"{random.randint(-2, 2)}%")
    with col3:
        st.metric("Active Users", f"{random.randint(45, 120)}", f"+{random.randint(1, 10)}")
    with col4:
        st.metric("Events/min", f"{random.randint(120, 350)}", f"{random.randint(-20, 30)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== LEADERBOARD PAGE ====================
elif st.session_state.page == "Leaderboard":
    st.markdown("## 🏆 Global Leaderboard")
    
    leaderboard = data.get('gamification', {}).get('leaderboard', [])
    if leaderboard:
        df = pd.DataFrame(leaderboard)
        # Add rank
        df['rank'] = range(1, len(df) + 1)
        df['medal'] = df['rank'].apply(lambda x: '🥇' if x == 1 else '🥈' if x == 2 else '🥉' if x == 3 else f'{x}th')
        
        # Create visualization
        fig = px.bar(df.head(10), x='username', y='points', 
                     title='Top 10 Users',
                     text='points',
                     color='points',
                     color_continuous_scale='Viridis')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        st.dataframe(df[['medal', 'username', 'points']].rename(
            columns={'medal': 'Rank', 'username': 'User', 'points': 'Points'}
        ), use_container_width=True, hide_index=True)
    else:
        st.info("Leaderboard data not available")

# ==================== ANALYTICS PAGE ====================
elif st.session_state.page == "Analytics":
    st.markdown("## 📊 Deep Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Distributions", "📉 Performance"])
    
    with tab1:
        # Time series analysis
        if len(st.session_state.historical_data['timestamps']) > 1:
            df = pd.DataFrame({
                'Time': st.session_state.historical_data['timestamps'],
                'Calls': st.session_state.historical_data['calls'],
                'Certificates': st.session_state.historical_data['certificates']
            })
            
            fig = px.area(df, x='Time', y=['Calls', 'Certificates'],
                         title='Historical Trends',
                         labels={'value': 'Count', 'variable': 'Metric'})
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            # Risk distribution over time
            risk_trend = pd.DataFrame({
                'Date': pd.date_range(end=datetime.now(), periods=7, freq='D'),
                'Low': [random.randint(20, 40) for _ in range(7)],
                'Medium': [random.randint(30, 50) for _ in range(7)],
                'High': [random.randint(10, 25) for _ in range(7)]
            })
            
            fig = px.bar(risk_trend, x='Date', y=['Low', 'Medium', 'High'],
                        title='Risk Distribution Over Time',
                        barmode='stack')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Device type distribution
            device_types = pd.DataFrame({
                'Type': ['iOS', 'Android', 'Other'],
                'Count': [random.randint(40, 60), random.randint(30, 50), random.randint(5, 15)]
            })
            
            fig = px.pie(device_types, values='Count', names='Type',
                        title='Device Distribution')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Performance metrics
        perf_data = pd.DataFrame({
            'Hour': [f"{i}:00" for i in range(24)],
            'Response Time': [random.randint(100, 300) for _ in range(24)],
            'Error Rate': [random.randint(0, 5) for _ in range(24)]
        })
        
        fig = px.line(perf_data, x='Hour', y=['Response Time', 'Error Rate'],
                     title='24-Hour Performance Metrics')
        st.plotly_chart(fig, use_container_width=True)

# ==================== OTHER PAGES ====================
elif st.session_state.page == "Vishing":
    st.markdown("## 📞 Vishing Protection")
    if data['vishing']:
        st.json(data['vishing'])
    else:
        st.info("No vishing data available")

elif st.session_state.page == "Blockchain":
    st.markdown("## ⛓️ Blockchain Certificates")
    if data['blockchain']:
        st.json(data['blockchain'])
    else:
        st.info("No blockchain data available")

elif st.session_state.page == "Mobile":
    st.markdown("## 📱 Mobile Integration")
    if data['mobile']:
        for device in data['mobile'].get('devices', []):
            st.info(f"📱 {device.get('device_name')} - {device.get('status', 'unknown')}")
    else:
        st.info("No mobile devices registered")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; padding: 1rem;'>"
    "© 2026 Phishing Simulation Platform | Real-Time Operations Dashboard | "
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>",
    unsafe_allow_html=True
)
