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

-- Tablas de relaciones N:M

DROP TABLE IF EXISTS Bienes_de_legislador;
CREATE TABLE Bienes_de_legislador(
	dni_legislador VARCHAR(8) NOT NULL,
	id_bien_economico INTEGER NOT NULL,
	fecha_obtencion DATE NOT NULL,
	fecha_sucesion DATE,
	PRIMARY KEY (dni_legislador, id_bien_economico, fecha_obtencion)
);

DROP TABLE IF EXISTS Peridos_del_legislador;
CREATE TABLE Peridos_del_legislador(
	dni_legislador VARCHAR(8) NOT NULL,
	fecha_inicio DATE NOT NULL, 
	fecha_fin DATE NOT NULL,
	PRIMARY KEY (dni_legislador, fecha_inicio, fecha_fin)
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

ALTER TABLE Bienes_de_legislador
	ADD CONSTRAINT `fk_legislador_bien`
	FOREIGN KEY (dni_legislador)
		REFERENCES Legislador (dni),

	ADD CONSTRAINT `fk_bien_economico`
	FOREIGN KEY (id_bien_economico)
		REFERENCES Bien_economico (id_bien_economico);

ALTER TABLE Peridos_del_legislador
	ADD CONSTRAINT `fk_legislador_periodo`
	FOREIGN KEY (dni_legislador)
		REFERENCES Legislador (dni),

	ADD CONSTRAINT `fk_periodo`
	FOREIGN KEY (fecha_inicio, fecha_fin)
		REFERENCES Periodo (fecha_inicio, fecha_fin);

-- Check constraints

