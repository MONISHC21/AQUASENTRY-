import pandas as pd
import streamlit as st
from datetime import datetime
import json
import io

def export_water_quality_data(water_data, format='csv'):
    """Export water quality data in various formats"""
    try:
        if format == 'csv':
            # Convert to CSV
            csv_buffer = io.StringIO()
            water_data.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'water_quality_data_{timestamp}.csv'
            
            st.download_button(
                label="📥 Download Water Quality Data (CSV)",
                data=csv_data,
                file_name=filename,
                mime='text/csv',
                key=f'download_water_{format}'
            )
            return True
            
        elif format == 'json':
            # Convert to JSON
            json_data = water_data.to_json(orient='records', indent=2)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'water_quality_data_{timestamp}.json'
            
            st.download_button(
                label="📥 Download Water Quality Data (JSON)",
                data=json_data,
                file_name=filename,
                mime='application/json',
                key=f'download_water_{format}'
            )
            return True
            
        elif format == 'excel':
            # Convert to Excel
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                water_data.to_excel(writer, sheet_name='Water Quality Data', index=False)
            excel_data = excel_buffer.getvalue()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'water_quality_data_{timestamp}.xlsx'
            
            st.download_button(
                label="📥 Download Water Quality Data (Excel)",
                data=excel_data,
                file_name=filename,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                key=f'download_water_{format}'
            )
            return True
            
    except Exception as e:
        st.error(f"Failed to export water quality data: {str(e)}")
        return False

def export_health_reports(health_reports, format='csv'):
    """Export health reports data"""
    try:
        if not health_reports or len(health_reports) == 0:
            st.warning("No health reports available to export")
            return False
        
        # Convert health reports to DataFrame
        reports_data = []
        for report in health_reports:
            report_copy = report.copy()
            # Convert symptoms list to string
            if 'symptoms' in report_copy:
                report_copy['symptoms'] = ', '.join(report_copy['symptoms'])
            # Convert date to string
            if 'date' in report_copy:
                report_copy['date'] = report_copy['date'].strftime('%Y-%m-%d %H:%M:%S')
            reports_data.append(report_copy)
        
        df = pd.DataFrame(reports_data)
        
        if format == 'csv':
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'health_reports_{timestamp}.csv'
            
            st.download_button(
                label="📥 Download Health Reports (CSV)",
                data=csv_data,
                file_name=filename,
                mime='text/csv',
                key=f'download_health_{format}'
            )
            return True
            
        elif format == 'json':
            json_data = json.dumps(reports_data, indent=2, default=str)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'health_reports_{timestamp}.json'
            
            st.download_button(
                label="📥 Download Health Reports (JSON)",
                data=json_data,
                file_name=filename,
                mime='application/json',
                key=f'download_health_{format}'
            )
            return True
            
        elif format == 'excel':
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Health Reports', index=False)
            excel_data = excel_buffer.getvalue()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'health_reports_{timestamp}.xlsx'
            
            st.download_button(
                label="📥 Download Health Reports (Excel)",
                data=excel_data,
                file_name=filename,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                key=f'download_health_{format}'
            )
            return True
            
    except Exception as e:
        st.error(f"Failed to export health reports: {str(e)}")
        return False

def export_disease_predictions(disease_data, format='csv'):
    """Export disease prediction data"""
    try:
        # Create DataFrame from disease data
        df = pd.DataFrame([disease_data])
        
        if format == 'csv':
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'disease_predictions_{timestamp}.csv'
            
            st.download_button(
                label="📥 Download Disease Predictions (CSV)",
                data=csv_data,
                file_name=filename,
                mime='text/csv',
                key=f'download_disease_{format}'
            )
            return True
            
        elif format == 'json':
            json_data = json.dumps(disease_data, indent=2)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'disease_predictions_{timestamp}.json'
            
            st.download_button(
                label="📥 Download Disease Predictions (JSON)",
                data=json_data,
                file_name=filename,
                mime='application/json',
                key=f'download_disease_{format}'
            )
            return True
            
    except Exception as e:
        st.error(f"Failed to export disease predictions: {str(e)}")
        return False

def export_comprehensive_report(water_data, health_reports, disease_risks, alerts):
    """Generate and export comprehensive dashboard report"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create comprehensive Excel report with multiple sheets
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            # Water Quality Data
            water_data.to_excel(writer, sheet_name='Water Quality', index=False)
            
            # Health Reports
            if health_reports and len(health_reports) > 0:
                reports_data = []
                for report in health_reports:
                    report_copy = report.copy()
                    if 'symptoms' in report_copy:
                        report_copy['symptoms'] = ', '.join(report_copy['symptoms'])
                    if 'date' in report_copy:
                        report_copy['date'] = report_copy['date'].strftime('%Y-%m-%d %H:%M:%S')
                    reports_data.append(report_copy)
                pd.DataFrame(reports_data).to_excel(writer, sheet_name='Health Reports', index=False)
            
            # Disease Risks
            if disease_risks:
                disease_df = pd.DataFrame([disease_risks])
                disease_df.to_excel(writer, sheet_name='Disease Risks', index=False)
            
            # Alerts
            if alerts and len(alerts) > 0:
                alerts_df = pd.DataFrame(alerts)
                alerts_df.to_excel(writer, sheet_name='Alerts', index=False)
            
            # Summary Statistics
            summary_data = {
                'Report Generated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                'Total Water Samples': [len(water_data)],
                'Total Health Reports': [len(health_reports) if health_reports else 0],
                'Total Alerts': [len(alerts) if alerts else 0],
                'Average Water Quality': [water_data['Potability'].mean() if 'Potability' in water_data.columns else 'N/A']
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        excel_data = excel_buffer.getvalue()
        filename = f'comprehensive_water_report_{timestamp}.xlsx'
        
        st.download_button(
            label="📥 Download Comprehensive Report (Excel)",
            data=excel_data,
            file_name=filename,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            key='download_comprehensive'
        )
        return True
        
    except Exception as e:
        st.error(f"Failed to generate comprehensive report: {str(e)}")
        return False
