import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import os

def load_water_quality_data():
    """Load water quality data from CSV file or generate sample data"""
    try:
        # Try to load from data directory first (main data source)
        if os.path.exists('data/sample_water_quality.csv'):
            df = pd.read_csv('data/sample_water_quality.csv')
            df.columns = df.columns.str.lower()
            st.success("✅ Successfully loaded water quality data from CSV file")
            return df
        # Try to load from attached_assets as fallback
        elif os.path.exists('attached_assets/water_potability_1760121508940.csv'):
            df = pd.read_csv('attached_assets/water_potability_1760121508940.csv')
            df.columns = df.columns.str.lower()
            # Add missing columns if needed
            if 'dissolved_oxygen' not in df.columns:
                df['dissolved_oxygen'] = np.random.normal(8, 2, len(df))
                df['dissolved_oxygen'] = np.clip(df['dissolved_oxygen'], 0, 15)
            if 'temperature' not in df.columns:
                df['temperature'] = np.random.normal(25, 5, len(df))
                df['temperature'] = np.clip(df['temperature'], 10, 40)
            if 'tds' not in df.columns and 'solids' in df.columns:
                df['tds'] = df['solids'] / 40  # Approximate conversion
            st.success("✅ Successfully loaded water quality data from attached assets")
            return df
    except Exception as e:
        st.warning(f"Could not load water quality data file: {e}. Using generated data instead.")
    
    # Generate realistic water quality data
    np.random.seed(42)
    n_samples = 1000
    
    # Generate correlated water quality parameters
    data = {
        'ph': np.random.normal(7.0, 0.8, n_samples),
        'Hardness': np.random.normal(200, 50, n_samples),
        'Solids': np.random.normal(20000, 5000, n_samples),
        'Chloramines': np.random.normal(7, 2, n_samples),
        'Sulfate': np.random.normal(300, 100, n_samples),
        'Conductivity': np.random.normal(400, 100, n_samples),
        'Organic_carbon': np.random.normal(14, 4, n_samples),
        'Trihalomethanes': np.random.normal(80, 20, n_samples),
        'Turbidity': np.random.exponential(4, n_samples),
        'Dissolved_Oxygen': np.random.normal(8, 2, n_samples),
        'Temperature': np.random.normal(25, 5, n_samples),
        'TDS': np.random.normal(500, 150, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Ensure realistic ranges
    df['ph'] = np.clip(df['ph'], 3, 14)
    df['Turbidity'] = np.clip(df['Turbidity'], 0.1, 20)
    df['Dissolved_Oxygen'] = np.clip(df['Dissolved_Oxygen'], 0, 15)
    df['Temperature'] = np.clip(df['Temperature'], 10, 40)
    df['TDS'] = np.clip(df['TDS'], 50, 2000)
    
    # Determine potability based on WHO standards
    potability_conditions = (
        (df['ph'] >= 6.5) & (df['ph'] <= 8.5) &
        (df['Turbidity'] <= 5) &
        (df['Dissolved_Oxygen'] >= 5) &
        (df['TDS'] <= 1000) &
        (df['Chloramines'] <= 4)
    )
    
    df['Potability'] = potability_conditions.astype(int)
    
    return df

def generate_iot_data():
    """Generate realistic IoT sensor time-series data"""
    
    # Generate hourly data for the last 7 days and next 12 hours for prediction
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    future_time = end_time + timedelta(hours=12)
    
    # Historical data (7 days)
    historical_periods = int((end_time - start_time).total_seconds() / 3600)  # hourly
    historical_timestamps = [start_time + timedelta(hours=i) for i in range(historical_periods)]
    
    # Future data points for prediction
    future_periods = 12  # 12 hours ahead
    future_timestamps = [end_time + timedelta(hours=i) for i in range(1, future_periods + 1)]
    
    all_timestamps = historical_timestamps + future_timestamps
    n_total = len(all_timestamps)
    
    # Generate base patterns with daily cycles and trends
    time_hours = np.array([(ts - start_time).total_seconds() / 3600 for ts in all_timestamps])
    
    # Daily cycle component
    daily_cycle = np.sin(2 * np.pi * time_hours / 24)
    
    # Weekly cycle component
    weekly_cycle = 0.3 * np.sin(2 * np.pi * time_hours / (24 * 7))
    
    # Random noise
    noise = np.random.normal(0, 0.1, n_total)
    
    # Generate parameters with realistic variations
    data = {
        'timestamp': all_timestamps,
        'ph': 7.0 + 0.5 * daily_cycle + 0.2 * weekly_cycle + 0.3 * noise,
        'turbidity': 2.0 + 1.0 * np.abs(daily_cycle) + 0.5 * np.abs(weekly_cycle) + 0.4 * np.abs(noise),
        'tds': 400 + 100 * daily_cycle + 50 * weekly_cycle + 30 * noise,
        'dissolved_oxygen': 8.0 - 2.0 * np.abs(daily_cycle) + 0.5 * weekly_cycle + 0.3 * noise,
        'temperature': 25 + 3 * daily_cycle + 1 * weekly_cycle + 0.5 * noise,
        'conductivity': 350 + 80 * daily_cycle + 40 * weekly_cycle + 20 * noise
    }
    
    df = pd.DataFrame(data)
    
    # Ensure realistic ranges
    df['ph'] = np.clip(df['ph'], 5.0, 9.0)
    df['turbidity'] = np.clip(df['turbidity'], 0.5, 8.0)
    df['tds'] = np.clip(df['tds'], 200, 800)
    df['dissolved_oxygen'] = np.clip(df['dissolved_oxygen'], 4.0, 12.0)
    df['temperature'] = np.clip(df['temperature'], 18, 35)
    df['conductivity'] = np.clip(df['conductivity'], 200, 600)
    
    # Mark historical vs future data
    df['is_historical'] = df.index < historical_periods
    
    return df

def calculate_water_quality_index(df):
    """Calculate Water Quality Index (WQI) based on multiple parameters"""
    
    # WHO standards for scoring
    ph_ideal = 7.0
    turbidity_max = 5.0
    tds_max = 1000
    do_min = 5.0
    
    # Calculate sub-indices (0-100 scale)
    ph_score = 100 - 20 * np.abs(df['ph'] - ph_ideal)
    turbidity_score = 100 - (df['turbidity'] / turbidity_max) * 100
    tds_score = 100 - (df['tds'] / tds_max) * 100
    do_score = np.minimum(100, (df['dissolved_oxygen'] / do_min) * 100)
    
    # Ensure scores are within 0-100
    ph_score = np.clip(ph_score, 0, 100)
    turbidity_score = np.clip(turbidity_score, 0, 100)
    tds_score = np.clip(tds_score, 0, 100)
    do_score = np.clip(do_score, 0, 100)
    
    # Weighted average (all parameters equally weighted for simplicity)
    wqi = (ph_score + turbidity_score + tds_score + do_score) / 4
    
    return wqi

def get_wqi_category(wqi_score):
    """Categorize WQI scores into quality levels"""
    if wqi_score >= 90:
        return "Excellent", "#4CAF50"
    elif wqi_score >= 70:
        return "Good", "#8BC34A"
    elif wqi_score >= 50:
        return "Moderate", "#FFC107"
    elif wqi_score >= 25:
        return "Poor", "#FF9800"
    else:
        return "Very Poor", "#F44336"
