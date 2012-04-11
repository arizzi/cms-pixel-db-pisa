#!/usr/bin/env python

# enable debugging
import cgitb
from datetime import *
cgitb.enable()

print "Content-Type: text/html"
print

from PixelDB import *
import random


pdb = PixelDBInterface(operator="tommaso",center="pisa")
pdb.connectToDB()

# add a fullmodule,  define all the ids
fmid=random.randint(1, 100000)
hdiid=random.randint(1, 100000)
tbmid=random.randint(1, 100000)
bmid=random.randint(1, 100000)
sensorid=random.randint(1, 100000)
rocids=[str(random.randint(1, 100000)),str(random.randint(1, 100000)),str(random.randint(1, 100000))]
# first, create the bare objects
#transfer sensor
t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
pdb.insertSensor(Sensor(SENSOR_ID=sensorid, TRANSFER_ID=t.TRANSFER_ID))
#transfer rocs
for i in rocids:
    t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
    pdb.insertRoc(Roc(ROC_ID=i, TRANSFER_ID=t.TRANSFER_ID))
#transfer tbm
t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
pdb.insertTbm(Tbm(TBM_ID=tbmid, TRANSFER_ID=t.TRANSFER_ID))
#transfer hdi
t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
pdb.insertHdi(Hdi(HDI_ID=hdiid, TRANSFER_ID=t.TRANSFER_ID))

#ASSEMBLE BAREMODULE
newbm = pdb.assembleBareModule(bmid, rocids,sensorid,"tommasino")
if (newbm is None):
    print "FAILED INSERTION"
#ASSEMBLE FULL MODULE
newfm = pdb.assembleFullModule(fmid, bmid, tbmid, hdiid, "ttttttt")
if (newfm is None):
    print "FAILED INSERTION"
#
print "INSERTED!!!"
print "now I insert a baremodule whose sensor in not in inventory"
newbm = pdb.assembleBareModule(bmid+1, rocids,sensorid+1,"tommasino")

print "FINISHED!!!"
