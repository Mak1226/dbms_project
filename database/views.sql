CREATE OR REPLACE VIEW customer_product_details AS (
SELECT product.product_id AS ProductID,
product.pname AS Product_Name, 
sells.price, sells.stock,
seller.sname AS Seller_Name, 
seller.seller_id AS SellerID
FROM sells 
NATURAL JOIN product     
NATURAL JOIN seller
);

CREATE OR REPLACE VIEW product_price_avg AS (
SELECT productid, pname AS Product_Name, 
cast(AVG(sells.price) as integer) AS Average_Price
FROM Product
LEFT JOIN sells 
ON Product.product_id = sells.product_id
GROUP BY Product.product_id, pname);

CREATE OR REPLACE VIEW sales_per_day AS (
SELECT date, SUM(amount) AS total_sales
FROM orders
GROUP BY date
);

CREATE OR REPLACE VIEW most_sold_items AS (
SELECT s.seller_id, s.sname AS seller_name, 
SUM(c.counts * c.cost) AS total_sales
FROM seller s
JOIN sells sl 
ON s.seller_id = sl.seller_id
JOIN contains c 
ON sl.seller_id = c.seller_id 
AND sl.product_id = c.product_id
GROUP BY s.seller_id, s.sname
ORDER BY SUM(c.counts * c.cost) DESC
);

CREATE OR REPLACE VIEW customer_details AS (
SELECT cname,email,dob,contact,
(apartment || ',' || street || ',' || city || ',' || state || ',' || pincode)
AS Residence FROM customer NATURAL JOIN address
WHERE customer_id = session_user::int
);

CREATE OR REPLACE VIEW view_orders AS (
SELECT orders.order_id,
orders.date,
orders.status AS order_status,
orders.amount,
payment.mode,
payment.status AS payment_status
FROM orders
JOIN payment ON orders.payment_id = payment.payment_id
WHERE orders.customer_id = session_user::integer;
);

CREATE OR REPLACE VIEW order_details AS (
SELECT pname,sname,c.counts,c.cost,c.order_id 
FROM contains AS c 
JOIN product 
ON product.product_id = c.product_id
JOIN seller
ON seller.seller_id = c.seller_id 
);

CREATE OR REPLACE VIEW view_cart AS(
SELECT product.product_id,
product.pname,
seller.sname,
seller.seller_id,
c.counts,
c.price
FROM cart c
JOIN product ON product.product_id = c.product_id
JOIN seller ON seller.seller_id = c.seller_id
WHERE c.customer_id = session_user::int;
);

CREATE OR REPLACE VIEW sales_report AS (
SELECT c.product_id AS ProductID, p.pname AS Product_Name, SUM(c.counts) as sold, SUM(c.counts * c.cost) AS sale
FROM contains AS c
JOIN product AS p ON p.product_id = c.product_id
WHERE c.seller_id = session_user::int
GROUP BY c.product_id, p.pname
);

CREATE OR REPLACE VIEW seller_details AS (
SELECT seller_id, sname, email, contact
FROM seller
WHERE seller_id = session_user::int
);


CREATE OR REPLACE PROCEDURE test(i int)
SECURITY DEFINER
LANGUAGE plpgsql
AS $$
BEGIN
INSERT INTO one values (i,i+5);
CALL chk(i-1);
END;
$$;

CREATE OR REPLACE PROCEDURE chk(i int)
SECURITY DEFINER
LANGUAGE plpgsql
AS $$
BEGIN
UPDATE one SET s = i - 5 WHERE f = i;
END;
$$;