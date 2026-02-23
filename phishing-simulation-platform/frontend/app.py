import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="AI Phishing Simulation Platform",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        animation: fadeIn 1s;
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
        margin-bottom: 1rem;
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
    .badge-info {
        background-color: #1E88E5;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: all 0.3s;
        border: 1px solid #e0e0e0;
    }
    .feature-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        transform: translateY(-2px);
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
    
    /* Custom button */
    .stButton > button {
        background: linear-gradient(45deg, #1E88E5, #1565C0);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #1565C0, #0D47A1);
        box-shadow: 0 5px 15px rgba(30, 136, 229, 0.4);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

def login_page():
    """Render login page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-header'>🎣 AI Phishing Simulation Platform</h1>", unsafe_allow_html=True)
        
        # Create a nice card for login
        st.markdown("""
        <div class='feature-card' style='padding: 2rem;'>
            <h3 style='text-align: center; color: #1E88E5; margin-bottom: 2rem;'>🔐 Welcome Back</h3>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2, col3 = st.columns(3)
            with col2:
                submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                # Demo credentials
                if username == "admin" and password == "admin123":
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        "full_name": "Admin User",
                        "username": "admin",
                        "role": "admin",
                        "email": "admin@example.com",
                        "department": "IT Security",
                        "points": 12450,
                        "level": 7
                    }
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                elif username == "employee" and password == "employee123":
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        "full_name": "John Employee",
                        "username": "employee",
                        "role": "employee",
                        "email": "john@example.com",
                        "department": "Sales",
                        "points": 3450,
                        "level": 3
                    }
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Demo credentials
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info("👤 **Admin Access**\nUsername: dmin\nPassword: dmin123")
        with col2:
            st.info("👤 **Employee Access**\nUsername: employee\nPassword: employee123")

def main_app():
    """Main application after login"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h1 style='color: #1E88E5; font-size: 2.5rem; margin: 0;'>🎣</h1>
            <h3 style='color: #333; margin: 0;'>PhishShield</h3>
            <p style='color: #666; font-size: 0.8rem;'>AI Security Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User profile
        if st.session_state.user:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"<div style='background: #1E88E5; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold;'>{st.session_state.user['full_name'][0]}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{st.session_state.user['full_name']}**")
                st.markdown(f"*{st.session_state.user['role'].title()}*")
                st.markdown(f"🏆 Level {st.session_state.user['level']} | {st.session_state.user['points']} pts")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📍 Navigation")
        
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
        if st.button("📧 Campaigns", use_container_width=True):
            st.session_state.page = "Campaigns"
        if st.button("👥 Users", use_container_width=True):
            st.session_state.page = "Users"
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.page = "Analytics"
        if st.button("🎓 Training", use_container_width=True):
            st.session_state.page = "Training"
        if st.button("🏆 Gamification", use_container_width=True):
            st.session_state.page = "Gamification"
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        st.markdown(f"**Active Users:** 1,245 👥")
        st.markdown(f"**Active Campaigns:** 3 📧")
        st.markdown(f"**Risk Score:** 45/100 ⚠️")
        st.markdown(f"**Training Rate:** 78% 🎓")
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    # Main content area
    st.markdown(f"<h1 class='main-header fade-in'>👋 Welcome, {st.session_state.user['full_name']}!</h1>", unsafe_allow_html=True)
    
    # Route to selected page
    if st.session_state.page == "Dashboard":
        show_dashboard()
    elif st.session_state.page == "Campaigns":
        show_campaigns()
    elif st.session_state.page == "Users":
        show_users()
    elif st.session_state.page == "Analytics":
        show_analytics()
    elif st.session_state.page == "Training":
        show_training()
    elif st.session_state.page == "Gamification":
        show_gamification()

def show_dashboard():
    """Display dashboard"""
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <h3>Total Users</h3>
            <h2>1,245</h2>
            <p style='opacity:0.9;'>+23 this month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <h3>Active Campaigns</h3>
            <h2>3</h2>
            <p style='opacity:0.9;'>2 completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h3>Risk Score</h3>
            <h2 style='color: #FFA000;'>45</h2>
            <p style='opacity:0.9;'>↓ 5 from last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
            <h3>Training Rate</h3>
            <h2 style='color: #00C851;'>78%</h2>
            <p style='opacity:0.9;'>↑ 12% improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Campaign Performance")
        
        # Sample data
        campaigns = ['Q1 Campaign', 'Q2 Campaign', 'Q3 Campaign', 'Q4 Campaign']
        opens = [245, 312, 289, 356]
        clicks = [78, 95, 87, 112]
        
        df = pd.DataFrame({
            'Campaign': campaigns,
            'Opens': opens,
            'Clicks': clicks
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Opens', x=campaigns, y=opens, marker_color='#1E88E5'))
        fig.add_trace(go.Bar(name='Clicks', x=campaigns, y=clicks, marker_color='#FFA000'))
        
        fig.update_layout(
            barmode='group',
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Risk by Department")
        
        # Sample data
        depts = ['IT', 'HR', 'Finance', 'Sales', 'Marketing']
        risks = [35, 42, 68, 58, 38]
        
        fig = go.Figure(data=[go.Pie(
            labels=depts,
            values=risks,
            hole=0.4,
            marker_colors=['#1E88E5', '#FFA000', '#DC143C', '#FF6B6B', '#00C851']
        )])
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.markdown("### 🔄 Recent Activity")
    
    activities = [
        {"time": "5 min ago", "user": "John Doe", "action": "Clicked phishing simulation", "status": "warning", "dept": "Finance"},
        {"time": "15 min ago", "user": "Jane Smith", "action": "Completed training module", "status": "success", "dept": "IT"},
        {"time": "1 hour ago", "user": "Bob Wilson", "action": "Failed security quiz", "status": "danger", "dept": "Sales"},
        {"time": "2 hours ago", "user": "Alice Brown", "action": "Reported suspicious email", "status": "success", "dept": "HR"},
        {"time": "3 hours ago", "user": "Charlie Davis", "action": "Earned Security Champion badge", "status": "success", "dept": "IT"}
    ]
    
    for activity in activities:
        cols = st.columns([1, 2, 3, 1, 1])
        cols[0].write(f"**{activity['time']}**")
        cols[1].write(activity['user'])
        cols[2].write(activity['action'])
        cols[3].write(activity['dept'])
        
        if activity['status'] == 'success':
            cols[4].markdown("<span class='badge-success'>✓</span>", unsafe_allow_html=True)
        elif activity['status'] == 'warning':
            cols[4].markdown("<span class='badge-warning'>⚠️</span>", unsafe_allow_html=True)
        else:
            cols[4].markdown("<span class='badge-danger'>🔴</span>", unsafe_allow_html=True)
        
        st.divider()

def show_campaigns():
    """Display campaigns page"""
    st.markdown("<h2 class='sub-header'>📧 Campaign Management</h2>", unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Active Campaigns", "Create Campaign", "Templates"])
    
    with tab1:
        st.markdown("### Active Campaigns")
        
        campaigns = [
            {"name": "Q4 Security Awareness", "status": "active", "sent": 245, "opens": 178, "clicks": 67, "progress": 72},
            {"name": "Invoice Scam Simulation", "status": "active", "sent": 189, "opens": 145, "clicks": 89, "progress": 85},
            {"name": "Password Reset Test", "status": "scheduled", "sent": 0, "opens": 0, "clicks": 0, "progress": 0}
        ]
        
        for campaign in campaigns:
            with st.expander(f"📊 {campaign['name']}", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Sent", campaign['sent'])
                col2.metric("Opens", campaign['opens'])
                col3.metric("Clicks", campaign['clicks'])
                
                status_color = "success" if campaign['status'] == 'active' else "warning"
                col4.markdown(f"<span class='badge-{status_color}'>{campaign['status'].upper()}</span>", unsafe_allow_html=True)
                
                if campaign['progress'] > 0:
                    st.progress(campaign['progress'] / 100)
    
    with tab2:
        st.markdown("### Create New Campaign")
        with st.form("campaign_form"):
            st.text_input("Campaign Name")
            st.multiselect("Target Departments", ["IT", "HR", "Finance", "Sales", "Marketing"])
            st.selectbox("Email Type", ["Invoice", "Security Update", "Password Reset", "Account Verification"])
            st.slider("Urgency Level", 1, 5, 3)
            
            if st.form_submit_button("Create Campaign"):
                st.success("Campaign created successfully!")
    
    with tab3:
        st.markdown("### Email Templates")
        cols = st.columns(3)
        templates = ["Invoice Template", "Security Alert", "Password Reset", "HR Benefits", "Package Delivery", "Account Verification"]
        
        for i, template in enumerate(templates):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='feature-card'>
                    <h4>{template}</h4>
                    <p>Effectiveness: {'⭐' * (i % 5 + 1)}</p>
                    <button class='custom-button'>Use Template</button>
                </div>
                """, unsafe_allow_html=True)

def show_users():
    """Display users page"""
    st.markdown("<h2 class='sub-header'>👥 User Management</h2>", unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("🔍 Search users", placeholder="Name, email, department...")
    with col2:
        st.selectbox("Department", ["All", "IT", "HR", "Finance", "Sales", "Marketing"])
    with col3:
        st.selectbox("Role", ["All", "Admin", "Manager", "Employee"])
    
    # Sample users
    users = [
        {"name": "John Smith", "email": "john.smith@company.com", "dept": "IT", "role": "Admin", "risk": 35, "status": "active"},
        {"name": "Sarah Johnson", "email": "sarah.j@company.com", "dept": "Finance", "role": "Manager", "risk": 68, "status": "active"},
        {"name": "Mike Wilson", "email": "mike.w@company.com", "dept": "Sales", "role": "Employee", "risk": 58, "status": "active"},
        {"name": "Lisa Brown", "email": "lisa.b@company.com", "dept": "HR", "role": "Employee", "risk": 42, "status": "inactive"},
        {"name": "Tom Davis", "email": "tom.d@company.com", "dept": "Marketing", "role": "Employee", "risk": 38, "status": "active"}
    ]
    
    for user in users:
        cols = st.columns([2, 2, 1, 1, 1, 1])
        cols[0].write(f"**{user['name']}**")
        cols[1].write(user['email'])
        cols[2].write(user['dept'])
        cols[3].write(f"{user['role']}")
        
        # Risk score with color
        risk_color = "success" if user['risk'] < 40 else "warning" if user['risk'] < 60 else "danger"
        cols[4].markdown(f"<span class='badge-{risk_color}'>{user['risk']}</span>", unsafe_allow_html=True)
        
        # Status
        status_color = "success" if user['status'] == 'active' else "warning"
        cols[5].markdown(f"<span class='badge-{status_color}'>{user['status']}</span>", unsafe_allow_html=True)
        
        st.divider()

def show_analytics():
    """Display analytics page"""
    st.markdown("<h2 class='sub-header'>📈 Advanced Analytics</h2>", unsafe_allow_html=True)
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Start Date", datetime.now())
    with col2:
        st.date_input("End Date", datetime.now())
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Events", "15,234", "+2,345")
    col2.metric("Avg. Risk", "45", "-3")
    col3.metric("Click Rate", "32%", "+5%")
    col4.metric("Training ROI", "285%", "+45%")
    
    # Trend chart
    st.markdown("### 📊 Risk Trend Analysis")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', end='2024-03-01', freq='D')
    risk_scores = [45 + 10 * np.sin(i/10) + random.randint(-5, 5) for i in range(len(dates))]
    
    df = pd.DataFrame({
        'Date': dates,
        'Risk Score': risk_scores
    })
    
    fig = px.line(df, x='Date', y='Risk Score', title='90-Day Risk Trend')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_training():
    """Display training page"""
    st.markdown("<h2 class='sub-header'>🎓 Training Modules</h2>", unsafe_allow_html=True)
    
    # User progress
    st.markdown("### 📊 Your Progress")
    st.progress(0.65, text="65% Complete - 8/12 modules completed")
    
    # Available modules
    st.markdown("### 📚 Available Modules")
    
    modules = [
        {"name": "Phishing Email Identification", "level": "Beginner", "duration": "15 min", "progress": 100},
        {"name": "Password Security Best Practices", "level": "Beginner", "duration": "20 min", "progress": 100},
        {"name": "Social Engineering Awareness", "level": "Intermediate", "duration": "25 min", "progress": 75},
        {"name": "Mobile Device Security", "level": "Intermediate", "duration": "20 min", "progress": 30},
        {"name": "Cloud Data Protection", "level": "Advanced", "duration": "35 min", "progress": 0},
        {"name": "Ransomware Prevention", "level": "Advanced", "duration": "30 min", "progress": 0}
    ]
    
    cols = st.columns(3)
    for i, module in enumerate(modules):
        with cols[i % 3]:
            level_color = "success" if module['level'] == "Beginner" else "warning" if module['level'] == "Intermediate" else "danger"
            
            st.markdown(f"""
            <div class='feature-card'>
                <h4>{module['name']}</h4>
                <p><span class='badge-{level_color}'>{module['level']}</span> ⏱️ {module['duration']}</p>
                <div class='progress-container'>
                    <div class='progress-bar' style='width: {module['progress']}%;'></div>
                </div>
                <p style='text-align: right;'>{module['progress']}% Complete</p>
            </div>
            """, unsafe_allow_html=True)

def show_gamification():
    """Display gamification page"""
    st.markdown("<h2 class='sub-header'>🏆 Gamification</h2>", unsafe_allow_html=True)
    
    # User stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Points", "12,450", "+350")
    col2.metric("Current Level", "7", "↑1")
    col3.metric("Badges Earned", "24", "+3")
    col4.metric("Global Rank", "#42", "↑5")
    
    # Level progress
    st.markdown("### 📊 Level Progress")
    st.progress(0.7, text="70% to Level 8 (17,500/25,000 points)")
    
    # Badges
    st.markdown("### 🏅 Recent Badges")
    
    badges = [
        {"name": "Phishing Spotter", "tier": "Gold", "icon": "🕵️", "date": "2024-03-15"},
        {"name": "Vigilant Guardian", "tier": "Silver", "icon": "🛡️", "date": "2024-03-10"},
        {"name": "Speed Learner", "tier": "Bronze", "icon": "⚡", "date": "2024-03-05"},
        {"name": "Team Player", "tier": "Silver", "icon": "🤝", "date": "2024-02-28"}
    ]
    
    cols = st.columns(4)
    for i, badge in enumerate(badges):
        with cols[i]:
            tier_colors = {"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
            color = tier_colors.get(badge['tier'], "#888")
            
            st.markdown(f"""
            <div class='feature-card' style='text-align: center; border-left: 5px solid {color};'>
                <div style='font-size: 3rem;'>{badge['icon']}</div>
                <h4>{badge['name']}</h4>
                <p style='color: {color}; font-weight: bold;'>{badge['tier']}</p>
                <p style='font-size: 0.8rem;'>Earned: {badge['date']}</p>
            </div>
            """, unsafe_allow_html=True)

# Main entry point
if __name__ == "__main__":
    if st.session_state.authenticated:
        main_app()
    else:
        login_page()
