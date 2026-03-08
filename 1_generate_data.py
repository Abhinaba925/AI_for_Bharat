import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_large_dataset(filename="water_grid_data.csv", num_records=50000):
    np.random.seed(42)
    
    # Define our three village nodes (Lat, Lon)
    nodes = {
        "S1_Main_Pump": (21.7781, 87.7517),
        "S2_Fields": (21.7850, 87.7600),
        "S3_School": (21.7700, 87.7450)
    }
    
    start_time = datetime(2026, 3, 1, 8, 0, 0)
    timestamps = [start_time + timedelta(minutes=5*i) for i in range(num_records)]
    
    data = []
    for i in range(num_records):
        node_id = np.random.choice(list(nodes.keys()))
        lat, lon = nodes[node_id]
        
        # 85% normal operations, 15% anomalies (leaks/bursts)
        is_leak = np.random.choice([0, 1], p=[0.85, 0.15])
        
        if is_leak == 0:
            pressure = np.random.normal(3.0, 0.2)
            flow_rate = np.random.normal(10.0, 1.0)
            temp = np.random.normal(25.0, 2.0)
        else:
            # Leak characteristics: Pressure drops, Flow rate fluctuates
            pressure = np.random.normal(1.2, 0.4) 
            flow_rate = np.random.normal(16.0, 3.0)
            temp = np.random.normal(25.0, 2.0)
            
        data.append([timestamps[i], node_id, lat, lon, pressure, flow_rate, temp, is_leak])
        
    df = pd.DataFrame(data, columns=["Timestamp", "Node_ID", "Latitude", "Longitude", 
                                     "Pressure_bar", "Flow_Rate_Ls", "Temperature_C", "Leak_Status"])
    df.to_csv(filename, index=False)
    print(f"✅ Generated {num_records} records and saved to {filename}")

if __name__ == "__main__":
    generate_large_dataset()
