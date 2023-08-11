-- database

DELIMITER //
CREATE TRIGGER after_insert_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.quantity
    WHERE id = NEW.item_id;
END;
//
DELIMITER ;
