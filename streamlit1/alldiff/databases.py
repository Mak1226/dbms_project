import psycopg2

def connect_to_database():
    conn = psycopg2.connect(
        host='localhost',
        database='dbms',
        user='postgres',
        password='postgres'
    )
    return conn

# def connect_to_user(x = None):
#     conn = psycopg2.connect(
#         host = 'localhost',
#         database = 'dbms',
#         user='aditya',
#         password= 'aditya'

#     )
#     return conn

