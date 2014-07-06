

-- Diputados que solo votaron positivo o ausente en los proyectos de ley de la comisión que integran
select distinct leg.nombre, leg.dni
from estudia est, proyecto_de_ley pro, participa_en_comision part, legislador leg, ley l
where (est.titulo_proyecto_ley = pro.titulo_proyecto_ley or est.titulo_proyecto_ley = l.titulo_proyecto_ley) and est.id_comision = part.id_comision
	and part.fecha_inicio_participacion <= pro.fecha and part.fecha_fin_participacion >= pro.fecha
	and part.dni_legislador = leg.dni and pro.estado_votaciones = 'C' and not exists
		(select vot.dni from votan vot where pro.titulo_proyecto_ley = vot.titulo_proyecto_ley and vot.dni = leg.dni
			and vot.id_voto in (10,11,20,21))
group by leg.dni
order by leg.nombre;
			
-- Cantidad de leyes promulgadas en cada sesión en los últimos tres años
	-- | sesión | cantidad de leyes promulgadas|

select ses.fecha_inicio_sesion, ses.fecha_fin_sesion, count(*) as cantidad
from sesion ses, ley
where ses.fecha_inicio_sesion <= ley.fecha_sancionada and ley.fecha_sancionada <= ses.fecha_fin_sesion 
	and ((DATEDIFF(CURRENT_DATE(), ses.fecha_fin_sesion)) / 365) < 3
group by ses.fecha_inicio_sesion;

-- Diez legisladores con más incremento porcentual desde que se iniciaron en el cargo

select s1.dni, s1.sumaNuevo/s2.sumaTotal * 100 as porcentaje, s1.sumaNuevo, s2.sumaTotal
from 
	(select leg.dni, sum(bien.valor) as sumaNuevo
	from bien_economico bien, Es_propietario_de bLeg, legislador leg
	where bien.id_bien_economico = bLeg.id_bien_economico and bLeg.dni_legislador = leg.dni
		and bLeg.fecha_obtencion >= (select max(per.fecha_inicio) from Legisla_durante per where leg.dni = per.dni_legislador)
		and bLeg.fecha_sucesion is NULL
	group by leg.dni) s1 
natural join
	(select leg.dni, sum(bien.valor) as sumaTotal
	from bien_economico bien, Es_propietario_de bLeg, legislador leg
	where bien.id_bien_economico = bLeg.id_bien_economico and bLeg.dni_legislador = leg.dni
		and bLeg.fecha_obtencion < (select max(per.fecha_inicio) from Legisla_durante per where leg.dni = per.dni_legislador)
		and (bLeg.fecha_sucesion is NULL or (bLeg.fecha_sucesion is not NULL and bLeg.fecha_sucesion > (select max(per.fecha_inicio) from Legisla_durante per where leg.dni = per.dni_legislador)))
	group by leg.dni) s2
group by s1.dni
order by porcentaje desc
limit 10;