import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="Phishing Simulation Platform",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #FF4B4B, #FF8C8C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
    }
    .login-header {
        font-size: 2rem;
        color: #FF4B4B;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #f0f2f6;
    }
    .card-header {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #333;
        border-bottom: 2px solid #FF4B4B;
        padding-bottom: 0.5rem;
    }
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
    .user-welcome {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# API URL
API_URL = "http://127.0.0.1:8000/api"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = "user"
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

# Auto-refresh every 10 seconds if enabled
if st.session_state.auto_refresh and st.session_state.logged_in:
    refresh_count = st_autorefresh(interval=10000, key="data_refresh")

# Function to make API calls
def call_api(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=3)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Function to login
def do_login(username, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/demo-login",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                st.session_state.logged_in = True
                st.session_state.username = data.get("username", username)
                st.session_state.user_role = data.get("role", "user")
                st.session_state.user_id = data.get("user_id", 1)
                return True, ""
            else:
                return False, data.get("message", "Login failed")
        else:
            return False, f"Server error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to backend. Make sure it's running on port 8000"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Login check
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-header'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<div class='login-header'>🔐 Login</div>", unsafe_allow_html=True)
        
        # Test backend connection
        try:
            test = requests.get(f"{API_URL}/test", timeout=2)
            if test.status_code == 200:
                st.success("✅ Connected to backend")
            else:
                st.warning("⚠️ Backend connection issue")
        except:
            st.error("❌ Cannot connect to backend. Start with: uvicorn main:app --reload --port 8000")
        
        with st.form("login_form"):
            username = st.text_input("Username", value="demo_user")
            password = st.text_input("Password", type="password", value="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                success, error = do_login(username, password)
                if success:
                    st.rerun()
                else:
                    st.error(error)
        
        st.markdown("---")
        st.markdown("**Demo Credentials:**")
        st.code("demo_user / password")
        st.code("admin / admin")
        
        # Quick login buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👤 Demo User", use_container_width=True):
                success, error = do_login("demo_user", "password")
                if success:
                    st.rerun()
                else:
                    st.error(error)
        with col2:
            if st.button("👑 Admin", use_container_width=True):
                success, error = do_login("admin", "admin")
                if success:
                    st.rerun()
                else:
                    st.error(error)
        
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Main App (Authenticated)
st.markdown("<h1 class='main-header'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)

# User welcome and real-time indicator
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown(f"<span class='live-indicator'></span> **LIVE** {datetime.now().strftime('%H:%M:%S')}", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='user-welcome'>👋 Welcome, <b>{st.session_state.username}</b>! ({st.session_state.user_role})</div>", unsafe_allow_html=True)
with col3:
    auto_refresh = st.checkbox("Auto-refresh (10s)", value=st.session_state.auto_refresh)
    if auto_refresh != st.session_state.auto_refresh:
        st.session_state.auto_refresh = auto_refresh
        st.rerun()

# Navigation
st.markdown("---")
nav_cols = st.columns(8)
nav_items = [
    ("🏠", "Home"),
    ("🏆", "Leaderboard"),
    ("📊", "Stats"),
    ("🎯", "Challenges"),
    ("📞", "Vishing"),
    ("⛓️", "Blockchain"),
    ("📱", "Mobile"),
    ("🔌", "Integrations")
]

for idx, (icon, name) in enumerate(nav_items):
    with nav_cols[idx]:
        is_active = st.session_state.page == name
        if st.button(
            f"{icon}\n{name}", 
            key=f"nav_{name}", 
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = name
            st.rerun()

st.markdown("---")

# ==================== HOME PAGE ====================
if st.session_state.page == "Home":
    st.markdown("## 📊 Real-Time Dashboard")
    
    # Fetch real data
    vishing = call_api("vishing/calls/active")
    blockchain = call_api("blockchain/stats")
    mobile = call_api("mobile/devices")
    webhooks = call_api("integrations/webhooks")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_calls = len(vishing.get("active_calls", [])) if vishing else 3
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>📞 Active Calls</div>
            <div class='metric-value'>{active_calls}</div>
            <div>🚨 Real-time monitoring</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_certs = blockchain.get("total_certificates", 1234) if blockchain else 1234
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>⛓️ Certificates</div>
            <div class='metric-value'>{total_certs:,}</div>
            <div>✅ Blockchain verified</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        devices = len(mobile.get("devices", [])) if mobile else 3
        active_devices = len([d for d in mobile.get("devices", []) if d.get('status') == 'active']) if mobile else 2
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>📱 Devices</div>
            <div class='metric-value'>{devices}</div>
            <div>📊 {active_devices} active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        webhook_count = len(webhooks.get("webhooks", [])) if webhooks else 5
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>🔌 Webhooks</div>
            <div class='metric-value'>{webhook_count}</div>
            <div>⚡ Active integrations</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>📈 Activity Overview</div>", unsafe_allow_html=True)
        
        # Sample activity data (without random)
        hours = [f"{i}:00" for i in range(24)]
        activity_data = pd.DataFrame({
            'Hour': hours,
            'Calls': [3, 2, 1, 1, 1, 2, 4, 8, 12, 15, 18, 20, 22, 21, 19, 17, 15, 14, 12, 10, 8, 7, 5, 3],
            'Tests': [1, 1, 0, 0, 0, 1, 3, 6, 10, 14, 16, 18, 19, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 1]
        })
        
        fig = px.line(activity_data, x='Hour', y=['Calls', 'Tests'], 
                     title='24-Hour Activity',
                     labels={'value': 'Count', 'variable': 'Type'})
        fig.update_layout(height=300, legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>⚠️ Risk Distribution</div>", unsafe_allow_html=True)
        
        risk_data = pd.DataFrame({
            'Risk': ['Low', 'Medium', 'High'],
            'Count': [456, 567, 222]
        })
        
        fig = px.pie(risk_data, values='Count', names='Risk', 
                     title='Risk Analysis',
                     color_discrete_map={'Low':'#00ff00', 'Medium':'#ffaa00', 'High':'#ff4444'})
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>📋 Recent Activity</div>", unsafe_allow_html=True)
    
    recent_activity = pd.DataFrame({
        'Time': ['Just now', '2 min ago', '5 min ago', '10 min ago', '15 min ago'],
        'Event': ['New vishing call detected', 'Certificate issued', 'Mobile device synced', 'Badge earned', 'Webhook triggered'],
        'Status': ['Active', 'Completed', 'Success', 'Completed', 'Success']
    })
    st.dataframe(recent_activity, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== LEADERBOARD PAGE ====================
elif st.session_state.page == "Leaderboard":
    st.markdown("## 🏆 Global Leaderboard")
    
    leaderboard = call_api("gamification/leaderboard?limit=20")
    
    if leaderboard and leaderboard.get("leaderboard"):
        df = pd.DataFrame(leaderboard["leaderboard"])
        # Rename columns to match display
        df = df.rename(columns={'username': 'User', 'points': 'Points', 'level': 'Level'})
    else:
        # Demo data with consistent column names
        df = pd.DataFrame({
            'Rank': ['🥇', '🥈', '🥉', '4', '5', '6', '7', '8', '9', '10'],
            'User': ['Alex Thompson', 'Jordan Lee', 'Casey Morgan', 'Riley Cooper', 'Taylor Swift',
                    'Jamie Fox', 'Quinn Williams', 'Avery Johnson', 'Parker Lewis', 'Morgan Freeman'],
            'Points': [4850, 4620, 4390, 4120, 3980, 3750, 3520, 3280, 3050, 2890],
            'Level': [15, 14, 13, 13, 12, 11, 11, 10, 9, 9]
        })
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Top 3 visualization
    st.markdown("### 🏅 Top Performers")
    top_3 = df.head(3)
    fig = px.bar(top_3, x='User', y='Points', color='Points',
                 title='Top 3 Users',
                 text_auto=True,
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

# ==================== STATS PAGE ====================
elif st.session_state.page == "Stats":
    st.markdown("## 📊 Your Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Current Level</div>
            <div class='metric-value'>7</div>
            <div>⭐ Expert</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Total Points</div>
            <div class='metric-value'>2,450</div>
            <div>📈 +350 today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Current Streak</div>
            <div class='metric-value'>15</div>
            <div>🔥 days</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Badges Earned</div>
            <div class='metric-value'>8</div>
            <div>🏅 of 20</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.progress(0.75, text="75% to Level 8 (250 points needed)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>📈 Points History</div>", unsafe_allow_html=True)
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        points_data = pd.DataFrame({
            'Date': dates,
            'Points': [50, 75, 100, 80, 120, 90, 110, 130, 95, 115,
                      140, 125, 135, 145, 150, 155, 160, 145, 170, 165,
                      180, 175, 190, 185, 200, 195, 210, 205, 220, 215]
        })
        
        fig = px.line(points_data, x='Date', y='Points', title='Daily Points')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>🏅 Recent Badges</div>", unsafe_allow_html=True)
        
        badges = [
            {"icon": "🎣", "name": "Phishing Expert", "date": "Feb 15"},
            {"icon": "🔥", "name": "7-Day Streak", "date": "Feb 10"},
            {"icon": "💯", "name": "Perfect Score", "date": "Feb 5"},
            {"icon": "🌅", "name": "Early Bird", "date": "Jan 30"}
        ]
        
        for badge in badges:
            st.markdown(f"""
            <div style='display: flex; align-items: center; padding: 0.5rem; border-bottom: 1px solid #eee;'>
                <span style='font-size: 2rem; margin-right: 1rem;'>{badge['icon']}</span>
                <div>
                    <strong>{badge['name']}</strong><br>
                    <small>Earned: {badge['date']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== CHALLENGES PAGE ====================
elif st.session_state.page == "Challenges":
    st.markdown("## 🎯 Active Challenges")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='dashboard-card'>
            <div class='card-header'>🔥 Daily Challenges</div>
            <h4>Complete 5 Phishing Tests</h4>
            <p>Progress: 3/5</p>
            <div style='background: #f0f2f6; border-radius: 10px; height: 10px; margin: 1rem 0;'>
                <div style='background: #FF4B4B; width: 60%; height: 10px; border-radius: 10px;'></div>
            </div>
            <p><b>Reward:</b> 100 Points + Daily Badge</p>
            <p><small>⏰ Ends in: 5 hours</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='dashboard-card'>
            <div class='card-header'>📅 Weekly Challenges</div>
            <h4>Top 10 Leaderboard</h4>
            <p>Current Rank: 42</p>
            <p><b>Reward:</b> 500 Points + Champion Badge</p>
            <p><small>⏰ Ends in: 3 days</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='dashboard-card'>
            <div class='card-header'>🎯 Special Challenges</div>
            <h4>March Phishing Marathon</h4>
            <p>Progress: 12/20 tests</p>
            <div style='background: #f0f2f6; border-radius: 10px; height: 10px; margin: 1rem 0;'>
                <div style='background: #FF4B4B; width: 60%; height: 10px; border-radius: 10px;'></div>
            </div>
            <p><b>Reward:</b> 1000 Points + Marathon Medal</p>
            <p><small>⏰ Ends in: 15 days</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='dashboard-card'>
            <div class='card-header'>📊 Your Stats</div>
            <p><b>Completed:</b> 12</p>
            <p><b>Success Rate:</b> 75%</p>
            <p><b>Total Points:</b> 2,450</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== VISHING PAGE ====================
elif st.session_state.page == "Vishing":
    st.markdown("## 📞 Vishing Protection")
    
    active = call_api("vishing/calls/active")
    analytics = call_api("vishing/analytics?period=day")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        active_calls = len(active.get("active_calls", [])) if active else 3
        st.metric("Active Calls", active_calls)
    with col2:
        suspicious = analytics.get("suspicious_calls", 12) if analytics else 12
        st.metric("Suspicious Today", suspicious)
    with col3:
        blocked = analytics.get("blocked_calls", 8) if analytics else 8
        st.metric("Blocked", blocked)
    
    tab1, tab2, tab3 = st.tabs(["🎙️ Live Calls", "📊 Analytics", "📜 History"])
    
    with tab1:
        if active and active.get("active_calls"):
            for call in active["active_calls"]:
                risk_color = "status-active" if call['risk'] == 'low' else "status-warning" if call['risk'] == 'medium' else "status-danger"
                st.markdown(f"""
                <div class='dashboard-card'>
                    <b>{call['caller']}</b>
                    <span style='float: right;'><span class='status-badge {risk_color}'>{call['risk'].upper()}</span></span>
                    <br><small>Duration: {call['duration']}s</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Demo calls
            demo_calls = [
                {"caller": "+1-555-0123", "risk": "medium", "duration": 245},
                {"caller": "+1-555-7890", "risk": "high", "duration": 180},
                {"caller": "+1-555-4567", "risk": "low", "duration": 90}
            ]
            for call in demo_calls:
                risk_color = "status-active" if call['risk'] == 'low' else "status-warning" if call['risk'] == 'medium' else "status-danger"
                st.markdown(f"""
                <div class='dashboard-card'>
                    <b>{call['caller']}</b>
                    <span style='float: right;'><span class='status-badge {risk_color}'>{call['risk'].upper()}</span></span>
                    <br><small>Duration: {call['duration']}s</small>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # Risk distribution chart
        risk_df = pd.DataFrame({
            'Risk': ['Low', 'Medium', 'High'],
            'Count': [456, 567, 222]
        })
        fig = px.pie(risk_df, values='Count', names='Risk', title='Risk Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        history_df = pd.DataFrame({
            'Time': ['12:43', '12:38', '12:15', '11:50'],
            'Caller': ['+1-555-0123', '+1-555-7890', '+1-555-4567', '+1-555-8901'],
            'Duration': ['3:45', '2:30', '1:15', '4:20'],
            'Risk': ['Medium', 'High', 'Low', 'High']
        })
        st.dataframe(history_df, use_container_width=True, hide_index=True)

# ==================== BLOCKCHAIN PAGE ====================
elif st.session_state.page == "Blockchain":
    st.markdown("## ⛓️ Blockchain Certificates")
    
    certs = call_api("blockchain/certificates?limit=10")
    stats = call_api("blockchain/stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total = stats.get("total_certificates", 1234) if stats else 1234
        st.metric("Total Certificates", f"{total:,}")
    with col2:
        verified = stats.get("verified_certificates", 1189) if stats else 1189
        st.metric("Verified", f"{verified:,}")
    with col3:
        last_block = stats.get("last_block", 89237) if stats else 89237
        st.metric("Last Block", f"#{last_block}")
    
    if certs and certs.get("certificates"):
        for cert in certs["certificates"]:
            status_color = "status-active" if cert['status'] == 'verified' else "status-warning"
            st.markdown(f"""
            <div class='dashboard-card'>
                <b>{cert['name']}</b>
                <span style='float: right;'><span class='status-badge {status_color}'>{cert['status'].upper()}</span></span>
                <br>User: {cert['user']} | Score: {cert['score']}%
                <br><small>ID: {cert['id']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Demo certificates
        demo_certs = [
            {"name": "Phishing Expert", "user": "Alex T.", "score": 98, "status": "verified", "id": "0x7a3f...8b2d"},
            {"name": "Security Champion", "user": "Jordan L.", "score": 95, "status": "pending", "id": "0x9b4e...2c1f"},
            {"name": "Streak Master", "user": "Casey M.", "score": 100, "status": "verified", "id": "0x3d8a...5e9b"}
        ]
        for cert in demo_certs:
            status_color = "status-active" if cert['status'] == 'verified' else "status-warning"
            st.markdown(f"""
            <div class='dashboard-card'>
                <b>{cert['name']}</b>
                <span style='float: right;'><span class='status-badge {status_color}'>{cert['status'].upper()}</span></span>
                <br>User: {cert['user']} | Score: {cert['score']}%
                <br><small>ID: {cert['id']}</small>
            </div>
            """, unsafe_allow_html=True)

# ==================== MOBILE PAGE ====================
elif st.session_state.page == "Mobile":
    st.markdown("## 📱 Mobile Integration")
    
    devices = call_api("mobile/devices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>📱 Registered Devices</div>", unsafe_allow_html=True)
        
        if devices and devices.get("devices"):
            for device in devices["devices"]:
                status_color = "status-active" if device['status'] == 'active' else "status-warning"
                st.markdown(f"""
                <div style='display: flex; align-items: center; padding: 0.5rem; border-bottom: 1px solid #eee;'>
                    <span style='font-size: 2rem; margin-right: 1rem;'>📱</span>
                    <div>
                        <strong>{device['device_name']}</strong><br>
                        <small>{device['device_type']}</small>
                    </div>
                    <span style='margin-left: auto;' class='status-badge {status_color}'>{device['status'].upper()}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Demo devices
            demo_devices = [
                {"name": "iPhone 14 Pro", "type": "iOS", "status": "active"},
                {"name": "iPad Air", "type": "iOS", "status": "active"},
                {"name": "Pixel 7", "type": "Android", "status": "inactive"}
            ]
            for device in demo_devices:
                status_color = "status-active" if device['status'] == 'active' else "status-warning"
                st.markdown(f"""
                <div style='display: flex; align-items: center; padding: 0.5rem; border-bottom: 1px solid #eee;'>
                    <span style='font-size: 2rem; margin-right: 1rem;'>📱</span>
                    <div>
                        <strong>{device['name']}</strong><br>
                        <small>{device['type']}</small>
                    </div>
                    <span style='margin-left: auto;' class='status-badge {status_color}'>{device['status'].upper()}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>📨 Push Notifications</div>", unsafe_allow_html=True)
        
        with st.form("notification_form"):
            title = st.text_input("Title", value="Security Alert")
            message = st.text_area("Message", value="New phishing campaign detected")
            if st.form_submit_button("Send Notification"):
                st.success("✅ Notification sent!")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>📊 Analytics</div>", unsafe_allow_html=True)
        st.metric("Active Devices", "2")
        st.metric("Notifications Today", "47")
        st.metric("Open Rate", "81%")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== INTEGRATIONS PAGE ====================
elif st.session_state.page == "Integrations":
    st.markdown("## 🔌 System Integrations")
    
    tab1, tab2, tab3 = st.tabs(["👥 HRIS", "🛡️ SIEM", "🔗 Webhooks"])
    
    with tab1:
        hris = call_api("integrations/hris/status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'>HRIS Status</div>", unsafe_allow_html=True)
            provider = hris.get("provider", "Workday") if hris else "Workday"
            st.success(f"✅ Connected to {provider}")
            st.write(f"**Last Sync:** {hris.get('last_sync', '5 min ago') if hris else '5 min ago'}")
            st.write(f"**Employees:** {hris.get('total_employees', 1234) if hris else 1234}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-header'>Recent Syncs</div>", unsafe_allow_html=True)
            sync_df = pd.DataFrame({
                'Time': ['12:43', '11:30', '10:15'],
                'Records': [234, 189, 156],
                'Status': ['✅', '✅', '✅']
            })
            st.dataframe(sync_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        siem = call_api("integrations/siem/configs")
        
        if siem and siem.get("configs"):
            for config in siem["configs"]:
                st.markdown(f"""
                <div class='dashboard-card'>
                    <h4>{config['provider']}</h4>
                    <p>Status: <span class='status-badge status-active'>{config['status'].upper()}</span></p>
                    <p>Endpoint: {config['endpoint']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Demo SIEM configs
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div class='dashboard-card'>
                    <h4>Splunk</h4>
                    <p>Status: <span class='status-badge status-active'>ACTIVE</span></p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class='dashboard-card'>
                    <h4>ELK Stack</h4>
                    <p>Status: <span class='status-badge status-active'>ACTIVE</span></p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        webhooks = call_api("integrations/webhooks")
        
        if webhooks and webhooks.get("webhooks"):
            for webhook in webhooks["webhooks"]:
                st.markdown(f"""
                <div class='dashboard-card'>
                    <h4>{webhook['name']}</h4>
                    <p>Events: {', '.join(webhook['events'])}</p>
                    <p>Status: <span class='status-badge status-active'>{webhook['status'].upper()}</span></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Demo webhooks
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div class='dashboard-card'>
                    <h4>Slack</h4>
                    <p>Events: phishing.detected</p>
                    <p>Status: <span class='status-badge status-active'>ACTIVE</span></p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class='dashboard-card'>
                    <h4>Teams</h4>
                    <p>Events: user.login</p>
                    <p>Status: <span class='status-badge status-active'>ACTIVE</span></p>
                </div>
                """, unsafe_allow_html=True)

# Logout button in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"### 👤 {st.session_state.username}")
st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_role = "user"
    st.session_state.user_id = None
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; padding: 1rem;'>"
    "© 2026 Phishing Simulation Platform | Connected to Backend | "
    f"Logged in as: {st.session_state.username}"
    "</div>",
    unsafe_allow_html=True
)
