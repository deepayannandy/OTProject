import streamlit as st
from PIL import Image
import os
base_path=os.getcwd()

def app():
    st.image(Image.open(base_path+"/comp_logo/logo.jpeg"))
