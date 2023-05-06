-- 1. How much worth of products are sold and how many orders are placed on a certain date
SELECT Orders.date,
COUNT(Order.order_id), SUM(Orders.amount)
FROM Orders
GROUP BY Orders.date
HAVING
Orders.date=<Orders.date>

-- 2. How many products are ordered by a customer.
SELECT Orders.order_id SUM(contains.counts)
FROM Orders NATURAL JOIN
contains NATURAL JOIN
Product
GROUP BY Orders.order_id
HAVING
Orders.order_id=<Orders.order_id>

-- 3. Total amount spent by each customer
SELECT Customer.customer_id, SUM(Orders.amount)
FROM Orders
NATURAL JOIN Customer
GROUP BY Customer.customer_id

-- 4. Calculate how many products each seller has.
SELECT s.seller_id, COUNT(p.product_id)
FROM sells as t
JOIN Seller as s ON
JOIN Product as p ON
GROUP BY s.seller_id

-- 5. Different number of products each order has.
SELECT Orders.order_id COUNT(Product.product_id) FROM Orders,
Product,
contains
WHERE Orders.order_id = contains.order_id AND contains.product_id = Product.product_id GROUP BY Orders.order_id