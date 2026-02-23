import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

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
    
    # Enhanced navigation with API Docs
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "Home"
    with col2:
        if st.button("🏆 Leaderboard"):
            st.session_state.page = "Leaderboard"
    with col3:
        if st.button("📊 Stats"):
            st.session_state.page = "Stats"
    with col4:
        if st.button("📞 Vishing"):
            st.session_state.page = "Vishing"
    with col5:
        if st.button("📚 API Docs"):
            st.session_state.page = "API Docs"
    
    st.markdown("---")
    
    # Page content
    if st.session_state.page == "Home":
        st.markdown("### Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Calls", "3")
        with col2:
            st.metric("Certificates", "1,234")
        with col3:
            st.metric("Devices", "2")
        with col4:
            st.metric("Webhooks", "5")
    
    elif st.session_state.page == "Leaderboard" and backend_connected:
        data = call_api("gamification", "GET")
        if data and 'leaderboard' in data:
            df = pd.DataFrame(data['leaderboard'])
            st.dataframe(df)
        else:
            st.info("Leaderboard data not available")
    
    elif st.session_state.page == "Vishing" and backend_connected:
        data = call_api("vishing", "GET")
        if data:
            st.json(data)
        else:
            st.info("Vishing data not available")
    
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
        
        st.markdown("### ⚡ Quick Test")
        if st.button("Test API Connection", use_container_width=True):
            try:
                test = requests.get(f"{API_URL}/test", timeout=3)
                if test.status_code == 200:
                    st.success("✅ API is responding!")
                    st.json(test.json())
                else:
                    st.error(f"❌ API returned {test.status_code}")
            except Exception as e:
                st.error(f"❌ Connection failed: {e}")
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
