#!/usr/bin/env python
#
# this is needed to observe a variety of full tests, ideally at least one per centre 
#


# enable debugging
import cgitb
import commands
import os
import tempfile
import datetime
from time import sleep
import signal
import sys
#sys.path.append("../../PixelDB")
sys.path.append("/home/robot/cms-pixel-db-pisa/Tier0")
import PixelTier0
#cgitb.enable()
#from storm.tracer import debug
#debug(True, stream=sys.stdout)

def handler (signum,frame):
    print "Interjected Signal - exiting"
    pdb.killAllInstances(DEBUG=True)
    exit(2)


import ConfigParser

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
        

DEBUG=True

INSERTED=0
numinjected=0

#(MACRO_INIT, INPUTDIR, CENTER, PATTERN, OPERATOR, TESTNAME, ok) = initProcessing(CONFIG=sys.argv[1], DEBUG=DEBUG)

  #
  # loop over the dir and search for tar files
  #

from PixelTier0 import *

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT,handler)

MAX=100000

pdb = PixelTier0()
pdb.initProcessing(CONFIG=sys.argv[1], DEBUG=False)
pdb.connectToDB()

listinserted=[]



if len(sys.argv) > 3 :

    tars = pdb.store.find(InputTar, InputTar.TESTNAME==sys.argv[2] and  InputTar.CENTER.like(u"%s"%sys.argv[3]))
    for tar in tars :
	tar.STATUS='new'
	listinserted.append(tar.TAR_ID)
        if (INSERTED>MAX):
            continue
    
	INSERTED+=1  	
        print "Reprocess tar = ", tar.TAR_ID, tar.CENTER, tar.TESTNAME
        pdb.store.commit()
	
    numinjected = pdb.injectsProcessingJobs(tarlist=listinserted)
        
else :
	print "Syntax: reprocess.py ini-file testname center-expr"

print "INSERTED ", INSERTED, " TAR FILES"
print "TARS are ",listinserted
print "injected processing runs " , numinjected



