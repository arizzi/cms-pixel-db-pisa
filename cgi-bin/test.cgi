#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/html"
print


from MySQLdb import *
from storm.locals import *
database = create_database("mysql://tester:pixels@cmspisa001/test_pixel")
store = Store(database)

class Roc(object):
  __storm_table__ = "inventory_roc"
  ROC_ID = Unicode(primary=True)
  TRANSFER_ID = Unicode()
  COMMENT = Unicode()

class Sensor(object):
  __storm_table__ = "inventory_sensor"
  SENSOR_ID = Unicode(primary=True)
  TRANSFER_ID = Unicode()
  COMMENT = Unicode()

class BareModule(object):
  __storm_table__ = "inventory_baremodule"
  BAREMODULE_ID = Unicode(primary=True)
  ROC_ID =  Unicode()
  SENSOR_ID = Unicode()
  TRANSFER_ID = Unicode()
  roc = Reference(ROC_ID, Roc.ROC_ID)
  sensor = Reference(SENSOR_ID, Sensor.SENSOR_ID)
  COMMENT = Unicode()

 
bm = store.find( BareModule ).one()

print "Roc id ", bm.roc.ROC_ID

