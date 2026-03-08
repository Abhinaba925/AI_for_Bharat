import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_and_save_model(data_file="water_grid_data.csv", model_file="rf_model.pkl"):
    print("Loading data...")
    df = pd.read_csv(data_file)
    
    # Features proposed in your architecture
    features = ["Pressure_bar", "Flow_Rate_Ls", "Temperature_C"]
    X = df[features]
    y = df["Leak_Status"]
    
    # Reserve 20% of data to act as our "live" future time-series feed
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    print("Training Random Forest Model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Quick validation
    preds = model.predict(X_test)
    print(f"Validation Accuracy: {accuracy_score(y_test, preds):.4f}")
    
    # Save the model
    joblib.dump(model, model_file)
    print(f"✅ Model saved to {model_file}")
    
    # Save the test data separately to act as our live stream in the app
    test_df = df.iloc[X_test.index].copy()
    test_df.to_csv("live_stream_data.csv", index=False)
    print("✅ Live stream test data saved to live_stream_data.csv")

if __name__ == "__main__":
    train_and_save_model()
