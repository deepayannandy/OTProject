import alt as alt
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import os
from streamlit_option_menu import option_menu
from datetime import date, datetime
import altair as alt
base_path=os.getcwd()
def streamlit_menu():
    options = ["Real Time Status","Add New"]  # requiredß
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
hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
def showdata(otdb):
    data= otdb.db.collection("rts").get()
    datas=[]
    containers=[]
    days=[]
    for data in data:
        temp=data.to_dict()
        datas.append(temp)
        containers.append(temp["Container"])
        day0=datetime.strptime(temp["Received"], '%Y-%m-%d')
        day1 = datetime.strptime(temp["Outbound"], '%Y-%m-%d')
        delta = day1 - day0
        days.append(delta.days)
    print(containers, days)

    chart_data = pd.DataFrame(
        days,
        index=containers,
    )
    data = pd.melt(chart_data.reset_index(), id_vars=["index"])
    chart = (
        alt.Chart(data)
            .mark_bar()
            .encode(
            x=alt.X("value", type="quantitative", title="Days"),
            y=alt.Y("index", type="nominal", title="Containers"),
            color=alt.Color("variable", type="nominal", title=""),
            order=alt.Order("variable", sort="descending"),
        )
    )

    st.altair_chart(chart, use_container_width=True)

    hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(datas)



def app(otdb):
    selected = streamlit_menu()
    if selected!="Real Time Status":
        st.title("Create New")
        col0, col1 = st.columns((2, 2))
        with col0:
            recieved=st.date_input("Received")
            seal=st.text_input("Seal/Trailer#")
            units=st.number_input("Units/Pallet",min_value=0,)
            apptime=st.text_input("App Time/ Arrived")
            finish=st.text_input("Finish")
            customer=st.text_input("Customer")
        with col1:
            container=st.text_input("Container")
            description=st.text_input("Description")
            oapointment=st.date_input("Outbound Appointment")
            start=st.text_input("Start")
            sale=st.text_input("Sale#")
            note=st.text_area("Note")
        save=st.button("Save")
        if save:
            data={"Received":str(recieved),"Seal/Trailer#":seal,"Units/Pallet":units,"AppTime":apptime,"Finish":finish,"Customer":customer,"Container":container,"Description":description,"Outbound":str(oapointment),"Start":start,"Sale":sale,"Note":note}
            otdb.db.collection("rts").document().set(data)
            st.success("Data uploaded successfully!")
    else:
        st.title("Real Time Status")
        showdata(otdb)



