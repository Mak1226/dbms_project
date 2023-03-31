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

-- update the amount in orders table

CREATE OR REPLACE FUNCTION get_stock(pid int)
RETURNS int
LANGUAGE plpgsql
AS
$$
DECLARE
p int;
BEGIN
SELECT SUM(sells.stock) INTO p FROM sells INNER JOIN product ON sells.product_id=product.product_id WHERE product.product_id = pid;
RETURN p;
END;
$$;

SELECT get_stock(<product_id>)