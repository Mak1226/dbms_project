CREATE TABLE Customer(
customer_id int PRIMARY KEY,
name char(50) NOT NULL,
email char(255),
contact char(50) NOT NULL,
DOB char(30)
);
CREATE TABLE Product(
product_id int NOT NULL, 
name char(50) NOT NULL, 
price int NOT NULL,
total int DEFAULT -1, 
PRIMARY KEY(product_id)
);
CREATE TABLE Orders(
order_id int NOT NULL,
date char(50) NOT NULL,
status char(20) DEFAULT 'Ordered',
amount int DEFAULT -1,
customer_id int,
PRIMARY KEY(order_id), 
FOREIGN KEY (customer_id) REFERENCES Customer (customer_id)
);
CREATE TABLE Address(
apartment char(50) NOT NULL, 
street char (30) NOT NULL,
city char (20) NOT NULL,
state char(30) NOT NULL,
pincode int NOT NULL, 
customer_id int,
PRIMARY KEY(customer_id, pincode, apartment, street), 
FOREIGN KEY (customer_id) REFERENCES Customer (customer_id)
);
CREATE TABLE Payment(
payment_id int NOT NULL,
mode char (50) NOT NULL, 
customer_id int, 
order_id int,
PRIMARY KEY(payment_id), 
FOREIGN KEY (customer_id) REFERENCES Customer (customer_id),
FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);
CREATE TABLE Seller(
seller_id int NOT NULL,
name char (50) NOT NULL, 
Contact char(20) NOT NULL, 
PRIMARY KEY(seller_id)
);
CREATE TABLE contains(
counts int NOT NULL, 
product_id int, 
order_id int,
PRIMARY KEY(product_id, order_id), 
FOREIGN KEY (product_id) REFERENCES Product (product_id), 
FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);
CREATE TABLE sells ( 
stock int NOT NULL, 
seller_id int,
product_id int,
PRIMARY KEY(seller_id, product_id), 
FOREIGN KEY (seller_id) REFERENCES Seller (seller_id), 
FOREIGN KEY (product_id) REFERENCES Product (product_id)
);
CREATE TABLE Cart(
customer_id int,
product_id int,
counts int DEFAULT 1,
PRIMARY KEY(customer_id, product_id),
FOREIGN KEY (customer_id) REFERENCES Customer (customer_id),
FOREIGN KEY (product_id) REFERENCES Product (product_id)
);
CREATE TABLE Record(
order_id int,
product_id int,
seller_id int,
counts int NOT NULL,
PRIMARY KEY (order_id,product_id,seller_id),
FOREIGN KEY (product_id) REFERENCES Product (product_id),
FOREIGN KEY (seller_id) REFERENCES Seller (seller_id),
FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

-- 101
CREATE TABLE weapon_category(
category_id int primary key,
category varchar(15)
);
-- 201
CREATE TABLE weapons(
weapon_id int primary key,
name varchar(10),
category int,
skin_id int,
FOREIGN KEY (category) REFERENCES weapon_category (category_id),
FOREIGN KEY (skin_id) REFERENCES skin (skin_id)
);
-- 301
CREATE TABLE skin(
skin_id int primary key,
name varchar(21),
price int
);
CREATE TABLE price_breakdown(
int price primary key,
breakdown varchar(50)
);

insert into weapon_category values
(101,'Sidearms'),
(102,'Smgs'),
(103,'Shotguns'),
(104,'Rifles'),
(105,'Sniper Rifles'),
(106,'Machine Guns'),
(107,'Melee');

-- id, name, category, price
update weapons set name='Classic' where weapon_id=201;
update weapons set name='Shorty' where weapon_id=202;
update weapons set name='Frenzy' where weapon_id=203;
update weapons set name='Ghost' where weapon_id=204;
update weapons set name='Sheriff' where weapon_id=205;
update weapons set name='Stinger' where weapon_id=206;
update weapons set name='Spectre' where weapon_id=207;
update weapons set name='Bucky' where weapon_id=208;
update weapons set name='Judge' where weapon_id=209;
update weapons set name='Bulldog' where weapon_id=210;
update weapons set name='Guardian' where weapon_id=211;
update weapons set name='Phantom' where weapon_id=212;
update weapons set name='Vandal' where weapon_id=213;
update weapons set name='Marshal' where weapon_id=214;
update weapons set name='Operator' where weapon_id=215;
update weapons set name='Ares' where weapon_id=216;
update weapons set name='Odin' where weapon_id=217;
update weapons set name='Melee' where weapon_id=218;

INSERT INTO skin VALUES 
(301,'Glitchpop'),
(302,'Araxys'),
(303,'Ion 2.0'),
(304,'Radiant Entertainment'),
(305,'Singularity'),
(306,'Prelude to Chaos'),
(307,'RGX 11Z Pro 2.0'),
(308,'Origin'),
(309,'Enderflame'),
(310,'Protocol 781-A'),
(311,'Spectrum'),
(312,'Champions 22'),
(313,'Gaia Vengence'),
(314,'Neo Frontier'),
(315,'Reaver'),
(316,'Sentinals of Light'),
(317,'BlastX'),
(318,'Valient Heroes');