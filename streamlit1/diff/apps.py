import streamlit as st
import home
import about

def main():
    # Use session state to store the current page
    session_state = st.session_state
    if "page" not in session_state:
        session_state.page = "home"

    # Display the appropriate page based on the current state
    if session_state.page == "home":
        page = home.show()
    elif session_state.page == "about":
        page = about.show()

    # Handle page navigation
    if page == "home":
        session_state.page = "home"
    elif page == "about":
        session_state.page = "about"

if __name__ == "__main__":
    main()
