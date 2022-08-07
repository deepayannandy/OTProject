import streamlit as st
from PIL import Image
import qrcode
import os

from streamlit_option_menu import option_menu

base_path=os.getcwd()
def openImage(path):
    im=Image.open(path)
    return im
def inDB(otdb,type,id):
    if type=="eq":
        res = otdb.db.collection("equipments").where("eqId", "==", id).get()

        if len(res)==1:
            return True

        else:
            return False

def createDataFrame(rawdata):
    AvailableQuantity=[]
    Descriptions=[]
    DispatchQuantityforProjects=[]
    EqName=[]
    InStock=[]
    eqId=[]
    for i in rawdata:
        eqId.append(i["eqId"])
        EqName.append(i["EqName"])
        InStock.append(i["InStock"])
        DispatchQuantityforProjects.append(i["DispatchQuantityforProjects"])
        Descriptions.append(i["Descriptions"])
        AvailableQuantity.append(i["AvailableQuantity"])
    df={"Equipment":EqName,"QR-ID":eqId,"InStock":InStock,"Available Quantity":AvailableQuantity,"Dispatch":DispatchQuantityforProjects,}
    return df
def streamlit_menu():
    options = ["Available Equipments","Add New"]  # requiredß
    icons = ["card-list","plus-square"]  # optional

    selected = option_menu(
            menu_title=None,  # required
            options=options, # required
            icons=icons,  # optional
            menu_icon="cast",  # optional nww
            default_index=0,  # optional
            orientation="horizontal",
        )
    return selected
def createequip(otdb):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    equipName=st.text_input("Equipment Name")
    col1, col2 = st.columns((2, 3))
    with col1:
        eqid=st.text_input("Equipment ID")
        st.write("Equipment ID Naming Convention: XXX123")
    count=col2.text_input("Purchase Quantity")
    desc=st.text_area("Description")
    submit=st.button("Add Equipment")
    if submit:
        if inDB(otdb,'eq',eqid):
            st.warning("This Equipment id already in use")
        else:
            if len(equipName)==0 or len(eqid)==0 or count==0:
                st.warning("Mandatory fields are empty!")
            else:
                data = {'EqName': equipName, "Descriptions": desc, "DispatchQuantityforProjects": 0, "InStock": int(count),
                        "AvailableQuantity": int(count), "eqId": eqid}
                otdb.db.collection("equipments").document(eqid).set(data)
                col0, col00 = st.columns((3, 1))
                col0.write("Scan to See the Equipment")
                with col00:
                    qr.add_data("http://3.95.56.247:8080/eq/" + eqid)
                    qr.make(fit=True)
                    img = qr.make_image()
                    imgpath = os.path.join("qr_images", eqid + ".png")
                    img.save(imgpath)
                    st.image(openImage(imgpath))
                    st.write("http://3.95.56.247:8080/eq/" + eqid)
                st.success("Equipment added successfully!")

def app(otdb):
    #st.image(Image.open(base_path+"/comp_logo/logo0.png"))
    selected = streamlit_menu()
    if selected=="Available Equipments":
        st.title("Equipment database")
        df = createDataFrame(otdb.getEQPList())
        hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df)
    if selected =="Add New":
        st.title("Add New Equipment")
        createequip(otdb)
