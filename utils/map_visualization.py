import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

def create_pollution_hotspot_map(water_data, location_data=None):
    """Create interactive map showing pollution hotspots"""
    
    # Generate sample location data if not provided
    if location_data is None:
        # Sample coordinates for Bangalore region
        np.random.seed(42)
        n_locations = min(len(water_data), 50)
        
        # Bangalore coordinates: approximately 12.9716° N, 77.5946° E
        base_lat = 12.9716
        base_lon = 77.5946
        
        location_data = pd.DataFrame({
            'lat': base_lat + np.random.uniform(-0.5, 0.5, n_locations),
            'lon': base_lon + np.random.uniform(-0.5, 0.5, n_locations),
            'location_name': [f'Station {i+1}' for i in range(n_locations)]
        })
    
    # Calculate pollution level for each location based on water quality data
    pollution_scores = []
    for i in range(len(location_data)):
        # Sample water quality for this location
        if i < len(water_data):
            sample = water_data.iloc[i]
            
            # Calculate pollution score (0-100, higher is worse)
            score = 0
            
            # pH factor
            ph = sample.get('ph', 7.0)
            if ph < 6.5 or ph > 8.5:
                score += 25
            
            # Turbidity factor
            turbidity = sample.get('Turbidity', 2.0)
            if turbidity > 5:
                score += 25
            
            # TDS factor
            tds = sample.get('TDS', 500)
            if tds > 1000:
                score += 25
            
            # Dissolved Oxygen factor
            do = sample.get('Dissolved_Oxygen', 8.0)
            if do < 5:
                score += 25
            
            pollution_scores.append(score)
        else:
            pollution_scores.append(np.random.uniform(0, 100))
    
    location_data['pollution_score'] = pollution_scores
    location_data['pollution_level'] = location_data['pollution_score'].apply(
        lambda x: 'Critical' if x >= 75 else 'High' if x >= 50 else 'Moderate' if x >= 25 else 'Low'
    )
    
    # Color mapping
    color_map = {
        'Critical': '#FF6B6B',
        'High': '#FF9800',
        'Moderate': '#FFC107',
        'Low': '#4CAF50'
    }
    
    location_data['color'] = location_data['pollution_level'].map(color_map)
    
    # Create map using plotly
    fig = go.Figure()
    
    for level in ['Low', 'Moderate', 'High', 'Critical']:
        level_data = location_data[location_data['pollution_level'] == level]
        if len(level_data) > 0:
            fig.add_trace(go.Scattermapbox(
                lat=level_data['lat'],
                lon=level_data['lon'],
                mode='markers',
                marker=dict(
                    size=level_data['pollution_score'] / 3 + 10,
                    color=color_map[level],
                    opacity=0.7
                ),
                text=level_data['location_name'] + '<br>' + 
                     'Pollution Level: ' + level + '<br>' + 
                     'Score: ' + level_data['pollution_score'].astype(str),
                hovertemplate='<b>%{text}</b><extra></extra>',
                name=level
            ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=base_lat, lon=base_lon),
            zoom=9
        ),
        height=600,
        title="Pollution Hotspot Map - Bangalore Region",
        font=dict(color="#CAF0F8"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(30, 58, 95, 0.8)',
            bordercolor="#00B4D8",
            borderwidth=1
        )
    )
    
    return fig, location_data

def create_heatmap_visualization(water_data):
    """Create heatmap of water quality parameters over time"""
    
    # Select parameters for heatmap
    params = ['ph', 'Turbidity', 'TDS', 'Dissolved_Oxygen', 'Temperature']
    available_params = [p for p in params if p in water_data.columns]
    
    if not available_params:
        st.warning("No suitable parameters available for heatmap")
        return None
    
    # Create normalized data for heatmap
    heatmap_data = water_data[available_params].tail(50)  # Last 50 samples
    
    # Normalize data to 0-1 scale
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(heatmap_data)
    
    fig = go.Figure(data=go.Heatmap(
        z=normalized_data.T,
        x=[f'Sample {i+1}' for i in range(len(normalized_data))],
        y=available_params,
        colorscale=[
            [0, '#4CAF50'],      # Low - Green
            [0.33, '#FFC107'],   # Moderate - Yellow
            [0.66, '#FF9800'],   # High - Orange
            [1, '#FF6B6B']       # Critical - Red
        ],
        hovertemplate='Parameter: %{y}<br>Sample: %{x}<br>Value: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Water Quality Parameters Heatmap (Last 50 Samples)",
        xaxis_title="Sample",
        yaxis_title="Parameter",
        height=400,
        font=dict(color="#CAF0F8"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_geographic_distribution_chart(health_reports):
    """Create geographic distribution of health reports"""
    
    if not health_reports or len(health_reports) == 0:
        return None
    
    # Count reports by district
    districts = [report.get('district', 'Unknown') for report in health_reports]
    district_counts = pd.Series(districts).value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=district_counts.index,
            y=district_counts.values,
            marker_color='#00B4D8',
            text=district_counts.values,
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Health Reports by District",
        xaxis_title="District",
        yaxis_title="Number of Reports",
        height=400,
        font=dict(color="#CAF0F8"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
