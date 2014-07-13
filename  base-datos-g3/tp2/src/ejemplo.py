# -*- coding: utf-8 -*-
import estimators
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


# salto = 25
# valores = [1611,314,2865,-291,-1070]
# atributo = 'c3'
# ##~ valores = [60,123,433,666,998]
# ##~ atributo = 'c1'
# print "#Buckets;Exacto;Clasico;Steps;Propia;"
# for numBuckets in range(50,301,salto):
# 	exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
# 	aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, numBuckets)
# 	bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, numBuckets)
# 	cEstimator = estimators.EstimatorGrupo('db.sqlite3', 'table1', atributo, numBuckets)
# 	for valor in valores:
# 		print str(numBuckets) + ";" + str(exacto.estimate_equal(valor)) + ";" + str(aEstimator.estimate_equal(valor)) + ";" + str(bEstimator.estimate_equal(valor)) + ";"+ str(cEstimator.estimate_equal(valor)) + ";"
		
salto = 40
valores = [-1000, -671,250,700,-200,1002, 1500]
atributo = 'c2'
print "#Buckets;Exacto;Clasico;Steps;Propia;"
for numBuckets in range(10,301,salto):
	exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
	aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, numBuckets)
	bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, numBuckets)
	for valor in valores:
		print "Classic Histogram"
		print "  Sel(=%d) : %3.5f" % (valor, aEstimator.estimate_equal(valor))
		print "  Sel(>%d) : %3.5f" % (valor, aEstimator.estimate_greater(valor))
		print "Pasos Distribuidos"
		print "  Sel(=%d) : %3.5f" % (valor, bEstimator.estimate_equal(valor))
		print "  Sel(>%d) : %3.5f" % (valor, bEstimator.estimate_greater(valor))