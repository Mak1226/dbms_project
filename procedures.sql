-- The procedure update_price will take an amount and a product_id as an input and will update the price of that product wrt that amount.

CREATE PROCEDURE update_price(change int, p_id int) LANGUAGE plpgsql
AS
$$
DECLARE
p_price int;
BEGIN
UPDATE Product
SET price = price + change
WHERE product_id = p_id;
COMMIT;
END;
$$;

CALL update_price(<change_amount_with_sign>, <product_id>)

-- update the stock of the product

CREATE OR REPLACE PROCEDURE get_amount(oid int)
LANGUAGE plpgsql
AS
$$
DECLARE
cost int;
BEGIN
cost = 0;
SELECT sum(t.counts*p.price) INTO cost FROM 
(SELECT c.counts, c.product_id 
FROM contains AS c 
NATURAL JOIN orders AS o
WHERE o.order_id = oid) AS t 
JOIN product AS p
ON p.product_id = t.product_id;
IF cost IS NOT null THEN
  UPDATE orders
  SET amount = cost WHERE order_id = oid;
ELSE
  UPDATE orders
  SET amount = 0 WHERE order_id = oid;
END IF;
END;
$$;

CALL get_amount(<order_id>)

CREATE OR REPLACE PROCEDURE place_order(id int)
LANGUAGE plpgsql
AS
$$
DECLARE
generate_order_id int;
BEGIN
INSERT INTO Orders(date, customer_id) values (current_date, id);
SELECT order_id INTO generate_order_id FROM Orders ORDER BY DESC LIMIT 1; 
INSERT INTO contains(counts, product_id, order_id) SELECT counts, product_id FROM Cart WHERE customer_id = id;

create or replace procedure add_passkey()
LANGUAGE plpgsql
as $$
declare 
pass text;
cid int;
begin
for cid in select customer_id from customer loop
  select (name || customer_id) into pass from customer where customer_id = cid;
  update customer set passkey = md5(pass) where customer_id = cid;
end loop;
end;
$$;