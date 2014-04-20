DROP DATABASE IF EXISTS TP;
CREATE DATABASE TP;
USE TP;

-- Tablas

DROP TABLE IF EXISTS Legislador;
CREATE TABLE Legislador(
	dni VARCHAR(8) NOT NULL,
	nombre VARCHAR(20),
	fecha_nacimiento DATE,
	id_bloque_politico INTEGER,
	provincia VARCHAR(20),
	PRIMARY KEY (dni)
);

DROP TABLE IF EXISTS Bloque_politico;
CREATE TABLE Bloque_politico(
	id_bloque_politico INTEGER NOT NULL,
	nombre VARCHAR(50),
	id_partido_politico INTEGER NOT NULL,
	PRIMARY KEY (id_bloque_politico)
);

DROP TABLE IF EXISTS Partido_politico;
CREATE TABLE Partido_politico(
	id_partido_politico INTEGER NOT NULL,
	nombre VARCHAR(50),
	PRIMARY KEY (id_partido_politico)
);

DROP TABLE IF EXISTS Provincia;
CREATE TABLE Provincia(
	Nombre VARCHAR(20) NOT NULL,
	Habitantes INTEGER,
	PRIMARY KEY (Nombre)
);

DROP TABLE IF EXISTS Bien_economico;
CREATE TABLE Bien_economico(
	id_bien_economico INTEGER NOT NULL,
	Valor INTEGER,
	PRIMARY KEY (id_bien_economico)
);

DROP TABLE IF EXISTS Periodo;
CREATE TABLE Periodo(
	fecha_inicio DATE,
	fecha_fin DATE,
	PRIMARY KEY (fecha_inicio, fecha_fin)
);

DROP TABLE IF EXISTS Sesion;
CREATE TABLE Sesion(
	fecha_inicio_sesion DATE NOT NULL,
	fecha_fin_sesion DATE NOT NULL,
	PRIMARY KEY (fecha_inicio_sesion,fecha_fin_sesion)
);

DROP TABLE IF EXISTS Comision;
CREATE TABLE Comision(
	nombre_comision VARCHAR(20) NOT NULL,
	PRIMARY KEY (nombre_comision)
);

DROP TABLE IF EXISTS Voto;
CREATE TABLE Voto(
	id_voto INTEGER NOT NULL,
	PRIMARY KEY (id_voto)
);

DROP TABLE IF EXISTS Proyecto_de_ley;
CREATE TABLE Proyecto_de_ley(
	titulo_proyecto_ley VARCHAR(20) NOT NULL,
	fecha DATE,
	PRIMARY KEY (titulo_proyecto_ley)
);

DROP TABLE IF EXISTS Ley;
CREATE TABLE Ley(
	numeracion INTEGER NOT NULL,
	titulo_ley VARCHAR(20) NOT NULL,
	fecha_sancionada DATE,
	titulo_proyecto_ley VARCHAR(20) NOT NULL,
	PRIMARY KEY (numeracion,titulo_ley)
);

DROP TABLE IF EXISTS Control_de_calidad;
CREATE TABLE Control_de_calidad(
	id_control_calidad INTEGER NOT NULL,
	empleado VARCHAR(20),
	titulo_proyecto_ley VARCHAR(20) NOT NULL,
	PRIMARY KEY (id_control_calidad)
);

DROP TABLE IF EXISTS Vicepresidente;
CREATE TABLE Vicepresidente(
	nombre_vicepresidente VARCHAR(20) NOT NULL,
	PRIMARY KEY (nombre_vicepresidente)
);







-- Tablas de relaciones N:M

DROP TABLE IF EXISTS Bienes_de_legislador;
CREATE TABLE Bienes_de_legislador(
	dni_legislador VARCHAR(8) NOT NULL,
	id_bien_economico INTEGER NOT NULL,
	fecha_obtencion DATE NOT NULL,
	fecha_sucesion DATE,
	PRIMARY KEY (dni_legislador, id_bien_economico, fecha_obtencion)
);

DROP TABLE IF EXISTS Periodos_del_legislador;
CREATE TABLE Periodos_del_legislador(
	dni_legislador VARCHAR(8) NOT NULL,
	fecha_inicio DATE NOT NULL, 
	fecha_fin DATE NOT NULL,
	PRIMARY KEY (dni_legislador, fecha_inicio, fecha_fin)
);

DROP TABLE IF EXISTS Asiste_sesion;
CREATE TABLE Asiste_sesion(
	dni_legislador VARCHAR(8) NOT NULL,  -- debo poner la fk
	fecha_inicio_sesion DATE NOT NULL, 
	fecha_fin_sesion DATE NOT NULL,
	PRIMARY KEY (dni_legislador, fecha_inicio_sesion, fecha_fin_sesion)
);

DROP TABLE IF EXISTS Participa_en_comision;
CREATE TABLE Participa_en_comision(
	dni_legislador VARCHAR(8) NOT NULL, 
	fecha_inicio_participacion DATE NOT NULL, 
	fecha_fin_participacion DATE NOT NULL,
	nombre_comision VARCHAR(20) NOT NULL, 
	PRIMARY KEY (dni_legislador, fecha_inicio_participacion, fecha_fin_participacion)
);

DROP TABLE IF EXISTS Estudia;
CREATE TABLE Estudia(
	nombre_comision VARCHAR(20) NOT NULL, 
	titulo_proyecto_ley VARCHAR(20) NOT NULL,
	PRIMARY KEY (nombre_comision, titulo_proyecto_ley)
);




-- Foreign keys

ALTER TABLE Legislador 
	ADD CONSTRAINT `fk_bloque_politico`
	FOREIGN KEY (id_bloque_politico)
		REFERENCES Bloque_politico (id_bloque_politico);

ALTER TABLE Legislador
	ADD CONSTRAINT `fk_provincia`
	FOREIGN KEY (provincia)
		REFERENCES Provincia (nombre);

ALTER TABLE Bloque_politico 
	ADD CONSTRAINT `fk_partido_politico`
	FOREIGN KEY (id_partido_politico)
		REFERENCES Partido_politico (id_partido_politico);

ALTER TABLE Ley 
	ADD CONSTRAINT `fk_proyecto_ley`
	FOREIGN KEY (titulo_proyecto_ley)
		REFERENCES Proyecto_de_ley (titulo_proyecto_ley);

ALTER TABLE Control_de_calidad
	ADD CONSTRAINT `fk_proyecto_paraControl_ley`
	FOREIGN KEY (titulo_proyecto_ley)
		REFERENCES Proyecto_de_ley (titulo_proyecto_ley);

ALTER TABLE Bienes_de_legislador
	ADD CONSTRAINT `fk_legislador_bien`
	FOREIGN KEY (dni_legislador)
		REFERENCES Legislador (dni),

	ADD CONSTRAINT `fk_bien_economico`
	FOREIGN KEY (id_bien_economico)
		REFERENCES Bien_economico (id_bien_economico);

ALTER TABLE Periodos_del_legislador
	ADD CONSTRAINT `fk_legislador_periodo`
	FOREIGN KEY (dni_legislador)
		REFERENCES Legislador (dni),

	ADD CONSTRAINT `fk_periodo`
	FOREIGN KEY (fecha_inicio, fecha_fin)
		REFERENCES Periodo (fecha_inicio, fecha_fin);

ALTER TABLE Asiste_sesion 
	ADD CONSTRAINT `fk_asiste_legislador`
	FOREIGN KEY (dni_legislador)
		REFERENCES Legislador (dni),
	
	ADD CONSTRAINT `fk_sesion_legislador`
	FOREIGN KEY (fecha_inicio_sesion,fecha_fin_sesion )
		REFERENCES Sesion (fecha_inicio_sesion,fecha_fin_sesion);

ALTER TABLE	Participa_en_comision
	ADD CONSTRAINT `fk_participa_legislador`
	FOREIGN KEY (dni_legislador)
		REFERENCES Legislador (dni),
	
	ADD CONSTRAINT `fk_participa_comision`
	FOREIGN KEY (nombre_comision)
		REFERENCES Comision (nombre_comision);

ALTER TABLE	Estudia
	ADD CONSTRAINT `fk_estudia_comision`
	FOREIGN KEY (nombre_comision)
		REFERENCES Comision(nombre_comision),
	
	ADD CONSTRAINT `fk_estudia_proyecto`
	FOREIGN KEY (titulo_proyecto_ley)
		REFERENCES Proyecto_de_ley (titulo_proyecto_ley);



-- Check constraints

