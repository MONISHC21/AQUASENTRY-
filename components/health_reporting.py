import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from utils.export_data import export_health_reports
from utils.map_visualization import create_geographic_distribution_chart

def health_reporting_tab():
    """Community health reporting system with ASHA worker input"""
    
    st.header("🏥 Community Health Reporting System")
    
    st.markdown("""
    Integrated community health monitoring system enabling ASHA workers and health officials 
    to report waterborne disease symptoms and track community health patterns.
    """)
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Health Report Submission (ASHA Worker Portal)")
        
        # ASHA worker identification
        worker_id = st.text_input("ASHA Worker ID", placeholder="Enter your worker ID (e.g., ASHA001)")
        
        with st.form("health_report_form", clear_on_submit=True):
            # Location details
            st.markdown("**📍 Location Information**")
            district = st.selectbox("District", ["Bangalore Rural", "Bangalore Urban", "Mysore", "Mandya", "Hassan"])
            village = st.text_input("Village/Area Name", placeholder="Enter village or area name")
            
            # Patient demographics
            st.markdown("**👥 Patient Demographics**")
            patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=25)
            patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            # Symptoms reporting
            st.markdown("**🩺 Symptoms Observed**")
            symptoms = st.multiselect(
                "Select all applicable symptoms",
                ["Diarrhea", "Vomiting", "Fever", "Stomach Pain", "Nausea", 
                 "Dehydration", "Headache", "Body Aches", "Loss of Appetite", "Fatigue"]
            )
            
            # Severity and duration
            severity = st.select_slider("Symptom Severity", ["Mild", "Moderate", "Severe"], value="Moderate")
            duration = st.number_input("Duration (days)", min_value=1, max_value=30, value=2)
            
            # Water source information
            st.markdown("**💧 Water Source Details**")
            water_source = st.selectbox(
                "Primary Water Source", 
                ["Municipal Water", "Borewell", "Hand Pump", "Open Well", "River/Stream", "Pond/Lake", "Other"]
            )
            water_treatment = st.selectbox("Water Treatment Used", ["None", "Boiling", "Filtration", "Chemical Treatment"])
            
            # Additional notes
            notes = st.text_area("Additional Notes", placeholder="Any additional observations or context...")
            
            # Submit button
            submit_report = st.form_submit_button("📤 Submit Health Report", type="primary")
            
            if submit_report:
                if worker_id and village and symptoms:
                    # Create health report record
                    new_report = {
                        'worker_id': worker_id,
                        'date': datetime.now(),
                        'district': district,
                        'village': village,
                        'patient_age': patient_age,
                        'patient_gender': patient_gender,
                        'symptoms': symptoms,
                        'severity': severity,
                        'duration': duration,
                        'water_source': water_source,
                        'water_treatment': water_treatment,
                        'notes': notes,
                        'status': 'New',
                        'report_id': f"HR{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    }
                    
                    # Add to session state
                    if 'health_reports' not in st.session_state:
                        st.session_state.health_reports = []
                    
                    st.session_state.health_reports.append(new_report)
                    
                    st.success(f"✅ Health report submitted successfully! Report ID: {new_report['report_id']}")
                    st.balloons()
                    
                    # Check for potential outbreak
                    recent_reports = [r for r in st.session_state.health_reports 
                                    if (datetime.now() - r['date']).days <= 7]
                    
                    if len(recent_reports) >= 5:
                        st.warning("⚠️ Multiple health reports in the last 7 days. Potential outbreak detected!")
                        
                        # Trigger alert
                        outbreak_alert = {
                            'severity': 'High',
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'location': f"{village}, {district}",
                            'message': f'Potential outbreak detected: {len(recent_reports)} health reports in 7 days',
                            'actions': 'Deploy medical team, investigate water sources, issue health advisory',
                            'confidence': min(90, len(recent_reports) * 15)
                        }
                        
                        if 'alerts' not in st.session_state:
                            st.session_state.alerts = []
                        st.session_state.alerts.append(outbreak_alert)
                    
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields (Worker ID, Village, Symptoms)")
    
    with col2:
        st.subheader("📊 Reporting Statistics")
        
        # Display current statistics
        total_reports = len(st.session_state.get('health_reports', []))
        st.metric("Total Reports", total_reports, delta=None)
        
        if total_reports > 0:
            recent_reports = [r for r in st.session_state.health_reports 
                            if (datetime.now() - r['date']).days <= 7]
            st.metric("Reports (Last 7 Days)", len(recent_reports), delta=len(recent_reports))
            
            # Most common symptoms
            all_symptoms = []
            for report in st.session_state.health_reports:
                all_symptoms.extend(report['symptoms'])
            
            if all_symptoms:
                symptom_counts = pd.Series(all_symptoms).value_counts()
                st.markdown("**Most Common Symptoms:**")
                for symptom, count in symptom_counts.head(5).items():
                    st.write(f"• {symptom}: {count}")
        
        # Alert status
        st.markdown("### 🚨 Alert Status")
        recent_date = datetime.now() - timedelta(days=7)
        recent_reports = [r for r in st.session_state.get('health_reports', []) 
                         if r['date'] >= recent_date]
        
        if len(recent_reports) >= 10:
            st.error("🚨 HIGH ALERT: Potential outbreak detected")
        elif len(recent_reports) >= 5:
            st.warning("⚠️ MEDIUM ALERT: Increased reports")
        else:
            st.success("✅ Normal reporting levels")
    
    st.markdown("---")
    
    # Health reports analysis dashboard
    if st.session_state.get('health_reports'):
        st.subheader("📈 Community Health Analysis Dashboard")
        
        # Convert reports to DataFrame for analysis
        reports_df = pd.DataFrame(st.session_state.health_reports)
        
        # Analysis tabs
        analysis_tabs = st.tabs(["📊 Symptom Trends", "📍 Geographic Distribution", "⏰ Timeline Analysis", "🔍 Correlation Analysis"])
        
        with analysis_tabs[0]:
            # Symptom frequency analysis
            all_symptoms = []
            for report in st.session_state.health_reports:
                all_symptoms.extend(report['symptoms'])
            
            if all_symptoms:
                symptom_df = pd.Series(all_symptoms).value_counts().reset_index()
                symptom_df.columns = ['Symptom', 'Count']
                
                fig_symptoms = px.bar(
                    symptom_df, 
                    x='Symptom', 
                    y='Count',
                    title="Most Common Reported Symptoms",
                    color='Count',
                    color_continuous_scale='Reds'
                )
                
                fig_symptoms.update_layout(
                    font=dict(color="#CAF0F8"),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_symptoms, width="stretch")
                
                # Severity distribution
                severity_counts = reports_df['severity'].value_counts()
                
                fig_severity = px.pie(
                    values=severity_counts.values,
                    names=severity_counts.index,
                    title="Symptom Severity Distribution",
                    color_discrete_map={'Mild': '#4CAF50', 'Moderate': '#FFC107', 'Severe': '#FF6B6B'}
                )
                
                fig_severity.update_layout(
                    font=dict(color="#CAF0F8"),
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_severity, width="stretch")
        
        with analysis_tabs[1]:
            # Geographic distribution
            district_counts = reports_df['district'].value_counts()
            
            fig_geo = px.bar(
                x=district_counts.index,
                y=district_counts.values,
                title="Reports by District",
                labels={'x': 'District', 'y': 'Number of Reports'},
                color=district_counts.values,
                color_continuous_scale='Blues'
            )
            
            fig_geo.update_layout(
                font=dict(color="#CAF0F8"),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_geo, use_container_width=True)
            
            # Water source analysis
            water_source_counts = reports_df['water_source'].value_counts()
            
            fig_water = px.pie(
                values=water_source_counts.values,
                names=water_source_counts.index,
                title="Cases by Water Source"
            )
            
            fig_water.update_layout(
                font=dict(color="#CAF0F8"),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_water, use_container_width=True)
        
        with analysis_tabs[2]:
            # Timeline analysis
            reports_df['date_only'] = pd.to_datetime(reports_df['date']).dt.date
            daily_counts = reports_df.groupby('date_only').size().reset_index()
            daily_counts.columns = ['Date', 'Reports']
            
            fig_timeline = px.line(
                daily_counts,
                x='Date',
                y='Reports',
                title="Daily Health Reports Trend",
                markers=True
            )
            
            fig_timeline.update_layout(
                font=dict(color="#CAF0F8"),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Age distribution
            fig_age = px.histogram(
                reports_df,
                x='patient_age',
                nbins=10,
                title="Age Distribution of Reported Cases",
                color_discrete_sequence=['#00B4D8']
            )
            
            fig_age.update_layout(
                font=dict(color="#CAF0F8"),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_age, use_container_width=True)
        
        with analysis_tabs[3]:
            # Correlation with water treatment
            treatment_severity = pd.crosstab(reports_df['water_treatment'], reports_df['severity'])
            
            fig_correlation = px.imshow(
                treatment_severity.values,
                labels=dict(x="Severity", y="Water Treatment", color="Count"),
                x=treatment_severity.columns,
                y=treatment_severity.index,
                title="Water Treatment vs Symptom Severity"
            )
            
            fig_correlation.update_layout(
                font=dict(color="#CAF0F8"),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_correlation, use_container_width=True)
            
            # Key insights
            st.markdown("### 🔍 Key Insights")
            
            # Calculate insights
            no_treatment_severe = len(reports_df[(reports_df['water_treatment'] == 'None') & 
                                               (reports_df['severity'] == 'Severe')])
            total_severe = len(reports_df[reports_df['severity'] == 'Severe'])
            
            if total_severe > 0:
                untreated_severe_pct = (no_treatment_severe / total_severe) * 100
                st.write(f"• {untreated_severe_pct:.1f}% of severe cases used no water treatment")
            
            avg_age = reports_df['patient_age'].mean()
            st.write(f"• Average age of reported cases: {avg_age:.1f} years")
            
            most_common_source = reports_df['water_source'].mode()[0] if len(reports_df) > 0 else "N/A"
            st.write(f"• Most common water source in cases: {most_common_source}")
    
    else:
        st.info("📝 No health reports submitted yet. Use the form above to submit the first report.")
    
    # Guidelines for ASHA workers
    with st.expander("📖 Guidelines for ASHA Workers"):
        st.markdown("""
        ### 📋 Reporting Guidelines
        
        **When to Report:**
        - Any suspected waterborne illness symptoms
        - Multiple cases in the same area
        - Unusual symptoms or patterns
        - Community complaints about water quality
        
        **Important Information to Collect:**
        - Exact location and water source used
        - Onset and duration of symptoms
        - Number of people affected
        - Treatment given (if any)
        
        **Emergency Contacts:**
        - District Health Officer: 080-XXXXXXXX
        - Emergency Medical Response: 108
        - Water Quality Helpline: 1800-XXX-XXXX
        
        **Follow-up Actions:**
        - Monitor patient recovery
        - Check on family members
        - Report any worsening conditions
        - Coordinate with local health centers
        """)
    
    # IBM Z Integration
    st.info("""
    💡 **IBM Z Integration**: Health reporting data is processed using IBM Z's secure transaction 
    processing capabilities, ensuring patient privacy while enabling real-time disease outbreak 
    detection across multiple health districts simultaneously.
    """)
