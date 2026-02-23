import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

def show(api_client):
    """Display campaigns page"""
    
    st.markdown("<h2 class='sub-header'>📧 Campaign Management</h2>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Active Campaigns", 
        "🎯 Create Campaign", 
        "📝 Templates",
        "📈 Campaign Analytics"
    ])
    
    with tab1:
        show_active_campaigns(api_client)
    
    with tab2:
        show_create_campaign(api_client)
    
    with tab3:
        show_templates(api_client)
    
    with tab4:
        show_campaign_analytics(api_client)

def show_active_campaigns(api_client):
    """Display active campaigns"""
    
    # Fetch campaigns
    with st.spinner("Loading campaigns..."):
        campaigns = api_client.get("/campaigns")
        
        if not campaigns:
            campaigns = get_mock_campaigns()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["draft", "scheduled", "active", "paused", "completed"],
            default=["active"]
        )
    with col2:
        search = st.text_input("🔍 Search campaigns", placeholder="Campaign name...")
    with col3:
        sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Name", "Status"])
    
    # Filter campaigns
    filtered = [c for c in campaigns if c.get('status') in status_filter]
    if search:
        filtered = [c for c in filtered if search.lower() in c.get('name', '').lower()]
    
    if not filtered:
        st.info("No campaigns found matching your criteria")
        return
    
    # Display campaigns
    for campaign in filtered:
        with st.expander(f"📊 {campaign['name']} - {campaign['status'].upper()}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📧 Sent", campaign.get('sent_count', 0))
            with col2:
                st.metric("👁️ Opened", campaign.get('opened_count', 0))
            with col3:
                st.metric("🖱️ Clicked", campaign.get('clicked_count', 0))
            with col4:
                st.metric("⚠️ Compromised", campaign.get('compromised_count', 0))
            
            # Progress bars
            col1, col2 = st.columns(2)
            
            with col1:
                open_rate = (campaign.get('opened_count', 0) / campaign.get('sent_count', 1)) * 100
                st.markdown(f"**Open Rate:** {open_rate:.1f}%")
                st.progress(open_rate / 100)
            
            with col2:
                click_rate = (campaign.get('clicked_count', 0) / campaign.get('sent_count', 1)) * 100
                st.markdown(f"**Click Rate:** {click_rate:.1f}%")
                st.progress(click_rate / 100, text=f"{click_rate:.1f}%")
            
            # Campaign details
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"**Created:** {campaign.get('created_at', 'N/A')}")
            with col2:
                st.markdown(f"**Target:** {', '.join(campaign.get('target_departments', ['All']))}")
            with col3:
                st.markdown(f"**Type:** {campaign.get('email_type', 'Generic')}")
            with col4:
                st.markdown(f"**ID:** `{campaign.get('id', 'N/A')}`")
            
            # Action buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if campaign['status'] == 'active':
                    if st.button("⏸️ Pause", key=f"pause_{campaign['id']}"):
                        st.success("Campaign paused")
                else:
                    if st.button("▶️ Resume", key=f"resume_{campaign['id']}"):
                        st.success("Campaign resumed")
            
            with col2:
                if st.button("📊 Details", key=f"details_{campaign['id']}"):
                    st.session_state['selected_campaign'] = campaign
            
            with col3:
                if st.button("📧 Preview", key=f"preview_{campaign['id']}"):
                    show_email_preview(campaign)
            
            with col4:
                if st.button("📈 Results", key=f"results_{campaign['id']}"):
                    show_campaign_results(campaign)
            
            with col5:
                if campaign['status'] != 'completed':
                    if st.button("🛑 End", key=f"end_{campaign['id']}"):
                        st.warning("Campaign ended")

def show_create_campaign(api_client):
    """Display create campaign form"""
    
    st.markdown("### 🎯 Create New Campaign")
    
    with st.form("campaign_form"):
        # Basic information
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name *", placeholder="e.g., Q4 Security Awareness")
        with col2:
            campaign_type = st.selectbox(
                "Campaign Type",
                ["invoice", "security_update", "password_reset", "account_verification", "generic"]
            )
        
        campaign_desc = st.text_area("Description", placeholder="Describe the campaign purpose...")
        
        # Target audience
        st.markdown("#### 🎯 Target Audience")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            departments = st.multiselect(
                "Departments",
                ["IT", "HR", "Finance", "Sales", "Marketing", "Operations", "Legal", "R&D"],
                default=["IT", "Finance"]
            )
        with col2:
            roles = st.multiselect(
                "Roles",
                ["Manager", "Employee", "Executive", "Intern", "Contractor"]
            )
        with col3:
            experience_level = st.select_slider(
                "Experience Level",
                options=["Beginner", "Intermediate", "Advanced", "All"]
            )
        
        # AI Email Generation
        st.markdown("#### 🤖 AI Email Generation")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            urgency = st.select_slider(
                "Urgency Level",
                options=["Low", "Medium", "High", "Critical"]
            )
        with col2:
            tone = st.selectbox(
                "Email Tone",
                ["Professional", "Friendly", "Urgent", "Official", "Casual"]
            )
        with col3:
            company_name = st.text_input("Company Name", "Your Company")
        
        # Generate email button
        generate_clicked = st.form_submit_button("🤖 Generate Email with AI")
        
        if generate_clicked:
            with st.spinner("AI is crafting the perfect phishing email..."):
                time.sleep(2)  # Simulate AI processing
                response = {
                    'subject': f"URGENT: Action Required - {campaign_type.replace('_', ' ').title()} Update",
                    'body': get_mock_email_template(campaign_type, urgency, company_name)
                }
                st.session_state['generated_email'] = response
                st.success("Email generated successfully!")
        
        # Show generated email if available
        if 'generated_email' in st.session_state:
            st.markdown("#### 📝 Generated Email Preview")
            
            email = st.session_state['generated_email']
            st.text_input("Subject", value=email['subject'], key="email_subject")
            st.text_area("Email Body", value=email['body'], height=300, key="email_body")
        
        # Schedule
        st.markdown("#### 📅 Schedule")
        
        col1, col2 = st.columns(2)
        with col1:
            schedule_type = st.radio("Schedule", ["Immediate", "Scheduled"], horizontal=True)
        with col2:
            if schedule_type == "Scheduled":
                schedule_date = st.date_input("Start Date", datetime.now() + timedelta(days=1))
                schedule_time = st.time_input("Start Time", datetime.now().time())
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            col1, col2 = st.columns(2)
            with col1:
                track_opens = st.checkbox("Track Email Opens", True)
                track_clicks = st.checkbox("Track Link Clicks", True)
                track_data = st.checkbox("Track Data Submission", True)
            with col2:
                send_reminders = st.checkbox("Send Reminders", False)
                adaptive_training = st.checkbox("Enable Adaptive Training", True)
                notify_admin = st.checkbox("Notify Admin on Completion", True)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Launch Campaign", type="primary", use_container_width=True)
        
        if submitted:
            if not campaign_name:
                st.error("Please enter a campaign name")
            elif not departments:
                st.error("Please select at least one department")
            else:
                with st.spinner("Creating and launching campaign..."):
                    time.sleep(2)
                    st.balloons()
                    st.success(f"✅ Campaign '{campaign_name}' created and launched successfully!")
                    st.info(f"📧 Emails will be sent to {len(departments) * 50} employees")

def show_templates(api_client):
    """Display email templates"""
    
    st.markdown("### 📝 Email Templates")
    
    templates = [
        {
            "name": "Invoice Payment",
            "type": "invoice",
            "description": "Urgent payment required for overdue invoice",
            "effectiveness": "High",
            "usage_count": 156,
            "success_rate": 78
        },
        {
            "name": "Security Update",
            "type": "security",
            "description": "Action required: Update your account security",
            "effectiveness": "Very High",
            "usage_count": 203,
            "success_rate": 85
        },
        {
            "name": "Password Reset",
            "type": "password",
            "description": "Password reset request detected",
            "effectiveness": "Medium",
            "usage_count": 98,
            "success_rate": 62
        },
        {
            "name": "Account Verification",
            "type": "verification",
            "description": "Verify your account to prevent suspension",
            "effectiveness": "High",
            "usage_count": 134,
            "success_rate": 71
        },
        {
            "name": "HR Benefits Update",
            "type": "hr",
            "description": "Open enrollment ends today",
            "effectiveness": "Very High",
            "usage_count": 89,
            "success_rate": 82
        },
        {
            "name": "Package Delivery",
            "type": "delivery",
            "description": "Failed delivery attempt notification",
            "effectiveness": "Medium",
            "usage_count": 67,
            "success_rate": 58
        }
    ]
    
    # Search and filter
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("🔍 Search templates", placeholder="Template name...")
    with col2:
        filter_type = st.multiselect("Filter by type", ["invoice", "security", "password", "verification", "hr", "delivery"])
    
    # Filter templates
    filtered = templates
    if search:
        filtered = [t for t in filtered if search.lower() in t['name'].lower()]
    if filter_type:
        filtered = [t for t in filtered if t['type'] in filter_type]
    
    # Display templates in grid
    cols = st.columns(3)
    for idx, template in enumerate(filtered):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div class='feature-card'>
                    <h4>{template['name']}</h4>
                    <p style='color: #666; font-size: 0.9rem;'>{template['description']}</p>
                    <hr style='margin: 1rem 0;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span>📊 Effectiveness: <strong>{template['effectiveness']}</strong></span>
                        <span>📈 {template['success_rate']}%</span>
                    </div>
                    <div style='margin-top: 1rem;'>
                        <span class='badge-success'>Used {template['usage_count']} times</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Use Template", key=f"use_{idx}"):
                    st.session_state['nav_to'] = 'Campaigns'
                    st.session_state['selected_template'] = template
                    st.success(f"Template '{template['name']}' selected")
                    st.rerun()

def show_campaign_analytics(api_client):
    """Display campaign analytics"""
    
    st.markdown("### 📈 Campaign Performance Analytics")
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Campaigns", "24", "+3")
    with col2:
        st.metric("Total Emails Sent", "15,234", "+2,345")
    with col3:
        st.metric("Avg. Open Rate", "68%", "+5%")
    with col4:
        st.metric("Avg. Click Rate", "32%", "-2%")
    
    # Campaign comparison chart
    st.markdown("#### Campaign Comparison")
    
    # Mock data
    campaigns = ['Campaign A', 'Campaign B', 'Campaign C', 'Campaign D']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Open Rate',
        x=campaigns,
        y=[72, 68, 81, 65],
        marker_color='#1E88E5'
    ))
    fig.add_trace(go.Bar(
        name='Click Rate',
        x=campaigns,
        y=[34, 28, 42, 31],
        marker_color='#FFA000'
    ))
    fig.add_trace(go.Bar(
        name='Compromise Rate',
        x=campaigns,
        y=[12, 8, 15, 9],
        marker_color='#DC143C'
    ))
    
    fig.update_layout(
        barmode='group',
        height=400,
        title="Campaign Performance Comparison"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Success rate over time
    st.markdown("#### Success Rate Trend")
    
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30, 0, -1)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=[random.randint(60, 80) for _ in range(30)],
        mode='lines',
        name='Success Rate',
        line=dict(color='#00C851', width=3),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        height=300,
        title="Campaign Success Rate Trend",
        xaxis_title="Date",
        yaxis_title="Success Rate (%)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_email_preview(campaign):
    """Show email preview modal"""
    
    with st.expander("📧 Email Preview", expanded=True):
        st.markdown(f"**To:** employees@company.com")
        st.markdown(f"**Subject:** {campaign.get('email_subject', 'Security Alert')}")
        st.markdown("---")
        st.markdown("""
        **Dear [Employee Name],**

        Our system has detected unusual activity on your account. 
        To protect your data, please verify your account immediately.

        [Verify Account](http://security-update.company.com)

        This verification must be completed within 24 hours to prevent account suspension.

        ---
        ⚠️ **TRAINING SIMULATION**: This is a simulated phishing email for security awareness training.
        """)

def show_campaign_results(campaign):
    """Show detailed campaign results"""
    
    with st.expander("📊 Detailed Results", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Department breakdown
            depts = ['IT', 'HR', 'Finance', 'Sales']
            sent = [45, 32, 28, 51]
            clicked = [12, 8, 15, 9]
            
            df = pd.DataFrame({
                'Department': depts,
                'Sent': sent,
                'Clicked': clicked
            })
            
            st.dataframe(df, use_container_width=True)
        
        with col2:
            # Time distribution
            times = ['9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm']
            clicks = [3, 7, 12, 8, 5, 9, 11, 6]
            
            fig = go.Figure(data=go.Scatter(
                x=times, y=clicks,
                mode='lines+markers',
                line=dict(color='#FFA000', width=3)
            ))
            
            fig.update_layout(
                title="Click Distribution by Time",
                height=250,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)

def get_mock_campaigns():
    """Generate mock campaigns"""
    
    return [
        {
            'id': 1,
            'name': 'Q4 Security Awareness',
            'status': 'active',
            'sent_count': 245,
            'opened_count': 178,
            'clicked_count': 67,
            'compromised_count': 23,
            'target_departments': ['IT', 'Finance', 'HR'],
            'email_type': 'security',
            'created_at': '2024-01-15',
            'email_subject': 'Action Required: Security Update'
        },
        {
            'id': 2,
            'name': 'Invoice Scam Simulation',
            'status': 'active',
            'sent_count': 189,
            'opened_count': 145,
            'clicked_count': 89,
            'compromised_count': 34,
            'target_departments': ['Finance', 'Sales'],
            'email_type': 'invoice',
            'created_at': '2024-01-20',
            'email_subject': 'Urgent: Overdue Invoice Payment'
        },
        {
            'id': 3,
            'name': 'Password Reset Test',
            'status': 'completed',
            'sent_count': 312,
            'opened_count': 267,
            'clicked_count': 98,
            'compromised_count': 45,
            'target_departments': ['All'],
            'email_type': 'password',
            'created_at': '2024-01-10',
            'email_subject': 'Password Reset Request'
        }
    ]

def get_mock_email_template(email_type, urgency, company):
    """Generate mock email template"""
    
    templates = {
        'invoice': f"""
Dear [Employee Name],

Our records show that invoice #INV-2024-{random.randint(1000, 9999)} is currently overdue. 
Please process this payment immediately to avoid service interruption.

View Invoice: {{tracking_link}}

Amount Due: ${random.randint(500, 5000)}
Due Date: {datetime.now().strftime('%B %d, %Y')}

This is an automated message from our billing system.

---
⚠️ **TRAINING SIMULATION**: This is a simulated phishing email for security awareness training. 
Never click links in emails without verification.
""",
        'security': f"""
Dear [Employee Name],

Our system detected unusual activity on your {company} account from an unrecognized device.
To protect your data, please verify your account immediately.

Secure Your Account: {{tracking_link}}

Details of the attempted access:
• Location: {random.choice(['New York, US', 'London, UK', 'Singapore', 'Unknown'])}
• Device: {random.choice(['Windows PC', 'MacBook', 'iPhone', 'Android Device'])}
• Time: {datetime.now().strftime('%I:%M %p')}

Failure to verify within 24 hours will result in account suspension.

---
⚠️ **TRAINING SIMULATION**: This is a simulated security alert for training purposes.
"""
    }
    
    return templates.get(email_type, templates['security'])