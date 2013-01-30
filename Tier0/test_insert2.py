#!/usr/bin/env python

# enable debugging
import cgitb
import os
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
# loop over a dir to search for tars

basedir="/data/tars"
tmpfile = "./tmpfile"
pattern = "*.tar"
os.system("rm -rf "+tmpfile)
os.system("find "+basedir+" -name "+pattern+" > "+tmpfile)

f=open(tmpfile)
for line in f:
    line= line.rstrip(os.linesep)
    print " working on Tar file: ",line
    

    
    tar = InputTar (NAME=os.path.basename(line),
                LOCATION=os.path.dirname(line),
                CKSUMTYPE='cksum', CKSUM='4294967295',     
                STATUS='new', CENTER = "Pisa", DATE = date.today())

    pp = pdb.insertNewTar(tar)

    if(pp is None):
        print "ERROR inserting Tar, skipping ...."
        continue


    print "Inserted new tar = ", tar.TAR_ID

    #
    # process it
    #
    
    print " try and process it"
    pr = pdb.processInputTar(tar)
    if(pr is None):
        print "ERROR inserting PR - skipping"
        continue
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
   pdb.startProcessing()
   sleep (1)   

