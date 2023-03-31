-- total_amount : this view shows the total amount that has been spend by each customer.
CREATE VIEW total_amount AS
SELECT customer_id, SUM(amount)
FROM Orders
NATURAL JOIN Customer
GROUP BY customer_id

-- total_product : this view shows how many different products each seller has.
CREATE VIEW total_product AS
SELECT COUNT
FROM sells as t
JOIN Seller as s ON t.seller_id = s.seller_id JOIN Product as p ON
t.product_id = p.product_id
GROUP BY s.seller_id

