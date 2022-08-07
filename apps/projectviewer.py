import os
import streamlit as st
from streamlit_option_menu import option_menu
import qrcode
from PIL import Image
import numpy as np

selection=["PO Number","WO Number"]
visiablereasult=False
logo="https://firebasestorage.googleapis.com/v0/b/ots-pocket.appspot.com/o/projectFiles%2Flogo.jpeg?alt=media&token=3c4bd26d-a8f4-41d9-9853-f07ff3ee4e32"
hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
def getProject(otdb,searchdata):
    res = otdb.db.collection("userProjects").where("po", "==", searchdata).get()
    return res
def streamlit_menu(options):
    selected = option_menu(
            menu_title=None,  # required
            options=options, # required  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
    return selected
def streamlit_menuEMP(options):
    visiableoption=[]
    for empname in options:
        visiableoption.append(empname.split("(")[1].split(")")[0])

    selected = option_menu(
            menu_title=None,  # required
            options=visiableoption, # required  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
    return options[visiableoption.index(selected)]
def openImage(path):
    im=Image.open(path)
    return im
def showEMPDetails(otdb,emp):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    employeeid=emp.split("(")[0]
    res = otdb.db.collection("users").where("uniqueid", "==", employeeid).get()
    em = res[0].to_dict()
    col0, col00 = st.columns((3, 1))
    col0.metric("Employee Name", em["fullname"])
    with col00:
        qr.add_data("http://3.95.56.247:8080/employee/"+em["uniqueid"])
        qr.make(fit=True)
        img=qr.make_image()
        imgpath=os.path.join("qr_images",em["uniqueid"]+".png")
        img.save(imgpath)
        st.image(openImage(imgpath))
        st.write("http://3.95.56.247:8080/employee/"+em["uniqueid"])

    col4, col5 = st.columns((1, 2))
    col4.metric("Unique id", em["uniqueid"])
    col5.metric("SSN No.", em["ssn"])
    col2, col3 = st.columns((3, 2))
    col2.metric("Email id", em["email"])
    col3.metric("Contact No.", em["mobileNo"])

def showWODetails(otdb,wo):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    res = otdb.db.collection("Workorders").where("wo", "==", wo).get()
    wo=res[0].to_dict()
    col0, col00 = st.columns((3, 1))
    col0.title("Work Details of : " + wo["wo"])
    with col00:
        qr.add_data("http://3.95.56.247:8080/wo/"+wo["wo"])
        qr.make(fit=True)
        img = qr.make_image()
        imgpath = os.path.join("qr_images", wo["wo"] + ".png")
        img.save(imgpath)
        st.image(openImage(imgpath))
        st.write("http://3.95.56.247:8080/wo/"+wo["wo"])
    hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.write("Used Equipments")
    st.table({"Equipment Name": wo["equipments"], "Quantity": wo["equipQ"]})
    st.write("Consumables items")
    st.table({"Consumables Name": wo["consumables"], "Quantity": wo["consQ"]})
    st.header("Assigned Employee details")
    selectedemp=streamlit_menuEMP(wo["assignedEmployee"])
    showEMPDetails(otdb,selectedemp)

def app(otdb):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    global visiablereasult
    st.title("Project Dashboard")
    col1 ,col2,= st.columns((1,2,))
    SSelection=col1.selectbox("Select Search type",selection)
    searchdata=col2.text_input("Enter "+SSelection)
    search=st.button("Search")
    if search:
        visiablereasult=True
    if SSelection=="PO Number" and visiablereasult:
        projdata=getProject(otdb,searchdata)
        if len(projdata)>0:
            prj=projdata[0].to_dict()
            #st.write(prj)
            col0, col00 = st.columns((3, 1))
            col0.title("Project Details:" + prj["po"])
            with col00:
                qr.add_data("http://3.95.56.247:8080/po/"+prj["po"])
                qr.make(fit=True)
                img = qr.make_image()
                imgpath = os.path.join("qr_images",prj["po"]+ ".png")
                img.save(imgpath)
                st.image(openImage(imgpath))
                st.write("http://3.95.56.247:8080/po/"+prj["po"])
            #col0.title("Project Details of : "+prj["po"])
            st.metric("Job Description",prj["jobDescriptions"])
            col2,col3 = st.columns((1,2))
            col2.metric("Client Name",prj["clientName"])
            col3.metric("Address", prj["address"])
            st.header("Attached WO details")
            selectedWO=streamlit_menu(prj["workorders"])
            showWODetails(otdb, selectedWO)
            close=st.button("Hide")
            if close:
                visiablereasult=False
        else:
            st.error("PO number not found!")
    if SSelection=="WO Number" and visiablereasult:
        visiablereasult = False
        showWODetails(otdb,searchdata)
        close = st.button("Hide")
        if close:
            visiablereasult = False

