import streamlit as st
from databases import connect_to_database
from home import *
import psycopg2
import home

# Connect to database
mydb = connect_to_database()

def login_page():
    st.title("Login")
    customer_id = st.text_input("Enter your customer ID:")
    if st.button("Submit"):
        # Connect to database
        conn = psycopg2.connect(
            host="localhost",
            database="dbms",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()

        # Check if customer ID exists in database
        cur.execute(f"SELECT * FROM customer WHERE customer_id='{customer_id}'")
        result = cur.fetchone()
        if result:
            st.success("Login successful!")
            # Redirect to home page
            home.show_home(result)
        else:
            st.error("Invalid customer ID. Please try again.")

        # Close database connection
        cur.close()
        conn.close()

