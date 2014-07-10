# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
# import pylab
import random

class Intervalo:

#    base=0
#    tope=1
#    valor=0
#    cantValues=0
    def __init__(self,base,tope,valor,cantValues,distinctValues):
        self.base = base
        self.tope = tope
        self.valor = valor
        self.cantValues=cantValues
        self.distinctValues=distinctValues

    def getTope(self):
        return self.tope

    def getBase(self):
        return self.base

    def getEntropia(self):
        return self.valor

    def getCantDistintos(self):
        return self.distinctValues

    def getCant(self):
        return self.cantValues

    def mostrar(self):
        print self.base
        print self.tope
        print self.valor
        print self.distinctValues
        print self.cantValues
