import streamlit as st
from PIL import Image
import os
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
def app(otdb):
    #st.image(Image.open(base_path+"/comp_logo/logo0.png"))
    st.title("Equipment database")
    df = createDataFrame(otdb.getEQPList())
    st.table(df)
