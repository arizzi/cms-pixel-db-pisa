#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
from datetime import *
cgitb.enable()

print "Content-Type: text/html"
print

from PixelDB import *
import random

#
# add new one
#
pdb = PixelDBInterface(operator="tommaso",center="pisa")
pdb.connectToDB()
newtransf = Transfer(SENDER="pippo",RECEIVER="pluto")
pdb.insertTransfer(newtransf)
print "THE TID IS ", newtransf.TRANSFER_ID
newsensor=Sensor(SENSOR_ID=random.randint(1, 10000000) , TRANSFER_ID=newtransf.TRANSFER_ID)
print "OOOO"
pdb.insertTransfer(newtransf)
pdb.insertSensor(newsensor)


# 
# baremodule
#
rocids=[str(random.randint(1, 100000)),str(random.randint(1, 100000)),str(random.randint(1, 100000))]
bmid=random.randint(1, 100000)
sensid=random.randint(1, 100000)
newbm = pdb.assembleBareModule(bmid, rocids,sensid,"tommasino")
#
# fullmodule
fmid=random.randint(1, 100000)
hdiid=random.randint(1, 100000)
tbmid=random.randint(1, 100000)
newfm = pdb.assembleFullModule(fmid, bmid, tbmid, hdiid, "ttttttt")
