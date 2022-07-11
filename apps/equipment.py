import streamlit as st
from PIL import Image
import os

from streamlit_option_menu import option_menu

base_path=os.getcwd()
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
    df={"EQPName":EqName,"EQId":eqId,"InStock":InStock,"AvailableQuantity":AvailableQuantity,"DispatchQuantityforProjects":DispatchQuantityforProjects,"Descriptions":Descriptions}
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
    equipName=st.text_input("Equipment Name")
    col1, col2 = st.columns((2, 3))
    eqid=col1.text_input("Equipment ID")
    count=col2.text_input("Purchase Qnt")
    desc=st.text_area("Description")
    submit=st.button("Add Equipment")
    if submit:
        if len(equipName)==0 or len(eqid)==0 or count==0:
            st.warning("Mandatory fields are empty!")
        else:
            data = {'EqName': equipName, "Descriptions": desc, "DispatchQuantityforProjects": 0, "InStock": int(count),
                    "AvailableQuantity": int(count), "eqId": eqid}
            otdb.db.collection("equipments").document(eqid).set(data)
            st.success("Equipment added successfully!")

def app(otdb):
    #st.image(Image.open(base_path+"/comp_logo/logo0.png"))
    selected = streamlit_menu()
    if selected=="Available Equipments":
        st.title("Equipment database")
        df = createDataFrame(otdb.getEQPList())
        st.table(df)
    if selected =="Add New":
        st.title("Add New Equipment")
        createequip(otdb)
