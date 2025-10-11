import streamlit as st
from datetime import datetime, timedelta
import numpy as np

def check_critical_alerts(water_data, iot_data, health_reports):
    """Check for critical alerts across all monitoring systems"""
    
    alerts = []
    current_time = datetime.now()
    
    # Check satellite imagery alerts (simulated based on water quality data)
    satellite_alert = check_satellite_alerts(water_data)
    if satellite_alert:
        alerts.append(satellite_alert)
    
    # Check IoT sensor alerts
    iot_alert = check_iot_alerts(iot_data)
    if iot_alert:
        alerts.append(iot_alert)
    
    # Check health reporting alerts
    health_alert = check_health_alerts(health_reports)
    if health_alert:
        alerts.append(health_alert)
    
    # Check for multi-system correlation
    if len(alerts) >= 2:
        correlation_alert = {
            'type': 'Multi-System Correlation',
            'severity': 'Critical',
            'message': f'Multiple monitoring systems showing contamination indicators ({len(alerts)} systems affected)',
            'confidence': min(95.0, float(np.mean([alert.get('confidence', 80) for alert in alerts]) + 15)),
            'timestamp': current_time,
            'location': 'Multiple Locations',
            'systems': [alert['type'] for alert in alerts]
        }
        alerts.append(correlation_alert)
    
    return alerts

def check_satellite_alerts(water_data):
    """Check satellite imagery for contamination indicators"""
    
    # Simulate satellite analysis based on recent water quality data
    if len(water_data) > 0:
        recent_samples = water_data.tail(50)  # Last 50 samples
        
        # Calculate contamination probability
        contaminated_ratio = (recent_samples['potability'] == 0).mean()
        
        if contaminated_ratio > 0.7:  # More than 70% contaminated samples
            return {
                'type': 'Satellite Imagery',
                'severity': 'Critical',
                'message': f'Satellite imagery shows {contaminated_ratio*100:.1f}% contamination probability',
                'confidence': min(95, contaminated_ratio * 100 + 10),
                'timestamp': datetime.now(),
                'location': 'Bangalore Rural District'
            }
        elif contaminated_ratio > 0.4:  # More than 40% contaminated samples
            return {
                'type': 'Satellite Imagery',
                'severity': 'High',
                'message': f'Satellite imagery shows {contaminated_ratio*100:.1f}% contamination probability',
                'confidence': min(85, contaminated_ratio * 100 + 15),
                'timestamp': datetime.now(),
                'location': 'Bangalore Rural District'
            }
    
    return None

def check_iot_alerts(iot_data):
    """Check IoT sensor data for anomalies"""
    
    if len(iot_data) == 0:
        return None
    
    # Get most recent historical data
    historical_data = iot_data[iot_data['is_historical']]
    if len(historical_data) < 10:
        return None
    
    recent_data = historical_data.tail(12)  # Last 12 hours
    
    # Check for parameter anomalies
    anomaly_count = 0
    anomaly_details = []
    
    # pH anomaly
    if recent_data['ph'].mean() < 6.0 or recent_data['ph'].mean() > 9.0:
        anomaly_count += 1
        anomaly_details.append(f"pH: {recent_data['ph'].mean():.2f}")
    
    # Turbidity anomaly
    if recent_data['turbidity'].mean() > 8.0:
        anomaly_count += 1
        anomaly_details.append(f"Turbidity: {recent_data['turbidity'].mean():.2f} NTU")
    
    # Dissolved Oxygen anomaly
    if recent_data['dissolved_oxygen'].mean() < 4.0:
        anomaly_count += 1
        anomaly_details.append(f"DO: {recent_data['dissolved_oxygen'].mean():.2f} mg/L")
    
    # TDS anomaly
    if recent_data['tds'].mean() > 1000:
        anomaly_count += 1
        anomaly_details.append(f"TDS: {recent_data['tds'].mean():.0f} ppm")
    
    if anomaly_count >= 2:
        severity = 'Critical' if anomaly_count >= 3 else 'High'
        return {
            'type': 'IoT Sensors',
            'severity': severity,
            'message': f'{anomaly_count} water quality parameters exceeding safe limits: {", ".join(anomaly_details)}',
            'confidence': min(90, 60 + anomaly_count * 10),
            'timestamp': datetime.now(),
            'location': 'IoT Network Stations'
        }
    
    return None

def check_health_alerts(health_reports):
    """Check community health reports for disease patterns"""
    
    if len(health_reports) == 0:
        return None
    
    # Analyze recent health reports (last 7 days)
    recent_date = datetime.now() - timedelta(days=7)
    recent_reports = [r for r in health_reports if r['date'] >= recent_date]
    
    if len(recent_reports) == 0:
        return None
    
    # Count waterborne disease symptoms
    waterborne_symptoms = ['diarrhea', 'vomiting', 'fever', 'stomach_pain']
    symptom_counts = {}
    
    for report in recent_reports:
        for symptom in report.get('symptoms', []):
            if symptom in waterborne_symptoms:
                symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
    
    total_cases = sum(symptom_counts.values())
    
    if total_cases >= 10:  # Threshold for alert
        return {
            'type': 'Health Reports',
            'severity': 'Critical' if total_cases >= 20 else 'High',
            'message': f'{total_cases} waterborne disease symptoms reported in last 7 days',
            'confidence': min(85, 50 + total_cases * 2),
            'timestamp': datetime.now(),
            'location': 'Community Health Network'
        }
    
    return None

def display_alert_banner(alerts):
    """Display critical alert banner"""
    
    if not alerts:
        return
    
    # Find highest severity alert
    severity_order = {'Critical': 3, 'High': 2, 'Medium': 1, 'Low': 0}
    top_alert = max(alerts, key=lambda x: severity_order.get(x['severity'], 0))
    
    # Color based on severity
    color_map = {
        'Critical': '#FF6B6B',
        'High': '#FF9800',
        'Medium': '#FFC107',
        'Low': '#4CAF50'
    }
    
    alert_color = color_map.get(top_alert['severity'], '#FF6B6B')
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, {alert_color} 0%, {alert_color}AA 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem; 
                animation: pulse 2s infinite; color: white; text-align: center;">
        <h3>🚨 {top_alert['severity'].upper()} ALERT - Water Quality Threat Detected</h3>
        <p><strong>{top_alert['message']}</strong></p>
        <p>Location: {top_alert['location']} | Confidence: {top_alert.get('confidence', 'N/A')}%</p>
        <p>Systems Affected: {len(alerts)} | Time: {top_alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-add to alert history
    if 'alerts' not in st.session_state:
        st.session_state.alerts = []
    
    # Add new alerts to history (avoid duplicates)
    existing_alert_messages = [alert.get('message', '') for alert in st.session_state.alerts]
    
    for alert in alerts:
        alert_record = {
            'severity': alert['severity'],
            'timestamp': alert['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
            'location': alert['location'],
            'message': alert['message'],
            'actions': get_recommended_actions(alert),
            'confidence': alert.get('confidence', 'N/A')
        }
        
        # Only add if not already in recent history
        if alert_record['message'] not in existing_alert_messages:
            st.session_state.alerts.append(alert_record)

def get_recommended_actions(alert):
    """Get recommended actions based on alert type and severity"""
    
    if alert['severity'] == 'Critical':
        base_actions = [
            "Immediate water source isolation",
            "Emergency public health advisory",
            "Activate emergency response teams",
            "Distribute safe water supplies",
            "Contact state health authorities"
        ]
    elif alert['severity'] == 'High':
        base_actions = [
            "Increase monitoring frequency",
            "Issue boil-water advisory",
            "Prepare emergency supplies",
            "Alert local health officials"
        ]
    else:
        base_actions = [
            "Monitor situation closely",
            "Review water treatment processes",
            "Inform relevant authorities"
        ]
    
    # Add system-specific actions
    if alert['type'] == 'Satellite Imagery':
        base_actions.append("Verify with ground-based sensors")
    elif alert['type'] == 'IoT Sensors':
        base_actions.append("Check sensor calibration")
    elif alert['type'] == 'Health Reports':
        base_actions.append("Deploy medical teams")
    
    return ", ".join(base_actions)

def generate_alert_email(alert, recipient="health.dept@state.gov.in"):
    """Generate email content for alert notification"""
    
    email_content = f"""
Subject: {alert['severity'].upper()} Water Quality Alert - {alert['location']}

Dear Health Authority Team,

ALERT DETAILS:
- Alert Type: {alert['type']}
- Severity Level: {alert['severity']}
- Confidence Level: {alert.get('confidence', 'N/A')}%
- Location: {alert['location']}
- Detection Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}

SITUATION SUMMARY:
{alert['message']}

RECOMMENDED IMMEDIATE ACTIONS:
{get_recommended_actions(alert)}

NEXT STEPS:
1. Verify alert through additional monitoring systems
2. Coordinate with local water authorities
3. Prepare public health response if confirmed
4. Monitor situation for escalation

This alert was generated by the AI-Powered Water Quality Prediction Dashboard.
For technical support, contact: tech-support@water-monitoring.gov.in

Best regards,
Water Quality Monitoring System
IBM Z Datathon 2025
    """
    
    return email_content.strip()
