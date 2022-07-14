import streamlit as st
from PIL import Image
import os
base_path=os.getcwd()

def app():
    col0, col00 = st.columns((2, 4))
    col0.image(Image.open(base_path+"/comp_logo/logo.jpeg"),)
    with col00:
        st.title(" ")
        new_title = '<p style= "color:Green; font-size: 45px;">Millions of Documents in your Pocket</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        #st.title("Millions of Documents in your Pocket")
