import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# Simple Prophet-like forecasting implementation
class SimpleTimeSeriesForecaster:
    """Simple time series forecasting model similar to Prophet"""
    
    def __init__(self):
        self.model = None
        self.is_fitted = False
        
    def fit(self, df, value_col='value', time_col='timestamp'):
        """Fit the model on historical data"""
        try:
            # Convert timestamps to numeric features
            df_copy = df.copy()
            df_copy['time_numeric'] = (df_copy[time_col] - df_copy[time_col].min()).dt.total_seconds() / 3600
            df_copy['hour'] = df_copy[time_col].dt.hour
            df_copy['day_of_week'] = df_copy[time_col].dt.dayofweek
            df_copy['day_of_year'] = df_copy[time_col].dt.dayofyear
            
            # Features for time series
            X = df_copy[['time_numeric', 'hour', 'day_of_week', 'day_of_year']]
            y = df_copy[value_col]
            
            # Use Random Forest for regression
            self.model = RandomForestRegressor(n_estimators=50, random_state=42)
            self.model.fit(X, y)
            self.is_fitted = True
            self.time_min = df_copy[time_col].min()
            
        except Exception as e:
            st.error(f"Error fitting forecasting model: {e}")
            self.is_fitted = False
    
    def predict(self, future_timestamps):
        """Make predictions for future timestamps"""
        if not self.is_fitted:
            return np.array([])
        
        try:
            # Create feature matrix for future predictions
            future_df = pd.DataFrame({'timestamp': future_timestamps})
            future_df['time_numeric'] = (future_df['timestamp'] - self.time_min).dt.total_seconds() / 3600
            future_df['hour'] = future_df['timestamp'].dt.hour
            future_df['day_of_week'] = future_df['timestamp'].dt.dayofweek
            future_df['day_of_year'] = future_df['timestamp'].dt.dayofyear
            
            X_future = future_df[['time_numeric', 'hour', 'day_of_week', 'day_of_year']]
            predictions = self.model.predict(X_future)
            
            return predictions
            
        except Exception as e:
            st.error(f"Error making predictions: {e}")
            return np.array([])

def forecast_water_parameters(iot_data, hours_ahead=12):
    """Forecast water quality parameters using time series models"""
    
    forecasts = {}
    parameters = ['ph', 'turbidity', 'tds', 'dissolved_oxygen', 'temperature', 'conductivity']
    
    # Filter historical data only
    historical_data = iot_data[iot_data['is_historical']].copy()
    
    if len(historical_data) < 24:  # Need at least 24 hours of data
        st.warning("Insufficient historical data for reliable forecasting")
        return {}
    
    # Generate future timestamps
    last_timestamp = historical_data['timestamp'].max()
    future_timestamps = [last_timestamp + timedelta(hours=i) for i in range(1, hours_ahead + 1)]
    
    for param in parameters:
        try:
            # Initialize and fit forecaster
            forecaster = SimpleTimeSeriesForecaster()
            forecaster.fit(historical_data, value_col=param, time_col='timestamp')
            
            if forecaster.is_fitted:
                # Make predictions
                predictions = forecaster.predict(future_timestamps)
                
                if len(predictions) > 0:
                    # Create forecast dataframe
                    forecast_df = pd.DataFrame({
                        'timestamp': future_timestamps,
                        param: predictions,
                        'is_forecast': True
                    })
                    
                    # Add confidence intervals (simple approach)
                    historical_std = historical_data[param].std()
                    forecast_df[f'{param}_lower'] = predictions - 1.96 * historical_std
                    forecast_df[f'{param}_upper'] = predictions + 1.96 * historical_std
                    
                    forecasts[param] = forecast_df
                    
        except Exception as e:
            st.error(f"Error forecasting {param}: {e}")
            continue
    
    return forecasts

def predict_contamination_risk(water_data):
    """Predict contamination risk based on water quality parameters"""
    
    try:
        # Prepare features for contamination prediction
        features = ['ph', 'Turbidity', 'TDS', 'Dissolved_Oxygen', 'Temperature']
        available_features = [col for col in features if col in water_data.columns]
        
        if len(available_features) < 3:
            return None, "Insufficient data for contamination risk prediction"
        
        # Use inverse of potability as contamination risk
        X = water_data[available_features].fillna(0)
        y = 1 - water_data['Potability']  # 1 = contaminated, 0 = clean
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Get feature importance
        feature_importance = pd.DataFrame({
            'feature': available_features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'model': model,
            'accuracy': accuracy,
            'feature_importance': feature_importance,
            'features': available_features
        }, None
        
    except Exception as e:
        return None, f"Error building contamination prediction model: {e}"

def predict_disease_risk(water_params):
    """Predict disease risk based on water quality parameters"""
    
    diseases = {
        'cholera': {
            'weight': 0.0,
            'factors': {
                'ph': (6.0, 8.0, 'outside'),  # Risk when pH outside 6-8
                'turbidity': (5.0, None, 'above'),  # Risk when turbidity > 5
                'dissolved_oxygen': (5.0, None, 'below'),  # Risk when DO < 5
                'tds': (1000, None, 'above')  # Risk when TDS > 1000
            }
        },
        'typhoid': {
            'weight': 0.0,
            'factors': {
                'ph': (6.5, 8.5, 'outside'),
                'turbidity': (4.0, None, 'above'),
                'dissolved_oxygen': (6.0, None, 'below'),
                'conductivity': (400, None, 'above')
            }
        },
        'diarrhea': {
            'weight': 0.0,
            'factors': {
                'ph': (6.5, 8.5, 'outside'),
                'turbidity': (3.0, None, 'above'),
                'tds': (500, None, 'above'),
                'dissolved_oxygen': (7.0, None, 'below')
            }
        },
        'hepatitis_a': {
            'weight': 0.0,
            'factors': {
                'ph': (7.0, 8.0, 'outside'),
                'turbidity': (2.0, None, 'above'),
                'dissolved_oxygen': (8.0, None, 'below')
            }
        }
    }
    
    # Calculate risk for each disease
    disease_risks = {}
    
    for disease, config in diseases.items():
        risk_score = 0.0
        factor_count = 0
        
        for param, (threshold_low, threshold_high, condition) in config['factors'].items():
            if param in water_params:
                value = water_params[param]
                
                if condition == 'outside' and threshold_high is not None:
                    if value < threshold_low or value > threshold_high:
                        risk_score += 1.0
                elif condition == 'above' and threshold_low is not None:
                    if value > threshold_low:
                        risk_score += min(1.0, (value - threshold_low) / threshold_low)
                elif condition == 'below' and threshold_low is not None:
                    if value < threshold_low:
                        risk_score += min(1.0, (threshold_low - value) / threshold_low)
                
                factor_count += 1
        
        # Normalize risk score (0-100%)
        if factor_count > 0:
            disease_risks[disease] = min(100, (risk_score / factor_count) * 100)
        else:
            disease_risks[disease] = 0
    
    return disease_risks

def generate_preventive_recommendations(disease_risks, water_params):
    """Generate preventive action recommendations based on disease risks"""
    
    recommendations = []
    
    # High-risk diseases (>50% risk)
    high_risk_diseases = [disease for disease, risk in disease_risks.items() if risk > 50]
    
    if high_risk_diseases:
        recommendations.extend([
            "🚨 IMMEDIATE ACTION REQUIRED:",
            "• Isolate affected water sources immediately",
            "• Issue public health advisory for boiling water",
            "• Distribute emergency water supplies",
            "• Activate disease surveillance protocols"
        ])
    
    # Medium-risk diseases (25-50% risk)
    medium_risk_diseases = [disease for disease, risk in disease_risks.items() if 25 <= risk <= 50]
    
    if medium_risk_diseases:
        recommendations.extend([
            "⚠️ PREVENTIVE MEASURES:",
            "• Increase water quality monitoring frequency",
            "• Public awareness campaign on water safety",
            "• Prepare emergency response teams",
            "• Contact local health authorities"
        ])
    
    # Parameter-specific recommendations
    if 'ph' in water_params:
        if water_params['ph'] < 6.5 or water_params['ph'] > 8.5:
            recommendations.append("• Adjust water pH through treatment systems")
    
    if 'turbidity' in water_params:
        if water_params['turbidity'] > 5:
            recommendations.append("• Implement sediment filtration")
    
    if 'dissolved_oxygen' in water_params:
        if water_params['dissolved_oxygen'] < 5:
            recommendations.append("• Improve water oxygenation systems")
    
    if 'tds' in water_params:
        if water_params['tds'] > 1000:
            recommendations.append("• Install reverse osmosis treatment")
    
    if not recommendations:
        recommendations = [
            "✅ ROUTINE MONITORING:",
            "• Continue regular water quality testing",
            "• Maintain existing treatment systems",
            "• Monitor community health indicators"
        ]
    
    return recommendations

def sort_diseases_by_priority(disease_risks, water_params):
    """
    Sort diseases by priority using ML-based scoring considering:
    - Risk probability
    - Severity of disease
    - Population impact
    - Treatment availability
    """
    
    # Disease severity weights (based on mortality and morbidity)
    severity_weights = {
        'cholera': 0.9,          # High mortality if untreated
        'typhoid': 0.8,          # Moderate-high mortality
        'hepatitis_a': 0.6,      # Lower mortality, high morbidity
        'diarrhea': 0.7          # Variable severity
    }
    
    # Population impact weights (transmission potential)
    transmission_weights = {
        'cholera': 0.95,         # Highly contagious
        'typhoid': 0.75,         # Moderately contagious
        'hepatitis_a': 0.80,     # Highly contagious
        'diarrhea': 0.85         # Highly contagious
    }
    
    # Calculate priority scores using weighted combination
    priority_scores = {}
    
    for disease, risk in disease_risks.items():
        # Combine risk probability, severity, and transmission
        severity = severity_weights.get(disease, 0.5)
        transmission = transmission_weights.get(disease, 0.5)
        
        # ML-based priority score (weighted average)
        priority_score = (
            risk * 0.5 +                    # 50% weight on risk probability
            severity * 100 * 0.3 +          # 30% weight on severity
            transmission * 100 * 0.2        # 20% weight on transmission
        )
        
        priority_scores[disease] = {
            'risk': risk,
            'priority_score': priority_score,
            'severity': severity * 100,
            'transmission_potential': transmission * 100,
            'action_urgency': 'CRITICAL' if priority_score >= 75 else 'HIGH' if priority_score >= 50 else 'MODERATE' if priority_score >= 25 else 'LOW'
        }
    
    # Sort by priority score (descending)
    sorted_diseases = sorted(priority_scores.items(), key=lambda x: x[1]['priority_score'], reverse=True)
    
    return sorted_diseases
