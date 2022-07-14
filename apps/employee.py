import streamlit as st
import pandas as pd
import os
base_path=os.getcwd()

def createDataFrame(rawdata):
    fullname=[]
    mobileNo=[]
    email=[]
    ssn=[]
    status=[]
    uniqueid=[]
    assignedprojects=[]
    for i in rawdata:
        fullname.append(i["fullname"])
        mobileNo.append(i["mobileNo"])
        email.append(i["email"])
        ssn.append(i["ssn"])
        uniqueid.append(i["uniqueid"])
        assignedprojects.append(i["assignedprojects"])
        if i["assignedprojects"]=="NA":
            status.append("Not Allocated")
        else:
            status.append("At a Job")
    df={"Name":fullname,"Contact":mobileNo,"Email":email,"SSN":ssn,"Project":assignedprojects,"QRID":uniqueid,"Status":status}
    return df
def app(otdb):
    #st.image(Image.open(base_path+"/comp_logo/logo0.png"))
    st.title("Employee database")
    df=createDataFrame(otdb.getUserList())
    st.table(df)