import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

def show(api_client):
    """Display users page"""
    
    st.markdown("<h2 class='sub-header'>👥 User Management</h2>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 All Users", 
        "➕ Add User", 
        "📊 User Analytics",
        "📈 Risk Distribution"
    ])
    
    with tab1:
        show_all_users(api_client)
    
    with tab2:
        show_add_user(api_client)
    
    with tab3:
        show_user_analytics(api_client)
    
    with tab4:
        show_risk_distribution(api_client)

def show_all_users(api_client):
    """Display all users"""
    
    # Search and filter
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search = st.text_input("🔍 Search", placeholder="Name or email...")
    with col2:
        dept_filter = st.multiselect(
            "Department",
            ["IT", "HR", "Finance", "Sales", "Marketing", "Operations"]
        )
    with col3:
        role_filter = st.multiselect("Role", ["Admin", "Manager", "Employee"])
    with col4:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])
    
    # Fetch users
    with st.spinner("Loading users..."):
        users = api_client.get("/users")
        
        if not users:
            users = get_mock_users()
    
    # Apply filters
    filtered = users
    if search:
        filtered = [u for u in filtered if search.lower() in u['name'].lower() or search.lower() in u['email'].lower()]
    if dept_filter:
        filtered = [u for u in filtered if u['department'] in dept_filter]
    if role_filter:
        filtered = [u for u in filtered if u['role'] in role_filter]
    if status_filter != "All":
        filtered = [u for u in filtered if u['status'] == status_filter.lower()]
    
        # Display user count
    st.markdown(f"**Showing {len(filtered)} users**")
    
    # Create DataFrame for display
    df = pd.DataFrame(filtered)
    
    # Display users in a table with custom formatting
    for _, user in df.iterrows():
        with st.container():
            cols = st.columns([2, 2, 1, 1, 1, 1, 1])
            
            # User info
            cols[0].markdown(f"**{user['name']}**")
            cols[1].markdown(user['email'])
            cols[2].markdown(user['department'])
            cols[3].markdown(f"`{user['role']}`")
            
            # Risk score with color
            risk_score = user['risk_score']
            if risk_score < 30:
                cols[4].markdown(f"<span style='color:#00C851'>● {risk_score}</span>", unsafe_allow_html=True)
            elif risk_score < 60:
                cols[4].markdown(f"<span style='color:#FFA000'>● {risk_score}</span>", unsafe_allow_html=True)
            else:
                cols[4].markdown(f"<span style='color:#DC143C'>● {risk_score}</span>", unsafe_allow_html=True)
            
            # Status badge
            if user['status'] == 'active':
                cols[5].markdown("<span class='badge-success'>Active</span>", unsafe_allow_html=True)
            else:
                cols[5].markdown("<span class='badge-warning'>Inactive</span>", unsafe_allow_html=True)
            
            # Actions
            with cols[6]:
                if st.button("👤", key=f"view_{user['id']}", help="View details"):
                    st.session_state['selected_user'] = user
                    show_user_details(user)
            
            st.markdown("<hr style='margin:0.5rem 0; opacity:0.2;'>", unsafe_allow_html=True)
    
    # Pagination
    col1, col2, col3 = st.columns(3)
    with col2:
        st.button("Load More", use_container_width=True)

def show_add_user(api_client):
    """Display add user form"""
    
    st.markdown("### ➕ Add New User")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email *", placeholder="john@company.com")
            department = st.selectbox("Department *", 
                ["IT", "HR", "Finance", "Sales", "Marketing", "Operations", "Legal"])
            role = st.selectbox("Role *", ["Employee", "Manager", "Admin"])
        
        with col2:
            username = st.text_input("Username *", placeholder="johndoe")
            password = st.text_input("Password *", type="password", 
                placeholder="Create strong password")
            job_title = st.text_input("Job Title", placeholder="Software Engineer")
            manager = st.selectbox("Manager", ["Select manager...", "John Smith", "Jane Doe", "Bob Wilson"])
        
        # Additional info
        with st.expander("📋 Additional Information"):
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Phone Number", placeholder="+1 234 567 8900")
                hire_date = st.date_input("Hire Date", datetime.now())
                employee_id = st.text_input("Employee ID", placeholder="EMP001")
            with col2:
                location = st.text_input("Location", placeholder="New York, NY")
                timezone = st.selectbox("Timezone", 
                    ["EST", "CST", "MST", "PST", "GMT", "IST"])
                training_level = st.select_slider(
                    "Training Level",
                    options=["Beginner", "Intermediate", "Advanced"]
                )
        
        # Permissions
        with st.expander("🔐 Permissions"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.checkbox("View Dashboard", True)
                st.checkbox("View Campaigns", True)
                st.checkbox("Create Campaigns", role in ["Admin", "Manager"])
            with col2:
                st.checkbox("View Users", role == "Admin")
                st.checkbox("Edit Users", role == "Admin")
                st.checkbox("Delete Users", role == "Admin")
            with col3:
                st.checkbox("View Analytics", True)
                st.checkbox("Export Data", role in ["Admin", "Manager"])
                st.checkbox("Manage Training", role in ["Admin", "Manager"])
        
        # Notifications
        with st.expander("🔔 Notification Settings"):
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox("Email Notifications", True)
                st.checkbox("Push Notifications", True)
                st.checkbox("SMS Alerts", False)
            with col2:
                st.checkbox("Campaign Updates", True)
                st.checkbox("Training Reminders", True)
                st.checkbox("Security Alerts", True)
        
        submitted = st.form_submit_button("➕ Create User", type="primary", use_container_width=True)
        
        if submitted:
            if not full_name or not email or not username or not password:
                st.error("Please fill in all required fields")
            else:
                with st.spinner("Creating user..."):
                    # Simulate API call
                    import time
                    time.sleep(1.5)
                    st.balloons()
                    st.success(f"✅ User {full_name} created successfully!")
                    st.info(f"📧 Welcome email sent to {email}")

def show_user_analytics(api_client):
    """Display user analytics"""
    
    st.markdown("### 📊 User Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "1,245", "+23")
    with col2:
        st.metric("Active Users", "1,189", "+18")
    with col3:
        st.metric("New This Month", "45", "+12")
    with col4:
        st.metric("Inactive", "56", "-5")
    
    # User growth chart
    st.markdown("#### 📈 User Growth Trend")
    
    # Mock growth data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    growth = [1100, 1125, 1150, 1175, 1180, 1190, 1200, 1210, 1220, 1230, 1240, 1245]
    
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=growth,
        mode='lines+markers',
        name='Total Users',
        line=dict(color='#1E88E5', width=3),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Month",
        yaxis_title="Number of Users",
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Department distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏢 Department Distribution")
        
        dept_data = {
            'IT': 245,
            'HR': 189,
            'Finance': 156,
            'Sales': 278,
            'Marketing': 198,
            'Operations': 179
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(dept_data.keys()),
            values=list(dept_data.values()),
            hole=0.4,
            marker_colors=['#1E88E5', '#FFA000', '#00C851', '#DC143C', '#9C27B0', '#FF5722']
        )])
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 👥 Role Distribution")
        
        role_data = {
            'Employees': 1050,
            'Managers': 150,
            'Admins': 45
        }
        
        fig = go.Figure(data=[go.Bar(
            x=list(role_data.keys()),
            y=list(role_data.values()),
            marker_color=['#1E88E5', '#FFA000', '#DC143C'],
            text=list(role_data.values()),
            textposition='auto',
        )])
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

def show_risk_distribution(api_client):
    """Display risk distribution analytics"""
    
    st.markdown("### 📈 Risk Distribution Analysis")
    
    # Risk summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Risk", "45", "-3")
    with col2:
        st.metric("High Risk Users", "124", "+12")
    with col3:
        st.metric("Medium Risk", "456", "-23")
    with col4:
        st.metric("Low Risk", "665", "+34")
    
    # Risk distribution chart
    st.markdown("#### 🎯 Risk Score Distribution")
    
    # Mock risk data
    risk_ranges = ['0-20', '21-40', '41-60', '61-80', '81-100']
    counts = [234, 431, 345, 156, 79]
    
    fig = go.Figure(data=[go.Bar(
        x=risk_ranges,
        y=counts,
        marker_color=['#00C851', '#7CB342', '#FFA000', '#FF6B6B', '#DC143C'],
        text=counts,
        textposition='auto',
    )])
    
    fig.update_layout(
        title="User Risk Distribution",
        xaxis_title="Risk Score Range",
        yaxis_title="Number of Users",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk by department
    st.markdown("#### 🏢 Risk by Department")
    
    departments = ['IT', 'HR', 'Finance', 'Sales', 'Marketing', 'Operations']
    avg_risk = [35, 42, 58, 62, 38, 45]
    
    fig = go.Figure(data=[go.Bar(
        x=departments,
        y=avg_risk,
        marker_color=['#1E88E5', '#FFA000', '#DC143C', '#DC143C', '#FFA000', '#1E88E5'],
        text=[f"{r} avg" for r in avg_risk],
        textposition='outside',
    )])
    
    fig.update_layout(
        title="Average Risk Score by Department",
        xaxis_title="Department",
        yaxis_title="Average Risk Score",
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # High risk users table
    st.markdown("#### ⚠️ High Risk Users")
    
    high_risk_users = [
        {"name": "John Smith", "dept": "Finance", "risk": 92, "last_incident": "2 days ago", "trainings": 3},
        {"name": "Sarah Johnson", "dept": "Sales", "risk": 88, "last_incident": "5 days ago", "trainings": 5},
        {"name": "Mike Williams", "dept": "Finance", "risk": 85, "last_incident": "1 week ago", "trainings": 2},
        {"name": "Lisa Brown", "dept": "Operations", "risk": 82, "last_incident": "3 days ago", "trainings": 4},
        {"name": "Tom Davis", "dept": "IT", "risk": 81, "last_incident": "2 weeks ago", "trainings": 6}
    ]
    
    df = pd.DataFrame(high_risk_users)
    st.dataframe(
        df,
        column_config={
            "name": "Name",
            "dept": "Department",
            "risk": st.column_config.ProgressColumn(
                "Risk Score",
                format="%d",
                min_value=0,
                max_value=100,
            ),
            "last_incident": "Last Incident",
            "trainings": "Trainings Completed"
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎯 Assign Training", use_container_width=True):
            st.success("Training assigned to high-risk users")
    with col2:
        if st.button("📧 Send Alert", use_container_width=True):
            st.info("Alert emails sent to managers")
    with col3:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("Risk report generated")

def show_user_details(user):
    """Show detailed user information in a modal"""
    
    with st.expander(f"📋 User Details: {user['name']}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Basic Information**")
            st.markdown(f"• **Name:** {user['name']}")
            st.markdown(f"• **Email:** {user['email']}")
            st.markdown(f"• **Department:** {user['department']}")
            st.markdown(f"• **Role:** {user['role']}")
            st.markdown(f"• **Status:** {user['status']}")
        
        with col2:
            st.markdown("**Security Information**")
            st.markdown(f"• **Risk Score:** {user['risk_score']}/100")
            st.markdown(f"• **Last Login:** {user.get('last_login', 'N/A')}")
            st.markdown(f"• **Trainings Completed:** {user.get('trainings', 0)}")
            st.markdown(f"• **Phishing Clicks:** {user.get('clicks', 0)}")
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("✏️ Edit", key=f"edit_{user['id']}"):
                st.info("Edit mode activated")
        with col2:
            if st.button("🔒 Reset Password", key=f"reset_{user['id']}"):
                st.success("Password reset email sent")
        with col3:
            if st.button("📧 Send Message", key=f"message_{user['id']}"):
                st.info("Message composer opened")
        with col4:
            if st.button("📊 View Activity", key=f"activity_{user['id']}"):
                st.session_state['view_user_activity'] = user['id']

def get_mock_users():
    """Generate mock users data"""
    
    first_names = ["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Tom", "Emma", "James", "Maria"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    departments = ["IT", "HR", "Finance", "Sales", "Marketing", "Operations"]
    roles = ["Employee", "Employee", "Employee", "Employee", "Manager", "Admin"]
    
    users = []
    for i in range(1, 51):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        users.append({
            'id': i,
            'name': name,
            'email': f"{name.lower().replace(' ', '.')}@company.com",
            'department': random.choice(departments),
            'role': random.choice(roles),
            'risk_score': random.randint(10, 95),
            'status': random.choice(['active', 'active', 'active', 'inactive']),
            'last_login': f"{random.randint(1, 30)} days ago",
            'trainings': random.randint(0, 20),
            'clicks': random.randint(0, 10)
        })
    
    return users