import streamlit as st
from PIL import Image
from databases import connect_to_database
from footer import footer
from login import *
# Connect to database
mydb = connect_to_database()

# Define the footer


def show_home(result):
    # import streamlit as st
    st.image("./pictures/home.jpg", width=300, caption="Home page")
    st.title("Welcome to our eCommerce website!")
    with st.container():
        st.image(Image.open("./pictures/logo.png"), width=200)
        st.write("Browse our selection of products and find the perfect item for you.")

        # Render featured products
        st.header("Featured Products")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(Image.open("./pictures/product1.jpg"), width=200)
            st.write("Product 1")
        with col2:
            st.image(Image.open("./pictures/product2.jpg"), width=200)
            st.write("Product 2")
        with col3:
            st.image(Image.open("./pictures/product3.jpg"), width=200)
            st.write("Product 3")

        # Render categories
        st.header("Shop by Category")
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open("./pictures/category1.jpg"), width=200)
            st.write("Category 1")
        with col2:
            st.image(Image.open("./pictures/category2.jpg"), width=200)
            st.write("Category 2")

    # Add the footer
    # login()
    footer()

    st.write("This is the home page.")

# if __name__ == "__main__":
    # login()





