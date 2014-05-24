# -*- coding: utf-8 -*-

# interfaz_bd.py : Implementar las consultas.

import sqlite3
#conn = sqlite3.connect('C:\\Users\\kotomi\\Desktop\\tp2-bundle.v1\\entregable\\tp2-bundle.v1\\src\\db.sqlite3')
conn = sqlite3.connect('C:\\Users\\kotomi\\Desktop\\tp2-bundle.v1\\entregable\\tp2-bundle.v1\\src\\midatabase')
statement = conn.cursor()
statement.execute("DROP TABLE personas");
statement.execute(''' CREATE TABLE personas( DNI INT PRIMARY KEY,  nombre TEXT,  apellido TEXT, edad INT) ''');
statement.execute(" INSERT INTO personas VALUES (3544824, 'Martin', 'Celave', 72) " )
statement.execute(" INSERT INTO personas VALUES (3998468, 'Martin', 'Gonzalez', 38) " )
statement.execute(" INSERT INTO personas VALUES (2952671, 'Martin', 'Scarpino', 19) " )
statement.execute(" INSERT INTO personas VALUES (3560812, 'Martin', 'Dabah', 40) " )
statement.execute(" INSERT INTO personas VALUES (1523350, 'Martin', 'Croce', 29) " )
statement.execute(" INSERT INTO personas VALUES (3130939, 'Martin', 'Fernandez', 35) " )
statement.execute(" INSERT INTO personas VALUES (2932280, 'Martin', 'Molina', 37) " )
statement.execute(" INSERT INTO personas VALUES (578295, 'Martin', 'Mendez', 26) " )
statement.execute(" INSERT INTO personas VALUES (1546747, 'Martin', 'Mazuce', 23) " )
statement.execute(" INSERT INTO personas VALUES (1354302, 'Sergio', 'Celave', 68) " )
statement.execute(" INSERT INTO personas VALUES (3457541, 'Sergio', 'Gonzalez', 74) " )
statement.execute(" INSERT INTO personas VALUES (3334456, 'Sergio', 'Scarpino', 56) " )
statement.execute(" INSERT INTO personas VALUES (290000, 'Sergio', 'Dabah', 20) " )
statement.execute(" INSERT INTO personas VALUES (1472143, 'Sergio', 'Croce', 71) " )
statement.execute(" INSERT INTO personas VALUES (3610040, 'Sergio', 'Fernandez', 60) " )
statement.execute(" INSERT INTO personas VALUES (3347285, 'Sergio', 'Molina', 51) " )
statement.execute(" INSERT INTO personas VALUES (2057112, 'Sergio', 'Mendez', 82) " )
statement.execute(" INSERT INTO personas VALUES (1071877, 'Sergio', 'Mazuce', 35) " )
statement.execute(" INSERT INTO personas VALUES (2777457, 'Gino', 'Celave', 27) " )
statement.execute(" INSERT INTO personas VALUES (2518324, 'Gino', 'Gonzalez', 71) " )
statement.execute(" INSERT INTO personas VALUES (3297430, 'Gino', 'Scarpino', 37) " )
statement.execute(" INSERT INTO personas VALUES (1465463, 'Gino', 'Dabah', 51) " )
statement.execute(" INSERT INTO personas VALUES (1668066, 'Gino', 'Croce', 34) " )
statement.execute(" INSERT INTO personas VALUES (2010995, 'Gino', 'Fernandez', 67) " )
statement.execute(" INSERT INTO personas VALUES (3528475, 'Gino', 'Molina', 23) " )
statement.execute(" INSERT INTO personas VALUES (3478008, 'Gino', 'Mendez', 64) " )
statement.execute(" INSERT INTO personas VALUES (677047, 'Gino', 'Mazuce', 75) " )
statement.execute(" INSERT INTO personas VALUES (2047145, 'Julian', 'Celave', 41) " )
statement.execute(" INSERT INTO personas VALUES (805882, 'Julian', 'Gonzalez', 22) " )
statement.execute(" INSERT INTO personas VALUES (2474903, 'Julian', 'Scarpino', 53) " )
statement.execute(" INSERT INTO personas VALUES (2245218, 'Julian', 'Dabah', 48) " )
statement.execute(" INSERT INTO personas VALUES (1512426, 'Julian', 'Croce', 48) " )
statement.execute(" INSERT INTO personas VALUES (2881092, 'Julian', 'Fernandez', 46) " )
statement.execute(" INSERT INTO personas VALUES (18105, 'Julian', 'Molina', 36) " )
statement.execute(" INSERT INTO personas VALUES (850831, 'Julian', 'Mendez', 79) " )
statement.execute(" INSERT INTO personas VALUES (3261139, 'Julian', 'Mazuce', 28) " )
statement.execute(" INSERT INTO personas VALUES (2187403, 'Gabi', 'Celave', 32) " )
statement.execute(" INSERT INTO personas VALUES (2542199, 'Gabi', 'Gonzalez', 59) " )
statement.execute(" INSERT INTO personas VALUES (1275049, 'Gabi', 'Scarpino', 27) " )
statement.execute(" INSERT INTO personas VALUES (11164, 'Gabi', 'Dabah', 32) " )
statement.execute(" INSERT INTO personas VALUES (3795030, 'Gabi', 'Croce', 44) " )
statement.execute(" INSERT INTO personas VALUES (2440859, 'Gabi', 'Fernandez', 64) " )
statement.execute(" INSERT INTO personas VALUES (2781731, 'Gabi', 'Molina', 60) " )
statement.execute(" INSERT INTO personas VALUES (719610, 'Gabi', 'Mendez', 76) " )
statement.execute(" INSERT INTO personas VALUES (475767, 'Gabi', 'Mazuce', 66) " )
statement.execute(" INSERT INTO personas VALUES (1954331, 'Foca', 'Celave', 77) " )
statement.execute(" INSERT INTO personas VALUES (3852141, 'Foca', 'Gonzalez', 28) " )
statement.execute(" INSERT INTO personas VALUES (2329790, 'Foca', 'Scarpino', 42) " )
statement.execute(" INSERT INTO personas VALUES (2017909, 'Foca', 'Dabah', 70) " )
statement.execute(" INSERT INTO personas VALUES (1248568, 'Foca', 'Croce', 71) " )
statement.execute(" INSERT INTO personas VALUES (3115225, 'Foca', 'Fernandez', 44) " )
statement.execute(" INSERT INTO personas VALUES (780173, 'Foca', 'Molina', 44) " )
statement.execute(" INSERT INTO personas VALUES (2932030, 'Foca', 'Mendez', 19) " )
statement.execute(" INSERT INTO personas VALUES (1076645, 'Foca', 'Mazuce', 31) " )
statement.execute(" INSERT INTO personas VALUES (1114060, 'Pedro', 'Celave', 18) " )
statement.execute(" INSERT INTO personas VALUES (165914, 'Pedro', 'Gonzalez', 34) " )
statement.execute(" INSERT INTO personas VALUES (1688264, 'Pedro', 'Scarpino', 45) " )
statement.execute(" INSERT INTO personas VALUES (3413069, 'Pedro', 'Dabah', 67) " )
statement.execute(" INSERT INTO personas VALUES (549114, 'Pedro', 'Croce', 50) " )
statement.execute(" INSERT INTO personas VALUES (3943603, 'Pedro', 'Fernandez', 72) " )
statement.execute(" INSERT INTO personas VALUES (1625702, 'Pedro', 'Molina', 57) " )
statement.execute(" INSERT INTO personas VALUES (2451615, 'Pedro', 'Mendez', 40) " )
statement.execute(" INSERT INTO personas VALUES (3638938, 'Pedro', 'Mazuce', 81) " )
statement.execute(" INSERT INTO personas VALUES (1069844, 'Juan', 'Celave', 52) " )
statement.execute(" INSERT INTO personas VALUES (674534, 'Juan', 'Gonzalez', 23) " )
statement.execute(" INSERT INTO personas VALUES (3357315, 'Juan', 'Scarpino', 50) " )
statement.execute(" INSERT INTO personas VALUES (2238916, 'Juan', 'Dabah', 59) " )
statement.execute(" INSERT INTO personas VALUES (964307, 'Juan', 'Croce', 41) " )
statement.execute(" INSERT INTO personas VALUES (2031557, 'Juan', 'Fernandez', 70) " )
statement.execute(" INSERT INTO personas VALUES (3163219, 'Juan', 'Molina', 79) " )
statement.execute(" INSERT INTO personas VALUES (1358687, 'Juan', 'Mendez', 37) " )
statement.execute(" INSERT INTO personas VALUES (187861, 'Juan', 'Mazuce', 33) " )
statement.execute(" INSERT INTO personas VALUES (2929681, 'Florencia', 'Celave', 77) " )
statement.execute(" INSERT INTO personas VALUES (1202561, 'Florencia', 'Gonzalez', 82) " )
statement.execute(" INSERT INTO personas VALUES (1718890, 'Florencia', 'Scarpino', 74) " )
statement.execute(" INSERT INTO personas VALUES (726423, 'Florencia', 'Dabah', 56) " )
statement.execute(" INSERT INTO personas VALUES (3642052, 'Florencia', 'Croce', 62) " )
statement.execute(" INSERT INTO personas VALUES (3466945, 'Florencia', 'Fernandez', 28) " )
statement.execute(" INSERT INTO personas VALUES (3987825, 'Florencia', 'Molina', 77) " )
statement.execute(" INSERT INTO personas VALUES (771140, 'Florencia', 'Mendez', 65) " )
statement.execute(" INSERT INTO personas VALUES (3861421, 'Florencia', 'Mazuce', 37) " )

print "las tablas son"
for row in statement.execute('SELECT * FROM personas'):
        print row
print "los mayores  35 son"
for row in statement.execute('SELECT nombre ,apellido  FROM personas  WHERE edad > 35'):
	print row 

print " actualizo el apellido de todas las focas(personas llamadas Foca) "
statement.execute("UPDATE personas SET apellido = 'Bebe' WHERE nombre='Foca' ")
#lista todas las focas bebe en la base de datos
print " las focas bebe son "
for row in statement.execute("SELECT DNI,nombre,apellido  FROM personas  WHERE nombre='Foca' "):
	print row 

statement.execute("DELETE FROM personas WHERE edad <40 ")

for row in statement.execute('SELECT nombre ,apellido  FROM personas  WHERE edad <40'):
	print row 

conn.close()

