import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from PIL import Image

# Import custom components
from components.satellite_monitor import satellite_monitoring_tab
from components.iot_forecasting import iot_forecasting_tab
from components.health_reporting import health_reporting_tab
from components.disease_prediction import disease_prediction_tab
from utils.alert_system import check_critical_alerts, display_alert_banner
from utils.data_processing import load_water_quality_data, generate_iot_data
from utils.email_alerts import send_health_alert, configure_email_settings, get_recent_alerts

# Page configuration
st.set_page_config(
    page_title="Water Quality Prediction Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for IBM Z theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #002B5B 0%, #00B4D8 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .alert-banner {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8E8E 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1E3A5F 0%, #2A5783 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        border-left: 4px solid #00B4D8;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1E3A5F 0%, #2A5783 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #00B4D8;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌊 AI-Powered Water Quality Prediction Dashboard</h1>
        <h3>Preventing Waterborne Disease Outbreaks</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'alerts' not in st.session_state:
        st.session_state.alerts = []
    if 'health_reports' not in st.session_state:
        st.session_state.health_reports = []
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # Load data
    water_data = load_water_quality_data()
    iot_data = generate_iot_data()
    
    # Check for critical alerts
    critical_alerts = check_critical_alerts(water_data, iot_data, st.session_state.health_reports)
    if critical_alerts:
        display_alert_banner(critical_alerts)
    
    # Main dashboard tabs
    tabs = st.tabs([
        "🛰️ Satellite Monitoring", 
        "📊 IoT Sensor Forecast", 
        "🏥 Health Reporting", 
        "🦠 Disease Risk Prediction",
        "📧 Alert System"
    ])
    
    with tabs[0]:
        satellite_monitoring_tab()
    
    with tabs[1]:
        iot_forecasting_tab(iot_data)
    
    with tabs[2]:
        health_reporting_tab()
    
    with tabs[3]:
        disease_prediction_tab(water_data)
    
    with tabs[4]:
        st.header("📧 Real-Time Email Alert System")
        
        # Email configuration section
        configure_email_settings()
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Recent Alert History")
            if st.session_state.alerts:
                for alert in reversed(st.session_state.alerts[-10:]):  # Show last 10 alerts
                    with st.container():
                        st.markdown(f"""
                        <div style="background: #1E3A5F; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {'#FF6B6B' if alert['severity'] == 'Critical' else '#FFA726' if alert['severity'] == 'High' else '#4CAF50'};">
                            <strong>{alert['severity']} Alert</strong> - {alert['timestamp']}<br>
                            <strong>Location:</strong> {alert['location']}<br>
                            <strong>Message:</strong> {alert['message']}<br>
                            <strong>Recommended Actions:</strong> {alert['actions']}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No alerts generated yet. Alerts will appear here when water quality parameters exceed safe thresholds.")
        
        with col2:
            st.subheader("Alert Configuration")
            
            # Email settings
            recipient_email = st.text_input("Health Authority Email", value="health.dept@state.gov.in")
            alert_threshold = st.selectbox("Alert Sensitivity", ["High", "Medium", "Low"], index=1)
            
            # Manual alert test with real email
            if st.button("🚨 Test Critical Alert & Send Email"):
                test_alert = {
                    'severity': 'Critical',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'location': 'Test Location - Bangalore Rural',
                    'message': 'Multiple contamination indicators detected across all monitoring systems',
                    'actions': 'Immediate water source isolation, public health advisory, emergency water distribution',
                    'confidence': 95.8
                }
                st.session_state.alerts.append(test_alert)
                
                # Send real email alert
                email_data = {
                    'type': 'Test Alert',
                    'severity': 'Critical',
                    'location': 'Test Location - Bangalore Rural',
                    'ph': '6.8',
                    'turbidity': '8.5',
                    'tds': '1200',
                    'dissolved_oxygen': '4.2',
                    'contamination_risk': '85',
                    'disease_risk': 'High',
                    'affected_population': 'Estimated 5,000+ residents',
                    'recommended_action': 'Immediate water source isolation, public health advisory, emergency water distribution'
                }
                send_health_alert(email_data)
                
                st.success("Test alert generated and email notification sent!")
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #CAF0F8; margin-top: 2rem;">
        <p><strong>Water Quality Prediction Dashboard</strong></p>
        <p>Real-time Satellite & IoT Integration | AI-Driven Disease Prevention</p>
        <p>Last Updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
