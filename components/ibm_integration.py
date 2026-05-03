import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

def ibm_integration_sidebar():
    """IBM Z integration explanation and system architecture sidebar"""
    
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #002B5B 0%, #00B4D8 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="color: white; text-align: center; margin: 0;">
                <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='30' height='30' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M12 2L2 7v10c0 5.55 3.84 9.74 9 9.74s9-4.19 9-9.74V7L12 2z'/%3E%3C/svg%3E" style="vertical-align: middle; margin-right: 10px;">
                IBM Z Integration
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # System architecture overview
        st.subheader("🏗️ System Architecture")
        
        st.markdown("""
        **Core Infrastructure:**
        - IBM Z15 Mainframe Systems
        - z/OS Operating System
        - IBM Db2 for z/OS Database
        - IBM MQ Message Queuing
        - IBM CICS Transaction Processing
        """)
        
        # Real-time processing metrics
        st.subheader("⚡ Real-time Metrics")
        
        # Simulated real-time metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Transactions/sec", "12,450", delta="342")
            st.metric("Response Time", "1.2ms", delta="-0.1ms")
        
        with col2:
            st.metric("System Load", "68%", delta="2%")
            st.metric("Uptime", "99.97%", delta="0.01%")
        
        # Security features
        st.subheader("🔒 Security Features")
        
        security_features = [
            "End-to-end encryption (AES-256)",
            "Pervasive encryption at rest",
            "Hardware Security Modules (HSM)",
            "Multi-factor authentication",
            "Secure enclaves for AI processing",
            "Audit trail and compliance logging"
        ]
        
        for feature in security_features:
            st.markdown(f"✅ {feature}")
        
        # Scalability metrics
        st.subheader("📈 Scalability Stats")
        
        # Create a mini performance chart
        import numpy as np
        hours = list(range(24))
        load = [45 + 20 * np.sin(2 * np.pi * h / 24) + np.random.normal(0, 3) for h in hours]
        load = [max(20, min(90, l)) for l in load]  # Clamp between 20-90%
        
        fig_load = go.Figure()
        fig_load.add_trace(go.Scatter(
            x=hours,
            y=load,
            mode='lines+markers',
            name='System Load %',
            line=dict(color='#00B4D8', width=2),
            marker=dict(size=4)
        ))
        
        fig_load.update_layout(
            height=200,
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(title="Hour", showgrid=False),
            yaxis=dict(title="Load %", range=[0, 100], showgrid=True),
            font=dict(size=10, color="#CAF0F8"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_load, width="stretch")
        
        # Data processing capabilities
        st.subheader("🔄 Data Processing")
        
        processing_stats = {
            "Satellite Images": "2.4TB/day",
            "IoT Data Points": "8.9M/hour", 
            "Health Reports": "15K/day",
            "ML Predictions": "50K/hour"
        }
        
        for stat, value in processing_stats.items():
            st.markdown(f"**{stat}:** {value}")
        
        # AI/ML acceleration
        st.subheader("🧠 AI/ML Acceleration")
        
        st.markdown("""
        **IBM Integrated Accelerator for AI:**
        - TensorFlow/PyTorch optimization
        - Real-time inference < 5ms
        - Parallel model execution
        - Auto-scaling based on load
        - GPU-accelerated training
        """)
        
        # Integration benefits
        st.subheader("💪 Key Benefits")
        
        benefits = [
            "**99.999% Availability**: Mission-critical uptime",
            "**Linear Scalability**: Handle population-scale data", 
            "**Sub-second Latency**: Real-time contamination alerts",
            "**Data Integrity**: Zero data loss guarantee",
            "**Compliance Ready**: Healthcare & govt standards",
            "**Cost Efficiency**: Pay-per-use consumption model"
        ]
        
        for benefit in benefits:
            st.markdown(f"• {benefit}")
        
        # Deployment architecture
        with st.expander("🌐 Deployment Architecture"):
            st.markdown("""
            **National Deployment:**
            - 5 Regional Data Centers
            - 500+ Edge Computing Nodes
            - 10,000+ IoT Sensor Networks
            - 50,000+ ASHA Worker Devices
            
            **Disaster Recovery:**
            - Real-time data replication
            - Automated failover < 30 seconds
            - Geographic load balancing
            - Emergency communication protocols
            """)
        
        # Technical specifications
        with st.expander("⚙️ Technical Specifications"):
            st.markdown("""
            **Hardware:**
            - IBM z15 T02 (190 cores)
            - 40TB Memory
            - 100TB NVMe Storage
            - 25Gb Network Connectivity
            
            **Software Stack:**
            - z/OS 2.5
            - IBM Db2 13 for z/OS
            - IBM MQ 9.3
            - IBM CICS TS 6.1
            - IBM Machine Learning for z/OS
            """)
        
        # Contact information
        st.markdown("---")
        st.markdown("**📞 Technical Support**")
        st.markdown("Email: ibm-z-support@datathon2025.com")
        st.markdown("Phone: 1-800-IBM-ZEDS")
        
        # System status indicator
        st.markdown(f"""
        <div style="background: #4CAF50; padding: 0.5rem; border-radius: 5px; text-align: center; margin-top: 1rem;">
            <strong style="color: white;">🟢 ALL SYSTEMS OPERATIONAL</strong><br>
            <small style="color: white;">Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """, unsafe_allow_html=True)

def display_integration_details():
    """Display detailed IBM Z integration information in main content area"""
    
    st.header("🏗️ IBM Z System Integration Architecture")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📡 Data Ingestion Layer")
        st.markdown("""
        **Satellite Data Processing:**
        - Real-time image processing pipelines
        - Multi-spectral analysis algorithms
        - Cloud detection and filtering
        - Automated quality assessment
        
        **IoT Sensor Integration:**
        - MQTT message broker cluster
        - Edge computing preprocessing
        - Data validation and cleansing  
        - Real-time aggregation
        
        **Health Report System:**
        - Mobile app data synchronization
        - ASHA worker authentication
        - Encrypted data transmission
        - Offline capability support
        """)
    
    with col2:
        st.subheader("🧮 Processing & Analytics")
        st.markdown("""
        **IBM Z AI Acceleration:**
        - TensorFlow Serving optimization
        - Parallel inference execution
        - Model versioning and A/B testing
        - Auto-scaling based on demand
        
        **Database Operations:**
        - High-frequency OLTP processing
        - Real-time analytics (HTAP)
        - Automatic indexing optimization
        - Data compression and archiving
        
        **Security Processing:**
        - Pervasive encryption
        - Hardware security modules
        - Access control and audit trails
        - Compliance reporting
        """)
    
    with col3:
        st.subheader("📤 Output & Integration")
        st.markdown("""
        **Real-time Alerts:**
        - Sub-second alert generation
        - Multi-channel notification
        - Priority-based routing
        - Delivery confirmation tracking
        
        **Dashboard Serving:**
        - High-concurrency web serving
        - Caching and optimization
        - Mobile-responsive delivery
        - Offline synchronization
        
        **API Services:**
        - RESTful API endpoints
        - GraphQL query optimization
        - Rate limiting and throttling
        - Documentation and SDKs
        """)
    
    # Performance metrics visualization
    st.subheader("📊 System Performance Metrics")
    
    # Create performance dashboard
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        # Transaction processing metrics
        fig_transactions = go.Figure()
        
        hours = list(range(24))
        base_tps = 10000
        tps_variation = [base_tps + 3000 * np.sin(2 * np.pi * h / 24) + np.random.normal(0, 500) for h in hours]
        tps_variation = [max(5000, t) for t in tps_variation]
        
        fig_transactions.add_trace(go.Scatter(
            x=hours,
            y=tps_variation,
            mode='lines+markers',
            name='Transactions per Second',
            line=dict(color='#00B4D8', width=3),
            fill='tonexty'
        ))
        
        fig_transactions.update_layout(
            title="24-Hour Transaction Processing",
            xaxis_title="Hour of Day",
            yaxis_title="Transactions/Second",
            height=350,
            font=dict(color="#CAF0F8"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_transactions, use_container_width=True)
    
    with perf_col2:
        # Response time distribution
        response_times = np.random.gamma(2, 0.5, 1000)  # Gamma distribution for realistic response times
        
        fig_response = go.Figure()
        fig_response.add_trace(go.Histogram(
            x=response_times,
            nbinsx=30,
            name='Response Time Distribution',
            marker_color='#4CAF50'
        ))
        
        fig_response.update_layout(
            title="Response Time Distribution",
            xaxis_title="Response Time (ms)",
            yaxis_title="Frequency",
            height=350,
            font=dict(color="#CAF0F8"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_response, use_container_width=True)
    
    # System architecture diagram
    st.subheader("🏛️ High-Level System Architecture")
    
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────────┐
    │                    Data Sources Layer                           │
    ├─────────────────┬─────────────────┬─────────────────────────────┤
    │ Satellite APIs  │ IoT Sensors     │ ASHA Health Reports         │
    │ • Sentinel-2    │ • pH Sensors    │ • Mobile Applications       │
    │ • Landsat       │ • Turbidity     │ • Web Portal               │
    │ • WorldView     │ • DO Sensors    │ • SMS Gateway              │
    └─────────────────┴─────────────────┴─────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                 IBM Z Processing Layer                          │
    ├─────────────────┬─────────────────┬─────────────────────────────┤
    │ Data Ingestion  │ AI/ML Pipeline  │ Real-time Analytics        │
    │ • Message Queue │ • Prophet ML    │ • Disease Prediction       │
    │ • Data Validation│ • Image Analysis│ • Risk Assessment         │
    │ • Edge Computing│ • Alert Engine  │ • Correlation Analysis     │
    └─────────────────┴─────────────────┴─────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                   Output & Integration                          │
    ├─────────────────┬─────────────────┬─────────────────────────────┤
    │ Web Dashboard   │ Mobile Apps     │ Alert Systems              │
    │ • Real-time UI  │ • ASHA Portal   │ • Email Notifications      │
    │ • Plotly Charts │ • Health Reports│ • SMS Alerts               │
    │ • Interactive   │ • Offline Sync  │ • API Integrations         │
    └─────────────────┴─────────────────┴─────────────────────────────┘
    ```
    """)