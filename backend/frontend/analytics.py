import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import numpy as np

def show(api_client):
    """Display analytics page"""
    
    st.markdown("<h2 class='sub-header'>📊 Advanced Analytics</h2>", unsafe_allow_html=True)
    
    # Date range selector
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    with col3:
        comparison = st.selectbox("Compare with", ["Previous Period", "Previous Year", "Custom"])
    
    # Executive summary
    st.markdown("### 📋 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Risk Score", "47", "-5", delta_color="inverse")
    with col2:
        st.metric("Training Completion", "78%", "+12%")
    with col3:
        st.metric("Phish-Prone %", "23%", "-7%")
    with col4:
        st.metric("ROI", "285%", "+45%")
    
    # Main analytics tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Trends", 
        "👥 Behavioral", 
        "🎓 Training Impact",
        "💰 ROI Analysis",
        "📊 Predictive"
    ])
    
    with tab1:
        show_trend_analytics()
    
    with tab2:
        show_behavioral_analytics()
    
    with tab3:
        show_training_impact()
    
    with tab4:
        show_roi_analysis()
    
    with tab5:
        show_predictive_analytics()

def show_trend_analytics():
    """Display trend analytics"""
    
    st.markdown("### 📈 Performance Trends")
    
    # Time series data
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(90, 0, -1)]
    
    # Generate trend data
    np.random.seed(42)
    risk_trend = 50 + np.cumsum(np.random.randn(90) * 2)
    risk_trend = np.clip(risk_trend, 20, 80)
    
    click_trend = 30 + np.cumsum(np.random.randn(90) * 1.5)
    click_trend = np.clip(click_trend, 10, 60)
    
    training_trend = 60 + np.cumsum(np.random.randn(90) * 1)
    training_trend = np.clip(training_trend, 40, 90)
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=risk_trend,
        mode='lines',
        name='Risk Score',
        line=dict(color='#DC143C', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=click_trend,
        mode='lines',
        name='Click Rate',
        line=dict(color='#FFA000', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=training_trend,
        mode='lines',
        name='Training Completion',
        line=dict(color='#00C851', width=3)
    ))
    
    fig.update_layout(
        title="90-Day Performance Trends",
        xaxis_title="Date",
        yaxis_title="Percentage",
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Seasonality analysis
    st.markdown("### 🌡️ Seasonality Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Day of week pattern
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        click_rates = [32, 35, 38, 42, 45, 28, 25]
        
        fig = go.Figure(data=[go.Bar(
            x=days,
            y=click_rates,
            marker_color=['#1E88E5', '#1E88E5', '#1E88E5', '#1E88E5', '#1E88E5', '#FFA000', '#FFA000'],
            text=[f"{r}%" for r in click_rates],
            textposition='auto',
        )])
        
        fig.update_layout(
            title="Click Rate by Day of Week",
            xaxis_title="Day",
            yaxis_title="Click Rate (%)",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Hour of day pattern
        hours = list(range(24))
        hour_clicks = [5, 3, 2, 1, 2, 3, 8, 15, 25, 32, 38, 35, 
                      30, 28, 32, 38, 42, 45, 40, 35, 28, 20, 12, 8]
        
        fig = go.Figure(data=[go.Scatter(
            x=hours,
            y=hour_clicks,
            mode='lines+markers',
            line=dict(color='#FFA000', width=3),
            fill='tozeroy'
        )])
        
        fig.update_layout(
            title="Click Distribution by Hour",
            xaxis_title="Hour of Day",
            yaxis_title="Number of Clicks",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_behavioral_analytics():
    """Display behavioral analytics"""
    
    st.markdown("### 👥 User Behavior Analysis")
    
    # Behavioral metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Response Time", "2.3h", "-0.5h")
    with col2:
        st.metric("Click Through Rate", "32%", "-3%")
    with col3:
        st.metric("Repeat Offenders", "45", "+8")
    with col4:
        st.metric("Improvement Rate", "67%", "+12%")
    
    # Behavior matrix
    st.markdown("#### 🔄 User Behavior Matrix")
    
    # Create behavior segments
    segments = pd.DataFrame({
        'Segment': ['Security Champions', 'Improving', 'At Risk', 'Critical'],
        'Count': [234, 456, 123, 45],
        'Click Rate': [8, 25, 58, 82],
        'Training Rate': [95, 75, 45, 30]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Click Rate',
        x=segments['Segment'],
        y=segments['Click Rate'],
        marker_color='#DC143C',
        text=segments['Click Rate'],
        textposition='auto',
    ))
    
    fig.add_trace(go.Bar(
        name='Training Rate',
        x=segments['Segment'],
        y=segments['Training Rate'],
        marker_color='#00C851',
        text=segments['Training Rate'],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Behavioral Segments Analysis",
        barmode='group',
        height=400,
        xaxis_title="User Segment",
        yaxis_title="Percentage"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Click pattern analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔗 Link Type Preferences")
        
        link_types = ['Invoice', 'Security', 'Password', 'HR', 'Delivery', 'Other']
        click_counts = [456, 389, 234, 178, 145, 89]
        
        fig = go.Figure(data=[go.Pie(
            labels=link_types,
            values=click_counts,
            hole=0.4,
            marker_colors=['#1E88E5', '#FFA000', '#DC143C', '#00C851', '#9C27B0', '#FF5722']
        )])
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📱 Device Preferences")
        
        devices = ['Desktop', 'Mobile', 'Tablet']
        device_clicks = [678, 543, 210]
        
        fig = go.Figure(data=[go.Bar(
            x=devices,
            y=device_clicks,
            marker_color=['#1E88E5', '#FFA000', '#00C851'],
            text=device_clicks,
            textposition='auto',
        )])
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

def show_training_impact():
    """Display training impact analysis"""
    
    st.markdown("### 🎓 Training Effectiveness Analysis")
    
    # Training metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Training ROI", "285%", "+45%")
    with col2:
        st.metric("Knowledge Retention", "76%", "+8%")
    with col3:
        st.metric("Behavior Change", "42%", "+12%")
    with col4:
        st.metric("Risk Reduction", "35%", "+5%")
    
    # Before/After comparison
    st.markdown("#### 📊 Before vs After Training")
    
    modules = ['Phishing Awareness', 'Link Safety', 'Password Security', 'Data Protection', 'Social Engineering']
    before = [65, 58, 72, 68, 55]
    after = [92, 88, 94, 89, 85]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Before Training',
        x=modules,
        y=before,
        marker_color='#DC143C',
        text=[f"{b}%" for b in before],
        textposition='auto',
    ))
    
    fig.add_trace(go.Bar(
        name='After Training',
        x=modules,
        y=after,
        marker_color='#00C851',
        text=[f"{a}%" for a in after],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Training Impact by Module",
        barmode='group',
        height=400,
        xaxis_title="Training Module",
        yaxis_title="Success Rate (%)",
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Learning curve
    st.markdown("#### 📈 Learning Curve Analysis")
    
    weeks = list(range(1, 13))
    scores = [45, 52, 58, 63, 68, 72, 75, 78, 80, 82, 83, 84]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=scores,
        mode='lines+markers',
        name='Average Score',
        line=dict(color='#1E88E5', width=3),
        fill='tozeroy'
    ))
    
    # Add trend line
    z = np.polyfit(weeks, scores, 1)
    trend = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=trend(weeks),
        mode='lines',
        name='Learning Trend',
        line=dict(color='#FFA000', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="12-Week Learning Progression",
        xaxis_title="Week",
        yaxis_title="Average Score",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_roi_analysis():
    """Display ROI analysis"""
    
    st.markdown("### 💰 Return on Investment Analysis")
    
    # ROI Calculator
    st.markdown("#### 🧮 ROI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Input Parameters**")
        employees = st.number_input("Number of Employees", value=1000, step=100)
        avg_breach_cost = st.number_input("Average Breach Cost ($)", value=3860000, step=100000)
        breach_probability = st.slider("Annual Breach Probability (%)", 0, 100, 15)
        training_cost_per_employee = st.number_input("Training Cost per Employee ($)", value=50, step=10)
    
    with col2:
        st.markdown("**ROI Calculation**")
        
        # Calculate metrics
        expected_loss = (breach_probability / 100) * avg_breach_cost
        training_investment = employees * training_cost_per_employee
        risk_reduction = 0.65  # 65% risk reduction from training
        prevented_loss = expected_loss * risk_reduction
        net_savings = prevented_loss - training_investment
        roi = (net_savings / training_investment) * 100
        
        st.metric("Expected Annual Loss", f"${expected_loss:,.0f}")
        st.metric("Training Investment", f"${training_investment:,.0f}")
        st.metric("Prevented Loss", f"${prevented_loss:,.0f}")
        st.metric("Net Savings", f"${net_savings:,.0f}")
        st.metric("ROI", f"{roi:.1f}%", delta="Excellent" if roi > 200 else "Good")
    
    # ROI Chart
    st.markdown("#### 📊 ROI Projection")
    
    years = [1, 2, 3, 4, 5]
    cumulative_savings = [prevented_loss * y - training_investment for y in years]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[f"Year {y}" for y in years],
        y=cumulative_savings,
        marker_color=['#DC143C' if x < 0 else '#00C851' for x in cumulative_savings],
        text=[f"${x:,.0f}" for x in cumulative_savings],
        textposition='auto',
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    fig.update_layout(
        title="5-Year Cumulative Savings",
        xaxis_title="Year",
        yaxis_title="Cumulative Savings ($)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💸 Cost Breakdown")
        
        costs = pd.DataFrame({
            'Category': ['Training Platform', 'Content Development', 'Administration', 'Employee Time', 'Total'],
            'Amount': [15000, 25000, 10000, 30000, 80000]
        })
        
        st.dataframe(costs, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 Savings Breakdown")
        
        savings = pd.DataFrame({
            'Category': ['Prevented Breaches', 'Productivity Gain', 'Compliance Savings', 'Insurance Reduction', 'Total'],
            'Amount': [250000, 75000, 50000, 25000, 400000]
        })
        
        st.dataframe(savings, hide_index=True, use_container_width=True)

def show_predictive_analytics():
    """Display predictive analytics"""
    
    st.markdown("### 🔮 Predictive Analytics")
    
    # Risk prediction
    st.markdown("#### 🎯 30-Day Risk Prediction")
    
    # Generate prediction
    future_dates = [(datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(1, 31)]
    predicted_risk = 45 + np.cumsum(np.random.randn(30) * 1.5)
    predicted_risk = np.clip(predicted_risk, 30, 70)
    
    # Confidence intervals
    lower_bound = predicted_risk - np.random.uniform(2, 5, 30)
    upper_bound = predicted_risk + np.random.uniform(2, 5, 30)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=predicted_risk,
        mode='lines+markers',
        name='Predicted Risk',
        line=dict(color='#DC143C', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=upper_bound,
        mode='lines',
        name='Upper Bound',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=lower_bound,
        mode='lines',
        name='Lower Bound',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(220,20,60,0.2)',
        showlegend=False
    ))
    
    fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Target")
    
    fig.update_layout(
        title="30-Day Risk Forecast with Confidence Intervals",
        xaxis_title="Date",
        yaxis_title="Predicted Risk Score",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # High-risk predictions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚠️ Predicted High-Risk Users")
        
        high_risk_pred = pd.DataFrame({
            'User': ['John Smith', 'Sarah Johnson', 'Mike Williams', 'Lisa Brown', 'Tom Davis'],
            'Current Risk': [92, 88, 85, 82, 81],
            'Predicted Risk (30d)': [95, 91, 89, 87, 85],
            'Confidence': [0.95, 0.92, 0.89, 0.87, 0.85]
        })
        
        st.dataframe(high_risk_pred, hide_index=True, use_container_width=True)
        
        if st.button("🎯 Assign Preventive Training", use_container_width=True):
            st.success("Preventive training assigned to predicted high-risk users")
    
    with col2:
        st.markdown("#### 📈 Department Risk Forecast")
        
        depts = ['IT', 'HR', 'Finance', 'Sales', 'Marketing']
        current = [35, 42, 58, 62, 38]
        predicted = [38, 45, 63, 68, 42]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Current',
            x=depts,
            y=current,
            marker_color='#1E88E5'
        ))
        
        fig.add_trace(go.Bar(
            name='Predicted (30d)',
            x=depts,
            y=predicted,
            marker_color='#FFA000'
        ))
        
        fig.update_layout(
            title="Department Risk Forecast",
            barmode='group',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ML Model Performance
    st.markdown("#### 🤖 ML Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Model Accuracy", "94.2%", "+2.1%")
    with col2:
        st.metric("Precision", "91.5%", "+1.8%")
    with col3:
        st.metric("Recall", "89.7%", "+3.2%")
    with col4:
        st.metric("F1 Score", "90.6%", "+2.5%")
    
    # Confusion matrix
    st.markdown("#### 📊 Confusion Matrix")
    
    # Create confusion matrix heatmap
    import plotly.figure_factory as ff
    
    confusion_matrix = [[245, 23], [18, 189]]
    
    fig = ff.create_annotated_heatmap(
        confusion_matrix,
        x=['Predicted Safe', 'Predicted Risky'],
        y=['Actual Safe', 'Actual Risky'],
        colorscale='Blues',
        showscale=True
    )
    
    fig.update_layout(
        title="Model Confusion Matrix",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)