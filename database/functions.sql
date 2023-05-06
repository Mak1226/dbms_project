-- 2 FUNCTIONS

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

-- procedure to place order from the cart

CREATE OR REPLACE PROCEDURE place_order (cid int)
LANGUAGE plpgsql
as 
$$
DECLARE
new_id int;
BEGIN
SELECT order_id INTO new_id FROM Orders ORDER BY order_id DESC LIMIT 1;
new_id = new_id + 1;
INSERT INTO Orders (order_id,date,customer_id) values (new_id,to_char(CURRENT_DATE, 'DD-MM-YYYY'),cid);
INSERT INTO contains SELECT counts, price, seller_id, product_id, new_id FROM Cart WHERE customer_id = cid;

UPDATE sells
SET stock = stock - counts
FROM cart
WHERE sells.seller_id = cart.seller_id 
AND sells.product_id = cart.product_id ;

DELETE FROM cart
WHERE  customer_id = cid;

SELECT get_amount(new_id)
END;
$$;

-- 5 TRIGGERS

-- trigger function for Failed payment

CREATE OR REPLACE FUNCTION procedure_failed_payment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS
$$
DECLARE
change int;
BEGIN
IF NEW.status ILIKE '%Failed%' THEN 
    UPDATE Orders
    SET status = 'Cancelled'
    WHERE order_id = NEW.order_id;

    UPDATE sells 
    SET stock = stock + contains.counts 
    FROM contains
    WHERE sells.seller_id = contains.seller_id 
    AND sells.product_id = contains.product_id 
    AND order_id = NEW.order_id;
END IF;
RETURN NEW;
END;
$$;

-- trigger function to add new role 

CREATE OR REPLACE FUNCION role_creation()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE 
id int;
idname text;
pass text;
BEGIN
SELECT NEW.customer_id INTO id;
SELECT id::varchar(5) INTO idname;
SELECT NEW.passkey INTO pass;
EXECUTE FORMAT('CREATE ROLE %I LOGIN PASSWORD %L', idname, pass);
EXECUTE FORMAT('CREATE POLICY customer_view ON customer FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id);
EXECUTE FORMAT('CREATE POLICY address_view ON address FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id); 
EXECUTE FORMAT('CREATE POLICY orders_view ON orders FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id);
EXECUTE FORMAT('CREATE POLICY payment_view ON payment FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id); 
EXECUTE FORMAT('CREATE POLICY cart_view ON cart FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id);
EXECUTE FORMAT('CREATE POLICY cart_insert ON cart FOR INSERT TO %I WITH CHECK (customer_id = %s::integer)', idname, id);
EXECUTE FORMAT('CREATE POLICY cart_update ON cart FOR UPDATE TO %I USING (customer_id = %s::integer)', idname, id);
EXECUTE FORMAT('CREATE POLICY cart_delete ON cart FOR DELETE TO %I WITH CHECK (customer_id = = %s::integer)', idname, id);
EXECUTE FORMAT('GRANT SELECT ON customer TO %I', idname);
EXECUTE FORMAT('GRANT SELECT ON address TO %I', idname);
EXECUTE FORMAT('GRANT SELECT ON orders TO %I', idname);
EXECUTE FORMAT('GRANT SELECT ON payment TO %I', idname);
EXECUTE FORMAT('GRANT SELECT, UPDATE(counts), INSERT, DELETE ON Cart TO %I', idname);
RETURN NEW;
END;
$$;

-- trigger function to update the total stock of product

CREATE OR REPLACE FUNCTION get_stock()
RETURNS trigger
LANGUAGE plpgsql
AS
$$
DECLARE
p int;
pid int;
BEGIN
SELECT NEW.product_id INTO pid;
SELECT SUM(stock) INTO p FROM sells WHERE product_id = pid;
IF p IS NOT NULL THEN 
UPDATE Product SET total = p WHERE product_id = pid; 
ELSE 
UPDATE Product SET total = 0 WHERE product_id = pid; 
END IF;
RETURN NULL;
END;
$$;

-- trigger function to check the cart stock

CREATE OR REPLACE FUNCTION check_stock()
RETURNS TRIGGER AS $$
DECLARE
stock_count int;
BEGIN

    select stock into stock_count  from sells WHERE seller_id = NEW.seller_id AND product_id = NEW.product_id;
    IF EXISTS (
        SELECT 1 FROM sells
        WHERE seller_id = NEW.seller_id AND product_id = NEW.product_id AND stock < NEW.counts
    ) THEN
        RAISE NOTICE 'Available stock count is %, So, you cannot add % stock in your cart', stock_count, NEW.counts;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- trigger function for Cancelled Order

CREATE OR REPLACE FUNCION procedure_cancelled_order()
RETURNS TRIGGER
LANGUAGE plpgsql
AS
$$
BEGIN
IF NEW.status ILIKE '%Cancelled%' THEN
    UPDATE sells
    SET stock = stock + contains.counts
    FROM contains
    WHERE sells.seller_id = contains.seller_id
    AND sells.product_id = contains.product_id
    AND order_id = NEW.order_id;
END IF;
RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION add_new_product(pro text, id int, cost int, stk int)
RETURNS VOID
LANGUAGE plpgsql
AS
$$
DECLARE
new_id int;
BEGIN
SELECT product_id INTO new_id FROM Product ORDER BY product_id DESC;
new_id = new_id + 1
INSERT INTO Product (product_id, pname) VALUES (new_id, pro);
INSERT INTO sells (product_id, seller_id, price, stock) VALUES (new_id, id, cost, stk);
END;
$$;