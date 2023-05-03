import streamlit as st

def show():
    st.image("about.jpg", width=300, caption="About page")

    # Clickable image to go back to home page
    if st.button("Home"):
        return "home"