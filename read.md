 AQUASENTRY-                                                                                                        
                                                                                                                      
  AI-Powered Water Quality Prediction Dashboad system💧                                                               
                                                                                                                      
  ## Overview                                                                                                         
                                                                                                                      
  AquaSentry is an AI-powered water quality prediction and monitoring dashboard built for the IBM Z Datathon 2025. The
  system integrates satellite imagery analysis, IoT sensor networks, and community health reporting to predict        
  waterborne disease risks and contamination events in real-time.                                                     
                                                                                                                      
  Core Purpose: Provide proactive water safety monitoring by correlating multiple data sources (satellite, IoT        
  sensors, health reports) to predict contamination risks and prevent waterborne disease outbreaks.                   
                                                                                                                      
  Tech Stack:                                                                                                         
                                                                                                                      
  • Frontend: Streamlit with Plotly for interactive visualizations                                                    
  • ML Models: Prophet-based time series forecasting, Random Forest classifiers                                       
  • Data Processing: Pandas, NumPy                                                                                    
  • Visualization: Plotly Express, Plotly Graph Objects                                                               
                                                                                                                      
  ## User Preferences                                                                                                 
                                                                                                                      
  Preferred communication style: Simple, everyday language.                                                           
                                                                                                                      
  ## System Architecture                                                                                              
                                                                                                                      
  ### 1. Application Structure                                                                                        
                                                                                                                      
  Single-File Architecture:                                                                                           
                                                                                                                      
  • Main entry point:  app.py  orchestrates the entire dashboard                                                      
  • Component-based organization with modular tabs for different features                                             
  • Utility modules for shared functionality (ML models, data processing, alerts)                                     
                                                                                                                      
  Design Pattern:                                                                                                     
                                                                                                                      
  • Tab-based navigation using Streamlit's native tab system                                                          
  • Each major feature is a self-contained component module                                                           
  • Separation of concerns: components (UI), utils (business logic)                                                   
                                                                                                                      
  ### 2. Core Monitoring Systems                                                                                      
                                                                                                                      
  Satellite Monitoring ( components/satellite_monitor.py ):                                                           
                                                                                                                      
  • Displays satellite imagery comparison (clean vs polluted water bodies)                                            
  • AI confidence scoring using Plotly indicator gauges                                                               
  • Real-time pollution detection with visual alerts                                                                  
  • Interactive region selection for multiple water sources                                                           
                                                                                                                      
  IoT Sensor Forecasting ( components/iot_forecasting.py ):                                                           
                                                                                                                      
  • Real-time sensor data visualization for water quality parameters (pH, turbidity, TDS, dissolved oxygen)           
  • Prophet-based ML forecasting for 12-hour contamination prediction                                                 
  • Color-coded KPI cards for risk assessment (red/yellow/green)                                                      
  • Time-series charts with dynamic updates                                                                           
                                                                                                                      
  Disease Prediction Engine ( components/disease_prediction.py ):                                                     
                                                                                                                      
  • Links water quality parameters to specific waterborne diseases                                                    
  • Probability scoring for disease risks (cholera, typhoid, dysentery, etc.)                                         
  • ML-based disease prioritization using Random Forest                                                               
  • Generates preventive recommendations based on risk factors                                                        
                                                                                                                      
  Community Health Reporting ( components/health_reporting.py ):                                                      
                                                                                                                      
  • ASHA worker portal for symptom reporting                                                                          
  • Patient demographics and symptom tracking                                                                         
  • Geographic distribution visualization                                                                             
  • Integration with alert system for outbreak detection                                                              
                                                                                                                      
  ### 3. Data Processing Architecture                                                                                 
                                                                                                                      
  Water Quality Index (WQI) Calculation:                                                                              
                                                                                                                      
  • Multi-parameter scoring algorithm combining pH, turbidity, TDS, dissolved oxygen                                  
  • Categorization: Excellent (90-100), Good (70-90), Fair (50-70), Poor (25-50), Very Poor (0-25)                    
  • Real-time calculation from sensor data                                                                            
                                                                                                                      
  Data Sources:                                                                                                       
                                                                                                                      
  • Primary: CSV files from  data/  directory                                                                         
  • Fallback: Sample data from  attached_assets/                                                                      
  • Synthetic generation: NumPy-based realistic data generation when files unavailable                                
                                                                                                                      
  ML Model Pipeline:                                                                                                  
                                                                                                                      
  • Forecasting: Custom SimpleTimeSeriesForecaster class mimicking Prophet behavior                                   
  • Classification: Random Forest for disease risk prediction and contamination detection                             
  • Feature Engineering: Time-based features (hour, day_of_week, day_of_year) for temporal patterns                   
                                                                                                                      
  ### 4. Alert & Notification System                                                                                  
                                                                                                                      
  Multi-Level Alert Architecture:                                                                                     
                                                                                                                      
  • Satellite-based alerts from imagery analysis                                                                      
  • IoT sensor threshold monitoring (pH, turbidity, DO levels)                                                        
  • Health report correlation for outbreak detection                                                                  
  • Cross-system correlation alerts when multiple systems indicate issues                                             
                                                                                                                      
  Alert Distribution:                                                                                                 
                                                                                                                      
  • Real-time dashboard banners with pulsing animation                                                                
  • Email notifications via SendGrid integration (when configured)                                                    
  • Alert severity levels: Critical, High, Moderate, Low                                                              
  • Historical alert logging for trend analysis                                                                       
                                                                                                                      
  ### 5. Visualization Strategy                                                                                       
                                                                                                                      
  Charting Library: Plotly for all visualizations                                                                     
                                                                                                                      
  • Interactive time-series charts with zoom/pan                                                                      
  • Gauge indicators for AI confidence scores                                                                         
  • Geographic heatmaps for pollution distribution                                                                    
  • Multi-panel dashboards using subplots                                                                             
                                                                                                                      
  Color Coding System:                                                                                                
                                                                                                                      
  • Green: Safe/Normal conditions                                                                                     
  • Yellow: Moderate risk/Warning                                                                                     
  • Red: High risk/Critical alert                                                                                     
  • Gradient backgrounds for IBM Z branding (#002B5B to #00B4D8)                                                      
                                                                                                                      
  ### 6. Export & Reporting                                                                                           
                                                                                                                      
  Data Export Formats:                                                                                                
                                                                                                                      
  • CSV for water quality data                                                                                        
  • JSON for API integration                                                                                          
  • Excel for comprehensive reports                                                                                   
  • Disease prediction summaries                                                                                      
  • Health report analytics                                                                                           
                                                                                                                      
  Report Types:                                                                                                       
                                                                                                                      
  • Real-time sensor readings                                                                                         
  • Disease risk assessments                                                                                          
  • Historical trend analysis                                                                                         
  • Geographic distribution reports                                                                                   
                                                                                                                      
  ## External Dependencies                                                                                            
                                                                                                                      
  ### Required Python Packages                                                                                        
                                                                                                                      
  •  streamlit  - Web application framework                                                                           
  •  plotly  - Interactive visualization library                                                                      
  •  pandas  - Data manipulation and analysis                                                                         
  •  numpy  - Numerical computing                                                                                     
  •  scikit-learn  - Machine learning algorithms (RandomForest)                                                       
  •  Pillow (PIL)  - Image processing for satellite imagery                                                           
  •  openpyxl  - Excel file generation                                                                                
                                                                                                                      
  ### Optional Integrations                                                                                           
                                                                                                                      
  • SendGrid - Email alert delivery (configured via  SENDGRID_API_KEY  environment variable)                          
  • Health authority email configured via  HEALTH_AUTHORITY_EMAIL  environment variable                               
                                                                                                                      
  ### Data Requirements                                                                                               
                                                                                                                      
  • Water quality CSV files with columns: pH, Turbidity, TDS, Dissolved_Oxygen, Temperature, Conductivity, Potability 
  • Satellite images:  clean_lake.png ,  polluted_lake.png  (referenced but not strictly required)                    
  • Historical health data for trend analysis                                                                         
                                                                                                                      
  Thankyou❤️  