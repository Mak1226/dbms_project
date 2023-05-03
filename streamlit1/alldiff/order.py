import streamlit as st
from footer import footer
from databases import connect_to_database

def show_order():
    st.image("./pictures/order.jpg", width=300, caption="Order page")

    footer()