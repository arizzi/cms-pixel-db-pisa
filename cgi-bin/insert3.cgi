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


print "<br>INSERT FULL MODULE - MUST BE OK<br>"

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
ppp = pdb.insertSensor(Sensor(SENSOR_ID=sensorid, TRANSFER_ID=t.TRANSFER_ID,TYPE="fake"))
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
newbm = pdb.assembleBareModule(bmid, rocids,sensorid,"tommasino",t.TRANSFER_ID)
if (newbm is None):
    print "FAILED INSERTION"
#ASSEMBLE FULL MODULE
newfm = pdb.assembleFullModule(fmid, bmid, tbmid, hdiid, "ttttttt",t.TRANSFER_ID)
print "OOO",newfm
if (newfm is None):
    print "FAILED INSERTION"
#
#test insert FM2
print "<br>INSERT FULL MODULE - MUST BE NOT OK<br>"
    
newfm = pdb.assembleFullModule(fmid+'2', bmid, tbmid, hdiid, "ttttttt",t.TRANSFER_ID)
if (newfm is None):
    print "<br>FAILED second INSERTION"
#

print "INSERTED!!!"
print "<br>INSERT BARE MODULE - MUST BE NOTOK<br>"
print "now I insert a baremodule whose sensor in not in inventory"
newbm = pdb.assembleBareModule(bmidplus1, rocids,sensoridplus1,"tommasino",t.TRANSFER_ID)
if (newbm is None):
    print "FAILED INSERTION"

print "FINISHED!!!"

#
# test a transfer
#
print "<br>INSERT TRANSFER - MUST BE OK<br>"
pp=pdb.transferSensor(sensorid,"pippo", "pluto", STATUS="SHIPPED")
if (pp is None):
    print "transferred failed!"
else:
    print "transferred ok!"
print "<br>RECEIVE A TRANSFER - MUST BE OK<br>"
pp = pdb.receiveTransfer(pp.TRANSFER_ID)
if (pp is None):
    print "reception failed!"
else:
    print "reception ok!"

#
#
#

#
# now Insert a FM from file
#
print "<br>INSERT TEST FULL MODULE FROM FILE - MUST BE OK<br>"

s = Session("Pisa", "Tommaso")
pdb.insertSession(s)
dir = '/afs/cern.ch/user/s/starodum/public/moduleDB/M1215-080320.09:34/T-10a/'
rr = pdb.insertTestFullModuleDir(dir,s.SESSION_ID)
if rr is None:
        print"<br>Error inserting test FM"

dir = '/afs/cern.ch/user/s/starodum/public/moduleDB/M1215-080320.09:34/T+17a/'
rr = pdb.insertTestFullModuleDir(dir,s.SESSION_ID)
if rr is None:
        print"<br>Error inserting test FM"

dir = '/afs/cern.ch/user/s/starodum/public/moduleDB/M1215-080320.09:34/T-10b/'
rr = pdb.insertTestFullModuleDir(dir,s.SESSION_ID)
if rr is None:
        print"<br>Error inserting test FM"

