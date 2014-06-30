

-- Diputados que solo votaron positivo o ausente en los proyectos de ley de la comisión que integran
select distinct leg.nombre, leg.dni
from estudia est, proyecto_de_ley pro, participa_en_comision part, legislador leg
where est.titulo_proyecto_ley = pro.titulo_proyecto_ley and est.nombre_comision = part.nombre_comision
	and part.fecha_inicio_participacion <= pro.fecha and part.fecha_fin_participacion >= pro.fecha
	and part.dni_legislador = leg.dni and not exists
		(select vot.dni from votan vot where pro.titulo_proyecto_ley = vot.titulo_proyecto_ley and vot.dni = leg.dni
			and vot.id_voto in (10,11,20,21));
															 
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