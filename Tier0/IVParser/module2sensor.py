#!/usr/bin/env python
import sys
sys.path.append("/home/robot/cms-pixel-db-pisa/PixelDB")
from PixelDB import *
pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

modules = pdb.store.find(FullModule,FullModule.FULLMODULE_ID==u"%s"%(sys.argv[1]))
m=modules[0]

import re

ID=m.baremodule.sensor.SENSOR_ID
ID=re.sub('S','',ID)
if len(sys.argv) >2 and sys.argv[2] == "-s" : 
 print ID
else : 
 spl=re.split('-',ID)
 print "BATCH",spl[0]
 print "WAFER",spl[1]
 print "SENSOR",spl[2]

#print m.baremodule.sensor.wafer.WAFER_ID
#print m.baremodule.sensor.wafer.batch.BATCH_ID


