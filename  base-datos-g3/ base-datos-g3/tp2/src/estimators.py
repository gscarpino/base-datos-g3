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
	
class ClassicHistogram(Estimator):
	"""Histograma clasico"""
	
	def build_struct(self):
		self.buckets = [0] * self.parameter
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		
		c.execute("Select min(" + self.column + ") From " + self.table + ";")
		min = c.fetchone()
		print "Minimo: " + str(min)
		
		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		max = c.fetchone()
		print "Maximo: " + str(max)
		
		rango = max[0] - min[0]
		
		self.anchoBucket = rango / self.parameter
		cantidad = 0
		for fila in c.execute("Select " + self.column + " From " + self.table + ";"):
			indice = fila[0] / self.anchoBucket 
			if(indice == len(self.buckets)):
				indice = indice - 1
			self.buckets[indice] = self.buckets[indice] + 1
			cantidad = cantidad + 1
		
		#print "Parametro: " + str(self.parameter) + " - Ancho: " + str(self.anchoBucket)
		print self.buckets
		print "Suma: " + str(sum(self.buckets))


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
		for i in range(indice+1,len(self.buckets)):
			acumulador = acumulador + self.buckets[i]
		return acumulador


class DistributedSteps(Estimator):
	"""Pasos distribuidos"""
	
	def build_struct(self):
		self.buckets = [0] * self.parameter
		conexion = sqlite3.connect(self.db)
		c = conexion.cursor()
		
		c.execute("Select min(" + self.column + ") From " + self.table + ";")
		min = c.fetchone()
		print "Minimo: " + str(min)
		
		c.execute("Select max(" + self.column + ") From " + self.table + ";")
		max = c.fetchone()
		print "Maximo: " + str(max)
		
		rango = max[0] - min[0]
		
		self.anchoBucket = rango / self.parameter
		cantidad = 0
		for fila in c.execute("Select " + self.column + " From " + self.table + ";"):
			indice = fila[0] / self.anchoBucket 
			if(indice == len(self.buckets)):
				indice = indice - 1
			self.buckets[indice] = self.buckets[indice] + 1
			cantidad = cantidad + 1
		
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
		for i in range(indice+1,len(self.buckets)):
			acumulador = acumulador + self.buckets[i]
		return acumulador
	