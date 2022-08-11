import streamlit as st
from PIL import Image
import os
import qrcode

from streamlit_option_menu import option_menu

options=["Search Equipment","Search Consumables"]
hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
def showQr(type,data,name):
    st.title("Scan to see know more")
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data("http://54.90.91.67:8080/po/"+type+"/"+ data)
    qr.make(fit=True)
    img = qr.make_image()
    imgpath = os.path.join("qr_images", data + ".png")
    img.save(imgpath)
    st.image(openImage(imgpath))
    st.write("http://54.90.91.67:8080/"+type+"/"+ data)
def openImage(path):
    im=Image.open(path)
    return im
def streamlit_menu():
    selected = option_menu(
            menu_title=None,  # required
            options=options, # required  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
    return selected
def app():
    col1, col2 = st.columns((1, 2))
    name=col1.selectbox("Search Type",options)
    data = col2.text_input(name.replace("Search ","") + " ID")
    col3, col4 = st.columns((10, 1))
    col3.write("")
    generate = col4.button("Find")
    if generate and len(data)>0:
        if name == "Search Equipment":
            showQr("eq",data,"Equipment")
        if name == "Search Consumables":
            showQr("con",data,"Consumable")
    if generate and len(data)<=0:
        st.warning("No search id found!")
