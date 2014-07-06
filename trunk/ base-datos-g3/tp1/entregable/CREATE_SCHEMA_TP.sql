DROP DATABASE IF EXISTS TP;
CREATE DATABASE TP;
USE TP;

-- Tablas

CREATE TABLE Legislador(
	dni VARCHAR(8) NOT NULL,
	nombre VARCHAR(80),
	fecha_nacimiento DATE,
	id_bloque_politico INTEGER,
	nombre_provincia VARCHAR(40),
	tipo CHAR(1),
	PRIMARY KEY (dni)
);

CREATE TABLE Camara(
	id_camara INTEGER,
	tipo CHAR(1),
	dni_presidente VARCHAR(8) NOT NULL,
	PRIMARY KEY (id_camara)
);

CREATE TABLE Bloque_politico(
	id_bloque_politico INTEGER NOT NULL,
	nombre VARCHAR(60),
	id_partido_politico INTEGER NOT NULL,
	PRIMARY KEY (id_bloque_politico)
);

CREATE TABLE Partido_politico(
	id_partido_politico INTEGER NOT NULL,
	nombre VARCHAR(60),
	PRIMARY KEY (id_partido_politico)
);

CREATE TABLE Provincia(
	nombre VARCHAR(40) NOT NULL,
	habitantes INTEGER,
	PRIMARY KEY (Nombre)
);

CREATE TABLE Bien_economico(
	id_bien_economico INTEGER NOT NULL AUTO_INCREMENT,
	valor INTEGER,
	tipo CHAR(1),
	PRIMARY KEY (id_bien_economico)
);

CREATE TABLE Periodo(
	fecha_inicio DATE,
	fecha_fin DATE,
	PRIMARY KEY (fecha_inicio, fecha_fin)
);

CREATE TABLE Sesion(
	fecha_inicio_sesion DATE NOT NULL,
	fecha_fin_sesion DATE NOT NULL,
	tipo CHAR(1) NOT NULL,
	camara CHAR(1) NOT NULL,
	PRIMARY KEY (fecha_inicio_sesion,fecha_fin_sesion,camara)
);

CREATE TABLE Comision(
	id_comision	INTEGER NOT NULL,
	nombre_comision VARCHAR(30) NOT NULL,
	dni_informante VARCHAR(8) NOT NULL,
	PRIMARY KEY (id_comision)
);

CREATE TABLE Voto(
	id_voto INTEGER NOT NULL,
	resultado CHAR(1),
	tipo CHAR(1),
	PRIMARY KEY (id_voto)
);

CREATE TABLE Proyecto_de_ley(
	titulo_proyecto_ley VARCHAR(50) NOT NULL,
	fecha DATE,
	id_camara_originaria INTEGER,
	estado_votaciones CHAR(1),
	PRIMARY KEY (titulo_proyecto_ley)
);

CREATE TABLE Ley(
	numeracion INTEGER NOT NULL AUTO_INCREMENT,
	titulo_ley VARCHAR(50) NOT NULL,
	fecha_sancionada DATE NOT NULL,
	titulo_proyecto_ley VARCHAR(50) NOT NULL,
	PRIMARY KEY (numeracion, titulo_ley, fecha_sancionada)
);

CREATE TABLE Control_de_calidad(
	id_control_calidad INTEGER NOT NULL,
	empleado VARCHAR(20),
	titulo_proyecto_ley VARCHAR(50) NOT NULL,
	PRIMARY KEY (id_control_calidad)
);

CREATE TABLE Vicepresidente(
	dni VARCHAR(8) NOT NULL,
	nombre VARCHAR(80) NOT NULL,
	PRIMARY KEY (dni)
);


-- Tablas de relaciones N:M

CREATE TABLE Es_propietario_de(
	dni_legislador VARCHAR(8) NOT NULL,
	id_bien_economico INTEGER NOT NULL,
	fecha_obtencion DATE NOT NULL,
	fecha_sucesion DATE,
	PRIMARY KEY (dni_legislador, id_bien_economico, fecha_obtencion)
);

CREATE TABLE Legisla_durante(
	dni_legislador VARCHAR(8) NOT NULL,
	fecha_inicio DATE NOT NULL, 
	fecha_fin DATE NOT NULL,
	PRIMARY KEY (dni_legislador, fecha_inicio, fecha_fin)
);

CREATE TABLE Asiste_sesion(
	dni_legislador VARCHAR(8) NOT NULL,
	idSesion INTEGER NOT NULL,
	fecha_inicio_sesion DATE NOT NULL, 
	fecha_fin_sesion DATE NOT NULL,
	idCamara INTEGER NOT NULL,
	PRIMARY KEY (dni_legislador, fecha_inicio_sesion, fecha_fin_sesion)
);

CREATE TABLE Participa_en_comision(
	dni_legislador VARCHAR(8) NOT NULL, 
	fecha_inicio_participacion DATE NOT NULL, 
	fecha_fin_participacion DATE NOT NULL,
	id_comision INTEGER NOT NULL, 
	PRIMARY KEY (dni_legislador, fecha_inicio_participacion, fecha_fin_participacion, id_comision)
);

CREATE TABLE Preside_bloque(
	dni_legislador VARCHAR(8) NOT NULL,
	fecha_inicio_presidencia_bloque DATE NOT NULL, 
	fecha_fin_presidencia_bloque DATE NOT NULL,
	id_bloque_politico INTEGER NOT NULL,
	PRIMARY KEY (dni_legislador, fecha_inicio_presidencia_bloque, fecha_fin_presidencia_bloque,id_bloque_politico )
);


CREATE TABLE Estudia(
	id_comision INTEGER NOT NULL, 
	titulo_proyecto_ley VARCHAR(50) NOT NULL,
	PRIMARY KEY (id_comision, titulo_proyecto_ley)
);

CREATE TABLE Preside_comision(
	id_comision INTEGER NOT NULL, 
	dni_diputado VARCHAR(8) NOT NULL, 
	fecha_inicio_preside DATE NOT NULL, 
	fecha_fin_preside DATE NOT NULL,
	PRIMARY KEY (id_comision, dni_diputado,fecha_inicio_preside,fecha_fin_preside)
);

CREATE TABLE Preside_camara_senadores(
	id_camara INTEGER NOT NULL, 
	dni_presidente VARCHAR(8) NOT NULL, 
	PRIMARY KEY (id_camara, dni_presidente)
);

CREATE TABLE Votan(
	dni VARCHAR(8) NOT NULL,
	id_voto INTEGER NOT NULL,
	titulo_proyecto_ley VARCHAR(50) NOT NULL,
	fecha DATE NOT NULL,	
	PRIMARY KEY (dni,titulo_proyecto_ley)
);


-- Foreign keys

ALTER TABLE Legislador 
	ADD CONSTRAINT `fk_bloque_politico`
	FOREIGN KEY (id_bloque_politico)
		REFERENCES Bloque_politico (id_bloque_politico),

	ADD CONSTRAINT `fk_provincia`
	FOREIGN KEY (nombre_provincia)
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

ALTER TABLE Es_propietario_de
	ADD CONSTRAINT `fk_legislador_bien`
	FOREIGN KEY (dni_legislador)
		REFERENCES Legislador (dni),

	ADD CONSTRAINT `fk_bien_economico`
	FOREIGN KEY (id_bien_economico)
		REFERENCES Bien_economico (id_bien_economico);

ALTER TABLE Legisla_durante
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
	FOREIGN KEY (id_comision)
		REFERENCES Comision (id_comision);

ALTER TABLE	Comision
	ADD CONSTRAINT `fk_informante`
	FOREIGN KEY (dni_informante)
		REFERENCES Legislador (dni);
		
ALTER TABLE Preside_bloque
	ADD CONSTRAINT `fk_preside_bloque_legislador`
	FOREIGN KEY (dni_legislador)
		REFERENCES Legislador (dni),
		
	ADD CONSTRAINT `fk_preside_bloque_bloquepolitico`
	FOREIGN KEY (id_bloque_politico)
		REFERENCES Bloque_politico (id_bloque_politico);
		
ALTER TABLE	Estudia
	ADD CONSTRAINT `fk_estudia_comision`
	FOREIGN KEY (id_comision)
		REFERENCES Comision(id_comision),
	
	ADD CONSTRAINT `fk_estudia_proyecto`
	FOREIGN KEY (titulo_proyecto_ley)
		REFERENCES Proyecto_de_ley (titulo_proyecto_ley);

ALTER TABLE	Preside_comision
	ADD CONSTRAINT `fk_comision_presidida`
	FOREIGN KEY (id_comision)
		REFERENCES Comision(id_comision),
	
	ADD CONSTRAINT `fk_diputado_presidente`
	FOREIGN KEY (dni_diputado)
		REFERENCES Legislador (dni);

ALTER TABLE	Proyecto_de_ley
	ADD CONSTRAINT `fk_camara_originaria`
	FOREIGN KEY (id_camara_originaria)
		REFERENCES Camara(id_camara);		

ALTER TABLE Preside_camara_senadores 
	ADD CONSTRAINT `fk_camara`
	FOREIGN KEY (id_camara)
		REFERENCES Camara (id_camara),

	ADD CONSTRAINT `fk_dni_presidente`
	FOREIGN KEY (dni_presidente)
		REFERENCES Vicepresidente (dni);
	
ALTER TABLE Votan
	ADD CONSTRAINT `fk_votan_leg`
	FOREIGN KEY (dni)
		REFERENCES Legislador (dni),

	ADD CONSTRAINT `fk_votan_voto`
	FOREIGN KEY (id_voto)
		REFERENCES Voto (id_voto),
	
	ADD CONSTRAINT `fk_votan_proyecto_ley`
	FOREIGN KEY (titulo_proyecto_ley )
		REFERENCES Proyecto_de_ley (titulo_proyecto_ley );
			

			
		

-- Check constraints

ALTER TABLE Legislador
	ADD CONSTRAINT `check_tipo_legislador` CHECK (tipo in ('S','D'));
	
ALTER TABLE Voto
	ADD CONSTRAINT `check_resultado_voto` CHECK (resultado in ('P','N','A')),
	ADD CONSTRAINT `check_resultado_voto` CHECK (tipo in ('E','N'));

ALTER TABLE Sesion
	ADD CONSTRAINT `check_tipo_sesion` CHECK (tipo in ('P','O','E')),
	ADD CONSTRAINT `check_camara_sesion` CHECK (camara in ('S','D'));

ALTER TABLE Camara
	ADD CONSTRAINT `check_tipo_camara` CHECK (tipo in('S','D'));

ALTER TABLE Proyecto_de_ley
	ADD CONSTRAINT `check_estado_votaciones` CHECK (estado_votaciones in('A','M','C'));
	
ALTER TABLE Es_propietario_de
	ADD CONSTRAINT `check_tipo_bien` CHECK (tipo in('A','S','I'));