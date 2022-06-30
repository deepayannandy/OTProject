import streamlit as st
from apps import home,employee, equipment, payroll, projects, salespreoprt, consumable
import pickle
from pathlib import Path
from streamlit_option_menu import option_menu
import otsDBConnector as otdb

st.set_page_config(page_title='OTS Admin App',page_icon='',menu_items={
'About': "An secure industrial app developed by OTS.",
'Get help': "https://www.dnyindia.in",
'Report a bug': None
})


menu=["Home","Project Tracking","Employee database","Equipment database","Consumable inventory","Payroll","Sales report"]

def streamlit_menu():
    options = ["Home", "Projects", "Employees", "Equipments", "Consumables","Payroll","Sales reoprt"]  # required
    icons = ["house", "hammer", "person-fill", "gear", "bag","wallet2","file-bar-graph"]  # optional
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",  # required
            options=options, # required
            icons=icons,  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
        )
    return selected
def main():
    selected = streamlit_menu()
    if selected=="Home":
        home.app()
    if selected=="Projects":
        projects.app(otdb)
    if selected=="Employees":
        employee.app(otdb)
    if selected=="Equipments":
        equipment.app(otdb)
    if selected=="Consumables":
        consumable.app(otdb)



if __name__ == '__main__':
    main()