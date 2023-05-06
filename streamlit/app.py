import streamlit as st
import psycopg2
from PIL import Image



# Define database connection parameters
DATABASE_URL = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "dbms_project"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = 'project'

# Define database query


# Connect to database
conn = psycopg2.connect(
    database='dbms_project',
    user='postgres',
    password='project',
    host='localhost',
    port=5432
)

# Define function to execute database query and return results
def get_data(query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Define main function
def main():

    # st.title("My eCommerce Website")

    st.set_page_config(page_title="My Navigation Bar")

    # Define navigation items
    pages = {
        "Home": home_page,
        "Products": products_page,
        "Cart": cart_page,
        "My Orders": orders_page
    }

    # Render navigation bar
    with st.container():
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Render selected page
    pages[selection]()

def home_page():
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
    st.write("This is the home page.")

def products_page():
    st.title("Products")
    st.write("Here are our products:")

def cart_page():
    st.title("Cart")
    st.write("Here is your shopping cart:")

def orders_page():
    st.title("Orders")
    

    input_value = st.number_input("Enter a order_id")
    try:
        input_value = int(input_value)
    except ValueError:
        st.error("Input must be an integer")
        return
    QUERY = "SELECT * FROM orders where customer_id = {}"
    formatted_query = QUERY.format(input_value)
    # Get data from database
    data = get_data(formatted_query)

    st.write("Here are your orders")

    x = st.table(data)
    print(x)

    # Display data
    # for row in data:
    #     st.write(row)

if __name__ == "__main__":
    main()
