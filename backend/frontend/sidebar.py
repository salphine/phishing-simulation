import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

def render_sidebar():
    """Render the navigation sidebar"""
    
    with st.sidebar:
        # Logo and title
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h1 style='color: #1E88E5; font-size: 2rem;'>🎣</h1>
            <h3 style='color: #333; margin: 0;'>PhishShield</h3>
            <p style='color: #666; font-size: 0.8rem;'>AI Security Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        if st.session_state.user:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"<div style='background: #1E88E5; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>{st.session_state.user['full_name'][0]}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{st.session_state.user['full_name']}**")
                st.markdown(f"<span style='color: #666; font-size: 0.8rem;'>{st.session_state.user['role'].title()}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu is now in main app
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        
        # Risk gauge
        risk_score = 45  # This would come from API
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Risk Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#DC143C" if risk_score > 60 else "#FFA000" if risk_score > 30 else "#00C851"},
                'steps': [
                    {'range': [0, 30], 'color': "#00C851"},
                    {'range': [30, 60], 'color': "#FFA000"},
                    {'range': [60, 100], 'color': "#DC143C"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': risk_score
                }
            }
        ))
        
        fig.update_layout(height=150, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
        
        # Active users
        st.markdown(f"**Active Users:** 1,189 👥")
        st.markdown(f"**Active Campaigns:** 3 📧")
        st.markdown(f"**Pending Training:** 45 🎓")
        
        st.markdown("---")
        
        # Theme toggle
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Dark", use_container_width=True):
                st.session_state.theme = 'dark'
                st.rerun()
        with col2:
            if st.button("☀️ Light", use_container_width=True):
                st.session_state.theme = 'light'
                st.rerun()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            for key in ['authenticated', 'user', 'access_token']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        # Version info
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.7rem;'>
            <p>Version 2.0.0</p>
            <p>© 2024 PhishShield</p>
        </div>
        """, unsafe_allow_html=True)