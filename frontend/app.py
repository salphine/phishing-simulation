import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Phishing Platform", page_icon="🎣", layout="wide")

# Get API URL from secrets
try:
    API_URL = st.secrets["API_URL"].rstrip('/')  # Remove trailing slash if any
    st.sidebar.success(f"✅ API URL: {API_URL}")
except:
    API_URL = "https://phishing-simulation-6.onrender.com/api"
    st.sidebar.warning("⚠️ Using default API URL")

# Test different endpoints to find the correct health check path
endpoints_to_test = [
    "/health",
    "/api/health",
    "/",
    "/api/test"
]

health_ok = False
for endpoint in endpoints_to_test:
    try:
        url = f"{API_URL}{endpoint}"
        st.sidebar.write(f"Testing: {url}")
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            st.sidebar.success(f"✅ Found working endpoint: {endpoint}")
            HEALTH_ENDPOINT = endpoint
            health_ok = True
            break
    except:
        continue

if not health_ok:
    st.sidebar.error("❌ Could not find working health endpoint")
    HEALTH_ENDPOINT = "/health"  # default

# Define correct endpoint paths based on your working tests
# From your curl test, these are working:
# - /api/health -> returns {"status":"healthy","service":"backend"}
# - /api/test -> returns API info
# - /api/auth/demo-login -> login works

# Set correct base paths
API_BASE = API_URL  # Already includes /api

# Test login endpoint explicitly
try:
    test_login = requests.post(
        f"{API_BASE}/auth/demo-login",
        json={"username": "demo_user", "password": "password"},
        timeout=3
    )
    if test_login.status_code == 200:
        st.sidebar.success("✅ Login endpoint working")
    else:
        st.sidebar.error(f"❌ Login endpoint returned {test_login.status_code}")
except Exception as e:
    st.sidebar.error(f"❌ Login test failed: {e}")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Function to make API calls with correct paths
def call_api(endpoint):
    """Call API with endpoint (should not include /api prefix)"""
    try:
        # Remove /api if present to avoid duplication
        if endpoint.startswith('/api/'):
            endpoint = endpoint[5:]
        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Login function
def do_login(username, password):
    try:
        response = requests.post(
            f"{API_BASE}/auth/demo-login",
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                st.session_state.logged_in = True
                st.session_state.username = data.get("username", username)
                return True, ""
            else:
                return False, data.get("message", "Login failed")
        else:
            return False, f"Login failed (status {response.status_code})"
    except Exception as e:
        return False, f"Connection error: {e}"

# Rest of your app code (keep your existing UI code below)
# ... 

# For now, add a simple test UI
st.title("🎣 Phishing Simulation Platform")

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", value="demo_user")
            password = st.text_input("Password", type="password", value="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                success, message = do_login(username, password)
                if success:
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(message)
else:
    st.success(f"✅ Logged in as {st.session_state.username}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
