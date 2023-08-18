DELIMITER $$
CREATE TRIGGER maximo_departamentos
BEFORE INSERT ON funcionario
FOR EACH ROW
BEGIN
    DECLARE num_funcionarios INT;
    SELECT COUNT(*) INTO num_funcionarios
    FROM funcionario
    WHERE Dnr = NEW.Dnr
    GROUP BY Dnr;
    
    IF num_funcionarios >= 4 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Limite de 4 funcionários por departamento atingido.';
    END IF;
END;
$$