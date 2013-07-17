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
        
def initProcessing(CONFIG, DEBUG):
    Config.read(CONFIG)
    #
    # force the presence of the fields
    #
    print " APRO", CONFIG
    if (DEBUG == True):
        print "Reading File ",CONFIG
        print ConfigSectionMap("MACRO")
    MACRO_INIT = ConfigSectionMap("MACRO")["init"]
    INPUTDIR = ConfigSectionMap("MACRO")["inputdir"]
    CENTER = ConfigSectionMap("MACRO")["center"]
    OPERATOR = ConfigSectionMap("MACRO")["operator"]
    PATTERN =  ConfigSectionMap("MACRO")["pattern"]
    if (MACRO_INIT=='null' or INPUTDIR=='null' or PATTERN == 'null'):
        print "Config file NOT ok"
        return (Null, Null, Null, Null, False)
    return (MACRO_INIT, INPUTDIR, CENTER, PATTERN,OPERATOR, True)


DEBUG=True
Config = ConfigParser.ConfigParser()

if (len(sys.argv) != 2):
    print " Need one input: the config file!"
    exit (2)
    
MACRO_INIT = 'null'
INPUTDIR = 'null'
CENTER =  'null'
PATTERN ='null'


(MACRO_INIT, INPUTDIR, CENTER, PATTERN, OPERATOR, ok) = initProcessing(CONFIG=sys.argv[1], DEBUG=DEBUG)

if (ok == False):
    print "Failed in reading the ini file",sys.argv[1]
    exit(1)

  #
  # loop over the dir and search for tar files
  #

from PixelTier0 import *

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT,handler)

MAX=100000

pdb = PixelTier0()
pdb.initProcessing(CONFIG=MACRO_INIT, DEBUG=False)
pdb.connectToDB()


#
# upload what you can
#

#new session
s = Session (CENTER=CENTER, OPERATOR=OPERATOR,TYPE="TESTSESSION",DATE=date.today(), COMMENT="")
ppp= pdb.PixelDB.insertSession(s)
if (ppp is None):
    print "Failed to create a session"
    exit (2)

pdb.uploadAllTests(s)
#

os.system ("rm -f "+tmpfile)


