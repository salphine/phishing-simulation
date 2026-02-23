import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

st.set_page_config(page_title="Phishing Platform", page_icon="🎣", layout="wide")

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

# API Documentation links
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
    st.session_state.page = "Home"  # Default to Home

# Function to call API
def call_api(endpoint_type, method="GET", data=None):
    if not backend_connected or endpoint_type not in available_endpoints:
        return None
    
    endpoint = available_endpoints[endpoint_type]
    url = f"{API_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=3)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=3)
        else:
            return None
            
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Login function
def do_login(username, password):
    if not backend_connected:
        if username == "demo_user" and password == "password":
            st.session_state.logged_in = True
            st.session_state.username = username
            return True, "Demo mode - backend not connected"
        return False, "Backend not connected"
    
    try:
        response = requests.post(
            f"{API_URL}/auth/demo-login",
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                st.session_state.logged_in = True
                st.session_state.username = data.get("username", username)
                return True, "Login successful"
            else:
                return False, data.get("message", "Login failed")
        else:
            return False, f"Login failed (status {response.status_code})"
    except Exception as e:
        return False, f"Connection error: {e}"

# Main UI
st.title("🎣 Phishing Simulation Platform")

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login")
        
        if backend_connected:
            st.success("✅ Backend connected - using live data")
        else:
            st.warning("⚠️ Backend not connected - using demo mode")
        
        with st.form("login_form"):
            username = st.text_input("Username", value="demo_user")
            password = st.text_input("Password", type="password", value="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                success, message = do_login(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        st.markdown("---")
        st.markdown("**Demo credentials:** demo_user / password")
else:
    st.success(f"✅ Logged in as {st.session_state.username}")
    
    # Navigation
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with col2:
        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.page = "Leaderboard"
            st.rerun()
    with col3:
        if st.button("📊 Stats", use_container_width=True):
            st.session_state.page = "Stats"
            st.rerun()
    with col4:
        if st.button("📞 Vishing", use_container_width=True):
            st.session_state.page = "Vishing"
            st.rerun()
    with col5:
        if st.button("📚 API Docs", use_container_width=True):
            st.session_state.page = "API Docs"
            st.rerun()
    
    st.markdown("---")
    
    # ==================== HOME PAGE ====================
    if st.session_state.page == "Home":
        st.markdown("## 📊 Real-Time Dashboard")
        st.markdown(f"### 👋 Welcome back, {st.session_state.username}!")
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            with st.container():
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;'>
                    <div style='font-size: 1rem; opacity: 0.9;'>📞 Active Calls</div>
                    <div style='font-size: 2.5rem; font-weight: bold; margin: 0.5rem 0;'>3</div>
                    <div>🚨 Real-time monitoring</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;'>
                    <div style='font-size: 1rem; opacity: 0.9;'>⛓️ Certificates</div>
                    <div style='font-size: 2.5rem; font-weight: bold; margin: 0.5rem 0;'>1,234</div>
                    <div>✅ Blockchain verified</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            with st.container():
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;'>
                    <div style='font-size: 1rem; opacity: 0.9;'>📱 Devices</div>
                    <div style='font-size: 2.5rem; font-weight: bold; margin: 0.5rem 0;'>2</div>
                    <div>📊 2 active</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            with st.container():
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;'>
                    <div style='font-size: 1rem; opacity: 0.9;'>🔌 Webhooks</div>
                    <div style='font-size: 2.5rem; font-weight: bold; margin: 0.5rem 0;'>5</div>
                    <div>⚡ Active integrations</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin-bottom: 1rem;'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem; border-bottom: 2px solid #FF4B4B; padding-bottom: 0.5rem;'>📈 Activity Overview</div>", unsafe_allow_html=True)
            
            # Sample activity data
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
            st.markdown("<div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin-bottom: 1rem;'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem; border-bottom: 2px solid #FF4B4B; padding-bottom: 0.5rem;'>⚠️ Risk Distribution</div>", unsafe_allow_html=True)
            
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
        st.markdown("<div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin-bottom: 1rem;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem; border-bottom: 2px solid #FF4B4B; padding-bottom: 0.5rem;'>📋 Recent Activity</div>", unsafe_allow_html=True)
        
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
        
        data = {
            'Rank': ['🥇', '🥈', '🥉', '4th', '5th', '6th', '7th', '8th', '9th', '10th'],
            'User': ['Alex T.', 'Jordan L.', 'Casey M.', 'Riley C.', 'Taylor S.',
                    'Jamie F.', 'Quinn W.', 'Avery J.', 'Parker L.', 'Morgan F.'],
            'Points': [4850, 4620, 4390, 4120, 3980, 3750, 3520, 3280, 3050, 2890],
            'Level': [15, 14, 13, 13, 12, 11, 11, 10, 9, 9]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ==================== STATS PAGE ====================
    elif st.session_state.page == "Stats":
        st.markdown("## 📊 Your Statistics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Level", "7")
        with col2:
            st.metric("Total Points", "2,450")
        with col3:
            st.metric("Current Streak", "15 days")
        
        st.progress(0.75, text="75% to Level 8 (250 points needed)")

    # ==================== VISHING PAGE ====================
    elif st.session_state.page == "Vishing":
        st.markdown("## 📞 Vishing Protection")
        
        calls = [
            {"caller": "+1-555-0123", "risk": "Medium", "duration": "3:45"},
            {"caller": "+1-555-7890", "risk": "High", "duration": "2:30"},
            {"caller": "+1-555-4567", "risk": "Low", "duration": "1:15"}
        ]
        
        for call in calls:
            st.info(f"📞 {call['caller']} - {call['risk']} Risk - {call['duration']}")

    # ==================== API DOCS PAGE ====================
    elif st.session_state.page == "API Docs":
        st.markdown("## 📚 API Documentation")
        st.markdown("### Interactive API Explorer")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🔷 Swagger UI")
            st.markdown("Interactive documentation where you can test API calls directly:")
            st.link_button(
                "🚀 Open Swagger UI",
                "https://phishing-simulation-6.onrender.com/docs",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            st.markdown("#### 📖 ReDoc")
            st.markdown("Clean, three-panel documentation for reference:")
            st.link_button(
                "📚 Open ReDoc",
                "https://phishing-simulation-6.onrender.com/redoc",
                use_container_width=True
            )
        
        st.markdown("---")
        st.markdown("### 🔍 Available Endpoints")
        if available_endpoints:
            for key, value in available_endpoints.items():
                st.code(f"{key}: {value}", language="text")
    
    # Logout button
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()
