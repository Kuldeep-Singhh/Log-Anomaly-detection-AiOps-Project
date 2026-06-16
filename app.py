import streamlit as st
import pandas as pd
from src.parser import LogParser
from src.detector import AnomalyDetector
from src.runbook import get_runbook_actions

# --- Page Config ---
st.set_page_config(page_title="Server Log Anomaly Detector", layout="wide", page_icon="🔍")

# --- Custom CSS ---
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
    }
    .metric-value.anomaly {
        color: #F44336;
    }
    .metric-label {
        font-size: 1rem;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# --- Title and Description ---
st.title("🔍 Server Log Anomaly Detector")
st.markdown("Upload your server logs to automatically detect performance bottlenecks and unusual error patterns using ML and statistical rules.")

# --- File Ingestion ---
uploaded_file = st.file_uploader("Upload Server Log File (.log, .txt, .csv)", type=['log', 'txt', 'csv'])

if uploaded_file is not None:
    # --- Parsing ---
    with st.spinner("Parsing logs..."):
        parser = LogParser()
        df = parser.parse(uploaded_file)
        
    if df.empty:
        st.error("No valid logs could be parsed from the file. Please check the format.")
    else:
        # --- Anomaly Detection ---
        with st.spinner("Detecting anomalies..."):
            detector = AnomalyDetector()
            results_df = detector.detect(df)
            
        total_logs = len(results_df)
        flagged_logs = results_df['is_anomaly'].sum()
        
        # --- Dashboard Display ---
        st.header("Dashboard Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Logs Processed</div>
                <div class="metric-value">{total_logs}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Flagged Anomalies</div>
                <div class="metric-value anomaly">{flagged_logs}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # --- Data Table ---
        st.subheader("⚠️ Detected Anomalies")
        if flagged_logs == 0:
            st.success("No anomalies detected in the uploaded logs! Your system appears healthy.")
        else:
            anomalies_df = results_df[results_df['is_anomaly']].copy()
            # Clean up display columns
            hide_cols = ['anomaly_text', 'anomaly_stat', 'cluster', 'is_anomaly']
            display_cols = [c for c in anomalies_df.columns if c not in hide_cols]
            
            # Put the reason column at the front for better visibility
            if 'anomaly_reason' in display_cols:
                display_cols.insert(0, display_cols.pop(display_cols.index('anomaly_reason')))
                
            st.dataframe(anomalies_df[display_cols], use_container_width=True)
            
            # --- Runbook Integration ---
            st.markdown("---")
            st.subheader("🛠️ DevOps Troubleshooting Runbook")
            st.markdown("Actionable steps based on the detected error patterns:")
            
            # Aggregate runbook actions based on the unique reasons found
            unique_reasons = anomalies_df['anomaly_reason'].unique()
            all_actions = set()
            for reason in unique_reasons:
                if pd.notna(reason) and str(reason).strip():
                    actions = get_runbook_actions(reason)
                    all_actions.update(actions)
                    
            if all_actions:
                for idx, action in enumerate(sorted(list(all_actions)), 1):
                    st.info(f"**Step {idx}:** {action}")
            else:
                st.write("No specific runbook actions available. Manual investigation recommended.")
                
        # Optional: Show raw data expander
        with st.expander("View Raw Parsed Data"):
            st.dataframe(results_df, use_container_width=True)
