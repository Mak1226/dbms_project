import streamlit as st
import pandas as pd
from databases import connect_to_database
# from databases import connect_to_user
from footer import footer
from query import *
# st.set_page_config(page_title="Online Store", page_icon=":money_with_wings:")

# Connect to database
# mydb = connect_to_database()


def insert_data(table_name, values):
    cursor = mydb.cursor()
    sql = f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(values))})"
    cursor.execute(sql, values)
    mydb.commit()
    cursor.close()


def show_products():
    st.image("./pictures/products.jpg", width=300, caption="Products page")

    input_type = st.radio("Search by", ("Product ID", "Product Name"))

    if input_type == "Product ID":
        input_value = st.number_input("Enter a product id", step=1)
        try:
            input_value = int(input_value)
        except ValueError:
            st.error("Input must be an integer")
            return
        product_info = get_product_info_id(input_value)
    else:
        input_value = st.text_input("Enter a product name")
        product_info = get_product_info_name(input_value)

    if not product_info:
        st.warning("No product found")
        footer()
        return

    df = pd.DataFrame(product_info, columns=['product_id', 'name', 'price', 'seller_id'])
    st.write('Product Details')
    st.table(df)

    cart = st.session_state.get('cart', [])

    for i, row in df.iterrows():

        button_label = f"Add to Cart ({row['name']} -> {row['price']} $)"
        button_key = f"add_to_cart_{row['product_id']}_{i}"

        if st.button(button_label, key=button_key):
            admin = connect_to_database()
            cart.append({'product_id': row['product_id'], 'name': row['name'], 'price': row['price'], 'seller_id': row['seller_id']})
            # sql = f"INSERT INTO CART VALUES " 
            insert_into_cart("125", row['product_id'], "1", row['seller_id'], row['price'])
            st.session_state.cart = cart
            st.success("Added to Cart")

    if len(product_info) > 1:
        st.warning("There are multiple products with the same ID:")
        for i, row in df.iterrows():
            st.write(f"Product {i+1}: {row['name']} - {row['price']}")
    footer()
# Display the products
show_products()

