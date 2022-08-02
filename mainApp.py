import streamlit as st
from apps import home,employee, equipment, payroll, projects, expanceReport, consumable, projectviewer, search
import pickle
from pathlib import Path
from streamlit_option_menu import option_menu
import otsDBConnector as otdb

st.set_page_config(page_title='OTS Admin App',page_icon='',menu_items={
'About': "An secure industrial app developed by OTS.",
'Get help': "https://www.dnyindia.in",
'Report a bug': None
})



menu=["Home","Project Dashboard","Project Management","Employee database","Equipment database","Consumables","Payroll","Expence report"]

def streamlit_menu():
    options = ["Home","Project Dashboard", "Projects Management", "Employees", "Equipments", "Consumables","Payroll","Expence report"]  # required
    icons = ["house", "hammer","bi-card-text", "person-fill", "gear", "bag","wallet2","file-bar-graph"]  # optional
    with st.sidebar:
        selected = option_menu(
            menu_title="Quick Response Coded List( QRCL)",  # required
            options=options, # required
            icons=icons,  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
        )
    return selected
def main():
    streamlit_style = """
    			<style>
@import url('https://fonts.googleapis.com/css2?family=Lato&display=swap');

    			html, body, [class*="css"]  {
    			font-family: 'Roboto', sans-serif;
    			}
    			</style>
    			"""
    st.markdown(streamlit_style, unsafe_allow_html=True)
    selected = streamlit_menu()
    if selected=="Home":
        home.app()
        search.app()
    if selected=="Projects Management":
        projects.app(otdb)
    if selected=="Employees":
        employee.app(otdb)
    if selected=="Equipments":
        equipment.app(otdb)
    if selected=="Consumables":
        consumable.app(otdb)
    if selected=="Project Dashboard":
        projectviewer.app(otdb)
    if selected=="Expence report":
        expanceReport.app()



if __name__ == '__main__':
    main()