-- database

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_cursor CURSOR FOR
        SELECT id
        FROM users;
    
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    
    -- Declare variables for weighted average calculation
    DECLARE total_weight DECIMAL(10, 2);
    DECLARE weighted_sum DECIMAL(10, 2);
    
    -- Declare variables for temporary cursor row storage
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Open the user cursor
    OPEN user_cursor;
    
    -- Loop through users
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Initialize variables for each user
        SET total_weight = 0;
        SET weighted_sum = 0;

        -- Calculate weighted average score for the user
        INSERT INTO user_weighted_scores (user_id, weighted_average_score)
        SELECT user_id,
               SUM(score * weight) / SUM(weight)
        FROM corrections
        WHERE user_id = user_id;

    END LOOP;

    -- Close the user cursor
    CLOSE user_cursor;
    
END;
//
DELIMITER ;
