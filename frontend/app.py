import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# Page configuration - MUST be first
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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# IMPORTANT: Use your live Render backend
# For production, use the Render URL
API_URL = "https://phishing-simulation-6.onrender.com/api"

# For local testing only, uncomment this line:
# API_URL = "http://127.0.0.1:8000/api"

# Test connection on startup
try:
    test_response = requests.get(f"{API_URL}/health", timeout=5)
    if test_response.status_code == 200:
        print("✅ Backend connected successfully")
    else:
        print(f"⚠️ Backend returned status {test_response.status_code}")
except Exception as e:
    print(f"⚠️ Backend connection failed: {e}")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Function to call API
def call_api(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=3)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Simple login function
def do_login(username, password):
    if username == "demo_user" and password == "password":
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    elif username == "admin" and password == "admin":
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

# Login page
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-header'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='background:white; padding:2rem; border-radius:15px; box-shadow:0 10px 30px rgba(0,0,0,0.2);'>", unsafe_allow_html=True)
        st.markdown("### 🔐 Login")
        
        # Show backend status
        try:
            health = requests.get(f"{API_URL}/health", timeout=2)
            if health.status_code == 200:
                st.success("✅ Backend connected")
            else:
                st.warning("⚠️ Backend connection issue - using demo mode")
        except:
            st.warning("⚠️ Backend connection issue - using demo mode")
        
        with st.form("login_form"):
            username = st.text_input("Username", value="demo_user")
            password = st.text_input("Password", type="password", value="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                if do_login(username, password):
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.markdown("---")
        st.markdown("**Demo:** demo_user / password")
        st.markdown("**Admin:** dmin / dmin")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Main app
st.markdown("<h1 class='main-header'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)
st.markdown(f"### 👋 Welcome, {st.session_state.username}!")

# Simple navigation
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
with col2:
    if st.button("🏆 Leaderboard", use_container_width=True):
        st.session_state.page = "Leaderboard"
with col3:
    if st.button("📊 Stats", use_container_width=True):
        st.session_state.page = "Stats"
with col4:
    if st.button("📞 Vishing", use_container_width=True):
        st.session_state.page = "Vishing"

st.markdown("---")

# Home page
if st.session_state.page == "Home":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>3</div>
            <div>Active Calls</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>1,234</div>
            <div>Certificates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>2</div>
            <div>Devices</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>5</div>
            <div>Webhooks</div>
        </div>
        """, unsafe_allow_html=True)

# Leaderboard page
elif st.session_state.page == "Leaderboard":
    st.markdown("### Leaderboard")
    data = {
        'Rank': ['🥇', '🥈', '🥉', '4th', '5th'],
        'User': ['Alex T.', 'Jordan L.', 'Casey M.', 'Riley C.', 'Taylor S.'],
        'Points': [4850, 4620, 4390, 4120, 3980]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Stats page
elif st.session_state.page == "Stats":
    st.markdown("### Your Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Level", "7")
    with col2:
        st.metric("Points", "2,450")
    with col3:
        st.metric("Streak", "15 days")

# Vishing page
elif st.session_state.page == "Vishing":
    st.markdown("### Vishing Protection")
    calls = [
        {"caller": "+1-555-0123", "risk": "Medium"},
        {"caller": "+1-555-7890", "risk": "High"}
    ]
    for call in calls:
        st.info(f"📞 {call['caller']} - {call['risk']} Risk")

# Logout
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown(f"**User:** {st.session_state.username}")
