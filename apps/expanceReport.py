import streamlit as st
from PIL import Image
import pytesseract
import os
base_path=os.getcwd()

def app():
    col0, col00 = st.columns((4, 2))
    image=col0.file_uploader("Upload Bill")
    button=col00.button("Scan")
    if button:
        text=pytesseract.image_to_string(Image.open(image))
        print(text)
        st.write(text)
