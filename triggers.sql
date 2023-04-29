CREATE TRIGGER failed_payment
AFTER UPDATE OR INSERT ON PAYMENT
FOR ROW
WHEN (NEW.status ilike 'Failed')
EXECUTE failed_payment_procedure(new.order_id);