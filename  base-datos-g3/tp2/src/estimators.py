# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
# import pylab
import random
import intervalos
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
		self.min = c.fetchone()[0]

		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		self.max = c.fetchone()[0]

		c.execute("Select count(" + self.column + ") From " + self.table + ";")
		self.total = c.fetchone()[0]

		rango = self.max - self.min

		self.anchoBucket = rango / self.parameter
		#~ print "min:",self.min," max:",self.max," total:",self.total," rango:",rango," ancho:",self.anchoBucket
		c.execute("Select " + self.column + " From " + self.table + ";")
		while True:
			fila = c.fetchone()
			if(fila == None):
				break
			else:
				if self.min < 0 :
					indice = (abs(self.min) + fila[0]) / self.anchoBucket
				else:
					indice = fila[0] / self.anchoBucket
				indice = int(indice)
				if(len(self.buckets) <= indice):
					indice = len(self.buckets) - 1
				#~ print "b: ",self.parameter," - i: ",indice, " - valor: ", fila[0], " - min: ", self.min
				self.buckets[indice] = self.buckets[indice] + 1
		conexion.close()

		#print "Parametro: " + str(self.parameter) + " - Ancho: " + str(self.anchoBucket)
		#print self.buckets
		#print "Suma: " + str(sum(self.buckets))


	def estimate_equal(self,value):
		if self.min < 0 :
			indice = (abs(self.min) + value) / self.anchoBucket
		else:
			indice = value / self.anchoBucket
		indice = int(indice)
		if(len(self.buckets) <= indice):
			indice = len(self.buckets) - 1
		return (1.0*self.buckets[indice] / self.total)

	def estimate_greater(self,value):
		if self.min < 0 :
			indice = (abs(self.min) + value) / self.anchoBucket
		else:
			indice = value / self.anchoBucket
		indice = int(indice)
		if(len(self.buckets) <= indice):
			return 0
		acumulador = 0
		for i in range(indice+1,len(self.buckets)):
			acumulador = acumulador + self.buckets[i]
		return (1.0 * acumulador / self.total)

class ModifiedClassicHistogram(ClassicHistogram):
	
	def build_struct(self):
		super.build_struct()
		self.reacomodarValores()
		
	def reacomodarValores(self):
		"""Aca reacomodar los valores muy altos para mejorar la selectividad"""
	
		
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



class EstimatorGrupo(Estimator):

        def build_struct(self):
		self.buckets= []
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		c.execute("Select count(" + self.column + ") From " + self.table + ";")
		self.total = c.fetchone()[0]

		c.execute("Select min(" + self.column + ") From " + self.table + ";")
		self.minimo = c.fetchone()[0]

		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		self.maximo = c.fetchone()[0]

		#Es necesario ordenarlo?
		c.execute("Select " + self.column + " From " + self.table + " Order By " + self.column + " Asc;")
		

		cantBuckets = 1
		bucketInicial = dict()
		while True:
			fila = c.fetchone()
			if(fila == None):
				break
			else:
				if fila[0] not in bucketInicial:
					bucketInicial[fila[0]] = 0
				
				bucketInicial[fila[0]] = bucketInicial[fila[0]] + 1
		
		self.buckets.append(bucketInicial)
		aBorrar = dict()
		while len(self.buckets) < self.parameter:
			corte = self.calcularCorte(self.buckets)
			for b in self.buckets:
				if corte[0] in b:
					listado = b.items()
					listado1 = listado[:listado.index(corte)]
					listado2 = listado[listado.index(corte):]
					aBorrar = b
					break
			self.buckets.remove(aBorrar)
			self.buckets.append(dict(listado1))
			self.buckets.append(dict(listado2))
		
		#~ print "len: ",len(self.buckets)
		#~ for b in self.buckets:
			#~ print b
			#~ print ""
			#~ print ""
		#~ print "Consistente ", self.chequarConsistencia(self.buckets,bucketInicial)

	def calcularCorte(self,buckets):
		posiblesCortes = []
		for b in buckets:
			listado = b.items()
			if 4 <= len(listado):
				#elemento1 es par (key,value)
				elemento1 = listado[len(listado) / 4]
				elemento2 = listado[len(listado) / 2]
				elemento3 = listado[(3 * len(listado)) / 4]
				valor1 = self.calcularParDeEntropia(b,elemento1)
				valor2 = self.calcularParDeEntropia(b,elemento2)
				valor3 = self.calcularParDeEntropia(b,elemento3)
				if max(valor1,valor2,valor3) == valor1:
					posiblesCortes.append((elemento1,valor1))
				elif max(valor1,valor2,valor3) == valor2:
					posiblesCortes.append((elemento2,valor2))
				else:
					posiblesCortes.append((elemento3,valor3))
		maxH = 0
		maxElemento = (0,0)
		for c in posiblesCortes:
			if maxH < c[1]:
				maxElemento = c[0]
				maxH = c[1]
		return maxElemento
	
	def calcularParDeEntropia(self,bucket,corte):
		listado = bucket.items()
		listado1 = listado[:listado.index(corte)]
		listado2 = listado[listado.index(corte):]
		entropia1 = self.calcularEntropia(listado1)
		entropia2 = self.calcularEntropia(listado2)
		res = entropia1 + entropia2
		return res
	
	def calcularEntropia(self,lista):
		prob = 0
		res = 0
		total = self.calcularTotal(lista)
		for i in lista:
			prob = 1.0 * i[1] / total
			res = res + prob * math.log(prob,2) 
		return -res
	
	def calcularTotal(self,lista):
		res = 0
		for i in lista:
			res = res + i[1] 
		return res
		
	def chequarConsistencia(self, buckets,inicial):
		res = True
		suma = 0
		#No se perdieron valores
		for b in buckets:
			suma = suma + len(b)
			for k in b.keys():
				if k not in inicial:
					res = false
					break
			if not res:
				break
		#Un valor en un unico bucket
		res = res and suma == len(inicial)
		return res
		
        def estimate_equal(self,value):
		res = 0
		for b in self.buckets:
			if value in b:
				res = pow(2.0,-1.0*self.calcularEntropia(b.items()))
				#~ res =  1.0 / len(b.keys())
				break
		return res

        def estimate_greater(self,value):

		#~ for intervalo in self.buckets:
		#~ if (intervalo.getBase() < value) and (intervalo.getTope() > value):
		#~ stimated=value/float((intervalo.getTope()-intervalo.getBase()))
		#~ return intervalo.getCant() *stimated
		return 0
