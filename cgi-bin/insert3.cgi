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
fmid=unicode(random.randint(1, 100000))
hdiid=unicode(random.randint(1, 100000))
tbmid=unicode(random.randint(1, 100000))
ibmid=(random.randint(1, 100000))
isensorid=(random.randint(1, 100000))
bmid = unicode(ibmid)
sensorid=unicode(isensorid)
bmidplus1 = unicode(ibmid+1)
sensoridplus1=unicode(isensorid+1)

rocids=[str(random.randint(1, 100000)),str(random.randint(1, 100000)),str(random.randint(1, 100000))]
# first, create the bare objects
#transfer sensor
t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
ppp = pdb.insertSensor(Sensor(SENSOR_ID=sensorid, TRANSFER_ID=t.TRANSFER_ID))
if (ppp is None):
    print "Error cannot insert sensor"
#transfer rocs
for i in rocids:
    t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
    ppp=pdb.insertRoc(Roc(ROC_ID=i, TRANSFER_ID=t.TRANSFER_ID))
    if (ppp is None):
        print "Error cannot insert roc"

#transfer tbm
t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
ppp=pdb.insertTbm(Tbm(TBM_ID=tbmid, TRANSFER_ID=t.TRANSFER_ID))
if (ppp is None):
    print "Error cannot insert tmb"

#transfer hdi
t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
ppp=pdb.insertHdi(Hdi(HDI_ID=hdiid, TRANSFER_ID=t.TRANSFER_ID))
if (ppp is None):
    print "Error cannot insert hdi"

#ASSEMBLE BAREMODULE
newbm = pdb.assembleBareModule(bmid, rocids,sensorid,"tommasino")
if (newbm is None):
    print "FAILED INSERTION"
#ASSEMBLE FULL MODULE
newfm = pdb.assembleFullModule(fmid, bmid, tbmid, hdiid, "ttttttt")
print "OOO",newfm
if (newfm is None):
    print "FAILED INSERTION"
#
#test insert FM2
newfm = pdb.assembleFullModule(fmid+'2', bmid, tbmid, hdiid, "ttttttt")
if (newfm is None):
    print "<br>FAILED second INSERTION"
#

print "INSERTED!!!"
print "now I insert a baremodule whose sensor in not in inventory"
newbm = pdb.assembleBareModule(bmidplus1, rocids,sensoridplus1,"tommasino")
if (newbm is None):
    print "FAILED INSERTION"

print "FINISHED!!!"

#
# test a transfer
#
pp=pdb.transferSensor(sensorid,"pippo", "pluto")
if (pp is None):
    print "transferred failed!"
else:
    print "transferred ok!"

#
#
#

print "<br>TEST inserimento TEST_FM"
s = Session("Pisa", "Tommaso")
pdb.insertSession(s)
t = Test_FullModule(SESSION_ID=s.SESSION_ID,
                    FULLMODULE_ID=fmid,
                    RESULT=33,
                    DATA_ID=0, # no data id
                    ROCSWORSEPERCENT=44,
                    NOISE=33,
                    TRIMMING =66,
                    PHCAL = 99,
                    CURRENT1UA = 2,
                    CURRENT2UA  = 5,
                    CURRENT1501UA = 9,
                    CURRENT1502UA = 2,
                    IVSLOPE  = 23,
                    TEMPVALUE = 54,
                    TEMPERROR = 76,
                    TCYCLVALUE = 89,
                    TCYCLERROR = 55,
                    COMMENT= "ARANDOMTEST")
rr = pdb.insertFullModuleTest(t)
if (rr is None):
    print"<br>Error inserting test FM"
