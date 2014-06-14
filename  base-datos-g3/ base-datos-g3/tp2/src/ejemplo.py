# -*- coding: utf-8 -*-
import estimators

# Creo una instancia de la clase que representa al metodo
#exacto = estimators.Exacto('db.sqlite3', 'table1', 'c1')
# 'Histograma Clasico'
#aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', 'c1', parameter=20)
# 'Pasos Distribuidos'
#bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', 'c1', parameter=20)

#cEstimator = estimators.Entropia('db.sqlite3', 'table1', 'c1', parameter=3)
# Pruebo distintas instancias de estimacion
#~ print "Classic Histogram"
#~ print "  Sel(=%d) : %3.5f" % (50, aEstimator.estimate_equal(666))
#~ print "  Sel(>%d) : %3.5f" % (70, aEstimator.estimate_greater(70))

#~ print "Pasos Distribuidos"
#~ print "  Sel(=%d) : %3.5f" % (50, bEstimator.estimate_equal(666))
#~ print "  Sel(>%d) : %3.5f" % (70, bEstimator.estimate_greater(70))

#~ print "Implementacion Propia"
#~ print "  Sel(=%d) : %3.15f" % (50, cEstimator.estimate_equal(666))
#~ print "  Sel(>%d) : %3.15f" % (70, cEstimator.estimate_greater(70))

#~ print "Exacto"
#~ print "  Sel(=%d) : %3.5f" % (50, exacto.estimate_equal(666))
#~ print "  Sel(>%d) : %3.5f" % (70, exacto.estimate_greater(70))


print "#Buckets;Exacto;Clasico;Steps;"
for numBuckets in range(100,1001,100):
	exacto = estimators.Exacto('db.sqlite3', 'table1', 'c3')
	aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', 'c3', numBuckets)
	bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', 'c3', numBuckets)
	
	valores = [1611,314,2865,-291,-1070]
	for valor in valores:
		print str(numBuckets) + ";" + str(exacto.estimate_equal(valor)) + ";" + str(aEstimator.estimate_equal(valor)) + ";" + str(bEstimator.estimate_equal(valor)) + ";"
		

print "#Buckets;Exacto;Clasico;Steps;"
for numBuckets in range(100,1001,100):
	exacto = estimators.Exacto('db.sqlite3', 'table1', 'c3')
	aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', 'c3', numBuckets)
	bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', 'c3', numBuckets)
	
	valores = [1611,314,2865,-291,-1070]
	for valor in valores:
		print str(numBuckets) + ";" + str(exacto.estimate_greater(valor)) + ";" + str(aEstimator.estimate_greater(valor)) + ";" + str(bEstimator.estimate_greater(valor)) + ";"