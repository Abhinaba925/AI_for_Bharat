# AI_for_Bharat
AI-Driven Smart Water Grid 💧

Problem Statement: AI for Rural Innovation & Sustainable Systems 

📌 Project Overview
Rural water infrastructure often suffers from aging pipelines and corrosion, resulting in critical water contamination and supply losses. The lack of real-time monitoring systems in rural water networks prevents early detection of these issues. Recent preventable infrastructure failures have led to severe health crises, including 26 deaths in Indore, casualties in Srikakulam, and over 5,500 reported illnesses across 26 Indian cities.

To solve this, Team Q_Titans proposes an AI-Driven Smart Water Grid. Our solution leverages simulated IoT data and machine learning to detect pressure drops, flow anomalies, and pipeline leaks early, preventing contamination from spreading.

🚀 Key Features & USP

Pre-Emptive Safety: Detects pressure drops and abnormal flow patterns before large-scale water loss or contamination occurs.


Real-time Monitoring: Features an interactive Streamlit dashboard with GIS visualization to monitor village water infrastructure.


Vernacular Alert System: Automatically sends SMS or WhatsApp notifications in regional languages directly to local authorities and technicians.

Zone-Based Risk Assessment: Prioritizes drinking water safety through a critical alert system.


Critical Priority (<5 min response): Dedicated to drinking water pipelines and school tanks.


Standard Priority (<15 min response): Dedicated to irrigation channels and agricultural water supply.


Scalable Retrofit: Designed to be compatible with existing infrastructure, such as the Jal Jeevan Mission.

⚙️ System Architecture
Our cloud-based architecture ensures real-time monitoring and scalable storage:


Synthetic IoT Data Generator: Simulates sensor telemetry (Pressure, Flow Rate, Temperature) from nodes in a village water grid.


Machine Learning Engine: Analyzes incoming data flows to identify abnormal patterns and classify pipeline conditions.


AWS Cloud Storage: Uses AWS S3 to store system logs, datasets, and model files.


Monitoring & Alerts: Pushes data to a Streamlit dashboard for visualization and triggers AWS SNS for automated SMS notifications.

🧠 Machine Learning Model: Random Forest Classifier
The core decision engine of our system uses a Random Forest Classifier built with Scikit-learn.


Input Features (X): Pressure_bar, Flow_Rate_Ls, Temperature_C.


Target Variable (Y): Leak_Status (Normal: 0, Leak Detected: 1).


Training Pipeline: Trained sequentially on 80% of historical data, with the final 20% reserved to simulate a live data feed.

💻 Technology Stack

Language & Processing: Python 3.8+, Pandas, NumPy.

Machine Learning: Scikit-learn.

Dashboard & Visualization: Streamlit, Folium / Map Visualization.


Cloud Infrastructure: AWS S3, AWS SNS.

🛣️ The Road Ahead (Future Scope)

Physical IoT Integration: Transitioning from our synthetic data generator to deploying physical IoT sensors with a direct AWS data pipeline.

Advanced AI Architecture: Upgrading from the baseline Random Forest model to sophisticated Neural Network (NN) architectures for handling complex real-world telemetry.

True Real-Time Streaming: Replacing partitioned test datasets with continuous, live operational feeds.

Ultimate Vision: Bridging the gap between detection and action to drastically reduce casualties related to water contamination.

