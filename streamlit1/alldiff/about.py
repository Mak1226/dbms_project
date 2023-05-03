import streamlit as st
from footer import footer
from databases import connect_to_database

def show_about():
    st.image("./pictures/about.jpg", width=300, caption="About page")

    footer()