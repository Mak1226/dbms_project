CREATE TRIGGER failed_payment
AFTER UPDATE OR INSERT ON payment
FOR EACH ROW
EXECUTE PROCEDURE procedure_failed_payment();

CREATE TRIGGER add_new_user
AFTER INSERT ON customer
FOR EACH ROW
EXECUTE FUNCION role_creation();

CREATE TRIGGER update_product_total_stock_trigger
AFTER UPDATE OR INSERT ON sells
FOR EACH ROW
EXECUTE FUNCTION get_stock();

CREATE TRIGGER check_stock_trigger
BEFORE INSERT ON Cart
FOR EACH ROW
EXECUTE FUNCTION check_stock();

CREATE TRIGGER cancel_order
AFTER UPDATE ON Orders
FOR EACH ROW
EXECUTE FUNCTION procedure_cancelled_order()