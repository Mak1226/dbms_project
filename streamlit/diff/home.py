import streamlit as st

def show():
    st.image("home.jpg", width=300, caption="Home page")

    # Clickable image to go to about page
    if st.button("About"):
        return "about"