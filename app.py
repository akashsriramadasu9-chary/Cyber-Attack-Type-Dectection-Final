import streamlit as st
import pandas as pd
import pickle

st.title("Cyber Attack Detection System")

# Load all objects
@st.cache_resource
def load_objects():
    model = pickle.load(open("attack_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    encoder = pickle.load(open("encoder.pkl", "rb"))
    return model, scaler, encoder

model, scaler, encoder = load_objects()

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data", df.head())

    # Apply encoding
    df_encoded = encoder.transform(df)

    # Apply scaling
    df_scaled = scaler.transform(df_encoded)

    # Prediction
    predictions = model.predict(df_scaled)

    df["Predicted_Attack"] = predictions

    st.write("Prediction Results", df.head())

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Report",
        csv,
        "attack_report.csv",
        "text/csv"
    )
