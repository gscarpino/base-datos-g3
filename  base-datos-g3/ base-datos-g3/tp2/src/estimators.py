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
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		c.execute("Select count(" + self.column + ") From " + self.table + ";")
		self.total = c.fetchone()[0]
		conexion.close()

	def estimate_equal(self,value):
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		resultado = 0
		c.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + " = " + str(value)  + ";")
		resultado = c.fetchone()[0]
		conexion.close()
		return 1.0 * resultado / self.total
		
	def estimate_greater(self,value):
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		resultado = 0
		c.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + " > " + str(value)  + ";")
		resultado = c.fetchone()[0]
		conexion.close()
		return 1.0 * resultado  / self.total

class ClassicHistogram(Estimator):
	"""Histograma clasico"""
	
	def build_struct(self):
		self.buckets = [0] * self.parameter
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		
		c.execute("Select min(" + self.column + ") From " + self.table + ";")
		min = c.fetchone()[0]
		
		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		max = c.fetchone()[0]
		
		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		self.total = c.fetchone()[0]
		
		rango = max - min
		
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
		return (1.0*self.buckets[indice] / self.total) / 100.0
		
	def estimate_greater(self,value):
		indice = value / self.anchoBucket
		if(indice == len(self.buckets)):
			indice = indice - 1
		acumulador = 0
		for i in range(indice + 1,len(self.buckets)):
			acumulador = acumulador + self.buckets[i]
		return (1.0*acumulador / self.total) / 100.0


class DistributedSteps(Estimator):
	"""Pasos distribuidos"""
	
	def build_struct(self):
		self.buckets = [[0,0]] * self.parameter
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		
		c.execute("Select count(" + self.column + ") From " + self.table + ";")
		self.total = c.fetchone()[0]
		
		c.execute("Select min(" + self.column + ") From " + self.table + ";")
		self.minimo = c.fetchone()[0]
		
		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		self.maximo = c.fetchone()[0]
		
		self.anchoBucket = self.total / self.parameter
		c.execute("Select " + self.column + " From " + self.table + " Order By " + self.column + " Asc;")
		contador = 0
		contador2 = 0
		bucketActual = 0
		temp = 0
		#testing = [0] * self.parameter
		while True:
			#testing[bucketActual] = testing[bucketActual] + 1
			fila = c.fetchone()
			if(fila == None):
				if(not (contador == 0)):
					self.buckets[bucketActual] = [temp,contador]
				break
			else:
				if(contador == bucketActual):
					temp2 = fila[0]
				if(contador < self.anchoBucket):
					contador = contador + 1
					temp = fila[0]
				else:
					self.buckets[bucketActual] = [temp2,contador+1]
					contador = 0
					bucketActual = bucketActual + 1
			contador2 = contador2 + 1
		conexion.close()
		#por las dudas, revisar si hace falta
		#self.buckets[0][0] = self.minimo
		#self.buckets[len(self.buckets)-1][1] = self.maximo
		#print "Total: " + str(self.total)
		
		#print "Parametro: " + str(self.parameter) + " - Ancho: " + str(self.anchoBucket)
		#print self.buckets
		#print testing
		#print "Suma: " + str(sum(self.buckets))


	def estimate_equal(self,value):
		s = 0
		resultado = 0
		if(self.maximo < value or value < self.minimo):
			resultado = 0
		else:
			while( self.buckets[s][0] < value ):
				s = s + 1
			if(s == 0):
				if(value == self.buckets[0][0]):
					#repeticiones0 es cuantos steps del mismo valor incluyendo el inicial
					repeticiones0 = 1
					s = s + 1
					while( self.buckets[s][0] == value ):
						repeticiones0 = repeticiones0 + 1
						s = s + 1
					resultado = (repeticiones0 - 0.5) / self.total
				else:
					resultado = 0
			else:
				if(s == (len(self.buckets)-1)):
					resultado = (0.5 / self.parameter)
				else:
					if(self.buckets[s][0] == value):
						repeticiones = 1
						s = s + 1
						while( self.buckets[s][0] == value ):
							repeticiones = repeticiones + 1
							s = s + 1
						if(s == (len(self.buckets)-1)):
							#caso de repeticiones de steps incluyendo el ultimo
							resultado = (((1.0 * repeticiones) - 0.5) / self.parameter)
						else:
							#repeticiones de steps pero no incluye al 1ero ni al ultimo
							resultado = ((1.0 * repeticiones) / self.parameter)
					else:
						#Esta entre steps
						resultado =  ((1.0/3.0) / self.parameter) 
		return resultado
		
	def estimate_greater(self,value):
		s = 0
		resultado = 0
		if(self.maximo <= value):
			resultado = 0
		else:
			if(value < self.minimo):
				resultado = 1
			else:
				while( self.buckets[s][0] < value ):
					s = s + 1
				if(s == 0):
					if(value == self.buckets[0][0]):
						#repeticiones0 es cuantos steps del mismo valor incluyendo el inicial
						repeticiones0 = 1
						s = s + 1
						while( self.buckets[s][0] == value ):
							repeticiones0 = repeticiones0 + 1
							s = s + 1
						resultado = 1 - (((1.0 * repeticiones0) - 0.5) / self.parameter)
					else:
						#esta demas
						resultado = 0
				else:
					if(s == (len(self.buckets)-1)):
						resultado = (0.5 / self.parameter)
					else:
						if(self.buckets[s][0] == value):
							repeticiones = 1
							s = s + 1
							while( self.buckets[s][0] == value ):
								repeticiones = repeticiones + 1
								s = s + 1
							if(s == (len(self.buckets)-1)):
								#caso de repeticiones de steps incluyendo el ultimo
								resultado = 0 
							else:
								#repeticiones de steps pero no incluye al 1ero ni al ultimo
								resultado = 1 - ((s - 0.5) / self.parameter) - self.estimate_equal(value)
						else:
							#Esta entre steps
							resultado =  1- ((1.0 * s + (1.0/3.0)) / self.parameter) -self.estimate_equal(value)
		return resultado
	