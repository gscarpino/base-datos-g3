# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
import pylab
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



##class Entropia(Estimator):
##
##
##
##        def cantidadDeValoresDistintosEnBucket(self,base,tope,column,table,cursor):
##            res=0
##            for a in range(base,tope):
##                resConsulta=cursor.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + "=" + str(a) +";")
##                totalDeValor=resConsulta.fetchone()[0]
##                if totalDeValor>0:
##                    res=res+totalDeValor
##
##            return res
##
##        def cantidadEnBucket(self,base,tope,column,table,cursor):
##             res=0
##             for a in range(base,tope):
##                resConsulta=cursor.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + "=" + str(a) +";")
##                totalDeValor=resConsulta.fetchone()[0]
##                res=res+totalDeValor
##
##             return res
##
##
##
##
##        def entropiaTotal(lista):
##			acum=0
##			for entry in lista:
##			  acum= entry.getEntropia+acum
##			return acum
##
##        def calcular_Entropia(minRange,maxRange,cursor,table,column):
##            resConsulta=cursor.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + ">=" + str(minRange)+ "and" + self.column+ "<="+ str(maxRange)  + ";")
##            totalenBucket=resConsulta.fetchone()[0]
##            print "el total en bucket es..." +totalenBucket
##            acum=0
##            for a in range(minRange,math.floor(maxRange)):
##                #resConsulta=resConsulta=cursor.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + "=" a ";")
##                resConsulta=cursor.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + "="+ a + ";")
##                probabilidad = resConsulta.fetchone()[0]/totalenBucket
##                acum = acum+ (a* math.log(probabilidad))
##            return (-1*acum)
##        #divido cada bucket en 3 y me fijo con cual maximizo la entropia
##        def splitInterval(intervalo,p,cursor,table,column):
##
##            base=intervalo.getBase
##            top=intervalo.getTope
##            ancho = top-base
##            granularidad= ancho/3
##            entropiaActual= intervalo.getEntropia
##            entropia1=calcularEntropia(base,base+granularidad,cursor,table,column)
##            entropia2=calcularEntropia((base,base+(2*granularidad),cursor,table,column))
##            entropia3= calcularEntropia(base+(2*granularidad),top,cursor,table,column)
##            entropia4=calcularEntropia(base+granularidad,top,cursor,table,column)
##            result=[]
##            if entropia1 > entropia2:
##                    distintosIntervalos= cantidadDeValoresDistintosEnBucket(base,base+granularidad,column,table,cursor)
##                    cantEnInter= cantidadEnBucket(base,base+granularidad,column,table,cursor)
##                    intervalo1=intervalos.Intervalo(base,base+granularidad,entropia1,cantEnInter,distintosIntervalos)
##
##                    distintosIntervalos= cantidadDeValoresDistintosEnBucket(base+granularidad,top,column,table,cursor)
##                    cantEnInter= cantidadEnBucket(base+granularidad,top,column,table,cursor)
##                    intervalo2=intervalos.Intervalo(base+granularidad,top,entropia4,cantEnInter,distintosIntervalos)
##                    result =[intervalo1,intervalo2]
##                    return result
##            if entropia2>entropia1:
##                    distintosIntervalos= cantidadDeValoresDistintosEnBucket(base,base+(2*granularidad),column,table,cursor)
##                    cantEnInter= cantidadEnBucket(base,base+(2*granularidad),column,table,cursor)
##                    intervalo3=intervalos.Intervalo(base,base+(2*granularidad),entropia2,cantEnInter,distintosIntervalos)
##
##                    distintosIntervalos= cantidadDeValoresDistintosEnBucket(base+(2*granularidad),top,column,table,cursor)
##                    cantEnInter= cantidadEnBucket(base+(2*granularidad),top,column,table,cursor)
##                    intervalo4=intervalos.Intervalo(base+(2*granularidad),top,entropia3,cantEnInter,distintosIntervalos)
##
##                    result =[intervalo3,intervalo4]
##                    return result
##            if entropia4>entropia3:
##                    distintosIntervalos= cantidadDeValoresDistintosEnBucket(base,base+granularidad,column,table,cursor)
##                    cantEnInter= cantidadEnBucket(base, base+granularidad,column,table,cursor)
##                    intervalo5=intervalos.Intervalo(base,base+granularidad,entropia1,cantEnInter,distintosIntervalos)
##
##                    distintosIntervalos= cantidadDeValoresDistintosEnBucket(base+granularidad,top,column,table,cursor)
##                    cantEnInter= cantidadEnBucket(base+granularidad,top,column,table,cursor)
##                    intervalo6=intervalos.Intervalo(base+granularidad,top,entropia4,cantEnInter,distintosIntervalos)
##
##                    result =[intervalo5,intervalo6]
##                    return result
##
##            #nunca deberia entrar aca pero pongo por las dudas si entropia 3 >a entropia 4
##            distintosIntervalos= cantidadDeValoresDistintosEnBucket(base,base+(2*granularidad),column,table,cursor)
##            cantEnInter= cantidadEnBucket(base,base+(2*granularidad),column,table,cursor)
##            intervalo7=intervalos.Intervalo(base,base+(2*granularidad),entropia2,cantEnInter,distintosIntervalos)
##
##            distintosIntervalos= cantidadDeValoresDistintosEnBucket(base+(2*granularidad),top,column,table,cursor)
##            cantEnInter= cantidadEnBucket(base+(2*granularidad),top,column,table,cursor)
##            intervalo8=intervalos.Intervalo(base+(2*granularidad),top,entropia3,cantEnInter,distintosIntervalos)
##            result =[intervalo7,intervalo8]
##            return result
##
##
##
##        def build_struct(self):
##            self.buckets= []
##            conexion = sqlite3.connect(self.db)
##    	    c = conexion.cursor()
##    	    c.execute("Select count(" + self.column + ") From " + self.table + ";")
##    	    #self.total = c.fetchone()[0]
##            total = c.fetchone()[0]
##            #print "el total es....."+ str(total)
##            c.execute("Select min(" + self.column + ") From " + self.table + ";")
##            #self.minimo = c.fetchone()[0]
##            self.minimo = c.fetchone()[0]
##            c.execute("Select max(" + self.column + ") From " + self.table + ";")
##            #self.maximo = c.fetchone()[0]
##            self.maximo = c.fetchone()[0]
##            anchoTotal = self.maximo -self.minimo
##            cantValoresDistin=self.cantidadDeValoresDistintosEnBucket(self.minimo,self.maximo,self.column,self.table,c)
##            cantVal=self.cantidadEnBucket(self.minimo,self.maximo,self.column,self.table,c)
##            i=intervalos.Intervalo(self.minimo,self.maximo,0,cantVal,cantValoresDistin)
##            self.buckets.append(i)
##            print "tengo la primer entropia todo esta en un bucket por lo tanto es 0"
##            k=0
##            copiaBuckets=buckets
##            while k <= parameter:
##                listaEntropias =[[]]
##                j=0
##                for intervalo in buckets:
##                    listaConIntervaloDividido=[]
##                    divisionIntervalos =splitInterval(intervalo,k,c,self.table,self.column)
##                    listaConIntervaloDividido =buckets[:j]+divisionIntervalos+buckets[j+1:]
##                    listaEntropias.append(listaConIntervaloDividido)
##                    j=j+1
##
##
##                entropiaMaxima=0
##                resultado=[]
##                for histogramaCandidato in listaEntropias:
##                    entropiaActual=entropiaTotal(histogramaCandidato)
##                    if entropiaActual >entropiaMaxima:
##                        resultado=histogramaCandidato
##                        entropiaMaxima=entropiaActual
##
##                copiaBuckets=resultado
##
##            buckets=copiaBuckets
##
##
##        def estimate_equal(self,value):
##
##                for intervalo in buckets:
##                    if (intervalo.getBase <= value) and (intervalo.getTope > value):
##                        return intervalo.getCant *intervalo.getCantDistintos
##                return 0
##
##        def estimate_greater(self,value):
##
##                for intervalo in buckets:
##                    if (intervalo.getBase < value) and (intervalo.getTope > value):
##                        stimated=value/(intervalo.getTope-intervalo.getBase)
##                        return intervalo.getCant *stimated
##                return 0