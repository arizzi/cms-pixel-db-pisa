#!/usr/bin/env python



# enable debugging
import cgitb
import os
import datetime
from time import sleep
import signal
#cgitb.enable()


def handler (signum,frame):
    print "Interjected Signal - exiting"
    pdb.killAllInstances(DEBUG=True)
    exit(2)


print "Content-Type: text/html"
print

from PixelTier0 import *
import random


signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT,handler)

pdb = PixelTier0()
pdb.initProcessing(CONFIG="./test.ini", DEBUG=False)
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
   num = pdb.checkAllRunning(DEBUG=False)
   num2 = pdb.startProcessingJobs()
   print str(datetime.now())," Running Instances = ",num, " Waiting Instances = ",num2
   sleep (2)   
   if (num==0 and num2==0):
       print "---- FINISHED----"
       break

#



