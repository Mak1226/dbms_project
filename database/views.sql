CREATE OR REPLACE VIEW customer_product_details AS (
SELECT product.pname AS Product_Name, 
seller.sname AS Seller_Name, 
sells.price, sells.stock, product_id, seller_id
FROM sells 
NATURAL JOIN product     
NATURAL JOIN seller);

CREATE OR REPLACE VIEW product_price_avg AS (
SELECT pname AS Product_Name, 
cast(AVG(sells.price) as integer) AS Average_Price
FROM Product
LEFT JOIN sells 
ON Product.product_id = sells.product_id
GROUP BY Product.product_id, pname);

CREATE OR REPLACE VIEW sales_per_day AS (
SELECT date, SUM(amount) AS total_sales
FROM orders
GROUP BY date);

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
ORDER BY SUM(c.counts * c.cost) DESC);