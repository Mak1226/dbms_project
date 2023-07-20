-- 2 Procedures

-- update the amount in Orders table

CREATE OR REPLACE PROCEDURE get_amount(id int)
SECURITY DEFINER
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

-- procedure to place order from the cart

CREATE OR REPLACE PROCEDURE place_order (pay int)
SECURITY DEFINER
LANGUAGE plpgsql
AS 
$$

DECLARE
new_id int;
pay_status text;

BEGIN
SELECT order_id INTO new_id 
FROM Orders 
ORDER BY order_id DESC 
LIMIT 1;

SELECT status INTO pay_status 
FROM Payment 
WHERE payment_id = pay;

IF pay_status ILIKE '%Failed%' THEN
    RAISE NOTICE 'Failed Payment. Cannot Place Order. Try Again';
ELSE
    new_id = new_id + 1;
    INSERT INTO Orders (order_id,date,customer_id,payment_id) 
    VALUES (new_id,to_char(CURRENT_DATE, 'DD-MM-YYYY'),session_user::int,pay);
    INSERT INTO contains 
    SELECT counts, price, seller_id, product_id, new_id 
    FROM Cart 
    WHERE customer_id = session_user::int;

    UPDATE sells
    SET stock = stock - counts
    FROM cart
    WHERE sells.seller_id = cart.seller_id 
    AND sells.product_id = cart.product_id ;
    DELETE FROM cart
    WHERE customer_id = session_user::int;
    RAISE NOTICE 'Order placed successfully';
    CALL get_amount(new_id);
END IF;

END;
$$;

CREATE OR REPLACE FUNCTION view_order_details(id int)
RETURNS SETOF customer_data
SECURITY DEFINER
LANGUAGE plpgsql
AS 
$$
BEGIN
IF EXISTS (SELECT order_id, customer_id FROM Orders WHERE order_id = id AND customer_id = session_user::int)
THEN
    RETURN QUERY 
    SELECT * FROM order_details WHERE order_id = id;
ELSE
    RAISE NOTICE 'Wrong order_id.'; 
END IF;
END;
$$;

CREATE TYPE customer_data AS(
pname character(15), 
sname character(15), 
counts INT, cost INT, 
order_id INT
);

CREATE OR REPLACE PROCEDURE add_to_cart(pid int,sid int,q int)
SECURITY DEFINER
LANGUAGE plpgsql
AS
$$
DECLARE
c int;
p int;
BEGIN
IF EXISTS (SELECT stock,price FROM sells WHERE product_id = pid AND seller_id = sid)
THEN
    SELECT stock,price INTO c,p 
    FROM sells 
    WHERE product_id = pid AND seller_id = sid;
    IF q <= c THEN
        INSERT INTO Cart 
        VALUES (session_user::int,pid,sid,q,p);
        RAISE NOTICE 'Item has been added to your cart successfully';
    ELSE
        RAISE NOTICE 'Quantity more than available stock';
    END IF;
ELSE
    RAISE NOTICE 'Not valid Product ID or Stock Id';
END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_from_cart(pid int,sid int)
SECURITY DEFINER
LANGUAGE plpgsql
AS
$$
BEGIN
IF EXISTS (SELECT counts,price FROM cart WHERE product_id = pid AND seller_id = sid)
THEN
    DELETE FROM Cart 
    WHERE customer_id = session_user::int 
    AND product_id = pid 
    AND seller_id = sid;
    RAISE NOTICE 'Item has been deleted from the cart successfully.';
ELSE
    RAISE NOTICE 'Not valid Product ID or Stock Id';
END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE update_to_cart(pid int,sid int,q int)
SECURITY DEFINER
LANGUAGE plpgsql
AS
$$
DECLARE
c int;
p int;
BEGIN
IF EXISTS (SELECT counts,price FROM cart WHERE product_id = pid AND seller_id = sid)
THEN
    SELECT stock,price INTO c,p 
    FROM sells 
    WHERE product_id = pid 
    AND seller_id = sid;
    IF q <= c THEN
        UPDATE Cart 
        SET counts = q 
        WHERE customer_id = session_user::int 
        AND product_id = pid 
        AND seller_id = sid;
        RAISE NOTICE 'Item has been updated in your cart.';
    ELSE
        RAISE NOTICE 'Quantity more than available stock';
    END IF;
ELSE
    RAISE NOTICE 'Not valid Product ID or Stock Id';
END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE make_payment(id int)
SECURITY DEFINER
LANGUAGE plpgsql
AS
$$
DECLARE
total int;
new_id int;
m text;
BEGIN
IF id IN (1,2,3,4) THEN
    SELECT SUM(counts * price) INTO total 
    FROM cart
    WHERE customer_id = session_user::int;
    RAISE NOTICE E'Order Total = %',total;
    SELECT payment_id INTO new_id 
    FROM payment 
    ORDER BY payment_id DESC 
    LIMIT 1;
    new_id = new_id + 1;

    SELECT
    CASE
        WHEN id = 1 THEN 'COD'
        WHEN id = 2 THEN 'UPI'
        WHEN id = 3 THEN 'Wallet'
        WHEN id = 4 THEN 'Card'
    END
    INTO m;
    INSERT INTO Payment(payment_id,mode) 
    VALUES (new_id,m,'Successful');
    RAISE NOTICE 'Payment done! Your payment ID: %', new_id;
    CALL place_order(new_id);
ELSE
    RAISE NOTICE 'Wrong Choice.';
END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE Cancel_order(id int)
SECURITY DEFINER
LANGUAGE plpgsql
AS
$$
DECLARE
s text;
BEGIN
IF EXISTS (SELECT order_id,customer_id FROM Orders WHERE order_id = id AND customer_id = session_user::int)
THEN
    SELECT status INTO s FROM Orders WHERE order_id = id;
    IF s NOT ILIKE '%Delivered%' OR s NOT ILIKE '%Cancelled%'
    THEN
        UPDATE Orders
        SET status = 'Cancelled'
        WHERE order_id = id;
        RAISE NOTICE 'Your Order has been cancelled successfully.';
    ELSE
        RAISE NOTICE 'Cannot cancel order as it is already %',s;
    END IF;
ELSE
    RAISE NOTICE 'Wrong Order ID.';
END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE add_new_product(pro text, id int, cost int, stk int)
SECURITY DEFINER
LANGUAGE plpgsql
AS
$$

DECLARE
new_id int;

BEGIN
IF id = session_user::int
THEN
    SELECT product_id INTO new_id 
    FROM Product 
    ORDER BY product_id DESC
    LIMIT 1;
    new_id = new_id + 1;
    INSERT INTO Product (product_id, pname) 
    VALUES (new_id, pro);
    INSERT INTO sells (product_id, seller_id, price, stock) 
    VALUES (new_id, id, cost, stk);
    RAISE NOTICE 'Product Added Successfully!';
ELSE
    RAISE NOTICE 'Enter your sellerID correctly';
END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE help_customer()
LANGUAGE plpgsql
AS $$
BEGIN
RAISE NOTICE 'view cart: select * from view_cart';
RAISE NOTICE 'view order: select * from view_orders';
RAISE NOTICE 'view customer details: select * from customer_details';
RAISE NOTICE 'view products: select * from customer_product_details;';
RAISE NOTICE 'view order details: select view_order_details(<order_id>)';
RAISE NOTICE E'call make payment(<mode>)\n         1.COD\n         2.UPI\n         3.Wallet\n         4.Card';
RAISE NOTICE 'call cancel order(<order_id>)';
RAISE NOTICE 'call delete from cart((<product_id>,<seller_id>))';
RAISE NOTICE 'call add_to_cart(<product_id>,<seller_id>,<quantity>);';
RAISE NOTICE 'call update_to_cart(<product_id>,<seller_id>,<quantity>)';
END;
$$;

CREATE OR REPLACE PROCEDURE help_seller()
LANGUAGE plpgsql
AS $$
BEGIN
RAISE NOTICE 'view products available: select * from product_price_avg';
RAISE NOTICE 'view products: select * from customer_product_details';
RAISE NOTICE 'view inventory: select * from sales_report;'
RAISE NOTICE 'add a new product: call add_new_product(<Product Name>,<seller_id>,<Product price>,<Product quantity>);';
END;
$$;