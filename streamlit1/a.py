import streamlit as st

def main():
    # Use session state to store the current page
    session_state = st.session_state
    if "page" not in session_state:
        session_state.page = "home"

    # Display the appropriate page based on the current state
    if session_state.page == "home":
        st.image("home.jpg", width=300, caption="Home page")

        # Clickable image to go to about page
        if st.button("About"):
            session_state.page = "about"

    elif session_state.page == "about":
        st.image("about.jpg", width=300, caption="About page")

        # Clickable image to go back to home page
        if st.button("Home"):
            session_state.page = "home"

if __name__ == "__main__":
    main()
