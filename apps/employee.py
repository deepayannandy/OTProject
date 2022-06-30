import streamlit as st
import pandas as pd
import os
base_path=os.getcwd()

def createDataFrame(rawdata):
    fullname=[]
    mobileNo=[]
    email=[]
    ssn=[]
    uniqueid=[]
    assignedprojects=[]
    for i in rawdata:
        fullname.append(i["fullname"])
        mobileNo.append(i["mobileNo"])
        email.append(i["email"])
        ssn.append(i["ssn"])
        uniqueid.append(i["uniqueid"])
        assignedprojects.append(i["assignedprojects"])
    df={"Name":fullname,"Contact":mobileNo,"Email":email,"SSN":ssn,"Project":assignedprojects,"QRID":uniqueid}
    return df
def app(otdb):
    #st.image(Image.open(base_path+"/comp_logo/logo0.png"))
    st.title("Employee database")
    df=createDataFrame(otdb.getUserList())
    st.table(df)