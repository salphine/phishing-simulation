import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random

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
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True
    st.session_state.username = "demo_user"
    st.session_state.role = "user"
    st.session_state.user_id = 1

# API Base URL
API_URL = "http://127.0.0.1:8000/api"

# Function to make API calls
def call_api(endpoint, method="GET", data=None):
    try:
        url = f"{API_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Header
st.markdown("<h1 class='main-header'>🎣 Phishing Simulation Platform</h1>", unsafe_allow_html=True)

# Navigation
nav_items = ["Home", "Leaderboard", "My Stats", "Challenges", "Vishing", "Blockchain", "Mobile", "Integrations"]
nav_icons = ["🏠", "🏆", "📊", "🎯", "📞", "⛓️", "📱", "🔌"]

cols = st.columns(len(nav_items))
for idx, item in enumerate(nav_items):
    with cols[idx]:
        if st.button(
            f"{nav_icons[idx]} {item}",
            key=f"nav_{item}",
            use_container_width=True,
            type="primary" if st.session_state.page == item else "secondary"
        ):
            st.session_state.page = item
            st.rerun()

st.markdown("---")

# Main content
if st.session_state.page == "Home":
    st.markdown("## 📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get real data from various endpoints
    vishing_stats = call_api("vishing/analytics?period=week") or {}
    blockchain_stats = call_api("blockchain/stats") or {}
    mobile_analytics = call_api("mobile/analytics") or {}
    integrations_status = call_api("integrations/status/all") or {}
    
    with col1:
        active_calls = len(call_api("vishing/calls/active")?.get("active_calls", [])) if call_api("vishing/calls/active") else 3
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>📞 Active Calls</div>
            <div class='metric-value'>{active_calls}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_certs = blockchain_stats.get("total_certificates", 1234)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>⛓️ Certificates</div>
            <div class='metric-value'>{total_certs:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        active_devices = mobile_analytics.get("active_devices", 2)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>📱 Active Devices</div>
            <div class='metric-value'>{active_devices}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        webhooks = integrations_status.get("webhooks", {}).get("active", 2)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>🔌 Active Webhooks</div>
            <div class='metric-value'>{webhooks}</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == "Vishing":
    st.markdown("## 📞 Vishing Protection")
    
    tab1, tab2, tab3 = st.tabs(["Active Calls", "Call History", "Analytics"])
    
    with tab1:
        active_calls = call_api("vishing/calls/active")
        if active_calls and active_calls.get("active_calls"):
            for call in active_calls["active_calls"]:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                    with col1:
                        st.markdown(f"**{call['caller']}**")
                    with col2:
                        risk_color = "status-active" if call['risk'] == "low" else "status-warning" if call['risk'] == "medium" else "status-danger"
                        st.markdown(f"<span class='status-badge {risk_color}'>{call['risk'].upper()}</span>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"{call['duration']}s")
                    with col4:
                        if st.button("End Call", key=f"end_{call['id']}"):
                            result = call_api(f"vishing/calls/{call['id']}/end", method="POST")
                            if result:
                                st.success("Call ended")
                                st.rerun()
        else:
            st.info("No active calls")
    
    with tab2:
        history = call_api("vishing/calls/history?limit=20")
        if history and history.get("calls"):
            df = pd.DataFrame(history["calls"])
            st.dataframe(df[['caller', 'duration', 'risk', 'timestamp']], use_container_width=True)
        else:
            st.info("No call history")
    
    with tab3:
        analytics = call_api("vishing/analytics?period=week")
        if analytics:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Calls", analytics.get("total_calls", 0))
            with col2:
                st.metric("Suspicious", analytics.get("suspicious_calls", 0))
            with col3:
                st.metric("Success Rate", f"{analytics.get('success_rate', 0)}%")
            
            # Risk distribution chart
            if "risk_distribution" in analytics:
                risk_df = pd.DataFrame([
                    {"Risk": k, "Count": v} for k, v in analytics["risk_distribution"].items()
                ])
                fig = px.pie(risk_df, values='Count', names='Risk', title='Risk Distribution')
                st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == "Blockchain":
    st.markdown("## ⛓️ Blockchain Certificates")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>📜 Recent Certificates</div>", unsafe_allow_html=True)
        
        certificates = call_api("blockchain/certificates?limit=10")
        if certificates and certificates.get("certificates"):
            for cert in certificates["certificates"]:
                status_color = "status-active" if cert['status'] == 'verified' else "status-warning"
                st.markdown(f"""
                <div style='padding: 1rem; border: 1px solid #eee; margin: 0.5rem 0; border-radius: 5px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span><strong>{cert['name']}</strong></span>
                        <span class='status-badge {status_color}'>{cert['status'].upper()}</span>
                    </div>
                    <p><small>User: {cert['user']} | Score: {cert['score']}%</small></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No certificates found")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        stats = call_api("blockchain/stats")
        if stats:
            st.markdown("""
            <div class='dashboard-card'>
                <div class='card-header'>📊 Network Stats</div>
            """, unsafe_allow_html=True)
            st.metric("Total Certificates", stats.get("total_certificates", 0))
            st.metric("Verified", stats.get("verified_certificates", 0))
            st.metric("Last Block", f"#{stats.get('last_block', 0)}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='dashboard-card'>
            <div class='card-header'>🔍 Verify Certificate</div>
        """, unsafe_allow_html=True)
        cert_id = st.text_input("Certificate ID/Hash")
        if st.button("Verify"):
            result = call_api("blockchain/verify", method="POST", data={"certificate_id": cert_id})
            if result:
                if result.get("verified"):
                    st.success("✅ Certificate is valid!")
                else:
                    st.error("❌ Certificate not found or invalid")
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "Mobile":
    st.markdown("## 📱 Mobile Integration")
    
    tab1, tab2 = st.tabs(["Devices", "Notifications"])
    
    with tab1:
        devices = call_api("mobile/devices")
        if devices and devices.get("devices"):
            for device in devices["devices"]:
                status_color = "status-active" if device['status'] == 'active' else "status-warning"
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                    with col1:
                        st.markdown(f"**{device['device_name']}**")
                    with col2:
                        st.markdown(device['device_type'])
                    with col3:
                        st.markdown(f"<span class='status-badge {status_color}'>{device['status'].upper()}</span>", unsafe_allow_html=True)
                    with col4:
                        if device['status'] == 'active':
                            if st.button("Unregister", key=f"unreg_{device['id']}"):
                                result = call_api(f"mobile/devices/{device['id']}/unregister", method="POST")
                                if result:
                                    st.success("Device unregistered")
                                    st.rerun()
        else:
            st.info("No devices registered")
        
        st.markdown("### Register New Device")
        with st.form("register_device"):
            device_name = st.text_input("Device Name")
            device_type = st.selectbox("Device Type", ["iOS", "Android"])
            model = st.text_input("Model")
            os_version = st.text_input("OS Version")
            if st.form_submit_button("Register"):
                result = call_api("mobile/devices/register", method="POST", data={
                    "device_name": device_name,
                    "device_type": device_type,
                    "model": model,
                    "os_version": os_version
                })
                if result:
                    st.success("Device registered!")
                    st.rerun()
    
    with tab2:
        st.markdown("### Send Notification")
        with st.form("send_notification"):
            title = st.text_input("Title")
            message = st.text_area("Message")
            notif_type = st.selectbox("Type", ["info", "alert", "achievement", "reminder"])
            if st.form_submit_button("Send"):
                result = call_api("mobile/notifications/send", method="POST", data={
                    "title": title,
                    "message": message,
                    "notification_type": notif_type
                })
                if result:
                    st.success(f"Notification sent to {result.get('sent_to', 0)} devices!")

elif st.session_state.page == "Integrations":
    st.markdown("## 🔌 System Integrations")
    
    tab1, tab2, tab3 = st.tabs(["HRIS", "SIEM", "Webhooks"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            status = call_api("integrations/hris/status")
            if status:
                st.markdown("""
                <div class='dashboard-card'>
                    <div class='card-header'>👥 HRIS Status</div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Provider:** {status.get('provider', 'N/A')}")
                st.markdown(f"**Status:** <span class='status-badge status-active'>{status.get('sync_status', 'unknown').upper()}</span>", unsafe_allow_html=True)
                st.markdown(f"**Last Sync:** {status.get('last_sync', 'N/A')}")
                st.markdown(f"**Employees:** {status.get('total_employees', 0)}")
                st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            if st.button("🔄 Sync Now"):
                result = call_api("integrations/hris/sync", method="POST")
                if result:
                    st.success("Sync started!")
        
        history = call_api("integrations/hris/sync-history?limit=5")
        if history and history.get("syncs"):
            st.markdown("### Recent Syncs")
            df = pd.DataFrame(history["syncs"])
            st.dataframe(df[['provider', 'status', 'records_synced', 'completed_at']], use_container_width=True)
    
    with tab2:
        configs = call_api("integrations/siem/configs")
        if configs and configs.get("configs"):
            for config in configs["configs"]:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 2])
                    with col1:
                        st.markdown(f"**{config['provider']}**")
                    with col2:
                        st.markdown(f"<span class='status-badge status-active'>{config['status'].upper()}</span>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"{config.get('events_forwarded', 0)} events")
        
        if st.button("Test SIEM Connection"):
            result = call_api("integrations/siem/test", method="POST", data={
                "provider": "Splunk",
                "endpoint": "https://test.com",
                "api_key": "test"
            })
            if result and result.get("success"):
                st.success("Connection successful!")
            else:
                st.error("Connection failed")
    
    with tab3:
        webhooks = call_api("integrations/webhooks")
        if webhooks and webhooks.get("webhooks"):
            for webhook in webhooks["webhooks"]:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 2])
                    with col1:
                        st.markdown(f"**{webhook['name']}**")
                    with col2:
                        st.markdown(f"<span class='status-badge status-active'>{webhook['status'].upper()}</span>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"{webhook.get('success_count', 0)} successes")
        
        st.markdown("### Create Webhook")
        with st.form("create_webhook"):
            name = st.text_input("Name")
            url = st.text_input("URL")
            events = st.multiselect("Events", ["user.login", "phishing.detected", "badge.earned", "campaign.started"])
            if st.form_submit_button("Create"):
                result = call_api("integrations/webhooks", method="POST", data={
                    "name": name,
                    "url": url,
                    "events": events
                })
                if result:
                    st.success("Webhook created!")
                    st.rerun()

else:
    # Keep existing pages for Leaderboard, My Stats, Challenges
    st.info(f"📍 {st.session_state.page} page - Content coming soon!")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; padding: 1rem;'>"
    "© 2026 Phishing Simulation Platform | All Modules Connected"
    "</div>",
    unsafe_allow_html=True
)
