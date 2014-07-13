# -*- coding: utf-8 -*-
import estimators
import sqlite3
#~ atributo = 'c3'
# atributo = 'c1'
# # Creo una instancia de la clase que representa al metodo
# exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
# # 'Histograma Clasico'
# aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, parameter=20)
# # 'Pasos Distribuidos'
# bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, parameter=20)
# # 'Implementacion Propia'
# cEstimator = estimators.EstimatorGrupo('db.sqlite3', 'table1', atributo, parameter=20)
# Pruebo distintas instancias de estimacion

#~ valorEqual=332
#~ valorGreater=1797

# print "Classic Histogram"
# print "  Sel(=%d) : %3.5f" % (valorEqual, aEstimator.estimate_equal(valorEqual))
# print "  Sel(>%d) : %3.5f" % (valorGreater, aEstimator.estimate_greater(valorGreater))
# 
# print "Pasos Distribuidos"
# print "  Sel(=%d) : %3.5f" % (valorEqual, bEstimator.estimate_equal(valorEqual))
# print "  Sel(>%d) : %3.5f" % (valorGreater, bEstimator.estimate_greater(valorGreater))
# 
# print "Implementacion Propia"
# print "  Sel(=%d) : %3.5f" % (valorEqual, cEstimator.estimate_equal(valorEqual))
# print "  Sel(>%d) : %3.5f" % (valorGreater, cEstimator.estimate_greater(valorGreater))
# 
# print "Exacto"
# print "  Sel(=%d) : %3.5f" % (valorEqual, exacto.estimate_equal(valorEqual))
# print "  Sel(>%d) : %3.5f" % (valorGreater, exacto.estimate_greater(valorGreater))


#~ salto = 10
#~ valores = [-268,-12,323,699,940]
#~ atributo = 'c2'
#~ valores = [32,150,461,704,927]
#~ atributo = 'c0'
#~ print "#Buckets;Exacto;Clasico;Steps;Propia;"
#~ for numBuckets in range(10,201,salto):
	#~ exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
	#~ aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, numBuckets)
	#~ bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, numBuckets)
	#~ cEstimator = estimators.EstimatorGrupo('db.sqlite3', 'table1', atributo, numBuckets)
	#~ for valor in valores:
		#~ print str(numBuckets) + ";" + str(exacto.estimate_equal(valor)) + ";" + str(aEstimator.estimate_equal(valor)) + ";" + str(bEstimator.estimate_equal(valor)) + ";"+ str(cEstimator.estimate_equal(valor)) + ";"

saltoBuckets = 10
cantValores = 20
#atributos = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']
atributos = ['c8', 'c9']
histogram = estimators.ClassicHistogram('db.sqlite3', 'table1', 'c8', 50)
def mediaError(exacto, estimator, atributo):
	conexion = sqlite3.connect('db.sqlite3')
	c = conexion.cursor()
	c.execute("Select min(" + atributo + ") From table1;")
	minimo = c.fetchone()[0]
	c.execute("Select max(" + atributo + ") From table1;")
	maximo = c.fetchone()[0]
	saltoValor = (maximo - minimo) / cantValores
	acumuladorError = 0
	for valor in range(minimo, maximo, saltoValor):
		acumuladorError += abs( estimator.estimate_equal(valor) - exacto.estimate_equal(valor) )
	return (1.0 * acumuladorError) / cantValores
		
for atributo in atributos:
	print "Atributo: ", atributo
	print "#Buckets\tPromErrorClasico\tPromErrorSteps\tPromErrorGrupo"
	for numBuckets in range(10, 120, saltoBuckets):
		exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
		histogram = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, numBuckets)
		steps = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, numBuckets)
		grupo = estimators.EstimatorGrupo('db.sqlite3', 'table1', atributo, numBuckets)
		mediaErrorHistogram = mediaError(exacto, histogram, atributo)
		mediaErrorSteps = mediaError(exacto, steps, atributo)
		mediaErrorGrupo = mediaError(exacto, grupo, atributo)
		print str(numBuckets) + "\t" + '%f'%mediaErrorHistogram + "\t" + '%f'%mediaErrorSteps + "\t" + '%f'%mediaErrorGrupo
	print ""



#~ ''' Misma columna, mismo parametro, variacion de valor '''
#~ numBuckets = 20
#~ atributo = 'c2'
#~ salto = 50
#~ min = -700
#~ max = 1100
#~ ##~ valores = [60,123,433,666,998]
#~ ##~ atributo = 'c1'
#~ exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
#~ aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, numBuckets)
#~ bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, numBuckets)
#~ cEstimator = estimators.EstimatorGrupo('db.sqlite3', 'table1', atributo, numBuckets)

#~ print "#Buckets\tExacto\tHisrograma\tSteps\tGrupo"
#~ for valor in range(min, max, salto):
	#~ print str(valor) + "\t" + '%f'%exacto.estimate_equal(valor) + "\t" + '%f'%aEstimator.estimate_equal(valor) + "\t" + '%f'%bEstimator.estimate_equal(valor) + "\t" + '%f'%cEstimator.estimate_equal(valor)