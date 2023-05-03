import streamlit as st
from databases import *
mydb = connect_to_database()

def get_cart_info_id():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cart;")
    result = mycursor.fetchall()
    return result

def get_product_info_id(product_id):
    mycursor = mydb.cursor()
    # mycursor.execute("SELECT * FROM cart")
    mycursor.execute("SELECT * FROM (SELECT product.product_id, name, price, sells.seller_id FROM product JOIN sells ON product.product_id = sells.product_id) AS foo WHERE product_id = %s ", (product_id,))
    result = mycursor.fetchall()
    # st.write(result)
    return result

def get_product_info_name(product_name):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM (SELECT product.product_id, name, price, sells.seller_id FROM product JOIN sells ON product.product_id = sells.product_id) AS foo WHERE name = %s ", (product_name,))
    result = mycursor.fetchall()
    return result

def insert_into_cart(cust_id, prod_id, seller_id, counts, price):
    # admin = connect_to_database()
    with mydb.cursor() as cur:
        # cur.execute(f"SELECT * FROM cart where customer_id = {cust_id} AND product_id = {prod_id} AND seller_id = {seller_id}")
        # res = cur.fetchone()
        # if res is not None:
        #     counts = (int)(res[3]) + 1
        #     cur.execute(f"UPDATE Cart SET counts = {counts} WHERE customer_id = {cust_id} AND seller_id = {seller_id} and product_id = {prod_id}");
        # else :
        # # cur.execute(f"UPDATE Cart SET counts = counts + {c} WHERE customer_id = {cust_id} AND seller_id");
        #     st.write("HIIIIII")
            cur.execute(f"INSERT INTO cart (customer_id, product_id, seller_id, counts, price) VALUES ({cust_id}, {prod_id}, {seller_id}, {counts}, {price})")
    # admin.commit()
    # admin.close()
