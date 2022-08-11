import streamlit as st

import os
base_path=os.getcwd()

def app():
    col0, col00 = st.columns((4, 2))
    image=col0.file_uploader("Upload Bill")
    button=col00.button("Scan")
    if button:
        st.write("This part is under development!")
