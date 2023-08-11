-- database

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE weighted_avg DECIMAL(10, 2);

    -- Calculate the weighted average score
    SELECT SUM(score * weight) / SUM(weight) INTO weighted_avg
    FROM corrections
    WHERE user_id = user_id;
    
    -- Update user's weighted average score
    UPDATE users
    SET weighted_average_score = weighted_avg
    WHERE id = user_id;
END;
//
DELIMITER ;
