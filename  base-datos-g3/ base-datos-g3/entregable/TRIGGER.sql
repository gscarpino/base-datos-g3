-- Cuando se produce un update en la tabla Proyecto_de_ley que cierra las votaciones del proyecto, se dispara el trigger
-- el cual verifica que los votos positivos sean mayores a los negativos, y si esto pasa, convierte el proyecto en ley.

DELIMITER $$
CREATE TRIGGER convertir_proyecto_en_ley AFTER UPDATE ON Proyecto_de_ley
	FOR EACH ROW 
	BEGIN
		DECLARE votos_positivos INT;
		DECLARE votos_negativos INT;
		IF OLD.estado_votaciones = 'A' and NEW.estado_votaciones = 'C'
		THEN
			SET votos_positivos = ( SELECT count(1) 
									  FROM Votan v
									 WHERE v.titulo_proyecto_ley = NEW.titulo_proyecto_ley
									   AND v.resultado = 'P');
			SET votos_negativos = ( SELECT count(1) 
									  FROM Votan v
									 WHERE v.titulo_proyecto_ley = NEW.titulo_proyecto_ley
									   AND v.resultado = 'N');
			
			IF votos_positivos > votos_negativos
			THEN
				INSERT INTO Ley(titulo_ley, fecha_sancionada, titulo_proyecto_ley)
				VALUES (NEW.titulo_proyecto_ley, CURRENT_DATE(), NEW.titulo_proyecto_ley);
			END IF;
		END IF;
	END$$
DELIMITER ;