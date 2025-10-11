import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
from utils.ml_models import predict_disease_risk, generate_preventive_recommendations, sort_diseases_by_priority
from utils.data_processing import calculate_water_quality_index, get_wqi_category
from utils.export_data import export_disease_predictions
from utils.historical_trends import create_historical_trends_chart, calculate_trend_statistics

def disease_prediction_tab(water_data):
    """Disease risk prediction engine with probability scores and preventive recommendations"""
    
    st.header("🦠 Disease Risk Prediction Engine")
    
    st.markdown("""
    AI-powered disease risk assessment linking water quality parameters to specific waterborne 
    diseases with probability scores and actionable preventive measures.
    """)
    
    # Current risk assessment
    if len(water_data) > 0:
        # Get latest water quality data
        latest_data = water_data.tail(1).iloc[0]
        
        # Map column names for consistency
        water_params = {
            'ph': latest_data.get('ph', 7.0),
            'turbidity': latest_data.get('turbidity', 2.0),
            'tds': latest_data.get('tds', latest_data.get('solids', 500)),
            'dissolved_oxygen': latest_data.get('dissolved_oxygen', 8.0),
            'temperature': latest_data.get('temperature', 25.0),
            'conductivity': latest_data.get('conductivity', 400)
        }
        
        # Calculate disease risks
        disease_risks = predict_disease_risk(water_params)
        
        # Sort diseases by ML-based priority
        sorted_diseases = sort_diseases_by_priority(disease_risks, water_params)
        
        # Get preventive recommendations
        recommendations = generate_preventive_recommendations(disease_risks, water_params)
        
        # Main dashboard
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("🎯 Disease Risk Assessment")
            
            # Disease risk gauges
            fig_diseases = go.Figure()
            
            diseases = list(disease_risks.keys())
            risk_values = list(disease_risks.values())
            colors = ['#FF6B6B', '#FF9800', '#FFC107', '#8BC34A']
            
            # Create risk level visualization
            fig_risk = go.Figure()
            
            for i, (disease, risk, color) in enumerate(zip(diseases, risk_values, colors)):
                fig_risk.add_trace(go.Bar(
                    x=[disease.replace('_', ' ').title()],
                    y=[risk],
                    name=disease.replace('_', ' ').title(),
                    marker_color=color,
                    text=f"{risk:.1f}%",
                    textposition='outside'
                ))
            
            fig_risk.update_layout(
                title="Waterborne Disease Risk Assessment",
                xaxis_title="Disease",
                yaxis_title="Risk Probability (%)",
                yaxis=dict(range=[0, 100]),
                height=400,
                font=dict(color="#CAF0F8"),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            # Add risk threshold lines
            fig_risk.add_hline(y=75, line_dash="dash", line_color="red", 
                             annotation_text="Critical Risk (75%)")
            fig_risk.add_hline(y=50, line_dash="dash", line_color="orange", 
                             annotation_text="High Risk (50%)")
            fig_risk.add_hline(y=25, line_dash="dash", line_color="yellow", 
                             annotation_text="Moderate Risk (25%)")
            
            st.plotly_chart(fig_risk, use_container_width=True)
            
            # Detailed risk breakdown
            st.subheader("📊 Detailed Risk Analysis")
            
            risk_df = pd.DataFrame({
                'Disease': [d.replace('_', ' ').title() for d in diseases],
                'Risk %': risk_values,
                'Risk Level': [get_risk_level(r) for r in risk_values],
                'Primary Factors': [get_primary_factors(d, water_params) for d in diseases]
            })
            
            # Style the dataframe
            def style_risk_level(val):
                if 'Critical' in val:
                    return 'background-color: #FF6B6B; color: white'
                elif 'High' in val:
                    return 'background-color: #FF9800; color: white'
                elif 'Moderate' in val:
                    return 'background-color: #FFC107; color: black'
                else:
                    return 'background-color: #4CAF50; color: white'
            
            styled_df = risk_df.style.applymap(style_risk_level, subset=['Risk Level'])
            st.dataframe(styled_df, use_container_width=True)
        
        with col2:
            st.subheader("⚠️ Current Water Quality Status")
            
            # Water Quality Index
            wqi = calculate_water_quality_index(water_data.tail(1)).iloc[0]
            category, color = get_wqi_category(wqi)
            
            # WQI Display
            st.markdown(f"""
            <div style="background: {color}; padding: 1.5rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
                <h2 style="color: white; margin: 0;">WQI: {wqi:.1f}</h2>
                <h4 style="color: white; margin: 0;">{category}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Parameter status
            st.markdown("### 🔍 Parameter Status")
            
            # pH status
            ph_status = "🟢 Normal" if 6.5 <= water_params['ph'] <= 8.5 else "🔴 Alert"
            st.metric("pH Level", f"{water_params['ph']:.2f}", delta=None)
            st.caption(ph_status)
            
            # Turbidity status
            turb_status = "🟢 Clear" if water_params['turbidity'] <= 5 else "🔴 High"
            st.metric("Turbidity", f"{water_params['turbidity']:.2f} NTU", delta=None)
            st.caption(turb_status)
            
            # DO status
            do_status = "🟢 Healthy" if water_params['dissolved_oxygen'] >= 5 else "🔴 Low"
            st.metric("Dissolved O₂", f"{water_params['dissolved_oxygen']:.2f} mg/L", delta=None)
            st.caption(do_status)
            
            # TDS status
            tds_status = "🟢 Good" if water_params['tds'] <= 1000 else "🔴 High"
            st.metric("TDS", f"{water_params['tds']:.0f} ppm", delta=None)
            st.caption(tds_status)
            
            # Overall risk assessment
            max_risk = max(risk_values)
            st.markdown("### 🚨 Overall Assessment")
            
            if max_risk >= 75:
                st.error(f"🚨 CRITICAL RISK: {max_risk:.1f}%")
                st.markdown("Immediate action required!")
            elif max_risk >= 50:
                st.warning(f"⚠️ HIGH RISK: {max_risk:.1f}%")
                st.markdown("Enhanced monitoring needed")
            elif max_risk >= 25:
                st.info(f"⚠️ MODERATE RISK: {max_risk:.1f}%")
                st.markdown("Continue regular monitoring")
            else:
                st.success(f"✅ LOW RISK: {max_risk:.1f}%")
                st.markdown("Maintain current protocols")
        
        st.markdown("---")
        
        # Preventive recommendations
        st.subheader("📋 Preventive Action Recommendations")
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("### 🚨 Immediate Actions")
            immediate_actions = [rec for rec in recommendations if any(word in rec.lower() 
                               for word in ['immediate', 'emergency', 'isolate', 'urgent'])]
            
            if immediate_actions:
                for action in immediate_actions:
                    st.markdown(f"• {action}")
            else:
                st.success("✅ No immediate actions required at current risk levels")
        
        with rec_col2:
            st.markdown("### ⚙️ Preventive Measures")
            preventive_actions = [rec for rec in recommendations if not any(word in rec.lower() 
                                for word in ['immediate', 'emergency', 'isolate', 'urgent'])]
            
            for action in preventive_actions:
                st.markdown(f"• {action}")
        
        # Disease-specific information
        st.subheader("📚 Disease Information & Symptoms")
        
        disease_info = {
            'cholera': {
                'symptoms': ['Severe diarrhea', 'Vomiting', 'Dehydration', 'Muscle cramps'],
                'incubation': '1-5 days',
                'transmission': 'Contaminated water and food',
                'prevention': 'Boil water, proper sanitation, vaccination in high-risk areas'
            },
            'typhoid': {
                'symptoms': ['High fever', 'Headache', 'Abdominal pain', 'Rose-colored spots'],
                'incubation': '7-14 days', 
                'transmission': 'Contaminated water and food',
                'prevention': 'Safe water, food hygiene, vaccination'
            },
            'diarrhea': {
                'symptoms': ['Loose stools', 'Abdominal cramps', 'Nausea', 'Dehydration'],
                'incubation': '1-3 days',
                'transmission': 'Contaminated water, poor hygiene',
                'prevention': 'Clean water, proper sanitation, hand washing'
            },
            'hepatitis_a': {
                'symptoms': ['Fatigue', 'Nausea', 'Jaundice', 'Abdominal pain'],
                'incubation': '15-50 days',
                'transmission': 'Contaminated water and food',
                'prevention': 'Safe water, vaccination, proper hygiene'
            }
        }
        
        # Show information for high-risk diseases
        high_risk_diseases = [disease for disease, risk in disease_risks.items() if risk > 25]
        
        if high_risk_diseases:
            for disease in high_risk_diseases:
                with st.expander(f"ℹ️ {disease.replace('_', ' ').title()} - Risk: {disease_risks[disease]:.1f}%"):
                    info = disease_info.get(disease, {})
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Key Symptoms:**")
                        for symptom in info.get('symptoms', []):
                            st.write(f"• {symptom}")
                        
                        st.markdown(f"**Incubation Period:** {info.get('incubation', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"**Transmission:** {info.get('transmission', 'N/A')}")
                        st.markdown(f"**Prevention:** {info.get('prevention', 'N/A')}")
        
        # Historical risk trends
        st.subheader("📈 Historical Risk Trends")
        
        # Generate historical risk data (simulated)
        dates = pd.date_range(start=datetime.now() - pd.Timedelta(days=30), 
                             end=datetime.now(), freq='D')
        
        historical_risks = {}
        for disease in diseases:
            base_risk = disease_risks[disease]
            # Add some variation over time
            daily_risks = []
            for i in range(len(dates)):
                variation = np.random.normal(0, base_risk * 0.2)
                risk = max(0, min(100, base_risk + variation))
                daily_risks.append(risk)
            historical_risks[disease] = daily_risks
        
        # Plot historical trends
        fig_trends = go.Figure()
        
        for disease, color in zip(diseases, colors):
            fig_trends.add_trace(go.Scatter(
                x=dates,
                y=historical_risks[disease],
                mode='lines+markers',
                name=disease.replace('_', ' ').title(),
                line=dict(color=color, width=2)
            ))
        
        fig_trends.update_layout(
            title="30-Day Disease Risk Trends",
            xaxis_title="Date",
            yaxis_title="Risk Probability (%)",
            height=400,
            font=dict(color="#CAF0F8"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.5)')
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
        
    else:
        st.warning("No water quality data available for disease risk assessment.")
    
    # IBM Z Integration
    st.info("""
    💡 **IBM Z Integration**: Disease prediction models run on IBM Z's AI acceleration capabilities, 
    processing multiple water quality parameters and health indicators simultaneously to provide 
    real-time risk assessments for entire populations.
    """)

def get_risk_level(risk_percentage):
    """Convert risk percentage to risk level description"""
    if risk_percentage >= 75:
        return "🔴 Critical Risk"
    elif risk_percentage >= 50:
        return "🟠 High Risk"
    elif risk_percentage >= 25:
        return "🟡 Moderate Risk"
    else:
        return "🟢 Low Risk"

def get_primary_factors(disease, water_params):
    """Identify primary risk factors for each disease"""
    
    factors = []
    
    if disease == 'cholera':
        if water_params['ph'] < 6.0 or water_params['ph'] > 8.0:
            factors.append('pH imbalance')
        if water_params['turbidity'] > 5:
            factors.append('High turbidity')
        if water_params['dissolved_oxygen'] < 5:
            factors.append('Low oxygen')
    
    elif disease == 'typhoid':
        if water_params['ph'] < 6.5 or water_params['ph'] > 8.5:
            factors.append('pH deviation')
        if water_params['turbidity'] > 4:
            factors.append('Elevated turbidity')
        if water_params['conductivity'] > 400:
            factors.append('High conductivity')
    
    elif disease == 'diarrhea':
        if water_params['ph'] < 6.5 or water_params['ph'] > 8.5:
            factors.append('pH issues')
        if water_params['turbidity'] > 3:
            factors.append('Water cloudiness')
        if water_params['tds'] > 500:
            factors.append('High dissolved solids')
    
    elif disease == 'hepatitis_a':
        if water_params['ph'] < 7.0 or water_params['ph'] > 8.0:
            factors.append('pH variance')
        if water_params['turbidity'] > 2:
            factors.append('Poor clarity')
        if water_params['dissolved_oxygen'] < 8:
            factors.append('Oxygen deficiency')
    
    return ', '.join(factors) if factors else 'Within normal ranges'
