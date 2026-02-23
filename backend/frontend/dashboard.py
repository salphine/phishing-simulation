import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def show(api_client):
    """Display dashboard page"""
    
    st.markdown("<h2 class='sub-header'>📊 Dashboard Overview</h2>", unsafe_allow_html=True)
    
    # Fetch dashboard data
    with st.spinner("Loading dashboard data..."):
        dashboard_data = api_client.get("/analytics/dashboard")
        
        if not dashboard_data:
            # Mock data for demonstration
            dashboard_data = get_mock_dashboard_data()
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card fade-in' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <h3>Total Users</h3>
            <h2>{dashboard_data.get('total_users', 0)}</h2>
            <p style='opacity:0.9;'>Active employees</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card fade-in' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <h3>Active Campaigns</h3>
            <h2>{dashboard_data.get('active_campaigns', 0)}</h2>
            <p style='opacity:0.9;'>Currently running</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        risk_score = dashboard_data.get('avg_risk_score', 45)
        risk_color = "#00C851" if risk_score < 30 else "#FFA000" if risk_score < 60 else "#DC143C"
        st.markdown(f"""
        <div class='metric-card fade-in' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h3>Risk Score</h3>
            <h2 style='color:{risk_color};'>{risk_score}/100</h2>
            <p style='opacity:0.9;'>Organization average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card fade-in' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
            <h3>Training Rate</h3>
            <h2>{dashboard_data.get('training_completion_rate', 0)}%</h2>
            <p style='opacity:0.9;'>Completion rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Campaign Performance")
        
        # Campaign performance chart
        campaign_data = dashboard_data.get('campaign_performance', [])
        if campaign_data:
            df = pd.DataFrame(campaign_data)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Opened',
                x=df['campaign'],
                y=df['opened'],
                marker_color='#1E88E5',
                text=df['opened'],
                textposition='auto',
            ))
            fig.add_trace(go.Bar(
                name='Clicked',
                x=df['campaign'],
                y=df['clicked'],
                marker_color='#FFA000',
                text=df['clicked'],
                textposition='auto',
            ))
            fig.add_trace(go.Bar(
                name='Compromised',
                x=df['campaign'],
                y=df['compromised'],
                marker_color='#DC143C',
                text=df['compromised'],
                textposition='auto',
            ))
            
            fig.update_layout(
                barmode='group',
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Department Risk Levels")
        
        # Department risk chart
        dept_risk = dashboard_data.get('department_risk', [])
        if dept_risk:
            df = pd.DataFrame(dept_risk)
            
            fig = px.pie(
                df,
                values='risk_score',
                names='department',
                title='Risk Distribution by Department',
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.3
            )
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#000000', width=2))
            )
            
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Risk trend chart
    st.markdown("### 📉 Risk Trend Analysis")
    
    risk_trend = dashboard_data.get('risk_trend', [])
    if risk_trend:
        df = pd.DataFrame(risk_trend)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['risk_score'],
            mode='lines+markers',
            name='Risk Score',
            line=dict(color='#DC143C', width=3),
            marker=dict(size=8, color='#DC143C'),
            fill='tozeroy',
            fillcolor='rgba(220,20,60,0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['target'],
            mode='lines',
            name='Target',
            line=dict(color='#00C851', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Organization Risk Score Trend',
            xaxis_title='Date',
            yaxis_title='Risk Score',
            height=400,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity and alerts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔄 Recent Activity")
        
        activities = dashboard_data.get('recent_activity', [])
        for activity in activities:
            with st.container():
                cols = st.columns([1, 3, 2])
                
                # Time
                cols[0].markdown(f"**{activity['time']}**")
                
                # Description with icon
                icon = "📧" if activity['type'] == 'campaign' else "🎓" if activity['type'] == 'training' else "⚠️"
                cols[1].markdown(f"{icon} {activity['description']}")
                
                # Status badge
                status = activity['status']
                if status == 'success':
                    cols[2].markdown("<span class='badge-success'>Completed</span>", unsafe_allow_html=True)
                elif status == 'warning':
                    cols[2].markdown("<span class='badge-warning'>Clicked</span>", unsafe_allow_html=True)
                else:
                    cols[2].markdown("<span class='badge-danger'>Compromised</span>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin:0.5rem 0; opacity:0.2;'>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⚠️ Recent Alerts")
        
        alerts = dashboard_data.get('recent_alerts', [])
        for alert in alerts:
            severity_color = {
                'critical': '#DC143C',
                'high': '#FFA000',
                'medium': '#FFD700',
                'low': '#00C851'
            }.get(alert['severity'], '#888')
            
            with st.container():
                cols = st.columns([1, 3, 1])
                
                # Time
                cols[0].markdown(f"**{alert['time']}**")
                
                # Alert message
                cols[1].markdown(
                    f"<span style='color:{severity_color};'>●</span> {alert['message']}",
                    unsafe_allow_html=True
                )
                
                # Action button
                if cols[2].button("View", key=f"alert_{alert['id']}"):
                    st.session_state['selected_alert'] = alert
                
                st.markdown("<hr style='margin:0.5rem 0; opacity:0.2;'>", unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎯 New Campaign", use_container_width=True):
            st.session_state['nav_to'] = 'Campaigns'
            st.rerun()
    
    with col2:
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Report generation started. You'll be notified when ready.")
    
    with col3:
        if st.button("👥 Add Users", use_container_width=True):
            st.session_state['nav_to'] = 'Users'
            st.rerun()
    
    with col4:
        if st.button("🎓 Training Modules", use_container_width=True):
            st.session_state['nav_to'] = 'Training'
            st.rerun()

def get_mock_dashboard_data():
    """Generate mock dashboard data for demonstration"""
    
    # Mock campaign performance
    campaigns = ['Q1 Campaign', 'Q2 Campaign', 'Q3 Campaign', 'Q4 Campaign']
    campaign_data = []
    for campaign in campaigns:
        campaign_data.append({
            'campaign': campaign,
            'opened': random.randint(50, 200),
            'clicked': random.randint(10, 50),
            'compromised': random.randint(5, 20)
        })
    
    # Mock department risk
    departments = ['IT', 'HR', 'Finance', 'Sales', 'Marketing']
    dept_risk = []
    for dept in departments:
        dept_risk.append({
            'department': dept,
            'risk_score': random.randint(20, 80)
        })
    
    # Mock risk trend
    risk_trend = []
    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
        risk_trend.append({
            'date': date,
            'risk_score': random.randint(30, 70),
            'target': 50
        })
    
    # Mock recent activity
    recent_activity = []
    for i in range(5):
        recent_activity.append({
            'time': f'{i*10} min ago',
            'description': f'User clicked on phishing simulation' if i % 2 == 0 else 'Training module completed',
            'type': 'campaign' if i % 2 == 0 else 'training',
            'status': random.choice(['success', 'warning', 'danger'])
        })
    
    # Mock alerts
    recent_alerts = []
    for i in range(3):
        recent_alerts.append({
            'id': i,
            'time': f'{i*15} min ago',
            'message': f'High risk activity detected in {departments[i]} department',
            'severity': random.choice(['critical', 'high', 'medium'])
        })
    
    return {
        'total_users': 1250,
        'active_campaigns': 3,
        'avg_risk_score': 45,
        'training_completion_rate': 78,
        'campaign_performance': campaign_data,
        'department_risk': dept_risk,
        'risk_trend': risk_trend,
        'recent_activity': recent_activity,
        'recent_alerts': recent_alerts
    }