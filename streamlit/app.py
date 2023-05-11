import streamlit as st
import sqlalchemy
from sqlalchemy.engine import create_engine
#from st import option_menu
from sqlalchemy.sql import text
import pandas as pd
from streamlit_option_menu import option_menu
cust_id = 0

class PostgresqlDB:


    def __init__(self,user_name,password,host,port,db_name):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.engine = self.create_db_engine()

    def create_db_engine(self):
        try:
            db_uri = f"postgresql+psycopg2://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            return create_engine(db_uri)
        except Exception as err:
            return
    def execute_dql_commands(self,stmnt,values=None):
        try:
            with self.engine.connect() as conn:
                if values is not None:
                    result = conn.execute(text(stmnt),values)
                else:
                    result = conn.execute(text(stmnt))
            return result
        except Exception as err:
            print(f'Failed to execute dql commands -- {err}')
    
    def execute_ddl_and_dml_commands(self,stmnt,values=None):
        connection = self.engine.connect()
        trans = connection.begin()
        try:
            if values is not None:

                result = connection.execute(text(stmnt),values)
            else:
                result = connection.execute(text(stmnt))
            trans.commit()
            connection.close()
            print('Command executed successfully.')
        except Exception as err:
            trans.rollback()
            print(f'Failed to execute ddl and dml commands -- {err}')
            
            
            
gname = ''
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'login_or_register'
    st.session_state.check_login = 0
    st.session_state.check_register = 0
    st.session_state.l_name = ''
    st.session_state.l_pwd = ''
st.session_state.update(st.session_state)

def cb_login_home():
    st.session_state.active_page = 'login_home'
def cb_editcomment():
    st.session_state.active_page = 'edit_comment'
def cb_register_home():
    st.session_state.active_page = 'register_home'
def cb_product_page(pid):
    st.session_state.pidvalue = pid
    st.session_state.active_page = 'Product_info'
def cb_edit_address():
    st.session_state.active_page = 'Edit_Address'
def cb_edit_bank():
    st.session_state.active_page = 'Edit_Bank'
def cb_order_page(oid, statuss):
    st.session_state.orderid = oid
    st.session_state.state = statuss
    st.session_state.active_page = 'order_info'
def cb_cust_or_emp():
    st.session_state.active_page = 'login_or_register'
def cb_login_login():
    st.session_state.check_login=1
    st.session_state.check_register=0
    st.session_state.active_page = 'authentication'
def cb_register_login():
    st.session_state.check_login=0
    st.session_state.check_register=1
    st.session_state.active_page = 'authentication'
def cb_authentication():
    st.session_state.active_page = 'authentication'

def cb_otherdetails():
    st.session_state.active_page = 'otherdetails'
 
def login(name, password):
         USER_NAME = 'postgres'
         PASSWORD = 'postgres'
         PORT = 5432
         DATABASE_NAME = 'ecomm_project'
         HOST = 'localhost'

         db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
         engine = db.engine
         username = name
         print(username)
         values = {'username': username,'password': password}
         select_query_stmnt = "SELECT * FROM customer"
         result_1 = db.execute_dql_commands(select_query_stmnt)
         print("here")
         for r in result_1:
             print(r.customer_id)
             if int(r.customer_id) == int(username)  :
                gname = username
                st.balloons()
                return True
        #  return False

def register_insert(userName, name, email, phnumber, dob) :
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    ###
    Values = {'username': userName, 'name': name,'email': email, 'phoneNumber' : phnumber, 'dob': dob}
    single_insert_stmnt = "INSERT INTO customer VALUES ( :username , :name , :email, :phoneNumber, :dob );"
    db.execute_ddl_and_dml_commands(single_insert_stmnt,Values)
    # if(option == 'Buyer'):
    # Values = {'username': userName}
    # ####
    # single_insert_stmnt = "INSERT INTO customer VALUES ( :username );"
    # db.execute_ddl_and_dml_commands(single_insert_stmnt,Values)
    # if(option == 'Seller'):
    #             Values = {'username': userName}
    #             ####
    #             single_insert_stmnt = "INSERT INTO Seller VALUES ( :username );"
    #             db.execute_ddl_and_dml_commands(single_insert_stmnt,Values)
    import psycopg2
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST)
    values = {'uname': userName}
    select_query_stmnt = "CREATE USER {uname} WITH PASSWORD '{upassword}'"
    with conn.cursor() as cur:
         cur.execute(select_query_stmnt.format(**values))
    values = {'uname' : userName}
    select_query_stmnt = "GRANT {option} to {uname}"
    with conn.cursor() as cur:
         cur.execute(select_query_stmnt.format(**values))
         conn.commit()
    conn.close()

 
def register(userName, name, email, phnumber, dob):
            register_insert(userName, name, email, phnumber, dob)
            return True         

def LoggedIn_Clicked(userName, password):
        if login(userName, password):
            st.session_state.l_name = userName
            st.session_state.l_pwd = password
            cust_id = userName
            st.session_state.active_page = 'login_home'
        else:
            st.error("Invalid user name or password")

def registerIn_Clicked(userName, name, email, phnumber, dob):
        if register(userName, name, email, phnumber, dob):
            st.session_state.active_page = 'register_home'
        else:
            st.error("Username already exists")
            
def LoggedOut_Clicked():
         st.session_state.active_page = 'login_or_register'
                     
def authentication():
    if(st.session_state.check_login):
        st.title("Welcome to ShopKart \U0001F6CD")
        st.subheader("LogIn")
        userName = st.text_input (label = "",placeholder="Enter Id")
        password = st.text_input (label = "",placeholder="Enter password", type="password")
        st.button ("Login", on_click=LoggedIn_Clicked, args= (userName, password))
    if(st.session_state.check_register):
        st.title("Welcome to ShopKart \U0001F6CD")
        st.subheader("Registration Form")
        count = 1
        cnt = 1
        name = st.text_input("Name", key =f'{count}_{cnt}')
        cnt = 2
        userName = st.number_input("Username", key =f'{count}_{cnt}', step=1)
        cnt = 3
        userpassword = st.text_input("Password",type="password", key =f'{count}_{cnt}')
        cnt = 4
        Email = st.text_input("Email",  key =f'{count}_{cnt}')
        cnt = 5
        phnumber = st.text_input("Phone Number", key =f'{count}_{cnt}')
        cnt = 6
        dob = st.date_input("DOB", key = f'{count}_{cnt}')
        cnt = 7
        option = st.selectbox('Type of User',('Customer', 'Seller'), key =f'{count}_{cnt}')
        st.button("Register", on_click=registerIn_Clicked, args= (userName, name, Email, phnumber, dob))
        
def savingcart(custid, pid, quantity, s_id, price):
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'custId': custid, 'pid': pid,'seller_id': s_id, 'quantity': quantity,  'price': price}
    print(values)
    # k = 518
    st.write(custid)
    single_insert_stmnt = "INSERT INTO cart() values (:custId, :pid, :seller_id, :quantity, :price) ;"
    # select_query_stmnt = f"INSERT INTO Cart values {custid}, {pid}, {quantity}, {s_id}, {price};"
    db.execute_ddl_and_dml_commands(single_insert_stmnt, values)
    query = db.execute_dql_commands("select * from cart")
    data=pd.DataFrame(query)
    st.table(data)
    cb_login_home()

# def prod_info() :
#     st.sidebar.button("Back to Home Page", on_click = cb_login_home)
#     st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
#     USER_NAME = 'postgres'
#     PASSWORD = 'project'
#     PORT = 5432
#     DATABASE_NAME = 'test_project'
#     HOST = 'localhost'
#     db = PostgresqlDB(user_name=USER_NAME,
#                     password=PASSWORD,
#                     host=HOST,port=PORT,
#                     db_name=DATABASE_NAME)
#     engine = db.engine
#     value = {'pid' : st.session_state.pidvalue}
#     select_query_stmnt = "SELECT * FROM product where pid = :pid" 
#     result_1 = db.execute_dql_commands(select_query_stmnt, value)
#     st.title("Smart Buy")
#     st.subheader("Product Details")
#     for r in result_1:
#         c1, c2 = st.columns(2)
#         with c1 :
#             st.write(f"Name : {r.name}")
#             st.write(f"Category : {r.type}")
#             st.write(f"Color : {r.color}")
#             st.write(f"Brand : {r.brandname}")
#             st.write(f"Model Number : {r.modelnumber}")
#         with c2 :
#             st.write(f"price : {r.price}")
#             st.write(f"Grade : {r.productgrade}")
#         st.subheader("Comments")
#         value = {'pid' : st.session_state.pidvalue}
#         select_query_stmnt2 = "SELECT * FROM Comments where pid = :pid" 
#         result_2 = db.execute_dql_commands(select_query_stmnt2, value)
#         for r2 in result_2:
#             c1, c2 = st.columns(2)
#             with c1 :
#                 st.write(f"User : {r2.username}")
#                 st.write(f"Comment : {r2.content}")
#             with c2 :
#                 st.write(f"Rating : {r2.grade}")
#                 st.write(f"{r2.creationtime}")
#             st.write("----------------------------------------")      
#         st.button("Add/Edit your comment", on_click= cb_editcomment)
#         st.subheader("Add to Cart")
#         num = st.number_input('Enter the quantity', min_value= 1, step = 1)
        
def display_products(name):
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = f"SELECT * FROM customer_product_details where product_name like '%{name}%'" 
    result_1 = db.execute_dql_commands(select_query_stmnt)
    data= pd.DataFrame(result_1)
    # st.table(data)
   
    st.subheader("Products")
    k = 0

    for index, rows in data.iterrows():
        name = rows['product_name']
        sel_name = rows['seller_name']
        stok = rows['stock']
        cost = rows['price']
        sel_id = rows['seller_id']
        pro_id = rows['product_id']
        k = k+1
        # st.write(sel_id)
        st.write("----------------------")
        st.write(f"Product Name  : {name}")
        st.write(f"Seller Name  : {sel_name}")
        st.write(f"Stock Available : {stok}")
        st.write(f"Price of One piece: {cost}")

        st.button(f"Add to Cart \n {cost}", on_click = savingcart, args = (st.session_state.l_name, pro_id, 1, sel_id, cost))





    # for i in data :
        
    #     # st.write(i)
    #     # if i.product_name == name :
    #     #     st.write("Hello")
    #     # st.table(result_1)

    #     k = k + 1
    #     z = 1
    #     for j, l in data['product_name'], data['price']:
    #         if name == j : 
    #             st.write("----------------------")
    #             # st.write(f"Price : {l[j]}" )
    #             st.write(l)
    #             x = "View Product :" + str(z)
    #             z = z+1
    #             st.write(j)

    #         # st.write(f"")
    #     # st.write(z)

    #     if k == 1: 
    #         break
        # st.write("----------------------")
            # st.write(f"Product Name  : {data['product_name']}")
        # st.write(f"Seller Name : {i.seller_name}" )
        # st.write(f"Stock Available : {i.stock}")
    #    st.write(f"Total : {r.total}")
        # st.write(f"Price of One piece: {i.price}")
    #    st.write(f"Grade : {r.productgrade}")
    #    pid = r.product_id
        # x = str(i.price)
        #    st.button(f"Add to Cart \n {x}", on_click = savingcart, args = (st.session_state.l_name, 1, r.seller_id, r.price))
 
        #    st.write("----------------------")
        # # st.write(f"Name  : {r.product_name}")
        # # st.write("HIIIi")
           
        #    pid = r.product_id
        #    st.button(x, on_click = cb_product_page, args=[pid])
        
         
def not_yet_clicked():
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME) 
    engine = db.engine
    select_query_stmnt = "SELECT * FROM customer_product_details LIMIT 10" 
    st.subheader("Products")
    result_1 = db.execute_dql_commands(select_query_stmnt)
    for r in result_1 :
           st.write("----------------------")
           st.write(f"Product Name  : {r.product_name}")
           st.write(f"Seller Name : {r.seller_name}" )
           st.write(f"Stock Available : {r.stock}")
        #    st.write(f"Total : {r.total}")
           st.write(f"Price of One piece: {r.price}")
        #    st.write(f"Grade : {r.productgrade}")
        #    pid = r.product_id
           x = str(r.price)
           st.button(f"Add to Cart \n {x}", on_click = savingcart, args = (st.session_state.l_name, r.product_id, 1, r.seller_id, r.price))

        #    st.button(x, on_click = cb_product_page, args=[pid])
        
# def unique_category_list():
#     USER_NAME = 'postgres'
#     PASSWORD = 'postgres'
#     PORT = 5432
#     DATABASE_NAME = 'test_project'
#     HOST = 'localhost'
#     db = PostgresqlDB(user_name=USER_NAME,
#                     password=PASSWORD,
#                     host=HOST,port=PORT,
#                     db_name=DATABASE_NAME)
#     engine = db.engine
#     select_query_stmnt = "SELECT * FROM product" 
#     result_1 = db.execute_dql_commands(select_query_stmnt)
#     l = []
#     l.append('Search by Category')
#     for r in result_1 :
#         l.append(r.pname)
#     return l
    
# def unique_brand_list(option1):
#     if option1 == 'Search by Category':
#        option1 = 'NONE'
#     USER_NAME = 'postgres'
#     PASSWORD = 'postgres'
#     PORT = 5432
#     DATABASE_NAME = 'test_project'
#     HOST = 'localhost'
#     db = PostgresqlDB(user_name=USER_NAME,
#                     password=PASSWORD,
#                     host=HOST,port=PORT,
#                     db_name=DATABASE_NAME)
#     engine = db.engine
#     # value = {'category': option1}
#     select_query_stmnt = "SELECT * FROM product" 
#     result_1 = db.execute_dql_commands(select_query_stmnt)
#     l = []
#     l.append('Search by Brand')
#     for r in result_1 :
#         l.append(r.product_id)
#     return l

def update_cart_fun(pid, quantity):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'pid': pid, 'quantity': quantity}
    select_query_stmnt = "UPDATE Buyer_Save_to_Cart values SET quantity = :quantity WHERE pid = :pid;"
    db.execute_ddl_and_dml_commands(select_query_stmnt,values)
    cb_login_home()
    
def order_now():
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    select_query_stmnt10 = f"CALL place_order({st.session_state.l_name})"
    db.execute_ddl_and_dml_commands(select_query_stmnt10)
    # st.table(x)
    # for r2 in result10:
    #     if r2.transactions2 == 1 :
    #         st.error("Quantity ordered for one of your products exceeds supply quantity")
    #     else :
    #         st.info(f"Order processing...")
    #         cb_otherdetails()

def cart_products():
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = f"SELECT * FROM cart where customer_id = {st.session_state.l_name};" 
    # st.write()
    result = db.execute_dql_commands(select_query_stmnt) 
    st.table(result)
    total_amount = 0
    for r in result:
        select_query_stmnt1 = "SELECT pname FROM product where product_id = :pid ORDER BY product_id;"
        values = {'pid' : r.product_id}
        result1 = db.execute_dql_commands(select_query_stmnt1, values) 
        st.write("----------------------")
        st.write(f"Product Id : {r.product_id}")
        # st.write(result1)
        for r1 in result1:
            st.write(f"Product Name  : {r1.pname}")
        # st.write(f"Addtime : {r.addtime}")
        x = 'Quantity of pid ' + str(r.product_id)
        num = st.number_input(x, value = r.counts, step = 1, min_value = 0)
        # update_cart_fun(r.product_id, 1)
        # st.write(f"Amount : {r.cost}")
        # total_amount = total_amount + r.cost
        x = "View Product " + str(r.product_id)
        st.button(x, on_click = cb_product_page, args =[r.product_id])
    st.subheader(f"Total Amount : {total_amount}")
    st.button("Order Now", on_click = order_now)

def proceedfun(option1, option2) :
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    import psycopg2
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST)
    if option1 == 'Select Address':
            option1 = 'NONE'
    if option2 == 'Select BankCard':
            option2 = 123456789120
    values = {'option1' : option1, 'option2' : option2}
    select_query_stmnt = "SELECT * from transactions('{option1}', {option2})"
    with conn.cursor() as cur:
        cur.execute(select_query_stmnt.format(**values))
        result_1 = cur.fetchall()
        for r2 in result_1:
            if r2[0] == 0 :
                st.info("Transaction Success")
            else :
                st.error("Transaction Failure")
        conn.commit()
    cb_login_home()

def otherdetails():
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    st.header("Ordering ...")
    st.subheader("Select Address")
    select_query_stmnt = "SELECT category FROM user_addresses" 
    result_1 = db.execute_dql_commands(select_query_stmnt)
    l = []
    l.append('Select Address')
    for r in result_1 :
        l.append(r.category)
    option1 = st.selectbox('', l)
    st.subheader("Select BankCard")
    select_query_stmnt = "SELECT cardnumber FROM user_bankcard" 
    result_1 = db.execute_dql_commands(select_query_stmnt)
    l = []
    l.append('Select BankCard')
    for r in result_1 :
        l.append(r.cardnumber)
    option2 = st.selectbox('', l)
    click = st.button("Proceed", on_click = proceedfun, args = (option1, option2))
    
def change_name(phonenumber):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'name' : st.text_input("", placeholder= "Enter your Full Name"), 'phoneNumber' : phonenumber}
    select_query_stmnt5 = "INSERT INTO User_details values(:name, :phoneNumber)" 
    db.execute_dql_commands(select_query_stmnt5, values)

def display_personal_details():
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = f"SELECT * FROM customer where customer_id = {st.session_state.l_name}" 
    result = db.execute_dql_commands(select_query_stmnt)
    for r in result : 
        st.write(f"Full Name      :                    {r.name}")
        st.write(f"ContactPhoneNumber   :                 {r.contact}")
        st.write(f"Email Address      :                    {r.email}")
        st.write(f"DOB    :                    {r.dob}")
        # st.write(f"Phone Number   :                 {r.phonenumber}")
        st.write("-----------------------------------------------------------")
    select_query_stmnt = f"SELECT * FROM address where customer_id = {st.session_state.l_name}" 
    result = db.execute_dql_commands(select_query_stmnt)
    st.subheader("Address Details")
    for r in result : 
        st.write(f"Apartment   :                    {r.apartment}")
        st.write(f"Street   :                 {r.street}")
        st.write(f"City      :                    {r.city}")
        st.write(f"State    :                    {r.state}")
        # st.write(f"City   :                 {r.city}")
        st.write(f"Pin Code   :                 {r.pincode}")
        # st.write(f"Category    :                    {r.category}")
        st.write("-----------------------------------------------------------")
    # st.button("Edit Address", on_click = cb_edit_address)
    # select_query_stmnt = "SELECT * FROM User_bankCard" 
    # result = db.execute_dql_commands(select_query_stmnt)
    # st.subheader("Bank Card Details")
    # for r in result : 
    #     st.write(f"Card Holder Name      :                    {r.holdername}")
    #     st.write(f"Card Number   :                 {r.cardnumber}")
    #     st.write(f"Expiry Date      :                    {r.expirydate}")
    #     st.write(f"Bank    :                    {r.bank}")
    #     st.write("-----------------------------------------------------------")
    # st.button("Edit Bank Details", on_click = cb_edit_bank)

def your_orders() :
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    # st.write(cust_id)
    select_query_stmnt = f"SELECT * FROM Orders where customer_id = {st.session_state.l_name}" 

    result = db.execute_dql_commands(select_query_stmnt)
    c1, c2, c3, c4, c5 = st.columns([1,1.0,1.0,1.1, 1])
    with c1 :
        st.write("Order Id")
    with c2 :
        st.write("Order date")
    with c3 :
        st.write("Order Status")
    with c4 :
        st.write("Amount")
    with c5 :
        st.write("View Orders")
    # st.write(result)
    for r in result : 
        with c1 :    
            st.write(f"{r.order_id}")
            st.write("\n")
            st.write("-----------------\n")
        with c2 :
            st.write(r.date)
            st.write("\n")
            st.write("-----------------\n")
        with c3 :
            st.write(f"{r.status}")
            st.write("\n")
            st.write("-----------------\n")
        with c4 :
            st.write(f" \u20B9 {r.amount}")
            st.write("\n")
            st.write("-----------------\n")
        with c5 :
            # st.write("View the orders")
            # st.write("\n")
            # st.write("\n")
            # st.write("-----------------\n")
            x = 'View ' + str(r.order_id)
            st.button(x, on_click = cb_order_page, args = (r.order_id, r.status))
            st.write("-------------------\n")

def orderinfo():
    st.header("Order Details")
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'oid' : st.session_state.orderid} 
    select_query_stmnt = "SELECT * FROM contains where order_id = :oid  " 
    result = db.execute_dql_commands(select_query_stmnt, values)
    df = pd.DataFrame(result)
    df.index = [df.index+1]
    st.table(df)
    result1 = db.execute_dql_commands(select_query_stmnt, values)
    total_amount = 0
    for r in result1:
        total_amount += r.cost
    st.write(f"Total Amount for this order : {total_amount}")
    if st.session_state.state == 'success':
        st.subheader("Payment Details")
        select_query_stmnt = "SELECT holdername, cardnumber, bank FROM payment NATURAL JOIN bankcard where orderNumber = :oid" 
        result = db.execute_dql_commands(select_query_stmnt, values)
        for r in result:
            st.write(f"Holder Name: {r.holdername}")
            st.write(f"Card Number: {r.cardnumber}")
            st.write(f"Bank Name  : {r.bank}")
        st.subheader("Delivered to")
        select_query_stmnt1 = "SELECT name, contactphonenumber, province, city, streetaddr, postcode FROM deliver_to NATURAL JOIN address where orderNumber = :oid" 
        result1 = db.execute_dql_commands(select_query_stmnt1, values)
        for r in result1:
            st.write(f"Name              : {r.name}")
            st.write(f"ContactPhoneNumber: {r.contactphonenumber}")
            st.write(f"Province          : {r.province}")
            st.write(f"City              : {r.city}")
            st.write(f"Street Address    : {r.streetaddr}")
            st.write(f"Post Code         : {r.postcode}")

def login_home():
    with st.sidebar :
         selected = option_menu(st.session_state.l_name , ['Search', 'Profile', 'Cart', 'Orders'], icons=['search', 'person', "cart", 'list-task'], 
    menu_icon="house")
    st.sidebar.button("Log Out", on_click = LoggedOut_Clicked)
    if selected == 'Profile' :
       st.header("\U0001F464")
       st.subheader("Personal Details")
       display_personal_details() 
    if selected == 'Search' :
       st.title("Welcome to ShopKart \U0001F6CD")
       st.header("Search")
    #    st.subheader("Filters")
    #    category_list = unique_category_list()
    #    st.table(category_list)
    #    option1 = st.selectbox('', category_list)
    #    brand_list = unique_brand_list(option1)
    #    option2 = st.selectbox('', brand_list)
       option3 = st.text_input(label = "",placeholder="Enter your product name")
       clicked = st.button("Search")
       if clicked :
          display_products(option3)
       else :
          not_yet_clicked()
    if selected == 'Cart' :
        st.subheader("Your Cart\U0001F6D2")
        cart_products()
    if selected == 'Orders' :
        st.subheader("Your Orders \U0001F4E6")
        your_orders()
          
def register_home():
    st.title("Welcome to ShopKart \U0001F6CD") 
    st.subheader("Successful Registration")
    st.button("Go to main page", on_click = LoggedOut_Clicked)     
      
def login_or_register():
    st.title("Welcome to ShopKart \U0001F6CD")
    st.subheader("Login Or Sign Up")
    # c1, c2 = st.columns(2)
    # with c1:
    st.button("login", on_click=cb_login_login)
    # with c2:
    st.button("Sign Up", on_click=cb_register_login)       

def editadd(name, contactPhoneNumber, province, city, streetaddr, postcode, option):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    
    import psycopg2
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST)
    values = {'name' : name, 'contactPhoneNumber' : contactPhoneNumber, 'province' : province, 'city' : city, 'streetaddr' : streetaddr, 'postcode' : postcode, 'category' : option}
    select_query_stmnt = "INSERT INTO user_addresses values('{name}' , {contactPhoneNumber}, '{province}', '{city}', '{streetaddr}', {postcode}, '{category}')"
    with conn.cursor() as cur:
         cur.execute(select_query_stmnt.format(**values))
         conn.commit()
    conn.close()

def editaddressclicked(name, contactPhoneNumber, province, city, streetaddr, postcode, option) :
    editadd(name, contactPhoneNumber, province, city, streetaddr, postcode, option)
    cb_login_home()

def editaddress():
    st.header("Add/Edit Address")
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    option = st.selectbox('Select Category',('home', 'work', 'friend', 'other'))
    name = st.text_input("",placeholder = "Please type the Name")
    contactPhoneNumber = st.number_input("ContactPhoneNumber", step = 10000)
    province = st.text_input("",placeholder = "Please enter the Province")
    city = st.text_input("",placeholder = "Please enter the City")
    streetaddr = st.text_input("",placeholder = "Please enter the street address")
    postcode = st.number_input("postcode", step = 10000)
    st.button("Submit", on_click = editaddressclicked, args = (name, contactPhoneNumber, province, city, streetaddr, postcode, option))

def editbankclicked(holdername, banknumber, expirydate, bank):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    import psycopg2
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST)
    values = {'holdername' : holdername, 'banknumber' : banknumber, 'expirydate' : expirydate, 'bank' : bank}
    select_query_stmnt = "INSERT INTO user_bankcard values('{holdername}' , {banknumber}, '{expirydate}', '{bank}')"
    with conn.cursor() as cur:
         cur.execute(select_query_stmnt.format(**values))
         conn.commit()
    conn.close()
    cb_login_home()
    
def editbank():
    st.header("Add/Edit Bank Details")
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    holdername = st.text_input("",placeholder = "Please type the Bank holder name")
    banknumber = st.number_input("BankNumber", step = 10000)
    expirydate = st.date_input("Expiry Date")
    bank = st.text_input("Bank")
    st.button("Submit", on_click = editbankclicked, args = (holdername, banknumber, expirydate, bank))

def edit_comment(rating, content):
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    PORT = 5432
    DATABASE_NAME = 'ecomm_project'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    st.success("Added comment successfully")
    values = {'pid': st.session_state.pidvalue, 'option' : rating, 'content' : content}
    select_query_stmnt = "INSERT INTO Comments_product values(:pid, :option, :content);"
    db.execute_ddl_and_dml_commands(select_query_stmnt,values)
    cb_product_page(st.session_state.pidvalue)

def editcomment():
    st.header("Want to edit/add your comment!!")
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)  
    option = st.number_input('Rating', step = 1, max_value= 5, min_value= 1)
    content = st.text_input("Add your comment", placeholder = "Less than 500 characters",max_chars = 500)
    st.button("Add/Edit Comment", on_click = edit_comment, args = (option, content))
 
if st.session_state.active_page == 'login_home': 
    login_home()

elif st.session_state.active_page == 'register_home':
    register_home()

elif st.session_state.active_page == 'authentication':
    authentication()

elif st.session_state.active_page == 'login_or_register':
    login_or_register()
    
# elif st.session_state.active_page == 'Product_info':
#     prod_info()

elif st.session_state.active_page == 'otherdetails':
    otherdetails()
    
elif st.session_state.active_page == 'order_info' :
    orderinfo()

elif st.session_state.active_page == 'Edit_Address' :
    editaddress()

elif st.session_state.active_page == 'Edit_Bank' :
    editbank()

elif st.session_state.active_page == 'edit_comment' :
    editcomment()