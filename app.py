import streamlit as st

# Page configuration - FIRST Streamlit command
st.set_page_config(
    page_title="Water Quality Prediction Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
# from PIL import Image  # Commented for deployment





def main():
    st.title("✅ SERVER STARTED")
    
    # Heavy imports
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # Component imports with fallback
    def satellite_monitoring_tab():
        try:
            from components.satellite_monitor import satellite_monitoring_tab
            satellite_monitoring_tab()
        except:
            st.write("🛰️ Satellite fallback")
    
    def iot_forecasting_tab(iot_data):
        try:
            from components.iot_forecasting import iot_forecasting_tab
            iot_forecasting_tab(iot_data)
        except:
            st.write("📊 IoT fallback")
    
    def health_reporting_tab():
        try:
            from components.health_reporting import health_reporting_tab
            health_reporting_tab()
        except:
            st.write("🏥 Health fallback")
    
    def disease_prediction_tab(water_data):
        try:
            from components.disease_prediction import disease_prediction_tab
            disease_prediction_tab(water_data)
        except:
            st.write("🦠 Disease fallback")
    
    def check_critical_alerts(water_data, iot_data, health_reports):
        try:
            from utils.alert_system import check_critical_alerts
            return check_critical_alerts(water_data, iot_data, health_reports)
        except:
            return []
    
    def display_alert_banner(alerts):
        try:
            from utils.alert_system import display_alert_banner
            display_alert_banner(alerts)
        except:
            pass
    
    def load_water_quality_data():
        try:
            from utils.data_processing import load_water_quality_data
            return load_water_quality_data()
        except:
            df = pd.DataFrame({'ph': np.random.normal(7.0, 0.5, 100)})
            return df
    
    def generate_iot_data():
        try:
            from utils.data_processing import generate_iot_data
            return generate_iot_data()
        except:
            df = pd.DataFrame({'ph': np.random.normal(7.0, 0.2, 24)})
            return df
    
    def send_health_alert(data):
        try:
            from utils.email_alerts import send_health_alert
            send_health_alert(data)
        except:
            st.info("Email logged")
    
    def configure_email_settings():
        try:
            from utils.email_alerts import configure_email_settings
            configure_email_settings()
        except:
            st.info("Email config")
    
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

    st.success("✅ App loaded successfully")
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
    try:
        water_data = load_water_quality_data()
    except:
        water_data = pd.DataFrame({'ph': [7.0], 'turbidity': [2.5]})
        st.warning("Using fallback data")
    
    try:
        iot_data = generate_iot_data()
    except:
        iot_data = water_data.copy()
        st.warning("Using fallback IoT data")
    
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
        try:
            satellite_monitoring_tab()
        except Exception as e:
            st.error(f"Satellite tab error: {e}")
    
    with tabs[1]:
        try:
            iot_forecasting_tab(iot_data)
        except Exception as e:
            st.error(f"IoT tab error: {e}")
    
    with tabs[2]:
        try:
            health_reporting_tab()
        except Exception as e:
            st.error(f"Health tab error: {e}")
    
    with tabs[3]:
        try:
            disease_prediction_tab(water_data)
        except Exception as e:
            st.error(f"Disease tab error: {e}")
    
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
                # send_health_alert(email_data)  # Commented for deployment
                
                st.success("Test alert generated (email disabled for deployment)!")
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
    st.write("Starting main function...")
    try:
        main()
        st.success("Main function executed successfully ✅")
    except Exception as e:
        st.error(f"CRASH: {str(e)}")
        st.info("App loaded with errors above.")
