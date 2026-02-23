import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Phishing Platform", page_icon="🎣", layout="wide")

# Debug section - show what's happening
st.sidebar.markdown("## 🔍 Debug Info")

# Try to get API URL from secrets
try:
    # List all secrets keys (without values)
    if hasattr(st, 'secrets') and st.secrets:
        st.sidebar.write("✅ Secrets found")
        if 'API_URL' in st.secrets:
            API_URL = st.secrets['API_URL']
            st.sidebar.write(f"API_URL: {API_URL}")
            
            # Test connection
            try:
                test = requests.get(f"{API_URL}/health", timeout=5)
                if test.status_code == 200:
                    st.sidebar.success("✅ Backend connected")
                    st.session_state.backend_ok = True
                else:
                    st.sidebar.error(f"❌ Backend returned {test.status_code}")
                    st.session_state.backend_ok = False
            except Exception as e:
                st.sidebar.error(f"❌ Connection error: {e}")
                st.session_state.backend_ok = False
        else:
            st.sidebar.error("❌ API_URL not found in secrets")
            st.sidebar.write("Available keys:", list(st.secrets.keys()))
            API_URL = None
            st.session_state.backend_ok = False
    else:
        st.sidebar.error("❌ No secrets found")
        API_URL = None
        st.session_state.backend_ok = False
except Exception as e:
    st.sidebar.error(f"❌ Secrets error: {e}")
    API_URL = None
    st.session_state.backend_ok = False

# Rest of your app code follows...
# (keep your existing app code below this)
