import streamlit as st
from PIL import Image
import os
base_path=os.getcwd()

def createDataFrame(rawdata):
    ConName=[]
    DispatchQuantityforProject=[]
    NewpurchaseQuantity=[]
    StockQuantity=[]
    conId=[]
    for i in rawdata:
        ConName.append(i["ConName"])
        DispatchQuantityforProject.append(i["DispatchQuantityforProject"])
        NewpurchaseQuantity.append(i["NewpurchaseQuantity"])
        StockQuantity.append(i["StockQuantity"])
        conId.append(i["conId"])
    df={"CONId":conId,"Product Name":ConName,"StockQuantity":StockQuantity,"DispatchQuantityforProject":DispatchQuantityforProject,"NewpurchaseQuantity":NewpurchaseQuantity}
    return df
def app(otdb):
    #st.image(Image.open(base_path+"/comp_logo/logo0.png"))
    st.title("Consumable inventory")
    df = createDataFrame(otdb.getCONList())
    st.table(df)
