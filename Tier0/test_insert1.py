#!/usr/bin/env python

# enable debugging
import cgitb
import datetime
from time import sleep
#cgitb.enable()

print "Content-Type: text/html"
print

from PixelTier0 import *
import random


pdb = PixelTier0()
pdb.initProcessing(CONFIG="./test.ini", DEBUG=True)
pdb.connectToDB()

print " initialization done"

#
# test insert of a tar file

print "Insert new tar"

tar = InputTar (NAME='pippo.tar',
                LOCATION='/home/tom/CMSSW_6_1_0/src/UserCode/PixelDBPisa/Tier0/tar',
                CKSUMTYPE='cksum', CKSUM='4294967295',     
                STATUS='new', CENTER = "Pisa", DATE = date.today())

pp = pdb.insertNewTar(tar)

if(pp is None):
    print "ERROR inserting Tar"
    exit(1)


print "Inserted new tar = ", tar.TAR_ID

#
# process it
#

print " try and process it"
pr = pdb.processInputTar(tar)
if(pr is None):
    print "ERROR inserting PR"
    exit(1)
print "Insert done! ID=",pr.RUN_ID

#
#process it
#
procevd = pdb.startProcessing(pr)

#
# check

print "Starting check of who's running"

while (True):
   pdb.checkAllRunning(DEBUG=True)
   sleep (1)   

