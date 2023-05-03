import streamlit as st
from home import show_home
from about import show_about
from products import show_products
from cart import show_cart
from order import show_order

from databases import connect_to_database

def show():
    st.markdown("""
    <style>
    .navbar {
        background-color: #f8f9fa !important;
    }

    .navbar-brand {
        font-weight: bold !important;
        font-size: 24px !important;
    }

    .nav-link {
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

    pages = {
        "Home": show_home,
        "About": show_about,
        "Products": show_products,
        "Order": show_order,
        "Cart": show_cart,
    }

    st.markdown(
        """
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <a class="navbar-brand" href="#">My App</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              %s
            </ul>
          </div>
        </nav>
        """
        % "".join(
            [
                f'<li class="nav-item"><a class="nav-link" href="#" onclick="set_page(\'{page}\');">{page}</a></li>'
                for page in pages.keys()
            ]
        ),
        unsafe_allow_html=True,
    )

    def set_page(page_name):
        session_state = st.session_state
        session_state.current_page = pages[page_name]

    if "current_page" not in st.session_state:
        set_page("Home")

    st.session_state.current_page()