-- The function get_price will take product_id as an input and returns its price.

CREATE FUNCTION get_price(p_id int) RETURNS int
LANGUAGE plpgsql
AS
$$
DECLARE
P_price int;
BEGIN
SELECT price INTO p_price
FROM Product
WHERE product_id = p_id;
RETURN p_price;
END;
$$;

SELECT get_price(<product_id>)

-- update the STOCK in Product table

CREATE OR REPLACE FUNCTION get_stock(pid int)
RETURNS VOID
LANGUAGE plpgsql
AS
$$
DECLARE
p int;
BEGIN
SELECT SUM(stock) INTO p FROM sells GROUP BY product_id HAVING product_id = pid;
IF p IS NOT NULL THEN 
UPDATE Product SET max = p WHERE product_id = pid; 
ELSE 
UPDATE Product SET max = 0 WHERE product_id = pid; 
END IF;
END;
$$;

SELECT get_stock(<product_id>)

-- update the amount in Orders table

CREATE OR REPLACE FUNCTION get_amount(id int)
RETURNS VOID
LANGUAGE plpgsql
AS
$$
DECLARE
amt int;
BEGIN
SELECT SUM(counts * cost) INTO amt 
FROM contains
WHERE order_id = id;
IF amt IS NOT NULL THEN
UPDATE Orders
SET amount = amt WHERE order_id = id;
ELSE
UPDATE Orders
SET amount = 0 WHERE order_id = id;
END IF;
END;
$$;

SELECT get_amount(<order_id>);

CREATE OR REPLACE FUNCTION(id_order int)
RETURNS VOID
AS
$$
DECLARE
pid int;
oid int;
amt int;
BEGIN
UPDATE Orders
SET status = 'Cancelled'
WHERE order_id = id_order;