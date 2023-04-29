CREATE TRIGGER failed_payment
AFTER UPDATE OR INSERT ON PAYMENT
FOR EACH ROW
EXECUTE PROCEDURE procedure_failed_payment();


-- CREATE TRIGGER failed_payment
-- AFTER UPDATE OR INSERT ON payment
-- FOR EACH ROW
-- WHEN (NEW.status ILIKE 'Failed')
-- DECLARE
--   order_id INTEGER;
-- BEGIN
-- order_id := NEW.order_id;
-- EXECUTE FUNCTION failed_payment_procedure(order_id)
-- END;
