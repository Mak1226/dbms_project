CREATE TABLE Customer(
customer_id int PRIMARY KEY,
cname char(15) NOT NULL,
email char(30) NOT NULL,
contact char(10) NOT NULL,
passkey char(20) NOT NULL,
DOB char(10)
);
CREATE TABLE Product(
product_id int NOT NULL,
pname char(15) NOT NULL,
total int DEFAULT -1,
PRIMARY KEY(product_id)
);
CREATE TABLE Payment(
payment_id int NOT NULL,
mode char (15) NOT NULL,
status char(10) DEFAULT 'Pending',
PRIMARY KEY(payment_id)
);
CREATE TABLE Orders(
order_id int NOT NULL,
date char(10) NOT NULL,
status char(10) DEFAULT 'Ordered',
amount int DEFAULT -1,
customer_id int,
payment_id int,
PRIMARY KEY(order_id),
FOREIGN KEY (customer_id) REFERENCES Customer (customer_id),
FOREIGN KEY (payment_id) REFERENCES Payment (payment_id)
);
CREATE TABLE Address(
apartment char(5) NOT NULL,
street char (15) NOT NULL,
city char (20) NOT NULL,
state char(20) NOT NULL,
pincode int NOT NULL,
customer_id int,
PRIMARY KEY(customer_id, pincode, apartment, street),
FOREIGN KEY (customer_id) REFERENCES Customer (customer_id)
);
CREATE TABLE Seller(
seller_id int NOT NULL,
sname char (15) NOT NULL,
email char(30) NOT NULL,
contact char(10) NOT NULL,
passkey char(20) NOT NULL,
PRIMARY KEY(seller_id)
);
CREATE TABLE sells (
stock int DEFAULT 0,
price decimal,
seller_id int,
product_id int,
PRIMARY KEY(seller_id, product_id),
FOREIGN KEY (seller_id) REFERENCES Seller (seller_id),
FOREIGN KEY (product_id) REFERENCES Product (product_id)
);
CREATE TABLE contains(
counts int NOT NULL,
cost int,
seller_id int,
product_id int,
order_id int,
PRIMARY KEY(product_id, order_id, seller_id),
FOREIGN KEY (order_id) REFERENCES Orders (order_id),
FOREIGN KEY (seller_id, product_id) REFERENCES sells (seller_id, product_id)
);
CREATE TABLE Cart(
customer_id int,
product_id int,
seller_id int,
counts int DEFAULT 1,
price int NOT NULL,
PRIMARY KEY(customer_id, product_id, seller_id),
FOREIGN KEY (customer_id) REFERENCES Customer (customer_id),
FOREIGN KEY (seller_id, product_id) REFERENCES sells(seller_id, product_id)
);