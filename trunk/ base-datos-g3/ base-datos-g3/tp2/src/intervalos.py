# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
import pylab
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
        return tope

    def getBase(self):
        return base

    def getEntropia(self):
        return valor

    def getCantDistintos(self):
        return distinctValues

    def getCant(self):
        return cantValues
