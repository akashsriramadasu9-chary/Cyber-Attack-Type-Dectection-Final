import streamlit as st
import pandas as pd
import joblib
import io

# -------------------------------
# Load Model & Scaler
# -------------------------------
model = joblib.load("attack_model (5).pkl")
scaler = joblib.load("scaler.pkl")

st.title("🔐 Cyber Attack Detection System")

st.write("Upload a CSV file to analyze network activity.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df.head())

    try:
        # -------------------------------
        # Feature Check
        # -------------------------------
        if df.shape[1] != model.n_features_in_:
            st.error(f"Expected {model.n_features_in_} features but got {df.shape[1]}")
        else:
            # -------------------------------
            # Scaling
            # -------------------------------
            X_scaled = scaler.transform(df)

            # -------------------------------
            # Prediction
            # -------------------------------
            predictions = model.predict(X_scaled)
            probabilities = model.predict_proba(X_scaled)

            df["Prediction"] = predictions
            df["Confidence"] = probabilities.max(axis=1)

            st.subheader("📊 Prediction Results")
            st.dataframe(df.head())

            # -------------------------------
            # Summary
            # -------------------------------
            st.subheader("📈 Attack Distribution")
            st.bar_chart(df["Prediction"].value_counts())

            # -------------------------------
            # Download Report
            # -------------------------------
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)

            st.download_button(
                label="⬇ Download Full Report",
                data=csv_buffer.getvalue(),
                file_name="cyber_attack_report.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")
