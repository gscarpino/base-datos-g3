# -*- coding: utf-8 -*-
import estimators

# Creo una instancia de la clase que representa al metodo
exacto = estimators.Exacto('db.sqlite3', 'table1', 'c1')
# 'Histograma Clasico'
aEstimator = estimators.ClassicHistogram('db.sqlite3', 'table1', 'c1', parameter=20)
# 'Pasos Distribuidos'
bEstimator = estimators.DistributedSteps('db.sqlite3', 'table1', 'c1', parameter=20)

# Pruebo distintas instancias de estimacion
print "Classic Histogram"
print "  Sel(=%d) : %3.2f" % (50, aEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.2f" % (70, aEstimator.estimate_greater(70))

print "Pasos Distribuidos"
print "  Sel(=%d) : %3.2f" % (50, bEstimator.estimate_equal(93))
print "  Sel(>%d) : %3.2f" % (70, bEstimator.estimate_greater(70))

print "Exacto"
print "  Sel(=%d) : %3.2f" % (50, exacto.estimate_equal(50))
print "  Sel(>%d) : %3.2f" % (70, exacto.estimate_greater(70))

