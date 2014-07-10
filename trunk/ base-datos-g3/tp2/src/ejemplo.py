# -*- coding: utf-8 -*-
import estimators
atributo = 'c3'
# Creo una instancia de la clase que representa al metodo
exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
# 'Histograma Clasico'
aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, parameter=20)
# 'Pasos Distribuidos'
bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, parameter=20)
# 'Implementacion Propia'
cEstimator = estimators.Entropia('db.sqlite3', 'table1', atributo, parameter=20)
# Pruebo distintas instancias de estimacion

print "Classic Histogram"
print "  Sel(=%d) : %3.5f" % (50, aEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.5f" % (70, aEstimator.estimate_greater(70))

print "Pasos Distribuidos"
print "  Sel(=%d) : %3.5f" % (50, bEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.5f" % (70, bEstimator.estimate_greater(70))

print "Implementacion Propia"
print "  Sel(=%d) : %3.5f" % (50, cEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.5f" % (70, cEstimator.estimate_greater(70))

print "Exacto"
print "  Sel(=%d) : %3.5f" % (50, exacto.estimate_equal(50))
print "  Sel(>%d) : %3.5f" % (70, exacto.estimate_greater(70))


# salto = 25
# valores = [1611,314,2865,-291,-1070]
# atributo = 'c3'
 ##~ valores = [60,123,433,666,998]
 ##~ atributo = 'c1'
# print "#Buckets;Exacto;Clasico;Steps;Propia;"
# for numBuckets in range(50,301,salto):
	# exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
	# aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, numBuckets)
	# bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, numBuckets)
	# cEstimator = estimators.EstimatorGrupo('db.sqlite3', 'table1', atributo, numBuckets)
	# for valor in valores:
		# print str(numBuckets) + ";" + str(exacto.estimate_equal(valor)) + ";" + str(aEstimator.estimate_equal(valor)) + ";" + str(bEstimator.estimate_equal(valor)) + ";"+ str(cEstimator.estimate_equal(valor)) + ";"
		

# print "#Buckets;Exacto;Clasico;Steps;Propia;"
# for numBuckets in range(50,301,salto):
	# exacto = estimators.Exacto('db.sqlite3', 'table1', atributo)
	# aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', atributo, numBuckets)
	# bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', atributo, numBuckets)
	# for valor in valores:
		# print str(numBuckets) + ";" + str(exacto.estimate_greater(valor)) + ";" + str(aEstimator.estimate_greater(valor)) + ";" + str(bEstimator.estimate_greater(valor)) + ";" + str(cEstimator.estimate_greater(valor)) + ";"