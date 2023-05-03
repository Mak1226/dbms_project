import psycopg2

def connect_to_database():
    conn = psycopg2.connect(
        host='localhost',
        database='test_project',
        user='postgres',
        password='project'
    )
    return conn

def connect_to_user(x = None):
    conn = psycopg2.connect(
        host = 'localhost',
        database = 'test_project',
        user='aditya',
        password= 'aditya'

    )
    return conn

