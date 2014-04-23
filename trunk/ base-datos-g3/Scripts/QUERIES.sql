

-- Diputados que solo votaron positivo o ausente en los proyectos de ley de la comisión que integran
-- dni de diputados que votaron positivo en todos los proyectos de ley de las comisiones que integra.
SELECT votos.dni 
	FROM Votan votos
	WHERE 
		(SELECT e.titulo_proyecto_ley
			FROM Estudia e
			WHERE votos.titulo_proyecto_ley = e.titulo_proyecto_ley AND votos.dni IN (SELECT pec.dni_legislador
																						FROM Participa_en_comision pec 
																						WHERE pec.nombre_comision= e.nombre_comision
																						AND votos.id_voto IN (SELECT v.id_voto
																												FROM  Voto v
																												WHERE tipo LIKE 'P%')));
-- dni de diputados que estuvieron ausentes en todos los proyectos de ley de las comisiones que integra.	
--diputados tal que no existe un proyecto de ley ni comision en la que participe el diputado y haya sido estudiada por el proyecto de ley.
SELECT leg.dni
FROM Legislador leg
WHERE NOT EXISTS (SELECT e.titulo_proyecto_ley
				FROM Estudia e
				WHERE e.nombre_comision IN (SELECT pec.nombre_comision
												FROM Participa_en_comision pec 
												WHERE pec.dni_legislador= leg.dni));
															 

															
CREATE TABLE Participa_en_comision(
	dni_legislador VARCHAR(8) NOT NULL, 
	fecha_inicio_participacion DATE NOT NULL, 
	fecha_fin_participacion DATE NOT NULL,
	nombre_comision VARCHAR(30) NOT NULL, 
	PRIMARY KEY (dni_legislador, fecha_inicio_participacion, fecha_fin_participacion)

				
				CREATE TABLE Estudia(
	nombre_comision VARCHAR(30) NOT NULL, 
	titulo_proyecto_ley VARCHAR(50) NOT NULL,
	PRIMARY KEY (nombre_comision, titulo_proyecto_ley)
);



dni VARCHAR(8) NOT NULL,
	nombre VARCHAR(80),
	fecha_nacimiento DATE,
	id_bloque_politico INTEGER,
	provincia VARCHAR(40),
	tipo CHAR(1),
	PRIMARY KEY (dni)
);
	
	
	
	
-- Cantidad de leyes promulgadas en cada sesión en los últimos tres años
	-- | sesión | cantidad de leyes promulgadas|

	SELECT fecha_sancionada, COUNT(fecha_sancionada) 
	    FROM Ley 
	   WHERE (YEAR(DATE_SUB(CURRENT_DATE(), fecha_sancionada))) < 3 
	GROUP BY fecha_sancionada;

-- Diez legisladores con más incremento porcentual desde que se iniciaron en el cargo

	SELECT dni_legislador, suma_total/suma_antes_cargo as Incremento
	  FROM
		( SELECT l.dni_legislador, SUM(b.valor) AS suma_total
			FROM Bienes_de_legislador l, Bien_economico b
		   WHERE l.id_bien_economico = b.id_bien_economico
			 AND fecha_sucesion IS NULL	-- descarto los que ya no tiene mas
		GROUP BY l.dni_legislador) s1
		NATURAL JOIN
		 (SELECT l.dni_legislador, SUM(b.valor) AS suma_antes_cargo
			FROM Bienes_de_legislador l, Bien_economico b
		   WHERE l.id_bien_economico = b.id_bien_economico
			 AND fecha_sucesion IS NULL	-- descarto los que ya no tiene mas
			 AND fecha_obtencion < (SELECT MAX(fecha_inicio)
									 FROM Periodos_del_legislador
									WHERE dni_legislador = l.dni_legislador)
		GROUP BY l.dni_legislador) s2
	ORDER BY suma_total/suma_antes_cargo
	LIMIT 10;