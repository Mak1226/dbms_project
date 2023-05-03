import streamlit as st
from PIL import Image

def main():
    st.set_page_config(page_title="My eCommerce Website")

    # Define page layout
    with st.container():
        st.image(Image.open("logo.png"), width=200)
        st.title("Welcome to our eCommerce website!")
        st.write("Browse our selection of products and find the perfect item for you.")

        # Render featured products
        st.header("Featured Products")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(Image.open("product1.jpg"), width=200)
            st.write("Product 1")
        with col2:
            st.image(Image.open("product2.jpg"), width=200)
            st.write("Product 2")
        with col3:
            st.image(Image.open("product3.jpg"), width=200)
            st.write("Product 3")

        # Render categories
        st.header("Shop by Category")
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open("category1.jpg"), width=200)
            st.write("Category 1")
        with col2:
            st.image(Image.open("category2.jpg"), width=200)
            st.write("Category 2")
        # with col3:
        #     st.image(Image.open("category3.jpg"), width=200)
        #     st.write("Category 3")

if __name__ == "__main__":
    main()
