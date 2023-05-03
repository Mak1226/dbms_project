import streamlit as st
import pandas as pd
from footer import footer
from databases import connect_to_database

def show_cart():
    st.image("./pictures/cart.jpg", width=300, caption="Cart page")
    cart = st.session_state.get('cart', [])
    if len(cart) == 0:
        st.write("Your cart is empty!")
        footer()
        return
    total = 0
    for item in cart:
        # st.write(item)
        total += item['price'] 
    st.write("Total cost:", total)
    df = pd.DataFrame(cart, columns=['product_id', 'name', 'price', 'seller_id'])
    st.write('Cart Details')
    st.table(df)

    if st.button("Place Order"):
        st.success("Order Placed Successfully")
        st.balloons()
        st.session_state.cart = []

    if st.button("Empty cart"):
        st.session_state['cart'] = []
        st.balloons()
        st.success("Cart has been emptied!")

    footer()