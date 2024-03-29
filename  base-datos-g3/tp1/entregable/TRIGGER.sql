-- Cuando se produce un update en la tabla Proyecto_de_ley que cierra las votaciones del proyecto, se dispara el trigger
-- el cual verifica que los votos positivos sean mayores a los negativos, y si esto pasa, convierte el proyecto en ley.

DELIMITER $$
CREATE TRIGGER convertir_proyecto_en_ley AFTER UPDATE ON Proyecto_de_ley
	FOR EACH ROW 
	BEGIN
		DECLARE votos_positivos INT;
		DECLARE votos_negativos INT;
		DECLARE fechaSancionada DATE;
		IF OLD.estado_votaciones in ('M') and NEW.estado_votaciones = 'F'
		THEN
			SET votos_positivos = ( SELECT count(1) 
									  FROM Votan v
									 WHERE v.titulo_proyecto_ley = NEW.titulo_proyecto_ley
									   AND (v.id_voto = 0 OR v.id_voto = 1));
			SET votos_negativos = ( SELECT count(1) 
									  FROM Votan v
									 WHERE v.titulo_proyecto_ley = NEW.titulo_proyecto_ley
									   AND (v.id_voto = 10 OR v.id_voto = 11));
			IF votos_positivos > votos_negativos
			THEN
				SET fechaSancionada = (SELECT max(v.fecha) FROM Votan v WHERE v.titulo_proyecto_ley = NEW.titulo_proyecto_ley);
				INSERT INTO Ley(titulo_ley, fecha_sancionada, titulo_proyecto_ley)
				VALUES (NEW.titulo_proyecto_ley, fechaSancionada, NEW.titulo_proyecto_ley);
			END IF;
		END IF;
	END$$
DELIMITER ;