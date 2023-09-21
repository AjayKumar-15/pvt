import streamlit as st
import os

st.set_page_config(
    page_title="About",
    layout="centered",
    initial_sidebar_state="expanded",
)
path = os.path.dirname(__file__)
st.image(path +'/PVT CALCULATOR  Oil Reservoir.png')
st.image(path+'/About Text.png')
