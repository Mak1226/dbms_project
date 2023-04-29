-- The function get_price will take product_id as an input and returns its price.

-- Shailab ka phaltu procedure

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
UPDATE Product SET total = p WHERE product_id = pid; 
ELSE 
UPDATE Product SET total = 0 WHERE product_id = pid; 
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
amt float;
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

-- trigger function

CREATE OR REPLACE FUNCTION failed_payment_procedure(id_order int)
RETURNS TRIGGER
LANGUAGE plpgsql
AS
$$
DECLARE
change int;
BEGIN
UPDATE Orders
SET status = 'Cancelled'
WHERE order_id = id_order;

UPDATE sells 
SET stock = stock + contains.counts 
FROM contains
WHERE sells.seller_id = contains.seller_id 
AND sells.product_id = contains.product_id 
AND order_id = id_order;
RETURN NEW;
END;
$$;

-- procedure to place order from the cart

CREATE OR REPLACE PROCEDURE place_order (cid int)
LANGUAGE plpgsql
as 
$$
DECLARE
new_id int;
BEGIN
SELECT order_id INTO new_id FROM Orders ORDER BY order_id DESC;
new_id = new_id + 1;
INSERT INTO Orders (order_id,date,customer_id) values (new_id,CURRENT_DATE,cid);
INSERT INTO contains SELECT counts, price, seller_id, product_id, new_id FROM Cart WHERE customer_id = cid;
END;
$$;

-- procedure to change 