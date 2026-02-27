import streamlit as st

st.title("Cyber Attack Detection App")

name = st.text_input("Enter your name")

if name:
    st.success(f"Hello {name}")
