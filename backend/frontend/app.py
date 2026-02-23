import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_page(
    page_title="AI Phishing Simulation Platform",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    /* Sub header */
    .sub-header {
        font-size: 1.8rem;
        color: #333;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-card h3 {
        font-size: 1rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .metric-card h2 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Status badges */
    .badge-success {
        background-color: #00C851;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-warning {
        background-color: #FFA000;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-danger {
        background-color: #DC143C;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Custom buttons */
    .custom-button {
        background: linear-gradient(45deg, #1E88E5, #1565C0);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        text-align: center;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .custom-button:hover {
        background: linear-gradient(45deg, #1565C0, #0D47A1);
        box-shadow: 0 5px 15px rgba(30, 136, 229, 0.4);
        transform: translateY(-2px);
    }
    
    /* Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: all 0.3s;
    }
    .feature-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    /* Progress bars */
    .progress-container {
        background-color: #f0f0f0;
        border-radius: 25px;
        height: 10px;
        margin: 1rem 0;
    }
    .progress-bar {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        height: 10px;
        border-radius: 25px;
        transition: width 0.5s;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Loading spinner */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #1E88E5;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# Import page modules
from pages import (
    dashboard, campaigns, users, analytics, training,
    gamification, leaderboard, rewards, vishing, mobile,
    blockchain, integrations
)
from components.sidebar import render_sidebar
from components.notifications import show_notifications
from utils.auth import login_user, logout_user, register_user
from utils.api_client import APIClient

# Initialize API client
api_client = APIClient(API_BASE_URL)

def login_page():
    """Render login page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-header'>🎣 AI Phishing Simulation Platform</h1>", unsafe_allow_html=True)
        
        # Login/Register tabs
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("### Welcome Back!")
                st.markdown("Enter your credentials to access the platform.")
                
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col1, col2 = st.columns(2)
                with col1:
                    remember_me = st.checkbox("Remember me")
                with col2:
                    st.markdown("[Forgot password?](#)")
                
                submitted = st.form_submit_button("Login", use_container_width=True)
                
                if submitted:
                    with st.spinner("Authenticating..."):
                        success, result = login_user(username, password, API_BASE_URL)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user = result['user']
                            st.session_state.access_token = result['access_token']
                            st.success("Login successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error(f"Login failed: {result}")
        
        with tab2:
            with st.form("register_form"):
                st.markdown("### Create Account")
                st.markdown("Join the security awareness platform.")
                
                full_name = st.text_input("Full Name", placeholder="John Doe")
                email = st.text_input("Email", placeholder="john@company.com")
                username = st.text_input("Username", placeholder="johndoe")
                password = st.text_input("Password", type="password", placeholder="Create a strong password")
                confirm_password = st.text_input("Confirm Password", type="password")
                department = st.selectbox("Department", ["IT", "HR", "Finance", "Sales", "Marketing", "Operations"])
                
                terms = st.checkbox("I agree to the Terms and Conditions")
                
                submitted = st.form_submit_button("Register", use_container_width=True)
                
                if submitted:
                    if password != confirm_password:
                        st.error("Passwords do not match")
                    elif not terms:
                        st.error("Please accept the terms and conditions")
                    else:
                        with st.spinner("Creating account..."):
                            success, result = register_user({
                                "full_name": full_name,
                                "email": email,
                                "username": username,
                                "password": password,
                                "department": department
                            }, API_BASE_URL)
                            
                            if success:
                                st.success("Registration successful! Please login.")
                            else:
                                st.error(f"Registration failed: {result}")
        
        # Demo credentials
        st.markdown("---")
        st.markdown("""
        ### 🎯 Demo Access
        | Role | Username | Password |
        |------|----------|----------|
        | Admin | admin | admin123 |
        | Manager | manager | manager123 |
        | Employee | employee | employee123 |
        """)

def main_app():
    """Main application after login"""
    
    # Render sidebar
    render_sidebar()
    
    # Show notifications
    show_notifications()
    
    # Welcome header
    st.markdown(f"""
    <div class='fade-in'>
        <h1 class='main-header'>
            👋 Welcome, {st.session_state.user['full_name']}!
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard", "Campaigns", "Users", "Analytics", "Training",
            "Gamification", "Leaderboard", "Rewards", "Vishing",
            "Mobile", "Blockchain", "Integrations"
        ],
        icons=[
            "house", "envelope", "people", "graph-up", "book",
            "trophy", "award", "gift", "telephone", "phone",
            "database", "cloud"
        ],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#fafafa",
                "border-radius": "50px",
                "margin-bottom": "2rem"
            },
            "icon": {"color": "#1E88E5", "font-size": "1.2rem"},
            "nav-link": {
                "font-size": "0.9rem",
                "text-align": "center",
                "margin": "0px",
                "padding": "0.75rem 1rem",
                "transition": "all 0.3s"
            },
            "nav-link-selected": {
                "background-color": "#1E88E5",
                "color": "white",
                "border-radius": "50px"
            },
        }
    )
    
    # Route to selected page
    if selected == "Dashboard":
        dashboard.show(api_client)
    elif selected == "Campaigns":
        campaigns.show(api_client)
    elif selected == "Users":
        users.show(api_client)
    elif selected == "Analytics":
        analytics.show(api_client)
    elif selected == "Training":
        training.show(api_client)
    elif selected == "Gamification":
        gamification.show(api_client)
    elif selected == "Leaderboard":
        leaderboard.show(api_client)
    elif selected == "Rewards":
        rewards.show(api_client)
    elif selected == "Vishing":
        vishing.show(api_client)
    elif selected == "Mobile":
        mobile.show(api_client)
    elif selected == "Blockchain":
        blockchain.show(api_client)
    elif selected == "Integrations":
        integrations.show(api_client)

# Entry point
if __name__ == "__main__":
    if st.session_state.authenticated:
        main_app()
    else:
        login_page()