import streamlit as st
import pandas as pd
import time
import joblib
import folium
import streamlit.components.v1 as components
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import boto3
import os

st.set_page_config(page_title="Q_Titans | Live Grid Simulation", layout="wide")

# --- 1. AWS S3 INTEGRATION (Cloud Storage) ---
@st.cache_resource
def load_assets():
    # Initialize S3 client (Ensure your EC2 instance has IAM roles or aws configure set)
    s3 = boto3.client('s3', region_name='ap-south-1') 
    bucket_name = 'qtitan' # ⚠️ CHANGE THIS to your S3 bucket name
    
    # Download from S3 to the EC2 instance if not already present
    if not os.path.exists("rf_model.pkl"):
        try:
            s3.download_file(bucket_name, 'rf_model.pkl', 'rf_model.pkl')
        except Exception as e:
            st.error(f"Failed to download model from S3: {e}")
            
    if not os.path.exists("live_stream_data.csv"):
        try:
            s3.download_file(bucket_name, 'live_stream_data.csv', 'live_stream_data.csv')
        except Exception as e:
            st.error(f"Failed to download data from S3: {e}")
            
    # Load the downloaded files into memory
    model = joblib.load("rf_model.pkl")
    stream_data = pd.read_csv("live_stream_data.csv")
    return model, stream_data

try:
    model, stream_data = load_assets()
except Exception as e:
    st.error("⚠️ S3 Download Failed. Ensure your bucket name is correct and credentials are set.")
    st.stop()

# --- 2. AWS SNS INTEGRATION (Mobile Alerts) ---
# Initialize the SNS client for vernacular alerts
sns_client = boto3.client('sns', region_name='ap-south-1')

st.title("💧 Q_Titans: Real-Time AI Leakage Simulation")
st.markdown("**Powered by AWS EC2, S3, and SNS (Local Monolith MVP)**")

# --- 3. UI LAYOUT ---
control_col, clock_col = st.columns([1, 2])
with control_col:
    start_sim = st.button("▶️ Start Time-Series Simulation", type="primary")
    num_steps = st.slider("Records to simulate", min_value=10, max_value=100, value=30)

with clock_col:
    clock_placeholder = st.empty()

# Placeholders for dynamic content to update in place
map_placeholder = st.empty()
metrics_placeholder = st.empty()
results_placeholder = st.empty()

# --- 4. SIMULATION LOGIC ---
if start_sim:
    actuals = []
    predictions = []
    
    for i in range(num_steps):
        row = stream_data.iloc[i]
        
        # Update the Clock
        current_time = row["Timestamp"]
        clock_placeholder.markdown(f"### 🕒 Current Grid Time: `{current_time}`")
        
        # Extract Features & Run Inference (Warning Fixed with Labeled DataFrame)
        feature_names = ["Pressure_bar", "Flow_Rate_Ls", "Temperature_C"]
        features_df = pd.DataFrame(
            [[row["Pressure_bar"], row["Flow_Rate_Ls"], row["Temperature_C"]]], 
            columns=feature_names
        )
        
        # Random Forest Prediction
        prediction = model.predict(features_df)[0]
        
        actuals.append(row["Leak_Status"])
        predictions.append(prediction)
        
        # Update the Live Map (Using raw HTML to prevent Streamlit crashes)
        m = folium.Map(location=[21.7781, 87.7517], zoom_start=14)
        
        node_color = "red" if prediction == 1 else "green"
        status_text = "LEAK DETECTED!" if prediction == 1 else "Normal"
        
        folium.Marker(
            [row["Latitude"], row["Longitude"]], 
            popup=f"{row['Node_ID']} - {status_text}", 
            icon=folium.Icon(color=node_color, icon="tint" if prediction==1 else "info-sign")
        ).add_to(m)
        
        with map_placeholder.container():
            components.html(m._repr_html_(), height=400)
            
        # Display current metrics & Fire AWS SNS Alert
        with metrics_placeholder.container():
            if prediction == 1:
                st.error(f"🚨 **CRITICAL ALERT | Node:** {row['Node_ID']} | **Pressure:** {row['Pressure_bar']:.2f} bar | **AI Status:** {status_text}")
                
                # TRIGGER AWS SNS VERNACULAR SMS ALERT
                try:
                    message = f"🚨 Q-TITANS चेतावनी: {row['Node_ID']} पर पानी का दबाव कम ({row['Pressure_bar']:.2f} bar) हो गया है। रिसाव की संभावना है।"
                    sns_client.publish(
                        PhoneNumber="+918250100174", # ⚠️ CHANGE THIS to your mobile number
                        Message=message
                    )
                    st.warning("📲 AWS SNS Vernacular SMS successfully dispatched!")
                except Exception as e:
                    st.warning(f"⚠️ AWS SNS Alert skipped (Check IAM/Credentials): {e}")
            else:
                st.success(f"✅ **Node:** {row['Node_ID']} | **Pressure:** {row['Pressure_bar']:.2f} bar | **AI Status:** Normal")
        
        # Delay for visual ticking effect
        time.sleep(0.5)
        
    # --- 5. POST-SIMULATION RESULTS ---
    clock_placeholder.success("✅ Simulation Complete!")
    
    with results_placeholder.container():
        st.markdown("---")
        st.subheader("📊 Post-Simulation Evaluation Metrics")
        st.write("Comparing the Ensemble ML model predictions against actual infrastructure test data.")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Accuracy", f"{accuracy_score(actuals, predictions):.2%}")
        col2.metric("Precision", f"{precision_score(actuals, predictions, zero_division=0):.2%}")
        col3.metric("Recall", f"{recall_score(actuals, predictions, zero_division=0):.2%}")
        col4.metric("F1-Score", f"{f1_score(actuals, predictions, zero_division=0):.2%}")

        st.dataframe(pd.DataFrame({
            "Timestamp": stream_data.iloc[:num_steps]["Timestamp"],
            "Location": stream_data.iloc[:num_steps]["Node_ID"],
            "Actual Status": actuals,
            "Predicted Status": predictions
        }))
