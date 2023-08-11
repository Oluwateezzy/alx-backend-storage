DELIMITER //
CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE project_id INT;
    
    -- Check if the project exists, and create it if not
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;
    
    -- Add a new correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
    
    -- Update user's total score
    UPDATE users
    SET total_score = total_score + score
    WHERE id = user_id;
END;
//
DELIMITER ;
