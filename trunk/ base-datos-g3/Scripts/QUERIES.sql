-- Diputados que solo votaron positivo o ausente en los proyectos de ley de la comisión que integran
	
-- Cantidad de leyes promulgadas en cada sesión en los últimos tres años
	-- | sesión | cantidad de leyes promulgadas|
	SELECT fecha_sancionada, COUNT(fecha_sancionada) FROM Ley WHERE (YEAR(DATE_SUB(CURRENT_DATE(), fecha_sancionada))) < 3 GROUP BY fecha_sancionada;

-- Diez legisladores con más incremento porcentual desde que se iniciaron en el cargo

