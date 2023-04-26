CREATE ROLE customer_
LOGIN 
PASSWORD 'dbms';

GRANT UPDATE
ON TABLE
address
TO customer_;

CREATE USER 
aditya WITH
PASSWORD 'aditya';

GRANT customer_
TO aditya;

