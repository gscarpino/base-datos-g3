# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
import pylab
import random

class Estimator(object):
    """Clase base de los estimadores."""

    def __init__(self, db, table, column, parameter=10):
        self.db = db
        self.table = table
        self.column = column
        self.parameter = parameter

        # Construye las estructuras necesita el estimador.
        self.build_struct()

    def build_struct(self):
        raise NotImplementedError()

    def estimate_equal(self, value):
        raise NotImplementedError()

    def estimate_greater(self, value):
        raise NotImplementedError()

class Exacto(Estimator):
	"""Metodo exacto"""

	def build_struct(self):
		pass

	def estimate_equal(self,value):
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		resultado = 0
		c.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + " = " + str(value)  + ";")
		resultado = c.fetchone()[0]
		conexion.close()
		return resultado
		
	def estimate_greater(self,value):
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		resultado = 0
		c.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + " > " + str(value)  + ";")
		resultado = c.fetchone()[0]
		conexion.close()
		return resultado

class ClassicHistogram(Estimator):
	"""Histograma clasico"""
	
	def build_struct(self):
		self.buckets = [0] * self.parameter
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		
		c.execute("Select min(" + self.column + ") From " + self.table + ";")
		min = c.fetchone()
		
		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		max = c.fetchone()
		
		rango = max[0] - min[0]
		
		self.anchoBucket = rango / self.parameter
		c.execute("Select " + self.column + " From " + self.table + ";")
		while True:
			fila = c.fetchone()
			if(fila == None):
				break
			else:
				indice = fila[0] / self.anchoBucket 
				if(indice == len(self.buckets)):
					indice = indice - 1
				self.buckets[indice] = self.buckets[indice] + 1
		conexion.close()
		
		#print "Parametro: " + str(self.parameter) + " - Ancho: " + str(self.anchoBucket)
		#print self.buckets
		#print "Suma: " + str(sum(self.buckets))


	def estimate_equal(self,value):
		indice = value / self.anchoBucket
		if(indice == len(self.buckets)):
			indice = indice - 1
		return self.buckets[indice]
		
	def estimate_greater(self,value):
		indice = value / self.anchoBucket
		if(indice == len(self.buckets)):
			indice = indice - 1
		acumulador = 0
		for i in range(indice + 1,len(self.buckets)):
			acumulador = acumulador + self.buckets[i]
		return acumulador


class DistributedSteps(Estimator):
	"""Pasos distribuidos"""
	
	def build_struct(self):
		self.buckets = [0] * self.parameter
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		
		c.execute("Select count(" + self.column + ") From " + self.table + ";")
		total = c.fetchone()
		
		self.anchoBucket = total[0] / self.parameter
		c.execute("Select " + self.column + " From " + self.table + " Order By " + self.column + " Asc;")
		contador = 0
		bucketActual = 0
		temp = 0
		#testing = [0] * self.parameter
		while True:
			#testing[bucketActual] = testing[bucketActual] + 1
			fila = c.fetchone()
			if(fila == None):
				if(not (contador == 0)):
					self.buckets[bucketActual] = temp
				break
			else:
				if(contador < self.anchoBucket):
					contador = contador + 1
					temp = fila[0]
				else:
					contador = 0
					self.buckets[bucketActual] = fila[0]
					bucketActual = bucketActual + 1
		conexion.close()
		
		#print "Parametro: " + str(self.parameter) + " - Ancho: " + str(self.anchoBucket)
		#print self.buckets
		#print testing
		#print "Suma: " + str(sum(self.buckets))


	def estimate_equal(self,value):
		return 0
		
	def estimate_greater(self,value):
		return 0
	