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
		###REVISAR###
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



class Entropia(Estimator):



        def cantidadDeValoresDistintosEnBucket(self,base,tope,column,table,cursor):
            res=0

            q = "(Select " + self.column + " From " + self.table + " Order By " + self.column + " Asc)"
            resConsulta=cursor.execute("Select count( Distinct " + self.column + ") From " + q + " Where " + self.column + " >= " +  str(base) + " and "+ self.column+ " <= "+ str(tope) +";")
            res=resConsulta.fetchone()[0]

            print "la cantidad de valores distintos en bucket es"
            print res
            return res

        def cantidadEnBucket(self,base,tope,column,table,cursor):
             res=0
             q = "(Select " + self.column + " From " + self.table + " Order By " + self.column + " Asc)"
             resConsulta=cursor.execute("Select count("+ self.column + ") From " + q + " Where " + self.column + " >= " +  str(base) + " and "+ self.column+ " <= "+ str(tope) +";")
             res=resConsulta.fetchone()[0]
             print "la cantidad de valores  en bucket es "
             print res
             return res

        def entropiaTotal(self,lista):
		acum=0
		for entry in lista:
		  acum= entry.getEntropia()+acum
		return acum

        def calcularEntropia(self,minRange,maxRange,cursor,table,column):
            q = "(Select " + self.column + " From " + self.table + " Order By " + self.column + " Asc)"
            resConsulta=cursor.execute("Select count(" + self.column + ") From " + q + " Where " + self.column + ">=" + str(minRange)+ " AND " + self.column+ "<="+ str(maxRange)  + ";")
            totalenBucket=resConsulta.fetchone()[0]
            print "el total en bucket es..." +str(totalenBucket)
            acum=0
            #for a in range(minRange,math.floor(maxRange)):
            for a in range(minRange,maxRange):
                resConsulta=cursor.execute("Select count(" + self.column + ") From " + self.table + " Where " + self.column + "="+ str(a) + ";")
                probabilidad = resConsulta.fetchone()[0]
                select=probabilidad/float(totalenBucket)
                acum = acum+ (a* math.log(select))
            return (-1*acum)
	    
        #divido cada bucket en 3 y me fijo con cual maximizo la entropia
        def splitInterval(self,intervalo,p,cursor,table,column):

            base=intervalo.getBase()
            top=intervalo.getTope()
            ancho = top-base
            granularidad= ancho/3
            entropiaActual= intervalo.getEntropia()
            entropia1=self.calcularEntropia(base,base+granularidad,cursor,table,column)
            entropia2=self.calcularEntropia(base,base+(2*granularidad),cursor,table,column)
            entropia3= self.calcularEntropia(base+(2*granularidad),top,cursor,table,column)
            entropia4=self.calcularEntropia(base+granularidad,top,cursor,table,column)
            result=[]
            if entropia1 > entropia2:
                    distintosIntervalos= self.cantidadDeValoresDistintosEnBucket(base,base+granularidad,column,table,cursor)
                    cantEnInter= self.cantidadEnBucket(base,base+granularidad,column,table,cursor)
                    intervalo1=Intervalo(base,base+granularidad,entropia1,cantEnInter,distintosIntervalos)

                    distintosIntervalos= self.cantidadDeValoresDistintosEnBucket(base+granularidad,top,column,table,cursor)
                    cantEnInter= self.cantidadEnBucket(base+granularidad,top,column,table,cursor)
                    intervalo2=intervalos.Intervalo(base+granularidad,top,entropia4,cantEnInter,distintosIntervalos)
                    result =[intervalo1,intervalo2]
                    return result
            if entropia2>entropia1:
                    distintosIntervalos= self.cantidadDeValoresDistintosEnBucket(base,base+(2*granularidad),column,table,cursor)
                    cantEnInter= self.cantidadEnBucket(base,base+(2*granularidad),column,table,cursor)
                    intervalo3=intervalos.Intervalo(base,base+(2*granularidad),entropia2,cantEnInter,distintosIntervalos)

                    distintosIntervalos= self.cantidadDeValoresDistintosEnBucket(base+(2*granularidad),top,column,table,cursor)
                    cantEnInter= self.cantidadEnBucket(base+(2*granularidad),top,column,table,cursor)
                    intervalo4=intervalos.Intervalo(base+(2*granularidad),top,entropia3,cantEnInter,distintosIntervalos)

                    result =[intervalo3,intervalo4]
                    return result
            if entropia4>entropia3:
                    distintosIntervalos= self.cantidadDeValoresDistintosEnBucket(base,base+granularidad,column,table,cursor)
                    cantEnInter= self.cantidadEnBucket(base, base+granularidad,column,table,cursor)
                    intervalo5=intervalos.Intervalo(base,base+granularidad,entropia1,cantEnInter,distintosIntervalos)

                    distintosIntervalos= self.cantidadDeValoresDistintosEnBucket(base+granularidad,top,column,table,cursor)
                    cantEnInter= self.cantidadEnBucket(base+granularidad,top,column,table,cursor)
                    intervalo6=intervalos.Intervalo(base+granularidad,top,entropia4,cantEnInter,distintosIntervalos)

                    result =[intervalo5,intervalo6]
                    return result

            #nunca deberia entrar aca pero pongo por las dudas si entropia 3 >a entropia 4
            distintosIntervalos= self.cantidadDeValoresDistintosEnBucket(base,base+(2*granularidad),column,table,cursor)
            cantEnInter= self.cantidadEnBucket(base,base+(2*granularidad),column,table,cursor)
            intervalo7=intervalos.Intervalo(base,base+(2*granularidad),entropia2,cantEnInter,distintosIntervalos)

            distintosIntervalos= self.cantidadDeValoresDistintosEnBucket(base+(2*granularidad),top,column,table,cursor)
            cantEnInter= self.cantidadEnBucket(base+(2*granularidad),top,column,table,cursor)
            intervalo8=intervalos.Intervalo(base+(2*granularidad),top,entropia3,cantEnInter,distintosIntervalos)
            result =[intervalo7,intervalo8]
            return result



        def build_struct(self):
            self.buckets= []
            conexion = sqlite3.connect(self.db)
    	    c = conexion.cursor()
    	    c.execute("Select count(" + self.column + ") From " + self.table + ";")
            total = c.fetchone()[0]
            c.execute("Select min(" + self.column + ") From " + self.table + ";")
            self.minimo = c.fetchone()[0]
            c.execute("Select max(" + self.column + ") From " + self.table + ";")
            self.maximo = c.fetchone()[0]
            anchoTotal = self.maximo -self.minimo
            cantValoresDistin=self.cantidadDeValoresDistintosEnBucket(self.minimo,self.maximo,self.column,self.table,c)
            cantVal=self.cantidadEnBucket(self.minimo,self.maximo,self.column,self.table,c)
            i=intervalos.Intervalo(self.minimo,self.maximo,0,cantVal,cantValoresDistin)
            self.buckets.append(i)
            print "tengo la primer entropia todo esta en un bucket por lo tanto es 0"
            k=3
            copiaBuckets=self.buckets
            while k <= self.parameter:
                listaEntropias =[[]]
                j=0
                for intervalo in self.buckets:
                    listaConIntervaloDividido=[]
                    divisionIntervalos =self.splitInterval(intervalo,k,c,self.table,self.column)
                    listaConIntervaloDividido =self.buckets[:j]+divisionIntervalos+self.buckets[j+1:]
                    listaEntropias.append(listaConIntervaloDividido)
                    j=j+1


                entropiaMaxima=0
                resultado=[]
                for histogramaCandidato in listaEntropias:
                    entropiaActual=self.entropiaTotal(histogramaCandidato)
                    if entropiaActual >entropiaMaxima:
                        resultado=histogramaCandidato
                        entropiaMaxima=entropiaActual
                #print "los buckets son :"
                #print listaEntropias
                copiaBuckets=resultado
                k=k+1
            self.buckets=copiaBuckets


        def estimate_equal(self,value):

                for intervalo in self.buckets:
                    if (intervalo.getBase() <= value) and (intervalo.getTope() > value):
                        #print value
                        #intervalo.mostrar()
                       # print "la cantidad en intervalo es "+ intervalo.getCant()
                       # print "la cantidad de valores distintos es " +intervalo.getCantDistintos()
                        #return pow(2.0,(-1.0) * intervalo.getEntropia())
			return 1.0 / intervalo.getCantDistintos()
                return 0

        def estimate_greater(self,value):

                for intervalo in self.buckets:
                    if (intervalo.getBase() < value) and (intervalo.getTope() > value):
                        stimated=value/float((intervalo.getTope()-intervalo.getBase()))
                        return intervalo.getCant() *stimated
                return 0