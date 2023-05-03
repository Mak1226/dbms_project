-- customer --- writes --- Review --- against --- Orders --- for --- Product

CREATE TABLE Review(
ratings int,
description varchar(100),
order_id int,
product_id int,
PRIMARY KEY (customer_id, order_id, product_id)
FOREIGN KEY (product_id)
REFERENCES Product (product_id),
FOREIGN KEY (order_id)
REFERENCES Orders (order_id)
-- customer_id int,
-- seller_id int,
-- FOREIGN KEY (customer_id)
-- REFERENCES Customer (customer_id),
-- FOREIGN KEY (seller_id)
-- REFERENCES Seller (seller_id)
);