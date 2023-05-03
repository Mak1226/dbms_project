import streamlit as st

def footer():
    st.markdown("""<style>
.footer {
    background-color: #333333;
    color: #FFFFFF;
    text-align: center;
    padding: 10px;
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    z-index: 10;
}

.footer p {
    margin: 0;
}

.footer a {
    color: #FFFFFF;
}

.footer .social {
    display: flex;
    justify-content: center;
    margin-top: 10px;
}

.footer .social a {
    margin: 0 10px;
}

.footer .social img {
    height: 30px;
}

.footer .payment-methods {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.footer .payment-methods img {
    height: 30px;
    margin: 0 10px;
}
</style>

<div class="footer">
    <p>Contact us: <a href="mailto:ad8051707907@gmail.com">contact@ecommerce.com</a></p>
    <div class="social">
        <a href="#"><img src="https://img.icons8.com/color/48/000000/facebook.png"/></a>
        <a href="#"><img src="https://img.icons8.com/color/48/000000/twitter.png"/></a>
        <a href="#"><img src="https://img.icons8.com/color/48/000000/instagram-new.png"/></a>
    </div>
    <div class="payment-methods">
        <p>Accepted payment methods:</p>
        <img src="https://img.icons8.com/color/48/000000/visa.png"/>
        <img src="https://img.icons8.com/color/48/000000/mastercard-logo.png"/>
        <img src="https://img.icons8.com/color/48/000000/paypal.png"/>
    </div>
</div>""", unsafe_allow_html=True)
