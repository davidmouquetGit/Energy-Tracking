import streamlit as st
from PIL import Image

def display_logo():
    logo = Image.open("images/suivilogo.jpg")
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.image(logo, width=150)
    with col2:
        st.markdown("<h1 style='margin-top: 20px;'></h1>", unsafe_allow_html=True)
    st.markdown("---")
