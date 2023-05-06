-- CREATE ROLE customer_
-- LOGIN 
-- PASSWORD 'dbms';

-- GRANT UPDATE
-- ON TABLE
-- address
-- TO customer_;

-- CREATE USER 
-- aditya WITH
-- PASSWORD 'aditya';

-- GRANT customer_
-- TO aditya;


-- Create customer role
CREATE ROLE customer_role LOGIN PASSOWORD "passkey";
GRANT SELECT ON Customer, Address, Payment, Orders, sells, contains;


-- Create seller role
CREATE ROLE seller;

-- Permissions required for seller
GRANT SELECT, INSERT, UPDATE, DELETE ON sells TO seller;
GRANT SELECT, INSERT, UPDATE, DELETE ON Product TO seller;
GRANT SELECT, INSERT, UPDATE, DELETE ON contains TO seller;
GRANT SELECT ON Orders TO seller;

-- Create admin role
CREATE ROLE admin LOGIN PASSOWORD "admindatabase";

-- Permissions required for admin
GRANT ALL ON ALL TABLES IN SCHEMA "public" T0 admin;