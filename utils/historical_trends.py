import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_historical_trends_chart(water_data, parameter='ph', start_date=None, end_date=None):
    """Create historical trends chart for water quality parameters with date filtering"""
    
    # Add timestamp if not present
    if 'timestamp' not in water_data.columns:
        water_data['timestamp'] = pd.date_range(
            end=datetime.now(),
            periods=len(water_data),
            freq='H'
        )
    
    # Filter by date range if provided
    if start_date and end_date:
        mask = (water_data['timestamp'] >= start_date) & (water_data['timestamp'] <= end_date)
        filtered_data = water_data[mask].copy()
    else:
        filtered_data = water_data.copy()
    
    if len(filtered_data) == 0:
        st.warning("No data available for selected date range")
        return None
    
    # Map parameter names
    param_map = {
        'ph': 'ph',
        'turbidity': 'Turbidity',
        'tds': 'TDS',
        'dissolved_oxygen': 'Dissolved_Oxygen',
        'temperature': 'Temperature'
    }
    
    actual_param = param_map.get(parameter, parameter)
    
    if actual_param not in filtered_data.columns:
        st.warning(f"Parameter {parameter} not found in data")
        return None
    
    # Create figure with trend line and safety thresholds
    fig = go.Figure()
    
    # Actual data points
    fig.add_trace(go.Scatter(
        x=filtered_data['timestamp'],
        y=filtered_data[actual_param],
        mode='lines+markers',
        name='Actual Values',
        line=dict(color='#00B4D8', width=2),
        marker=dict(size=6, color='#00B4D8')
    ))
    
    # Add moving average
    if len(filtered_data) >= 10:
        ma_window = min(10, len(filtered_data) // 2)
        filtered_data['ma'] = filtered_data[actual_param].rolling(window=ma_window).mean()
        
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'],
            y=filtered_data['ma'],
            mode='lines',
            name='Moving Average',
            line=dict(color='#FFC107', width=2, dash='dash')
        ))
    
    # Add safety thresholds
    if parameter == 'ph':
        fig.add_hline(y=6.5, line_dash="dash", line_color="green", 
                     annotation_text="Min Safe pH (6.5)")
        fig.add_hline(y=8.5, line_dash="dash", line_color="green", 
                     annotation_text="Max Safe pH (8.5)")
    elif parameter == 'turbidity':
        fig.add_hline(y=5, line_dash="dash", line_color="orange", 
                     annotation_text="Max Safe Turbidity (5 NTU)")
    elif parameter == 'tds':
        fig.add_hline(y=1000, line_dash="dash", line_color="orange", 
                     annotation_text="Max Safe TDS (1000 ppm)")
    elif parameter == 'dissolved_oxygen':
        fig.add_hline(y=5, line_dash="dash", line_color="green", 
                     annotation_text="Min Safe DO (5 mg/L)")
    
    fig.update_layout(
        title=f"Historical Trend - {parameter.replace('_', ' ').title()}",
        xaxis_title="Date/Time",
        yaxis_title=get_parameter_unit(parameter),
        height=500,
        font=dict(color="#CAF0F8"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    
    return fig

def get_parameter_unit(parameter):
    """Get display unit for parameter"""
    units = {
        'ph': 'pH Level',
        'turbidity': 'Turbidity (NTU)',
        'tds': 'TDS (ppm)',
        'dissolved_oxygen': 'Dissolved Oxygen (mg/L)',
        'temperature': 'Temperature (°C)',
        'conductivity': 'Conductivity (μS/cm)'
    }
    return units.get(parameter, parameter.title())

def create_comparison_chart(water_data, parameters=['ph', 'turbidity', 'tds'], start_date=None, end_date=None):
    """Create multi-parameter comparison chart"""
    
    # Add timestamp if not present
    if 'timestamp' not in water_data.columns:
        water_data['timestamp'] = pd.date_range(
            end=datetime.now(),
            periods=len(water_data),
            freq='H'
        )
    
    # Filter by date range
    if start_date and end_date:
        mask = (water_data['timestamp'] >= start_date) & (water_data['timestamp'] <= end_date)
        filtered_data = water_data[mask].copy()
    else:
        filtered_data = water_data.copy()
    
    if len(filtered_data) == 0:
        return None
    
    # Normalize data for comparison
    from sklearn.preprocessing import MinMaxScaler
    
    param_map = {
        'ph': 'ph',
        'turbidity': 'Turbidity',
        'tds': 'TDS',
        'dissolved_oxygen': 'Dissolved_Oxygen',
        'temperature': 'Temperature'
    }
    
    fig = go.Figure()
    
    for param in parameters:
        actual_param = param_map.get(param, param)
        
        if actual_param in filtered_data.columns:
            # Normalize to 0-100 scale
            values = filtered_data[actual_param].values.reshape(-1, 1)
            scaler = MinMaxScaler(feature_range=(0, 100))
            normalized = scaler.fit_transform(values).flatten()
            
            fig.add_trace(go.Scatter(
                x=filtered_data['timestamp'],
                y=normalized,
                mode='lines',
                name=param.replace('_', ' ').title(),
                line=dict(width=2)
            ))
    
    fig.update_layout(
        title="Multi-Parameter Comparison (Normalized)",
        xaxis_title="Date/Time",
        yaxis_title="Normalized Value (0-100)",
        height=500,
        font=dict(color="#CAF0F8"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    
    return fig

def calculate_trend_statistics(water_data, parameter, start_date=None, end_date=None):
    """Calculate statistical trends for a parameter"""
    
    # Add timestamp if not present
    if 'timestamp' not in water_data.columns:
        water_data['timestamp'] = pd.date_range(
            end=datetime.now(),
            periods=len(water_data),
            freq='H'
        )
    
    # Filter by date range
    if start_date and end_date:
        mask = (water_data['timestamp'] >= start_date) & (water_data['timestamp'] <= end_date)
        filtered_data = water_data[mask].copy()
    else:
        filtered_data = water_data.copy()
    
    param_map = {
        'ph': 'ph',
        'turbidity': 'Turbidity',
        'tds': 'TDS',
        'dissolved_oxygen': 'Dissolved_Oxygen',
        'temperature': 'Temperature'
    }
    
    actual_param = param_map.get(parameter, parameter)
    
    if actual_param not in filtered_data.columns or len(filtered_data) == 0:
        return None
    
    values = filtered_data[actual_param]
    
    # Calculate trend using linear regression
    from sklearn.linear_model import LinearRegression
    
    X = np.arange(len(values)).reshape(-1, 1)
    y = values.values
    
    model = LinearRegression()
    model.fit(X, y)
    
    trend = "Increasing" if model.coef_[0] > 0 else "Decreasing"
    trend_strength = abs(model.coef_[0])
    
    stats = {
        'mean': values.mean(),
        'median': values.median(),
        'std': values.std(),
        'min': values.min(),
        'max': values.max(),
        'trend': trend,
        'trend_strength': trend_strength,
        'samples': len(values)
    }
    
    return stats
