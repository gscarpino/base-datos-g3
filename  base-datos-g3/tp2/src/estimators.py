# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
# import pylab
import random
import math

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
		
########################
		

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

		
##################################


class ClassicHistogram(Estimator):
	"""Histograma clasico"""

	def build_struct(self):
		self.buckets = [0] * self.parameter
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()

		c.execute("Select min(" + self.column + ") From " + self.table + ";")
		self.min = c.fetchone()[0]

		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		self.max = c.fetchone()[0]

		c.execute("Select count(" + self.column + ") From " + self.table + ";")
		self.total = c.fetchone()[0]

		self.rango = self.max - self.min

		self.anchoBucket = self.rango / self.parameter
		#~ print "min:",self.min," max:",self.max," total:",self.total," rango:",rango," ancho:",self.anchoBucket
		c.execute("Select " + self.column + " From " + self.table + ";")
		while True:
			fila = c.fetchone()
			if(fila == None):
				break
			else:
				indice = self.calcularIndice(fila[0])
				if(len(self.buckets) <= indice):
					indice = len(self.buckets) - 1
				#~ print "b: ",self.parameter," - i: ",indice, " - valor: ", fila[0], " - min: ", self.min
				self.buckets[indice] = self.buckets[indice] + 1
		conexion.close()

		#print "Parametro: " + str(self.parameter) + " - Ancho: " + str(self.anchoBucket)
		#print self.buckets
		#print "Suma: " + str(sum(self.buckets))


	def estimate_equal(self,value):
		indice = self.calcularIndice(value)
		if(len(self.buckets) <= indice):
			indice = len(self.buckets) - 1
		return (1.0*self.buckets[indice] / self.total)

	def estimate_greater(self,value):
		indice = self.calcularIndice(value)
		if(len(self.buckets) <= indice):
			return 0
		acumulador = 0
		for i in range(indice+1,len(self.buckets)):
			acumulador = acumulador + self.buckets[i]
		return (1.0 * acumulador / self.total)
		
	def calcularIndice(self, value):
		indice = 0
		if self.min < 0 :
			indice = (abs(self.min) + abs(value)) / self.anchoBucket
		else:
			indice = value / self.anchoBucket
		indice = int(indice)
		return indice
	

#######################################
	
	
class EstimatorGrupo(Estimator):
	
	def build_struct(self):
		self.clasico = ClassicHistogram(self.db, self.table, self.column, self.parameter//2)
		self.cantBuckets = self.parameter//2
		print self.clasico.buckets
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		while self.cantBuckets < self.parameter:
			max = 0
			posMax = 0
			pos = 0
			for b in self.clasico.buckets:
				if(max < b):
					max = b
					posMax = pos
				pos = pos + 1
			
			###Calculo un estimativo de cual podria ser el minimo valor del bucket. Esto introduce un error pudiendo haber mayor cantidad
			###de elementos que en el original (casi seguro)
			minBucket = self.clasico.anchoBucket * posMax
			c.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + " > " + \
			str(minBucket)  + " and " + self.column + " < " + str(minBucket + (self.clasico.anchoBucket//2)) + ";")
			
			valor1 = c.fetchone()[0]
			valor2 = max - valor1
			if(valor2 <= 0 ):
				###Si los errores introducidos hacen que sea algo imposible se termina manteniendo algo usable
				break
			self.clasico.buckets.insert(posMax+1,valor1)
			self.clasico.buckets.insert(posMax+2,valor2)
			del self.clasico.buckets[posMax]
			#~ print self.clasico.buckets
			self.cantBuckets = self.cantBuckets + 1
			
			###Actualizo el ancho del bucket. Se introduce mas error, se asume que todos los buckets tienen mismo ancho.
			self.clasico.anchoBucket = (self.clasico.rango//self.cantBuckets) 
			
		conexion.close()
		print self.clasico.buckets

	def estimate_equal(self,value):
		return self.clasico.estimate_equal(value)

	def estimate_greater(self,value):
		return self.clasico.estimate_greater(value)
	
##################################
	
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
				if(contador < (self.anchoBucket-1)):
					contador = contador + 1
					temp = fila[0]
				else:
					self.buckets[bucketActual] = [temp2,contador+1]
					contador = 0
					bucketActual = bucketActual + 1
					if(bucketActual  == self.parameter):
						bucketActual = self.parameter - 1
			contador2 = contador2 + 1
		conexion.close()
		#por las dudas, revisar si hace falta
		self.buckets[0][0] = self.minimo
		self.buckets[len(self.buckets)-1][0] = self.maximo
		#print "Total: " + str(self.total)

		#print "Parametro: " + str(self.parameter) + " - Ancho: " + str(self.anchoBucket)
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
						resultado = 1.0 - (((1.0 * repeticiones0) - 0.5) / self.parameter)
					else:
						#esta demas
						resultado = 0	
				else:
					if(s == (len(self.buckets)-1)):
						#si es el último step
						#acaaaaaa cae cuando muchos steps
						resultado = 0

					else:
						if(self.buckets[s][0] == value):
							repeticiones = 1
							primerBucket = s
							s = s + 1
							while( self.buckets[s][0] == value ):
								repeticiones = repeticiones + 1
								s = s + 1
							if(s == (len(self.buckets)-1)):
								#caso de repeticiones de steps incluyendo el ultimo
								resultado = 0
							else:
								#repeticiones de steps pero no incluye al 1ero ni al ultimo
								resultado = 1.0 - ((1.0 * primerBucket - 0.5) / self.parameter) - ((1.0 * repeticiones) / self.parameter)
						else:
							#Esta entre steps
							resultado =  1.0 - ((1.0 * (s-1.0) + (1.0/3.0)) / self.parameter) - ((1.0/3.0) / self.parameter)
							
		return resultado
