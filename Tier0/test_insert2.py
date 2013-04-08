#!/usr/bin/env python



# enable debugging
import cgitb
import commands
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

MAX=100000

pdb = PixelTier0()
pdb.initProcessing(CONFIG="./test.ini", DEBUG=False)
pdb.connectToDB()

print " initialization done"

#
# loop over a dir to search for tars

basedir="/data/in_tests"
tmpfile = "./tmpfile"
pattern = "*.tar.gz"
os.system("rm -rf "+tmpfile)
os.system("find "+basedir+" -name "+pattern+" > "+tmpfile)

INSERTED=0
f=open(tmpfile)
for line in f:

    if (INSERTED>MAX):
        continue
    
    line= line.rstrip(os.linesep)
    print " working on Tar file: ",line
    

    if (pdb.getInputTarByName(os.path.basename(line),os.path.dirname(line)) is not None):
        continue
    

#
# get cksum
#

    (ret, ck) = commands.getstatusoutput('cksum '+line+" | awk \'{print $1}\'")

    tar = InputTar (NAME=os.path.basename(line),
                LOCATION=os.path.dirname(line),
                CKSUMTYPE='cksum', CKSUM=ck,     
                STATUS='new', CENTER = "Pisa", DATE = date.today())

    pp = pdb.insertNewTar(tar)

    if(pp is None):
        print "ERROR inserting Tar, skipping ...."
        continue


    print "Inserted new tar = ", tar.TAR_ID
    INSERTED=INSERTED+1

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
# inject processing for all tars with status still new
#

numinjected = pdb.injectsProcessingJobs()



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



