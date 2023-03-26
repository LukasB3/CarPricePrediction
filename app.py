import streamlit as st
st.set_page_config(layout="centered")

from predict_page import predict_page
from data_page import explore_page

page = st.sidebar.selectbox("Preis-Voraussage oder Daten anschauen", ("Preis-Voraussage", "Daten anschauen"))

if page == "Preis-Voraussage":
    predict_page()
else:
    explore_page()
