import streamlit as st
from login import login_page

from databases import connect_to_database

# Import pages
from home import show_home
from about import show_about
from products import show_products
from cart import show_cart
from order import show_order


# Set page title and favicon
st.set_page_config(page_title="E-commerce Website", page_icon=":moneybag:")
# st.set_page_config(page_title="Online Store", page_icon=":money_with_wings:")

# Define navigation bar
menu = ['Login', 'Home', 'About', 'Products', 'Cart', 'Order']
choice = st.sidebar.selectbox("Select a page", menu)

# Show the appropriate page based on user selection

if choice == 'Login':
    login_page()
elif choice == 'Home':
    show_home()
elif choice == 'About':
    show_about()
elif choice == 'Products':
    show_products()
elif choice == 'Cart':
    show_cart()
elif choice == 'Order':
    show_order()
