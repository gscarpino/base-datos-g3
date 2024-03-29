# -*- coding: utf-8 -*-

# interfaz_bd.py : Implementar las consultas.

import sqlite3
conn = sqlite3.connect('db.sqlite3')
statement = conn.cursor()
statement.execute(''' CREATE TABLE personas( DNI INT PRIMARY KEY,  nombre TEXT,  apellido TEXT, edad INT) ''');
statement.execute(''' CREATE TABLE salarios( ID INT ,salario INT,departamento TEXT, FOREIGN KEY(ID) REFERENCES personas(DNI)) ''');
statement.execute("INSERT INTO personas VALUES(2091811,'Martin','Celave',63)")
statement.execute("INSERT INTO personas VALUES(946861,'Martin','Gonzalez',24)")
statement.execute("INSERT INTO personas VALUES(1574416,'Martin','Scarpino',78)")
statement.execute("INSERT INTO personas VALUES(891997,'Martin','Dabah',20)")
statement.execute("INSERT INTO personas VALUES(3304472,'Martin','Croce',82)")
statement.execute("INSERT INTO personas VALUES(1699888,'Martin','Fernandez',43)")
statement.execute("INSERT INTO personas VALUES(1058491,'Martin','Molina',71)")
statement.execute("INSERT INTO personas VALUES(1579620,'Martin','Mendez',37)")
statement.execute("INSERT INTO personas VALUES(349399,'Martin','Mazuce',36)")
statement.execute("INSERT INTO personas VALUES(2187688,'Sergio','Celave',28)")
statement.execute("INSERT INTO personas VALUES(2070205,'Sergio','Gonzalez',31)")
statement.execute("INSERT INTO personas VALUES(1377940,'Sergio','Scarpino',75)")
statement.execute("INSERT INTO personas VALUES(2450727,'Sergio','Dabah',78)")
statement.execute("INSERT INTO personas VALUES(96934,'Sergio','Croce',31)")
statement.execute("INSERT INTO personas VALUES(731324,'Sergio','Fernandez',47)")
statement.execute("INSERT INTO personas VALUES(885268,'Sergio','Molina',66)")
statement.execute("INSERT INTO personas VALUES(477080,'Sergio','Mendez',42)")
statement.execute("INSERT INTO personas VALUES(1277482,'Sergio','Mazuce',20)")
statement.execute("INSERT INTO personas VALUES(600453,'Gino','Celave',31)")
statement.execute("INSERT INTO personas VALUES(850184,'Gino','Gonzalez',74)")
statement.execute("INSERT INTO personas VALUES(1929893,'Gino','Scarpino',28)")
statement.execute("INSERT INTO personas VALUES(1750045,'Gino','Dabah',46)")
statement.execute("INSERT INTO personas VALUES(556503,'Gino','Croce',65)")
statement.execute("INSERT INTO personas VALUES(1240370,'Gino','Fernandez',80)")
statement.execute("INSERT INTO personas VALUES(210312,'Gino','Molina',79)")
statement.execute("INSERT INTO personas VALUES(3136973,'Gino','Mendez',36)")
statement.execute("INSERT INTO personas VALUES(562295,'Gino','Mazuce',76)")
statement.execute("INSERT INTO personas VALUES(961105,'Julian','Celave',76)")
statement.execute("INSERT INTO personas VALUES(2617778,'Julian','Gonzalez',58)")
statement.execute("INSERT INTO personas VALUES(1219243,'Julian','Scarpino',56)")
statement.execute("INSERT INTO personas VALUES(261411,'Julian','Dabah',41)")
statement.execute("INSERT INTO personas VALUES(426540,'Julian','Croce',66)")
statement.execute("INSERT INTO personas VALUES(2533426,'Julian','Fernandez',50)")
statement.execute("INSERT INTO personas VALUES(322805,'Julian','Molina',46)")
statement.execute("INSERT INTO personas VALUES(2361418,'Julian','Mendez',58)")
statement.execute("INSERT INTO personas VALUES(2186889,'Julian','Mazuce',67)")
statement.execute("INSERT INTO personas VALUES(2241423,'Gabi','Celave',79)")
statement.execute("INSERT INTO personas VALUES(3237391,'Gabi','Gonzalez',40)")
statement.execute("INSERT INTO personas VALUES(1756604,'Gabi','Scarpino',22)")
statement.execute("INSERT INTO personas VALUES(1814642,'Gabi','Dabah',31)")
statement.execute("INSERT INTO personas VALUES(1841373,'Gabi','Croce',43)")
statement.execute("INSERT INTO personas VALUES(3370923,'Gabi','Fernandez',31)")
statement.execute("INSERT INTO personas VALUES(2343330,'Gabi','Molina',29)")
statement.execute("INSERT INTO personas VALUES(2252948,'Gabi','Mendez',21)")
statement.execute("INSERT INTO personas VALUES(2704906,'Gabi','Mazuce',29)")
statement.execute("INSERT INTO personas VALUES(2842640,'Javier','Celave',68)")
statement.execute("INSERT INTO personas VALUES(481145,'Javier','Gonzalez',50)")
statement.execute("INSERT INTO personas VALUES(1829272,'Javier','Scarpino',18)")
statement.execute("INSERT INTO personas VALUES(2929590,'Javier','Dabah',70)")
statement.execute("INSERT INTO personas VALUES(1218076,'Javier','Croce',42)")
statement.execute("INSERT INTO personas VALUES(3052765,'Javier','Fernandez',23)")
statement.execute("INSERT INTO personas VALUES(3137463,'Javier','Molina',34)")
statement.execute("INSERT INTO personas VALUES(3243273,'Javier','Mendez',59)")
statement.execute("INSERT INTO personas VALUES(589000,'Javier','Mazuce',43)")
statement.execute("INSERT INTO personas VALUES(1076068,'Pedro','Celave',54)")
statement.execute("INSERT INTO personas VALUES(2991359,'Pedro','Gonzalez',82)")
statement.execute("INSERT INTO personas VALUES(2811995,'Pedro','Scarpino',81)")
statement.execute("INSERT INTO personas VALUES(1701458,'Pedro','Dabah',57)")
statement.execute("INSERT INTO personas VALUES(821203,'Pedro','Croce',69)")
statement.execute("INSERT INTO personas VALUES(653045,'Pedro','Fernandez',52)")
statement.execute("INSERT INTO personas VALUES(1404592,'Pedro','Molina',30)")
statement.execute("INSERT INTO personas VALUES(2835034,'Pedro','Mendez',49)")
statement.execute("INSERT INTO personas VALUES(3385963,'Pedro','Mazuce',21)")
statement.execute("INSERT INTO personas VALUES(2538895,'Juan','Celave',66)")
statement.execute("INSERT INTO personas VALUES(1367104,'Juan','Gonzalez',29)")
statement.execute("INSERT INTO personas VALUES(2136458,'Juan','Scarpino',78)")
statement.execute("INSERT INTO personas VALUES(682524,'Juan','Dabah',30)")
statement.execute("INSERT INTO personas VALUES(2606526,'Juan','Croce',66)")
statement.execute("INSERT INTO personas VALUES(3860137,'Juan','Fernandez',52)")
statement.execute("INSERT INTO personas VALUES(1110683,'Juan','Molina',35)")
statement.execute("INSERT INTO personas VALUES(788691,'Juan','Mendez',72)")
statement.execute("INSERT INTO personas VALUES(2625782,'Juan','Mazuce',55)")
statement.execute("INSERT INTO personas VALUES(2812275,'Florencia','Celave',79)")
statement.execute("INSERT INTO personas VALUES(3972555,'Florencia','Gonzalez',33)")
statement.execute("INSERT INTO personas VALUES(616776,'Florencia','Scarpino',24)")
statement.execute("INSERT INTO personas VALUES(1536876,'Florencia','Dabah',82)")
statement.execute("INSERT INTO personas VALUES(1042691,'Florencia','Croce',80)")
statement.execute("INSERT INTO personas VALUES(562210,'Florencia','Fernandez',42)")
statement.execute("INSERT INTO personas VALUES(853216,'Florencia','Molina',21)")
statement.execute("INSERT INTO personas VALUES(98816,'Florencia','Mendez',48)")
statement.execute("INSERT INTO personas VALUES(2006073,'Florencia','Mazuce',82)")
statement.execute(" INSERT INTO salarios VALUES(2091811,6604,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(946861,21098,'it')")
statement.execute(" INSERT INTO salarios VALUES(1574416,11734,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(891997,5320,'it')")
statement.execute(" INSERT INTO salarios VALUES(3304472,21913,'it')")
statement.execute(" INSERT INTO salarios VALUES(1699888,3705,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(1058491,8550,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(1579620,11729,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(349399,14184,'it')")
statement.execute(" INSERT INTO salarios VALUES(2187688,12971,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2070205,2585,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(1377940,10532,'it')")
statement.execute(" INSERT INTO salarios VALUES(2450727,12690,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(96934,13206,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(731324,8601,'it')")
statement.execute(" INSERT INTO salarios VALUES(885268,19202,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(477080,14767,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1277482,21075,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(600453,15347,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(850184,19530,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1929893,19865,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1750045,20918,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(556503,13435,'it')")
statement.execute(" INSERT INTO salarios VALUES(1240370,3452,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(210312,19155,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(3136973,10580,'it')")
statement.execute(" INSERT INTO salarios VALUES(562295,2716,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(961105,6469,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(2617778,4837,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1219243,8127,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(261411,15812,'it')")
statement.execute(" INSERT INTO salarios VALUES(426540,11521,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2533426,8305,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(322805,14854,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(2361418,19434,'it')")
statement.execute(" INSERT INTO salarios VALUES(2186889,11221,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2241423,21280,'it')")
statement.execute(" INSERT INTO salarios VALUES(3237391,14969,'it')")
statement.execute(" INSERT INTO salarios VALUES(1756604,20129,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(1814642,21335,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1841373,19080,'it')")
statement.execute(" INSERT INTO salarios VALUES(3370923,17341,'it')")
statement.execute(" INSERT INTO salarios VALUES(2343330,6099,'it')")
statement.execute(" INSERT INTO salarios VALUES(2252948,3396,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2704906,10150,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2842640,9707,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(481145,21736,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(1829272,19351,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(2929590,21004,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1218076,20725,'it')")
statement.execute(" INSERT INTO salarios VALUES(3052765,16497,'it')")
statement.execute(" INSERT INTO salarios VALUES(3137463,6120,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(3243273,10706,'it')")
statement.execute(" INSERT INTO salarios VALUES(589000,10266,'it')")
statement.execute(" INSERT INTO salarios VALUES(1076068,14780,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2991359,2970,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2811995,14044,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1701458,13339,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(821203,18436,'it')")
statement.execute(" INSERT INTO salarios VALUES(653045,9584,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1404592,17537,'it')")
statement.execute(" INSERT INTO salarios VALUES(2835034,8030,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(3385963,18546,'it')")
statement.execute(" INSERT INTO salarios VALUES(2538895,17721,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(1367104,17398,'it')")
statement.execute(" INSERT INTO salarios VALUES(2136458,2857,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(682524,18116,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2606526,4359,'it')")
statement.execute(" INSERT INTO salarios VALUES(3860137,13619,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(1110683,3918,'it')")
statement.execute(" INSERT INTO salarios VALUES(788691,12330,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(2625782,19206,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(2812275,19303,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(3972555,7242,'it')")
statement.execute(" INSERT INTO salarios VALUES(616776,17994,'it')")
statement.execute(" INSERT INTO salarios VALUES(1536876,4475,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(1042691,9379,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(562210,6710,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(853216,8818,'ventas')")
statement.execute(" INSERT INTO salarios VALUES(98816,9812,'finanzas')")
statement.execute(" INSERT INTO salarios VALUES(2006073,17862,'finanzas')")



print "las tablas son"
for row in statement.execute('SELECT * FROM personas'):
    print row
print "los mayores  35 son"
for row in statement.execute('SELECT nombre ,apellido  FROM personas  WHERE edad > 35'):
	print row 
	
print "los Dni de quienes ganan mas de 7000"
for row in statement.execute('SELECT id  FROM salarios  WHERE salario> 7000'):
	print row 
	
	
print " actualizo el apellido de todas las Javiers"
statement.execute("UPDATE personas SET apellido = 'San Miguel' WHERE nombre='Javier' ")

print " las Javier San Miguel son "
for row in statement.execute("SELECT DNI,nombre,apellido  FROM personas  WHERE nombre='Javier' "):
	print row 

statement.execute("DELETE FROM personas WHERE edad <40 ")
for row in statement.execute('SELECT nombre ,apellido  FROM personas  WHERE edad <40'):
	print row 

conn.close()

