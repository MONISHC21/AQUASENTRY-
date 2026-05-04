# 💧 AquaSentry – AI-Powered Water Quality Prediction Dashboard

## 🌍 Overview
AquaSentry is an AI-powered system that monitors and predicts water quality in real-time.  
It combines satellite data, IoT sensors, and health reports to detect contamination risks and prevent waterborne diseases.

🎯 **Goal:**  
To provide early warnings about unsafe water and help prevent disease outbreaks.

---

## 🚀 Key Features

### 🛰️ Satellite Monitoring
- Compare clean vs polluted water images  
- AI-based pollution detection  
- Confidence score using visual indicators  
- Region-based analysis  

### 📡 IoT Sensor Monitoring
- Tracks water parameters:
  - pH  
  - Turbidity  
  - TDS  
  - Dissolved Oxygen  
- Real-time data visualization  
- 12-hour future prediction using AI  
- Color-coded risk indicators (🟢 🟡 🔴)

### 🦠 Disease Prediction
- Predicts diseases like:
  - Cholera  
  - Typhoid  
  - Dysentery  
- Uses ML models to estimate risk probability  
- Suggests preventive actions  

### 🏥 Community Health Reporting
- Health workers can report symptoms  
- Tracks patient data and location  
- Helps detect early outbreaks  

---

## 🧠 Tech Stack

| Category           | Tools Used |
|------------------|-----------|
| Frontend         | Streamlit |
| Visualization    | Plotly |
| Machine Learning | Random Forest, Time Series Forecasting |
| Data Handling    | Pandas, NumPy |

---

## ⚙️ System Architecture

### 🧩 Structure
- Main file: `app.py`
- Modular components for each feature
- Clean separation:
  - UI → Components  
  - Logic → Utils  

### 📊 Core Modules
- `satellite_monitor.py`
- `iot_forecasting.py`
- `disease_prediction.py`
- `health_reporting.py`

---

## 📈 Data Processing

### 💧 Water Quality Index (WQI)
Water quality is calculated using:
- pH  
- Turbidity  
- TDS  
- Dissolved Oxygen  

| Score | Category |
|------|---------|
| 90–100 | Excellent |
| 70–90 | Good |
| 50–70 | Fair |
| 25–50 | Poor |
| 0–25  | Very Poor |

---

## 🔔 Alert System

Multi-level alerts based on:
- Satellite data  
- Sensor readings  
- Health reports  

### 🚨 Alert Levels:
- 🔴 Critical  
- 🟠 High  
- 🟡 Moderate  
- 🟢 Low  

Alerts are shown:
- On dashboard (real-time)  
- Via email (optional)  

---

## 📊 Visualization
- Interactive charts (zoom & pan)  
- AI confidence gauges  
- Heatmaps for pollution  
- Color-coded dashboard  

---

## 📤 Export Options
You can export data as:
- CSV  
- JSON  
- Excel  

Reports include:
- Water quality data  
- Disease predictions  
- Historical trends  

---

## 📦 Requirements

Install dependencies:

```bash
pip install streamlit plotly pandas numpy scikit-learn pillow openpyxl
```
---
## ▶️ How to Run

```bash
streamlit run app.py
```
---
  ### Optional Integrations                                                                                           
                                                                                                                      
  • SendGrid - Email alert delivery (configured via  SENDGRID_API_KEY  environment variable)                          
  • Health authority email configured via  HEALTH_AUTHORITY_EMAIL  environment variable
---

<img width="1073" height="767" alt="Image" src="https://github.com/user-attachments/assets/00268f2a-eef7-4804-8cf5-70d93218403b" />
<img width="1352" height="718" alt="Image" src="https://github.com/user-attachments/assets/297f295d-4364-4b3b-803e-260f584a32f3" />
<img width="798" height="679" alt="Image" src="https://github.com/user-attachments/assets/808ebb55-9de3-4312-93ba-5e8c788a45cf" />
<img width="1355" height="725" alt="Image" src="https://github.com/user-attachments/assets/55216503-bd53-42f9-9e1f-3ba8441c2966" />

 ---
                                                                                                                      
  ### Data Requirements                                                                                               
                                                                                                                      
  • Water quality CSV files with columns: pH, Turbidity, TDS, Dissolved_Oxygen, Temperature, Conductivity, Potability 
  • Satellite images:  clean_lake.png ,  polluted_lake.png  (referenced but not strictly required)                    
  • Historical health data for trend analysis                                                                         
                                                                                                             ## 💡 Use Cases
- Smart city water monitoring  
- Rural health protection  
- Disaster response (flood contamination)  
- Government water safety systems  

---

## ❤️ Acknowledgment
Developed for **IBM Z Datathon 2025**

---

## ✨ Summary
AquaSentry helps:
- ✔ Detect unsafe water early  
- ✔ Predict disease risks  
- ✔ Enable faster response  
- ✔ Save lives  

  Thankyou❤️  
