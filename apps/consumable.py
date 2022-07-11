import streamlit as st
from PIL import Image
import os

from streamlit_option_menu import option_menu

base_path=os.getcwd()
isworkorder=False
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
def streamlit_menu():
    options = ["Available Consumables","Add New"]  # requiredß
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
def createcon(otdb):
    conName=st.text_input("Consumable Name")
    col1, col2 = st.columns((2, 3))
    conid=col1.text_input("Consumable ID")
    count=col2.text_input("Purchase Qnt")
    submit=st.button("Add Consumable")
    if submit:
        if len(conid)==0 or len(conName)==0 or count=="0":
            st.warning("Mandatory fields are empty!")
        else:
            data = {'ConName': conName , "StockQuantity": int(count), "NewpurchaseQuantity": int(count), "DispatchQuantityforProject": 0,
                    "conId": conid}
            otdb.db.collection("consumableItems").document(conid).set(data)
            st.success("Consumable added successfully!")
def showAddCon(otdb):
    global isworkorder
    st.title("Restock Inventory")
    col1, col2 = st.columns((3, 1))
    df= createDataFrame(otdb.getCONList())
    con = col1.selectbox("Select Consumable Product", df["Product Name"])
    qnt = col2.text_input("ReStock Qnt")
    submit=st.button("Add")
    if submit:
        if len(con)==0 or len(qnt)==0:
            st.warning("Please fill the required data!")
        else:
            index=df["Product Name"].index(con)
            data = {'ConName': con, "StockQuantity": int(df["StockQuantity"][index]+int(qnt)), "NewpurchaseQuantity": int(qnt), "DispatchQuantityforProject": df["DispatchQuantityforProject"][index],
                    "conId": df["CONId"][index]}
            otdb.db.collection("consumableItems").document(df["CONId"][index]).set(data)
            st.success("Inventory Updated successfully!")
            isworkorder=False
    if isworkorder==False:
        st.button("Close")

def app(otdb):
    #st.image(Image.open(base_path+"/comp_logo/logo0.png"))
    selected= streamlit_menu()
    global isworkorder
    if selected=="Available Consumables":
        st.title("Consumable inventory")
        df = createDataFrame(otdb.getCONList())
        st.table(df)
        if isworkorder == False:
            addWO = st.button("Restock Inventory")
            if addWO:
                isworkorder = True
        if isworkorder:
            showAddCon(otdb)
    if selected =="Add New":
        st.title("Add new Consumable inventory")
        createcon(otdb)