CREATE TRIGGER failed_payment
AFTER UPDATE OR INSERT ON payment
FOR EACH ROW
EXECUTE PROCEDURE procedure_failed_payment();

-- UPDATE Payment set status = 'Failed' where payment_id = 411;


CREATE TRIGGER add_new_user
AFTER INSERT ON customer
FOR EACH ROW
EXECUTE FUNCTION role_creation();

-- INSERT INTO Customer VALUES (126, 'ram', 'abcnjd@gmail.com', 1232321, 'ram126' ,'06-04-2022');

CREATE TRIGGER update_product_total_stock_trigger
AFTER UPDATE OR INSERT ON sells
FOR EACH ROW
EXECUTE FUNCTION get_stock();

-- update sells 
-- set stock = stock+10 where product_id = 210 and seller_id = 518;

CREATE TRIGGER check_stock_trigger
BEFORE INSERT ON Cart
FOR EACH ROW
EXECUTE FUNCTION check_stock();


CREATE TRIGGER cancel_order
AFTER UPDATE ON Orders
FOR EACH ROW
EXECUTE FUNCTION procedure_cancelled_order()
