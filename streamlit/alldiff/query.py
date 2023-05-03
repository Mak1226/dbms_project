import streamlit as st
from databases import *
mydb = connect_to_database()


def get_product_info_id(product_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM (SELECT product.product_id, name, price, sells.seller_id FROM product JOIN sells ON product.product_id = sells.product_id) AS foo WHERE product_id = %s ", (product_id,))
    result = mycursor.fetchall()
    return result

def get_product_info_name(product_name):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM (SELECT product.product_id, name, price, sells.seller_id FROM product JOIN sells ON product.product_id = sells.product_id) AS foo WHERE name = %s ", (product_name,))
    result = mycursor.fetchall()
    return result

def insert_into_cart(cust_id, prod_id, counts, seller_id, price):
    admin = connect_to_database()
    with admin.cursor() as cur:
        cur.execute(f"INSERT INTO cart (customer_id, product_id, counts, seller_id, price) VALUES ({cust_id}, {prod_id}, {counts}, {seller_id}, {price})")
    admin.commit()
    admin.close()
