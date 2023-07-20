-- done!
CREATE TRIGGER failed_payment
AFTER UPDATE ON payment
FOR EACH ROW
EXECUTE PROCEDURE payment_fail();

CREATE TRIGGER add_new_user
AFTER INSERT ON customer
FOR EACH ROW
EXECUTE FUNCTION add_customer();

CREATE TRIGGER add_new_seller
AFTER INSERT ON seller
FOR EACH ROW
EXECUTE FUNCTION add_seller();


CREATE TRIGGER product_stock_trigger
AFTER UPDATE OR INSERT ON sells
FOR EACH ROW
EXECUTE FUNCTION get_stock();

-- done!
CREATE TRIGGER check_stock_trigger
BEFORE INSERT ON Cart
FOR EACH ROW
EXECUTE FUNCTION check_stock();

CREATE TRIGGER cancel_order_trigger
AFTER UPDATE ON Orders
FOR EACH ROW
EXECUTE FUNCTION order_cancellation();


-- trigger function for Failed payment
-- done!
CREATE OR REPLACE FUNCTION payment_fail()
RETURNS TRIGGER
SECURITY DEFINER
LANGUAGE plpgsql
AS
$$

DECLARE
pay int;
id_order int;
BEGIN
IF NEW.status ILIKE '%Failed%' THEN 
    SELECT NEW.payment_id INTO pay;
    UPDATE Orders
    SET status = 'Cancelled'
    WHERE payment_id = pay;
    SELECT order_id INTO id_order
    FROM Orders
    WHERE payment_id = pay;

    UPDATE sells 
    SET stock = stock + contains.counts 
    FROM contains
    WHERE sells.seller_id = contains.seller_id 
    AND sells.product_id = contains.product_id 
    AND order_id = id_order;
    RAISE NOTICE 'Payment Failed. Your Order is Cancelled.';
END IF;
RETURN NEW;

END;
$$;

-- trigger function to update the total stock of product

CREATE OR REPLACE FUNCTION get_stock()
RETURNS TRIGGER
SECURITY DEFINER
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
RAISE NOTICE 'Product stocks updated.';
RETURN NULL;

END;
$$;

-- trigger function for Cancelled Order
-- done!
CREATE OR REPLACE FUNCTION order_cancellation()
RETURNS TRIGGER
SECURITY DEFINER
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
    RAISE NOTICE 'Order Cancelled Successfully. Order ID: %',NEW.order_id;
END IF;
RETURN NEW;

END;
$$;

-- trigger function to check the cart stock
-- done!
CREATE OR REPLACE FUNCTION check_stock()
RETURNS TRIGGER
SECURITY DEFINER
LANGUAGE plpgsql
AS
$$

DECLARE
stock_count int;

BEGIN
    SELECT stock INTO stock_count FROM sells WHERE seller_id = NEW.seller_id AND product_id = NEW.product_id;
    IF stock_count < NEW.counts THEN
    RAISE NOTICE 'Available stock = %. Therefore cannot place an order of % items.',stock_count, NEW.counts;
    RETURN NULL;
    ELSE
    RETURN NEW;
    END IF;

END;
$$;

-- trigger function to add new user
-- done!

CREATE OR REPLACE FUNCTION add_customer()
RETURNS TRIGGER
SECURITY DEFINER
LANGUAGE plpgsql
AS $$

DECLARE
id int;
p text;
n text;
BEGIN

SELECT new.customer_id INTO id;
SELECT id::text INTO n;
SELECT new.passkey INTO p;
EXECUTE FORMAT ('CREATE USER %I LOGIN PASSWORD %L', n, p);
EXECUTE FORMAT ('GRANT r1 TO %I', n);
RAISE NOTICE 'NEW USER CREATED!';
RETURN NEW;

END;
$$;

CREATE OR REPLACE FUNCTION add_seller()
RETURNS TRIGGER
SECURITY DEFINER
LANGUAGE plpgsql
AS $$

DECLARE
id int;
p text;
n text;
BEGIN

SELECT new.seller_id INTO id;
SELECT id::text INTO n;
SELECT new.passkey INTO p;
EXECUTE FORMAT('CREATE USER %I LOGIN PASSWORD %L',n,p);
EXECUTE FORMAT('GRANT r2 TO %I',n);
RAISE NOTICE 'NEW USER CREATED!';
RETURN NEW;

END;
$$;

-- CREATE OR REPLACE FUNCTION add_customer()
-- RETURNS TRIGGER
-- LANGUAGE plpgsql
-- AS $$
-- DECLARE 
-- id int;
-- idname text;
-- pass text;
-- BEGIN
-- SELECT NEW.customer_id INTO id;
-- SELECT id::varchar(5) INTO idname;
-- SELECT NEW.passkey INTO pass;
-- EXECUTE FORMAT('CREATE ROLE %I LOGIN PASSWORD %L', idname, pass);
-- EXECUTE FORMAT('CREATE POLICY customer_view ON customer FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id);
-- EXECUTE FORMAT('CREATE POLICY address_view ON address FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id); 
-- EXECUTE FORMAT('CREATE POLICY orders_view ON orders FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id);
-- EXECUTE FORMAT('CREATE POLICY payment_view ON payment FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id); 
-- EXECUTE FORMAT('CREATE POLICY cart_view ON cart FOR SELECT TO %I USING (customer_id = %s::integer)', idname, id);
-- EXECUTE FORMAT('CREATE POLICY cart_insert ON cart FOR INSERT TO %I WITH CHECK (customer_id = %s::integer)', idname, id);
-- EXECUTE FORMAT('CREATE POLICY cart_update ON cart FOR UPDATE TO %I USING (customer_id = %s::integer)', idname, id);
-- EXECUTE FORMAT('CREATE POLICY cart_delete ON cart FOR DELETE TO %I WITH CHECK (customer_id = = %s::integer)', idname, id);
-- EXECUTE FORMAT('GRANT SELECT ON customer TO %I', idname);
-- EXECUTE FORMAT('GRANT SELECT ON address TO %I', idname);
-- EXECUTE FORMAT('GRANT SELECT ON orders TO %I', idname);
-- EXECUTE FORMAT('GRANT SELECT ON payment TO %I', idname);
-- EXECUTE FORMAT('GRANT SELECT, UPDATE(counts), INSERT, DELETE ON Cart TO %I', idname);
-- RETURN NEW;
-- END;
-- $$;
