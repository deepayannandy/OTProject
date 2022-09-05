import streamlit as st
from PIL import Image
import os
base_path=os.getcwd()

hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
def app(otdb):
    st.title("Real Time Status")
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



