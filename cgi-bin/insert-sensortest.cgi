#!/usr/bin/env python

# enable debugging
import cgitb
from datetime import *
#cgitb.enable()

#print "Content-Type: text/html"
#print

from PixelDB import *
import random


pdb = PixelDBInterface(operator="tommaso",center="pisa")
pdb.connectToDB()

print "<br>SENSOR TEST - MUST BE OK<br>"

# add a fullmodule,  define all the ids
isensorid=unicode(random.randint(1, 100000))
ibatchid=unicode(random.randint(1, 100000))
iwaferid=unicode(random.randint(1, 100000))
t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
ppp = pdb.insertBatch(Batch(BATCH_ID=ibatchid, TRANSFER_ID=t.TRANSFER_ID))
if (ppp is None):
    print "Error cannot insert batch"
ppp = pdb.insertWafer(Wafer(WAFER_ID=iwaferid, BATCH_ID=ibatchid, TRANSFER_ID=t.TRANSFER_ID))
if (ppp is None):
    print "Error cannot insert wafer"


ppp = pdb.insertSensor(Sensor(SENSOR_ID=isensorid, TRANSFER_ID=t.TRANSFER_ID,TYPE="fake", WAFER_ID=iwaferid ))
if (ppp is None):
    print "Error cannot insert sensor"


#
# now try an insertion of a sensor test:
#
s = Session("Pisa", "Tommaso")
pdb.insertSession(s)

#
# just once
#
ppp = pdb.insertBatch(Batch(BATCH_ID='280253', TRANSFER_ID=t.TRANSFER_ID))
if (ppp is None):
    print "Error cannot insert batch"
ppp = pdb.insertWafer(Wafer(WAFER_ID='280253-16', BATCH_ID='280253', TRANSFER_ID=t.TRANSFER_ID))
if (ppp is None):
    print "Error cannot insert wafer"


ppp = pdb.insertSensor(Sensor(SENSOR_ID='280253-16-03', TRANSFER_ID=t.TRANSFER_ID,TYPE="fake", WAFER_ID='280253-16' ))
if (ppp is None):
    print "Error cannot insert sensor"



#

ppp =pdb.insertTestSensorDir('/home/robot/cgi-bin/test', 'pippo',  'pluto', s)
if (ppp is None):
    print "Error cannot insert sensor test"


exit(0)
