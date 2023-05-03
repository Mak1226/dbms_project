import streamlit as st

def main():
    st.set_page_config(page_title="My Navigation Bar")

    # Define navigation items
    pages = {
        "Home": home_page,
        "Products": products_page,
        "Cart": cart_page
    }

    # Render navigation bar
    with st.container():
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Render selected page
    pages[selection]()

def home_page():
    st.title("Welcome to our eCommerce website!")
    st.write("This is the home page.")

def products_page():
    st.title("Products")
    st.write("Here are our products:")

def cart_page():
    st.title("Cart")
    st.write("Here is your shopping cart:")

if __name__ == "__main__":
    main()
